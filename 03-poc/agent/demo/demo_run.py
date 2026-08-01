"""
Runs the curated feature-1 sign-off demo and writes a transcript for the live session.

Mirrors eval/run_eval.py's invocation path: WIKI_NAMESPACE set before the orchestrator
imports the tools; ask() per question; citation presence checked; usage summary at end.

Usage (from 03-poc/agent):
    venv/Scripts/python.exe demo/demo_run.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
# Windows consoles default to cp1252, which can't encode characters like ≤ that appear
# in wiki content and get echoed into answers — force UTF-8 so the run can't die mid-write.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

os.environ["WIKI_NAMESPACE"] = "wiki"

from orchestrator import ask, usage_summary  # noqa: E402 — lazy so WIKI_NAMESPACE is honoured

# (question, note)
QUESTIONS = [
    ("What does the optional pagingRange element do in the searchEmployer operation?",
     "Direct spec lookup"),
    ("What is the default number of results per page if pagingRange is not supplied in a searchEmployer request?",
     "Default behavior"),
    ("Why was pagination added to the searchEmployer operation?",
     "Explanation synthesis"),
    ("Would a client that calls searchEmployer without pagingRange see a change in behaviour?",
     "Backward compatibility / before-after delta"),
    ("Does the searchEmployer pagination change return Employer External References in the response?",
     "Negative / out-of-scope"),
    ("What defect reports 14 failing TDDs for the SaveEmployerTest and GetEmployerTest classes?",
     "Jira lifecycle lookup"),
    ("What exception does BASE-460272 report during the CreateEmployerAccount SBS request?",
     "Jira defect detail"),
    ("What is the status of the schema-change ticket BASE-458911?",
     "Jira status lookup"),
]

OUT = os.path.join(os.path.dirname(__file__), "demo_transcript.md")


def run() -> None:
    lines = [
        "# Feature-1 Sign-off Demo — live transcript",
        "",
        f"Run date: 2026-08-01 · source: live Wiki + Jira · questions: {len(QUESTIONS)}",
        "",
    ]
    for q, note in QUESTIONS:
        print(f"Q: {q}\n")
        answer, _ = ask(q)
        citation = bool(re.search(r"(Wiki:|Jira:)", answer))
        lines.append(f"## Q: {q}")
        lines.append(f"*{note} · citation present: {'YES' if citation else 'NO'}*")
        lines.append("")
        lines.append(answer)
        lines.append("")
        lines.append("---")
        lines.append("")
        print(f"A: {answer}\n{'-'*60}\n")

    u = usage_summary()
    tail = f"API usage: {u['calls']} calls · {u['input_tokens']:,} input · {u['output_tokens']:,} output · {u['cache_read_tokens']:,} cache-read"
    print(tail)
    lines.append(tail)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\nTranscript written to {OUT}")


if __name__ == "__main__":
    run()
