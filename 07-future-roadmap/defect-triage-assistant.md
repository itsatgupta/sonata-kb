# Proposed Workstream — Defect Triage Assistant

> Status: **proposal, later phase** — not in POC/Phase 1 scope.
> Captured 2026-07-31 as a candidate workstream, not a committed roadmap item.

## Goal

When a customer reports a defect, help the support team quickly determine:

1. **Has this already been reported — for any client?**
   - Search Jira + the vector corpus for a similar defect across clients.
   - If found → point the project team at the existing ticket(s) as a reference
     (cross-client reuse: same root cause, don't re-diagnose).
2. **Not found? → triage it.**
   - The support agent follows the customer-provided replication steps (grounded in
     a structured triage checklist — never invented).
   - The AI produces an initial analysis and a **draft** base ticket: replication
     steps + initial analysis, ready for the maintenance team.
   - A human (support lead / maintenance lead) reviews and approves before anything
     is written to Jira.

## Why it lives in this app (not a separate one)

- **Duplicate detection is the same retrieval stack already built** — Jira search +
  vector index + citation discipline — scoped to historical defects with client metadata.
- The two halves are **one decision flow** in a single agent conversation:
  search → found? (reference) / not found? (triage + create).
- A separate app would duplicate retrieval, indexing, citation, and the eval harness.

## Where it fits in the roadmap

| Piece | Maps to |
|---|---|
| Cross-client duplicate detection | Phase 3+ (needs a broad multi-client corpus + client profiles) |
| Triage: follow replication checklist → initial analysis | New workstream; model on Phase 3's draft generation (`generate_impact_draft`) |
| Create base ticket | Draft → human approval → Jira write (Phase 5 governance hardening) |

## Prerequisites / gates (why it is not earlier-phase)

1. **Client-attribution data** — cross-client dedup is only sound with reliable client
   metadata on defects. `gap-analysis.md` flags client profiles as the single biggest
   scope/timeline risk and unsolved. **This is the gating item.**
2. **Cross-client corpus + client-filtered indexing** — the vector DB must span many
   clients' defects with filterable metadata (client, module, symptom).
3. **Grounded triage checklist** — the support team's replication-step template must
   exist as structured content (wiki) the agent follows with citations, not invents.
4. **Base-ticket template** — SME-defined fields and replication-steps format.
5. **Dedup eval set** — the genuinely hard part: distinguish "same defect, different
   client" from "different defect, same symptom." Needs its own test questions and a
   threshold, or it will hallucinate cross-client links.

## Governance (non-negotiable)

- The agent **never auto-creates** a ticket. Output is always a draft for human
  approval — matches the catalogue RACI (Accountable roles keep sign-off) and the
  repo's no-auto-approval rule (`CLAUDE.md` rule 3).
- Write-back to Jira is a new capability and needs a governance decision first
  (`06-governance/`): which (sandbox/triage) Jira project, who may approve, audit trail.
- The existing assistant stays read-only; write is a separately gated, opt-in capability.

## Possible slice to prototype first

The **duplicate-detection half** is cheap on the current stack (search across existing
Jira + a small dedup eval set) and does not require write-back. Consider piloting it
before committing to the full workstream.

## Related docs

- Persona: `05-personas-and-usecases/personas-and-usecases.md` (Support / service-desk triage agent)
- Client-profile gap: `07-future-roadmap/gap-analysis.md` §1
- Governance: `06-governance/`
