# Phase 1 — Functional Knowledge Base (Chat, all modules)

## Goal
Scale the POC's proven pattern to the entire Sonata wiki + Jira corpus so the chatbot
can answer functional questions about any module, not just the pilot feature.

## Scope
- Full ingestion of Wiki (all spaces relevant to Sonata design/arch/tech specs) and
  Jira (all epics/stories/defects with acceptance criteria, historical + current).
- Build the **Feature/Module taxonomy** (see `01-architecture/system-design.md` entity
  table) — this likely needs an SME workshop to define, since it won't exist cleanly
  in either Wiki or Jira as-is.
- Basic entity linking: Wiki page ↔ Jira key (via free-text key references, labels, or
  page properties — audit what's actually there first).
- Expand chat UI: multi-turn conversation, follow-up questions, "show me the source" links.
- Start capturing a feedback signal (thumbs up/down + free text) on every answer —
  this feeds the eval framework and future fine-tuning of retrieval.

## Out of scope (deferred)
- Code/test ingestion (Phase 2)
- Version-diff / impact assessment (Phase 3)
- Voice (Phase 4, parallelizable but not required here)

## Entry criteria
- Phase 0 exit criteria met.
- Data-quality backlog from POC triaged (decide: fix source docs, or teach the system
  to flag known-stale content rather than assert it confidently).

## Exit criteria
- Coverage: chat can answer questions across all major Sonata modules (define "major"
  with SME input — likely 10-20 functional areas).
- Accuracy on a broadened test set (100+ questions spanning modules) at agreed threshold.
- SME escalation/"I don't know" rate tracked as a baseline metric.

## Key risk to watch
Wiki/Jira content quality is uneven across modules — some teams document meticulously,
others don't. Expect Phase 1 to surface a documentation-debt list; that's a valid and
useful output, not a failure of the system.
