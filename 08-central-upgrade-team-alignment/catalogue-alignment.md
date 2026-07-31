# Central Upgrade Team Alignment — How the KB Maps to a 60% Cost Reduction Target

Source docs: *Centralised Upgrade Team — Service Catalogue* and *Upgrade Subscription
Services and Deliverables v1* (Royal London). These are a genuinely strong input — they
don't just validate the plan, they turn Phase 3 from "a good idea" into "a costed
operating model with named roles, RACI, and deliverables we can automate against."

## Why this changes the plan (not just confirms it)

Before these docs, Phase 3 (Upgrade Impact Assessment) was designed around an assumed
workflow. The catalogue gives the **actual** workflow: 6 lifecycle phases, 12 named
service groups, specific owned deliverables, and a RACI matrix per activity. That means
the KB/assistant doesn't need to guess what "an impact assessment" should contain —
it needs to reproduce (and eventually pre-populate) documents the Upgrade Team is
already contracted to deliver, e.g.:

- Upgrade Impact Assessment
- Client Capability Heatmaps
- Configuration Alignment Summary
- Change impact outputs (from Release Change Analysis)
- CART Exit Reports / Test Reporting
- RAID Log Reporting
- Weekly Progress Reports

This is a much stronger POC and Phase-3 target than what was in the original plan:
instead of "produce a draft impact assessment," it's now **"produce a first draft of
the specific deliverables the Upgrade Team's own service catalogue already commits to,
faster and more consistently than manual production today."**

## The 60% cost-reduction goal — where the KB genuinely helps vs where it can't

The catalogue's RACI matrices are the best available map of where effort currently
goes, and therefore where automation has real leverage vs where it doesn't. Reading
across the RACI tables (Risk Scoring, RAID Dashboard, Risk Trend Analytics, Automated
Alerts, Dependency Monitoring, Go-Live Readiness, Lessons Learned):

**High-leverage (KB/assistant can directly reduce effort):**
- **Upgrade Impact Assessment / Release Change Analysis / Capability Heatmap Production**
  (Phase 1 of the lifecycle) — this is almost exactly the KB's core Q&A + version-diff
  capability already scoped in `02-phases/phase-3-impact-assessment.md`. Currently
  "Responsible: Upgrade Consultant" doing manual cross-referencing — directly
  replaceable by a first-draft generation step.
- **Configuration Gap Analysis** — needs the client-profile/config data this plan
  already flags as the hardest new workstream (see gap analysis) — now backed by a
  named service, which strengthens the case for prioritizing it.
- **Defect/Test Reporting, Weekly Progress Reporting, RAID Log Reporting** — these are
  recurring, templated, data-aggregation deliverables (owned by Upgrade PM / Test Lead)
  that a KB-connected reporting layer can draft automatically from Jira/X-ray data,
  freeing PM/Test Lead time for judgment calls, not data compilation.
- **No-Fix Analysis / Defect Analysis** — "documented explanation where no fix is
  required" is a pattern-matchable, precedent-based task (has this exact defect
  signature been seen and resolved this way before?) — a strong second-POC candidate
  once the KB has enough historical defect data indexed.
- **Release Notes Production** — already source data the KB ingests; drafting release
  notes from merged Jira issues/PRs is a natural output, not just an input.

**Lower-leverage / needs human judgment (KB assists, doesn't replace):**
- **Risk Scoring & Prioritisation, Go-Live Readiness, Escalation** — the RACI shows
  these are Accountable-heavy (PM/Architect sign-off), and rightly so — a KB can
  surface the underlying data (defect trends, test coverage gaps, dependency status)
  faster, but the risk judgment call stays human. Treat as "decision support," matching
  this plan's existing non-goal ("not auto-approving upgrade decisions").
- **Governance, Stakeholder meetings, Supplier Coordination** — inherently human
  coordination work; the KB's role here is purely informational prep (e.g. "brief me
  before the governance call"), not replacement.
- **Environment Build, Deployment, Hypercare** — operational/hands-on work; KB's role
  is limited to informing/triaging, not executing.

## Recommended plan adjustments

1. **Reframe the POC's target deliverable.** Instead of an open-ended Q&A demo, pick
   the POC enhancement AND produce a first draft of one specific catalogued deliverable
   — most naturally **Release Notes Production** or a mini **Upgrade Impact Assessment**
   section — so the POC directly demonstrates cost/time savings against a real,
   contracted deliverable, not just "the bot answered questions correctly."
2. **Add a costing/time-tracking dimension to the evaluation framework.** To ever
   claim progress against a 60% cost reduction goal, `06-governance/` needs a baseline:
   how long does each catalogued deliverable currently take to produce manually
   (by role, from the RACI), so KB-assisted production can be measured against it.
   This should be gathered from the Upgrade Team itself — this plan can't estimate it.
3. **Treat the Centralised Upgrade Team as the primary Phase 1+ user, not a secondary
   persona.** Update `05-personas-and-usecases/` — Upgrade Consultant, Upgrade PM, Test
   Lead, and Solution Architect (from the catalogue's "Core Roles" table) are now the
   named primary users of the Upgrade Impact Assistant, with their specific deliverables
   as target outputs.
4. **Client Profile bootstrap (flagged earlier as the biggest hidden risk) is now
   partially de-risked**: the catalogue confirms "Configuration Gap Analysis" and
   "SOT Upgrade & Alignment" are already-existing named services with an owning role
   (Upgrade Consultant) — meaning there is likely an existing, if manual, process and
   possibly existing artifacts (SOT records) to mine rather than building the client
   profile from nothing. Worth an early conversation with the Upgrade Team to find out
   what SOT data already exists in structured form.
5. **The like-for-like contractual constraint matters for scope.** Royal London's
   subscription explicitly excludes new/enhanced functionality delivery — so the
   Upgrade Impact Assistant's job for subscription clients is strictly "what changed
   and what's the like-for-like migration impact," not "should we adopt new features."
   Keep this framing explicit in any client-facing output to avoid scope-creep risk.
6. **Add a 13th "service" the catalogue doesn't yet have a home for**: this KB/assistant
   itself. Recommend it be owned as a capability under the Upgrade Centre of Excellence
   (matching the catalogue's own "Continuous Risk Improvement — Upgrade Centre of
   Excellence Manager" accountability line) rather than a standalone IT/engineering
   side project — this keeps the ownership question (raised in the earlier gap
   analysis) answered by the existing operating model rather than invented fresh.

## Open question to take back to the Upgrade Team
The docs describe *what* services and deliverables exist, and *who's* accountable, but
not the current effort/cost per deliverable — that baseline is essential to ever
credibly measure progress against a 60% reduction target, and it isn't something this
plan can infer from the catalogue alone.
