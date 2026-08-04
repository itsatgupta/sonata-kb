"""
Orchestrator: the actual chat loop. Wires wiki/jira/(bitbucket/xray stubs) tools
into a Claude tool-use conversation, enforces citation discipline, and returns a
grounded answer.

Run interactively:
    python orchestrator.py
"""
import copy
import json
import os
import sys

# Make this file's directory importable (config/ lives beside it) and load .env
# before any module reads os.environ. tools/__init__.py also loads it, but only
# after the tools package is imported — this guarantees ANTHROPIC_API_KEY etc.
# are present before the anthropic client is constructed in ask().
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.env import load_env

load_env()

import anthropic

from tools import wiki_tool, jira_tool, bitbucket_tool, xray_tool

# Model selection. Default is DeepSeek via its Anthropic-compatible endpoint — set
# ANTHROPIC_BASE_URL in .env (see config/env.example.txt). Override with LLM_MODEL;
# to go back to Claude, set LLM_MODEL=claude-sonnet-5 and point ANTHROPIC_BASE_URL
# at the real Anthropic API.
MODEL = os.environ.get("LLM_MODEL", "deepseek-v4-pro")

SYSTEM_PROMPT = """You are the Sonata Knowledge Assistant, a POC for Bravura Solutions.

Rules you must always follow:
1. Answer ONLY using information returned by your tools (wiki_search, jira_search,
   jira_version_range). Never answer a Sonata functional/technical question from your
   own general knowledge.
2. Every factual claim must carry a citation, taken verbatim from the `citation` field
   of the tool result you used (e.g. "Wiki: Trade Validation Rules § Overrides" or
   "Jira: SONATA-4821 — Add override reason code").
3. If your tools return nothing relevant, say so plainly: "I couldn't find this in the
   indexed Wiki/Jira content for this pilot area." Do not guess.
4. For "what changed between version X and Y" questions, use jira_version_range, not
   jira_search — it resolves the correct version range for you.
5. Keep answers concise and direct; list citations inline or at the end, not both.
6. bitbucket_search and xray_search are Phase 2 tools — if called and they raise
   NotImplementedError or return empty, tell the user this data isn't in scope for
   the current POC rather than treating it as "no data exists".
7. When the user names a specific Jira ticket key (e.g. "BASE-458911"), call
   jira_search with jql='key = <KEY>' — the free-text query parameter searches
   summary/description and cannot match an issue key.
"""

TOOLS = wiki_tool.TOOL_SCHEMAS + jira_tool.TOOL_SCHEMAS + bitbucket_tool.TOOL_SCHEMAS + xray_tool.TOOL_SCHEMAS
DISPATCH = {**wiki_tool.DISPATCH, **jira_tool.DISPATCH, **bitbucket_tool.DISPATCH, **xray_tool.DISPATCH}

# --- Cost/usage accounting (the eval loop makes several API calls per question) ---
USAGE = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0}


def _record_usage(usage) -> None:
    USAGE["calls"] += 1
    USAGE["input_tokens"] += getattr(usage, "input_tokens", 0) or 0
    USAGE["output_tokens"] += getattr(usage, "output_tokens", 0) or 0
    USAGE["cache_read_tokens"] += getattr(usage, "cache_read_input_tokens", 0) or 0


def usage_summary() -> dict:
    return dict(USAGE)


# Prompt caching: the system prompt and tool schemas are byte-identical on every API
# call in an agent loop, so marking the last system block and last tool as cacheable
# makes the ~constant prefix read from cache after the first call instead of being
# billed at the full input rate. Biggest single lever for a multi-question eval.
_CACHED_TOOLS = copy.deepcopy(TOOLS)
if _CACHED_TOOLS:
    _CACHED_TOOLS[-1]["cache_control"] = {"type": "ephemeral"}
_CACHED_SYSTEM = [
    {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}
]


def _run_tool(name: str, tool_input: dict) -> str:
    try:
        result = DISPATCH[name](**tool_input)
        return json.dumps(result, default=str)
    except NotImplementedError as e:
        return json.dumps({"error": str(e), "phase_2_scope": True})
    except Exception as e:  # noqa: BLE001 — POC: surface tool errors to the model, don't crash the loop
        return json.dumps({"error": f"{type(e).__name__}: {e}"})


def ask(question: str, history: list[dict] | None = None) -> tuple[str, list[dict]]:
    """Run one turn. Returns (answer_text, updated_history)."""
    # Base URL comes from ANTHROPIC_BASE_URL in the environment (set to the DeepSeek
    # Anthropic-compatible endpoint in .env). The SDK reads it automatically.
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = (history or []) + [{"role": "user", "content": question}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            system=_CACHED_SYSTEM,
            tools=_CACHED_TOOLS,
            messages=messages,
        )
        _record_usage(response.usage)
        messages.append({"role": "assistant", "content": response.content})

        tool_uses = [b for b in response.content if b.type == "tool_use"]
        if not tool_uses:
            text = "".join(b.text for b in response.content if b.type == "text")
            return text, messages

        tool_results = []
        for tu in tool_uses:
            result_text = _run_tool(tu.name, tu.input)
            tool_results.append(
                {"type": "tool_result", "tool_use_id": tu.id, "content": result_text}
            )
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print("Sonata Knowledge Assistant (POC) — type 'exit' to quit\n")
    history: list[dict] = []
    while True:
        q = input("> ")
        if q.strip().lower() in {"exit", "quit"}:
            break
        answer, history = ask(q, history)
        print(f"\n{answer}\n")
