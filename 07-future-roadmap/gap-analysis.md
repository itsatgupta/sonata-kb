# Gap Analysis — What's Missing From the Original Ask, and What to Add

The user's original scope (functional Q&A + upgrade impact assessment, chat + voice,
sourced from Bitbucket/Wiki/Jira/X-ray) is solid. Below is what's implicit but not
stated, ordered by how much it would hurt if skipped.

## 1. Client Profile data doesn't exist yet — this is the hidden hard part
Every other source (Wiki, Jira, Bitbucket, X-ray) is dev-side data that already exists
cleanly. "Which modules/customizations does Client Z actually use" almost certainly
does NOT exist as clean structured data anywhere — it lives in people's heads, old
upgrade docs, and config exports. **This should be called out explicitly as its own
workstream**, not assumed to fall out of the other four sources. Phase 3 accounts for
this, but it's worth flagging as the single biggest scope/timeline risk in the whole plan.

## 2. Client entitlement/config repository (if one exists) isn't in your source list
You listed Bitbucket, Wiki, Jira, X-ray. If Sonata client deployments have their own
configuration repos/exports (common in wealth platforms — client-specific rule sets,
workflow config, custom fields), that's a fifth potential data source directly relevant
to impact assessment accuracy. Worth an inventory question: "does each client have an
exportable config snapshot we could ingest?"

## 3. An evaluation/feedback loop, not just a build plan
The original ask is about building the KB; it doesn't mention how you'll know it's
working, or keep it accurate as it scales past a POC. Added: `06-governance/` —
evaluation framework, feedback capture, and drift detection. Without this, accuracy
degrades silently as source content evolves.

## 4. Security/access boundary for client data
Not mentioned in the original ask but load-bearing the moment client-facing use is
considered (explicitly a stated eventual interest — "help users" spans internal +
implicitly clients later). Cross-client data leakage in a shared KB is the single
biggest risk if this is ever exposed beyond internal teams. Addressed in governance doc.

## 5. Change management / documentation-debt feedback loop
Building this system will surface where wiki/Jira hygiene is inconsistent (stale pages,
fixVersion mismatches, inconsistent component tags). Worth deciding up front: is this
KB also going to be the mechanism that improves source documentation quality over time
(by routing findings back to owning teams), or purely a passive consumer of whatever
quality exists? Recommended: active feedback loop — otherwise KB accuracy plateaus at
whatever the messiest team's documentation habits allow.

## 6. Ownership model
Not addressed: who owns this system long-term? Recommend a small cross-functional
owning group (one architecture/wiki-side owner, one Jira/PM-side owner, one
engineering owner for ingestion pipelines) rather than it becoming an orphaned side
project after the initial build. Add this as a Phase 1 exit-criteria item.

## 7. Multi-tenancy in the impact-assessment output for account teams
Beyond a single client's impact report, account/delivery leadership likely wants a
portfolio view: "across all our clients, which are most exposed by upcoming trunk
release N+1's changes" — useful for proactive planning, not just reactive per-client
requests. Worth adding as a Phase 3/5 stretch capability once individual client
reports are trusted.

## 8. Localization/tone consistency between chat and voice
The ask specifies a "smoother tone" for voice specifically — worth explicitly deciding
whether chat answers should also be less clinical/more conversational by default, or
whether chat stays precise/technical and only voice gets the softer treatment. Recommend:
same underlying answer, tone/format transformed per channel (see Phase 4 doc) rather than
maintaining two separate "voices" for the assistant's personality.

## 9. Multi-language support
Not mentioned, but worth a one-line decision given international client base (Fidelity,
Royal London, NFUM are UK/US-centric, but "many more" may not be) — confirm English-only
is fine for v1 rather than assuming it.

## Suggested immediate additions to the plan (beyond what's already drafted)
- Add a **Client Profile bootstrap workstream** explicitly to Phase 3 timeline/effort
  (already reflected in `02-phases/phase-3-impact-assessment.md`, flagged here again
  because it's easy to underestimate).
- Add a **documentation-debt tracking mechanism** as a formal Phase 1 deliverable, not
  just an incidental finding.
- Decide an **ownership model** before Phase 1 kicks off, not after POC succeeds.
- Confirm whether a **client config/entitlement data source** exists to ingest alongside
  the four named sources.
