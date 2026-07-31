# Phase 3 — Upgrade Impact Assessment

This is the highest-value, highest-effort phase — the business case beyond "nice chatbot."

## Goal
Given a client, their current Sonata version, and a target version, automatically
produce a draft impact assessment: what changed, what's relevant to this client, what's
risky, and a rough effort estimate — reviewed and finalized by a human, not auto-approved.

## New things this phase requires (not free from Phases 0-2)

### 1. Client Profile data
The one entity that doesn't exist as clean structured data anywhere today. Needs:
- Current version per client (probably already tracked somewhere operationally — find it,
  don't rebuild it).
- Which modules/features/customizations each client actually uses (this is the hard part —
  likely a mix of: config exports, prior upgrade documents, SME interviews, and account-team
  knowledge). Plan for an SME workshop per client or client segment to bootstrap this.
- Prior upgrade history (what version-to-version jumps has this client already done,
  what issues came up last time).
- **Recommendation: start with 2-3 pilot clients** (e.g. the smaller/simpler ones first,
  not the most complex), not all clients at once.

### 2. Version-diff engine
- Given (v_from, v_to], resolve full set of Jira issues (all fixVersions in range) →
  group by module/component → pull release-note text + linked wiki spec changes.
- This is a structured query over the Phase 1/2 graph, not new ingestion — but it does
  need a clean "fixVersion → trunk release" mapping validated against actual release notes.

### 3. Impact/risk scoring model
Needs to be defined WITH the delivery/upgrade teams (this is domain expertise, not
something to invent from scratch). Suggested starting dimensions:
- **Breaking vs additive change** (from Jira type/labels + release note wording)
- **Client relevance** (does client profile show usage of the affected module?)
- **Customization overlap** (does client have custom code/config in the affected area? —
  highest risk category)
- **Historical defect density** in that area across past releases
- Output: a simple High/Medium/Low risk tag per changed item, rolled up to an overall
  report — resist over-engineering a numeric score before you have real feedback on
  whether the categories are even right.

### 4. Report generation
- Structured output (module → changes → risk → recommended action/test focus).
- Exportable to Word/PDF for client-facing or internal sign-off use (see docx/pdf skills
  if generating via Claude Code).

## Exit criteria
- End-to-end assessment produced for at least 2 pilot clients across a real version jump,
  reviewed by the delivery team, and judged materially faster/more complete than the
  manual process it replaces.
- Delivery team explicitly signs off that risk categorization is directionally trustworthy
  (this is a trust-building phase — expect iteration on the scoring model).
