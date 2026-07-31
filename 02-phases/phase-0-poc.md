# Phase 0 — POC

## Goal
Prove the core loop — ingest → index → retrieve → answer with citation — works well
enough to trust, on a single small, well-bounded feature area, before any investment
in the full architecture.

## Scope (deliberately narrow)
- **Pick ONE small enhancement/feature** already shipped in a recent trunk release
  (see `03-poc/poc-candidate-selection.md` for how to pick it).
- Ingest only:
  - The wiki page(s) describing that feature's design/spec
  - The Jira epic/stories/defects for that feature (with acceptance criteria)
  - The relevant release note entry
  - (Optional, stretch) the linked Bitbucket PRs
- Build a minimal chat interface (can be a simple internal web chat — no voice yet).
- Answer a curated test set of ~20–30 questions about that one feature, ranging from
  simple ("what does this field do") to harder ("what was the behavior before vs after
  this enhancement, and which clients would be affected").

## Explicit exclusions from POC
- No voice bot yet.
- No cross-client impact assessment (single feature, not full version diff).
- No X-ray/test ingestion.
- No production access control / client-facing exposure.

## Entry criteria
- One enhancement selected with complete wiki + Jira + release note trail (i.e. not a
  case where the docs are known to be out of date — that's a good Phase 1 stress test,
  not a good POC).
- Read-only API/export access to Wiki + Jira confirmed (see `04-data-sources/`).

## Exit criteria (go/no-go for Phase 1)
- ≥80% of the curated test questions answered correctly with correct source citation.
- Every answer traceable to a specific wiki page/section or Jira key (no un-sourced claims).
- Stakeholder demo sign-off from at least one SME who reviews the answers for the pilot feature.
- A written list of failure modes observed (ambiguous wiki content, conflicting
  Jira vs wiki info, missing content) — feeds Phase 1 data-quality backlog.

## Team & effort (indicative)
- 1 engineer (ingestion + retrieval), 1 person part-time from the SME/BA side to curate
  the test question set and grade answers. 3–4 weeks elapsed.

## Deliverables
- Working chat POC (internal only)
- Test question set + scoring results
- Findings doc → feeds `06-governance/evaluation-framework.md` and Phase 1 planning
