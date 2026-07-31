# CLAUDE.md — Sonata Knowledge Assistant (POC)

This file is the standing instruction set for Claude Code / any agent working in this
repo. Read this in full before writing or modifying ingestion, retrieval, or agent code.

## Current work status — read this first in a new session

The POC is mid-flight with **two pilot features** (searchEmployer SBS pagination and
Direct Uploads). Before doing anything, read `sonata-kb/03-poc/PROGRESS-STATUS.md` for
the live state: what is verified, what is blocked, pending SME grading, and the exact
commands to continue.

## What this repo is
A POC-stage knowledge assistant for Bravura's Sonata product. It answers functional
questions and (from Phase 3 onward) drafts upgrade-impact deliverables, grounded in
Wiki, Jira, Bitbucket, and X-ray content — never from model memory alone.

Read `sonata-kb/00-overview/vision-and-goals.md` and
`sonata-kb/08-central-upgrade-team-alignment/catalogue-alignment.md` and
`sonata-kb/08-central-upgrade-team-alignment/smart-discovery-alignment.md` for full
context before making architectural decisions. Read `sonata-kb/03-poc/` before touching
POC code.

## Non-negotiable rules for this codebase

1. **Every answer must cite a source** — a wiki page+section, a Jira key, a PR id, or
   an X-ray test key. If retrieval returns nothing relevant, the agent must say so
   explicitly rather than answering from general Sonata knowledge. This is the single
   most important behavior in the whole system — it's what makes the tool trustworthy
   enough to eventually touch client-facing deliverables.
2. **Read-only against source systems in this POC.** No tool in this repo writes back
   to Wiki, Jira, Bitbucket, or X-ray. Report-generation output goes to local files,
   never auto-published.
3. **No auto-approval of upgrade decisions.** Impact/risk output is always framed as a
   draft for human review (matches `sonata-kb/02-phases/phase-3-impact-assessment.md`
   and the catalogue's RACI: Accountable roles keep sign-off).
4. **Don't invent structured data.** If a client profile, fixVersion mapping, or
   component tag doesn't exist cleanly in the source system, say so and flag it as a
   data-gap rather than guessing (see `sonata-kb/07-future-roadmap/gap-analysis.md`).
5. **Secrets never in code.** All API tokens come from environment variables
   (`.env`, gitignored) — see `config/env.example.txt`.

## Repo layout (agent-relevant parts)

```
sonata-kb/03-poc/agent/
├── tools/                # one module per data source — the actual tool implementations
│   ├── wiki_tool.py
│   ├── jira_tool.py
│   ├── bitbucket_tool.py
│   └── xray_tool.py
├── retrieval/            # chunking, embedding, hybrid search, re-ranking
├── orchestrator.py       # ties tools + retrieval + Claude API together
├── eval/
│   ├── test_questions.md
│   └── run_eval.py
└── config/
    └── env.example.txt
```

## Tool definitions (per data source)

Each tool below is a thin, read-only wrapper: fetch → normalize → return structured
JSON with a `citation` field on every returned item. The orchestrator never calls raw
HTTP — always through these tools, so citation formatting and rate-limit handling stay
centralized.

### `wiki_search(query: str, space: str | None = None, max_results: int = 5) -> list[WikiChunk]`
- **Source**: `sonata-kb/04-data-sources/wiki.md`
- Searches ingested wiki chunks (embedding + keyword hybrid).
- Returns: `{page_title, section_heading, text, page_url, last_modified, citation}`
- `citation` format: `"Wiki: <page_title> § <section_heading> (updated <date>)"`

### `wiki_get_page(page_id: str) -> WikiPage`
- Fetches a full page by id when a chunk's parent context is needed (e.g. user asks a
  follow-up requiring surrounding sections).

### `jira_search(jql: str | None = None, query: str | None = None, fix_version: str | None = None, component: str | None = None, max_results: int = 20) -> list[JiraIssue]`
- **Source**: `sonata-kb/04-data-sources/jira.md`
- Two modes: raw `jql` for structured queries (e.g. version-diff lookups), or free-text
  `query` for semantic search over summary/description/acceptance criteria.
