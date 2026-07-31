# Governance, Security & Evaluation

## Access control
- v1 is internal-only (Bravura staff). Client-facing exposure (if pursued) needs a
  separate access model: a client user must only ever see content relevant to their own
  entitlements — no cross-client leakage of other clients' customizations, defects, or
  upgrade risk data. Design the client-profile/entitlement model with this boundary in
  mind from Phase 3 onward even before client-facing rollout, so it isn't retrofitted.
- Role-based scoping: support/BA vs delivery/architect vs (later) client user should see
  different levels of detail (e.g. internal defect discussion vs client-safe summary).

## Data sensitivity
- Client-specific customization/config details, defect specifics, and upgrade risk
  reports are sensitive — treat as client-confidential; don't let one client's data
  surface in another's session even indirectly via retrieval.

## Evaluation framework
- Maintain a growing test question set per phase (start with POC's 20-30, expand each phase).
- Track per answer: correctness, citation accuracy, hallucination (claims not
  traceable to a source), "I don't know" rate.
- Human-in-the-loop feedback (thumbs up/down + comment) feeds a review queue — treat
  as an ongoing evaluation set, not a one-time pass.
- For impact assessment specifically: track how often delivery teams accept vs
  significantly edit the generated risk categorization — this is the real signal of
  whether the scoring model is trustworthy.

## Freshness & trust
- Every answer shows "as of [source date]" — never silently assert stale info as current.
- Flag (don't hide) known documentation-drift areas surfaced during ingestion.

## Change management
- This system will surface documentation gaps and inconsistencies (fixVersion hygiene,
  stale wiki pages, inconsistent component tagging) as a byproduct — route these
  findings back to the owning teams rather than trying to silently work around them
  forever; the KB's accuracy is capped by source data quality.
