# Sonata Knowledge Assistant (SKA)

A knowledge base + chatbot/voicebot system for Bravura Solutions' **Sonata** wealth management
product, built to:

1. Answer any functional/technical question about Sonata (RDA + Web) for internal teams,
   support, and eventually clients (Fidelity, Royal London, SFA, NFUM, etc.)
2. Automate **upgrade impact assessment** across Sonata's monthly trunk releases, so
   client-specific yearly upgrades can be scoped, estimated, and risk-assessed faster.

This repo is structured to be dropped into **Claude Code** (or any repo-aware coding agent) as
a living knowledge base + set of agent instructions. It is designed to grow — see
`07-future-roadmap/gap-analysis.md` for what's deliberately left out of v1 and why.

## Folder Map

```
sonata-kb/
├── 00-overview/          Vision, goals, success metrics, glossary
├── 01-architecture/      System design: ingestion, storage, retrieval, serving layers
├── 02-phases/            Phase-by-phase delivery plan (POC → GA)
├── 03-poc/               Concrete POC scope: the one enhancement to pilot on
├── 04-data-sources/      Per-source integration specs (Bitbucket, Wiki, Jira, X-ray)
├── 05-personas-and-usecases/  Who uses this and how (chat + voice flows)
├── 06-governance/        Security, access control, data freshness, evaluation
└── 07-future-roadmap/    What's NOT in v1, and what to add as it matures
```

## How to use this with Claude Code

1. Clone/copy this folder into your working repo as `/docs/sonata-kb/` or similar.
2. Point Claude Code at `02-phases/phase-0-poc.md` and `03-poc/` first — that's the
   buildable slice.
3. Use `01-architecture/system-design.md` as the standing architecture reference doc
   any future session should re-read before making design changes.
4. Treat `04-data-sources/*.md` as connector specs — one file per system, each is a
   self-contained implementation brief an engineer or agent can pick up independently.

## Read this next
Start with `00-overview/vision-and-goals.md`, then `02-phases/roadmap-summary.md`.

## Ready to actually build it?
Go straight to **`SETUP-AND-EXECUTION-GUIDE.md`** — step-by-step Claude Code setup,
then phase-by-phase execution instructions from POC through production.

## New: Centralised Upgrade Team alignment
`08-central-upgrade-team-alignment/catalogue-alignment.md` maps this plan against the
Centralised Upgrade Team's Service Catalogue and Upgrade Subscription deliverables
(Royal London), and against the stated 60%-upgrade-cost-reduction goal — including
which catalogued services the KB can realistically automate vs where human judgment
stays load-bearing.

`08-central-upgrade-team-alignment/smart-discovery-alignment.md` covers the second,
parallel initiative (Smart Discovery — Foundation Phase): who's already building the
code-estate access + structural map this plan's Phase 2 was going to build itself, and
the one open question it raises (GitLab vs Bitbucket for the Sonata code estate).

## New: buildable POC agent
`CLAUDE.md` (repo root) is the standing instruction set for Claude Code / any agent
working in this repo — read it first for the non-negotiable rules (citation discipline,
read-only, no faked data).

`03-poc/agent/` is real, runnable skeleton code, not just a plan:
```
03-poc/agent/
├── tools/            wiki_tool.py, jira_tool.py (real), bitbucket_tool.py, xray_tool.py (Phase 2 stubs)
├── retrieval/         local TF-IDF vector index + markdown chunker (swap for your real vector store later)
├── ingestion/         wiki_ingest.py — pulls & indexes the pilot feature's wiki pages
├── orchestrator.py    the actual Claude tool-use chat loop
├── eval/              test_questions.md template + run_eval.py scorer
├── config/env.example.txt
└── requirements.txt
```
To run: copy `config/env.example.txt` to `.env`, fill in Wiki/Jira/Anthropic
credentials, `pip install -r requirements.txt`, run `ingestion/wiki_ingest.py --page-id
<id>` for your chosen pilot feature's wiki page(s), fill in `eval/test_questions.md`,
then `python orchestrator.py` to chat, or `python eval/run_eval.py` to score.