- Returns: `{key, type, summary, description, acceptance_criteria, fix_versions,
  components, status, linked_issues, url, citation}`
- `citation` format: `"Jira: <KEY> — <summary>"`
- **This is the primary tool for version-diff queries**: e.g.
  `jira_search(jql="project = SONATA AND fixVersion in (v11.5, v11.6, v12.0, v12.1) ...")`

### `jira_version_range(from_version: str, to_version: str, component: str | None = None) -> list[JiraIssue]`
- Convenience wrapper around `jira_search` — resolves the ordered list of trunk
  releases between two versions (using the validated fixVersion→trunk mapping, see
  `04-data-sources/jira.md` open questions) and returns all issues in that range.
- This is THE core primitive for upgrade impact assessment — build and test this before
  anything else in Phase 3.

### `bitbucket_search(jira_key: str | None = None, module: str | None = None, since: str | None = None) -> list[PullRequest]`
- **Source**: `sonata-kb/04-data-sources/bitbucket.md`
- Returns: `{pr_id, title, merged_date, target_branch, linked_jira_key, files_changed,
  modules_touched, url, citation}`
- Requires the path→module lookup table (not yet built — stub with an empty/passthrough
  mapping in POC and flag `modules_touched: ["UNMAPPED"]` rather than guessing).

### `xray_search(story_key: str | None = None, module: str | None = None) -> list[TestCase]`
- **Source**: `sonata-kb/04-data-sources/xray.md`
- Returns: `{test_key, title, linked_story, module, last_execution_status, citation}`
- Not required for POC (Phase 2 scope) — stub returns empty list with a note; don't
  build this out until Phase 2.

### `generate_impact_draft(client: str, from_version: str, to_version: str) -> ImpactDraftReport`
- **Phase 3 tool, not POC** — composes `jira_version_range` + client profile lookup
  (not yet built, see gap analysis) + risk-tagging. Stub this function to raise
  `NotImplementedError("Phase 3 — requires client profile data, see gap-analysis.md")`
  so it's clear this isn't silently faked.

## Orchestration behavior

- Intent routing: classify each user turn as (a) functional Q&A → `wiki_search` +
  `jira_search`, (b) version-diff → `jira_version_range`, (c) impact assessment →
  `generate_impact_draft` (Phase 3+), (d) anything else → ask a clarifying question
  rather than guessing which tool applies.
- Always synthesize an answer from tool results with inline citations; never present
  a raw tool result dump as the final answer.
- If tool results are empty or low-confidence, say so plainly: *"I couldn't find this
  in the indexed Wiki/Jira content — you may want to check with [team/SME]."* Do not
  fall back to general knowledge about Sonata.
- Voice-channel responses (Phase 4, not in POC) apply a post-processing formatter — see
  `sonata-kb/02-phases/phase-4-voice-interface.md` — never change retrieval/citation
  behavior for voice.

## Evaluation discipline

- `eval/test_questions.md` holds the curated POC question set (see
  `sonata-kb/03-poc/poc-candidate-selection.md` for how it was built) — write these
  BEFORE tuning retrieval, not after.
- `eval/run_eval.py` runs the full set and scores: correct / partially correct / wrong /
  hallucinated-citation. Any code change to `retrieval/` or `tools/` should be
  re-validated against this set before merging.
- Target for POC exit: ≥80% correct with accurate citations (see
  `sonata-kb/02-phases/phase-0-poc.md`).

## What NOT to build yet (see gap-analysis.md for full reasoning)
- Client profile / entitlement data — flagged as unsolved; don't fake it.
- Full source-code semantic search over Bitbucket — out of scope indefinitely.
- Any write-back to Jira/Wiki/Bitbucket/X-ray.
- Client-facing exposure or multi-tenant access control — internal only until governance
  work in `06-governance/` is addressed.
