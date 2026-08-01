# Phase 1 — Functional Knowledge Base: Implementation Plan

**Status:** draft — prepared 2026-08-01 after feature-1 (searchEmployer pagination) POC go/no-go **PASS**
(27/27 Correct, 100%, SME Pratigya). Companion to `phase-1-functional-kb.md` (the charter) and
`03-poc/poc-findings.md` (the POC findings that shape this plan).

## Context

Phase 0 proved the core loop — ingest → index → retrieve → answer-with-citation — on **one**
feature (searchEmployer SBS pagination, RLSI-6059) and passed the go/no-go bar. Phase 1 scales that
same pattern to the full Sonata Wiki + Jira corpus so the assistant answers functional questions
about **any module**, not just the pilot feature. The POC code in `03-poc/agent/` is the template:
per-source tools with citations, hybrid retrieval, `run_eval.py` scoring, and the SME eval set.

The plan is grounded in the Phase-1 charter, the entity model in `01-architecture/system-design.md`,
the Smart Discovery alignment (`08-central-upgrade-team-alignment/smart-discovery-alignment.md`), and
the data-quality findings from the POC.

## Scope

**In scope:**
- Full read-only ingestion of Wiki (Sonata design/arch/tech-spec spaces) and Jira (epics/stories/defects
  with acceptance criteria, historical + current).
- Feature/Module taxonomy (the entity table's `Feature/Module` node) — via SME workshop.
- Entity linking: Wiki page ↔ Jira key.
- Chat UX expansion: multi-turn, follow-ups, "show me the source" links.
- Feedback capture (thumbs up/down + free text) on every answer.
- Broaden eval set to 100+ questions spanning modules; track escalation/"I don't know" rate.

**Out of scope (deferred):** code/test ingestion (Phase 2), version-diff/impact assessment (Phase 3),
voice (Phase 4), client profiles (see `07-future-roadmap/gap-analysis.md`).

## Workstreams (roughly in order)

### WS1 — Corpus scoping & full ingestion
- Enumerate Wiki spaces and Jira projects to include; decide the namespace strategy (POC used one
  namespace per pilot feature — Phase 1 needs either a per-space/per-module namespace map or a
  unified corpus with module metadata).
- Generalize `03-poc/agent/ingestion/wiki_ingest.py` from single-page (`--page-id`) to space-level
  crawl; add a Jira ingestion script (POC only ingested Jira on-demand via `jira_tool`).
- Keep **read-only** posture (POC rule #2). Secrets stay in `.env` (gitignored).
- Target freshness: wiki/Jira within 24h; release notes within 1h of publish
  (`system-design.md` § Freshness/sync).

### WS2 — Feature/Module taxonomy (SME workshop)
- The taxonomy does **not exist cleanly** in Wiki or Jira (POC confirmed — see `poc-findings.md`).
  Run an SME workshop to define 10–20 functional areas and their component mapping.
- **Consume, don't rebuild**: Smart Discovery's C1 ("Sonata structural map", module/path taxonomy)
  may already be underway — align with it (roadmap-summary.md). Hold a fallback if it stalls.
- Output feeds the `Feature/Module` entity and the `modules_touched` metadata that Phase 3's
  `jira_version_range` will filter on.

### WS3 — Entity linking (Wiki page ↔ Jira key)
- POC already regex-matches Jira keys in wiki text (`PROJ-1234`). Extend to: labels, page properties,
  and fixVersion metadata. Audit what actually exists before committing to a mechanism
  (`system-design.md` entity table notes this is a "audit what's there first" item).

### WS4 — Retrieval scaling & metadata filters
- Scale hybrid search (vector + keyword) to the full corpus; add metadata filters (fixVersion,
  component/module, issue type) so structured queries (e.g. "what changed in vX") stay reliable —
  POC confirmed plain free-text search on the Jira DC instance is unreliable
  (`poc-findings.md` #1), so keep `summary ~ / description ~` and metadata filters first-class.
- **Apply the POC cost levers** before any broad run: cap chunk text sent to the model (~1500 chars),
  reduce default `wiki_search` results, lower `max_tokens` (POC: ~$2.25 for 21 questions, driven by
  input context).

### WS5 — Chat UX & feedback
- Multi-turn conversation (orchestrator already threads `history` — expose it in a real UI).
- "Show me the source" links (every answer already carries a `citation`).
- Thumbs up/down + free text per answer → feeds the eval framework
  (`06-governance/evaluation-framework.md`) and future retrieval tuning.

### WS6 — Eval expansion & data-quality triage
- Broaden `test_questions.md` from 27 (one feature) to **100+ spanning modules**; same
  `correct / partial / wrong / hallucinated_citation` rubric; target the agreed threshold
  (POC bar was ≥80% correct-with-citation).
- Triage the POC data-quality backlog (`poc-findings.md`) — decide per item: **fix the source doc**
  or **teach the system to flag known-stale content** rather than assert it confidently:
  1. Jira free-text unreliability + cross-project scope leakage (LIBSON-3635 helpdesk drift).
  2. Empty BASE ticket shells — substance lives in wiki IA pages (`customfield_22644` is the real AC field).
  3. Release-note ambiguity (official vs porting vs clone) — rank official first.
  4. External-ref "capability vs enhancement-scope" phrasing ambiguity.
  5. Wiki typo (`saveExternalCorespondence`).
  6. Security: rotate the Jira PAT hardcoded in `~/.claude/mcp.json` (use `{env:...}`).
- Track **escalation/"I don't know" rate** as a baseline metric (charter exit criterion) — this is a
  deliberate, honest behavior, not a failure.

## Entry / exit criteria (from the charter)

- **Entry:** Phase 0 exit met (PASS, graded, findings written ✓). Data-quality backlog triaged.
- **Exit:** coverage across all major modules (10–20 functional areas); 100+ question eval at agreed
  threshold; escalation rate tracked; documentation-debt list produced.

## Key risk

Wiki/Jira content quality is **uneven across modules** — some teams document meticulously, others
don't. Expect a documentation-debt list as a valid output, not a system failure (charter § Key risk).
Mitigate by making the escalation/"I don't know" path explicit and cheap, and by surfacing
last-updated dates on every citation.

## First concrete steps (next session)

1. Enumerate Wiki spaces + Jira projects for full ingestion; draft the namespace/module metadata map.
2. Start the SME workshop request for the taxonomy (WS2) — it's the long pole.
3. Add a Jira bulk-ingestion script; generalize `wiki_ingest.py` to space-level.
4. Apply POC cost levers before any broad run (WS4).
5. Rotate the Jira PAT in `~/.claude/mcp.json` (security, `poc-findings.md` #6).
