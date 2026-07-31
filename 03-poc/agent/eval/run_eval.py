"""
Runs a test-question set against the orchestrator and produces a scored CSV.
Grading of correctness is LEFT MANUAL/SME-reviewed in this POC (score column starts
blank) — automating "is this answer correct" reliably is its own hard problem; don't
let the eval harness quietly become the thing that needs evaluating.

The wiki index namespace is selectable so each pilot feature gets its own index and
question set (feature 1: wiki / test_questions.md; feature 2: wiki_directupload /
test_questions_directupload.md).

Usage:
    python eval/run_eval.py [--namespace wiki] [--questions eval/test_questions.md]
                            [--results eval/results.csv]
"""
import argparse
import csv
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
# Windows consoles/default codecs are cp1252, which can't encode characters like ≤
# that appear in wiki content and get echoed into answers — force UTF-8 so a single
# answer can't kill the whole eval run mid-write.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_QUESTIONS = os.path.join(os.path.dirname(__file__), "test_questions.md")
DEFAULT_RESULTS = os.path.join(os.path.dirname(__file__), "results.csv")


def parse_questions(path: str) -> list[dict]:
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(("What", "Why", "Does", "Would")):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue
            rows.append(
                {"question": parts[0], "expected_citation_contains": parts[1], "expected_answer_gist": parts[2]}
            )
    return rows


def run():
    parser = argparse.ArgumentParser(description="Run the POC eval question set.")
    parser.add_argument("--namespace", default="wiki",
                        help="wiki index namespace to search (e.g. wiki, wiki_directupload)")
    parser.add_argument("--questions", default=DEFAULT_QUESTIONS, help="question file (pipe-separated)")
    parser.add_argument("--results", default=DEFAULT_RESULTS, help="output CSV path")
    args = parser.parse_args()

    # Must be set BEFORE orchestrator imports the tools, because wiki_tool builds its
    # VectorIndex (and therefore its namespace) at import time.
    if args.namespace:
        os.environ["WIKI_NAMESPACE"] = args.namespace

    from orchestrator import ask, usage_summary  # noqa: E402 — lazy so WIKI_NAMESPACE is honoured

    questions = parse_questions(args.questions)
    if not questions:
        print(f"No parseable questions found in {args.questions} — fill in real "
              f"questions per the template before running eval.")
        return

    with open(args.results, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(
            ["question", "expected_citation_contains", "expected_answer_gist", "actual_answer",
             "citation_present", "score_manual"]
        )
        for q in questions:
            answer, _ = ask(q["question"])
            citation_present = bool(re.search(r"(Wiki:|Jira:)", answer))
            writer.writerow(
                [q["question"], q["expected_citation_contains"], q["expected_answer_gist"],
                 answer, citation_present, ""]  # score_manual left blank for SME review
            )
            print(f"Q: {q['question']}\nA: {answer}\n{'-'*40}")

    u = usage_summary()
    print(f"\nAPI usage: {u['calls']} calls | {u['input_tokens']:,} input | "
          f"{u['output_tokens']:,} output | {u['cache_read_tokens']:,} cache-read tokens")
    print(f"\nResults written to {args.results} — have your SME fill in score_manual "
          f"(correct / partial / wrong / hallucinated_citation) per phase-0-poc.md exit criteria.")


if __name__ == "__main__":
    run()
