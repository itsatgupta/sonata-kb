# Smart Discovery Foundation — Alignment with the Sonata Knowledge Assistant

Source doc: *Consultant Knowledge Base - foundation.docx* (AI Initiative Proposal — "Smart
Discovery – Foundation Phase", v0.2 draft for review, 27 Jul 2026; initiative lead Tamoor
Malik, sponsor Nick Fraser).

This is a second, complementary initiative from the same Centralised Upgrade Team / AI
working group. Where the Service Catalogue alignment told us *what to automate*
(`catalogue-alignment.md`), this doc tells us *who is already building the code-estate
access and knowledge layer this plan was going to have to build itself*. That makes it a
genuine de-risker for Phase 2 and Phase 3 — and the source of one important open question
(GitLab vs Bitbucket) that must be resolved before Phase 2.

## What Smart Discovery is (in one paragraph)

Smart Discovery is a roadmap AI capability: a consultant asks a natural-language question
(e.g. *"what initiatives, epics and stories are required to implement this change, and how
much is configuration vs new build"*) and gets a structured, defensible answer grounded in
the codebase, Jira and customer context. It is being approximated manually today (feeding
meeting transcripts to a model); the manual approximation works, but it cannot become a
repeatable product until three gaps are closed:

1. **Access** — consultants shouldn't hold the full Sonata repo on their machines; agents
   need controlled read access.
2. **Consistency** — every consultant improvises their own prompting; nothing accumulates
   as institutional knowledge.
3. **Live system context** — code and Jira describe intent; the running instance describes
   reality.

The proposed foundation phase (8 weeks from access being in place, ~$50–100/month for 5–10
consultants) delivers against these in order.

## The foundation phase deliverables (and what each means for SKA)

| Component | What it is | Weeks | What it means for SKA |
|---|---|---|---|
| **C1 — Sonata structural map** | `agents.md` describing module boundaries, naming conventions, where behaviours are implemented, a symbol/module index. Framed as "knowledge work, not engineering" and made the first-class deliverable ("the map matters more than the pipe"). | 1–4, refined throughout | **This is the Feature/Module taxonomy + path→module lookup that Phase 1/2 flagged as their hardest data-quality dependency** (see `01-architecture/system-design.md` entity table and `04-data-sources/bitbucket.md` open questions). SKA should consume C1, not rebuild it. Verify C1's granularity supports client-impact filtering before Phase 3 leans on it. |
| **C2a — Access mechanism spike** | 2-week timeboxed eval: direct GitLab API (scoped read-only token + a skill file describing the API) vs bespoke CLI bridge; also settles credential custody | 1–2 | The access route SKA's `bitbucket_tool` / ingestion layer rides on. Same governance posture as SKA's CLAUDE.md rules (read-only, no write path). |
| **C2b — Access mechanism build** | Implementation of whichever route the spike selects: read-only service account over VPN, plus distribution/update/credential-rotation | 2–5 | If it lands, SKA Phase 2 gets a maintained access mechanism instead of building one. Watch for whether it exposes PR metadata + files-changed (what SKA needs), not just raw code. |
| **C3 — Bravura skill pack** | Central markdown skill files (SpecKit conventions): access usage, Sonata/Bravura terminology, standard analysis & design workflow. Held centrally so updates roll out to all users. | 3–6 | **This answers the ownership-model question raised in `07-future-roadmap/gap-analysis.md` (#6)**: a centrally-held skill pack with named owners and a fortnightly AI working group is the institutional home SKA's shared knowledge layer slots into. SKA's own CLAUDE.md + per-tool specs are a per-repo instance of exactly this pattern. |
| **C4 — NL query over SBS services** | Read the SBS WSDL, call existing services for operational answers (failed-job counts, price-file arrival times). Read-only. | 5–8 | **A capability SKA doesn't have**: live-system verification of static-index answers. Candidate Phase 3+ addition ("is this client's running instance consistent with what the index says"). |
| **C5 — Read-only GraphQL layer** | Candidate only — explicitly NOT in this ask; separate decision with core-platform implications | post-foundation | Potential shared read-layer for code/config if it proceeds. Watch, don't build. |

## Where this changes SKA's plan

1. **Phase 2 should not build its own code access or module map from scratch.** If Smart
   Discovery's foundation is approved (it's a *v0.2 recommendation/proposal*, not a
   committed plan), Phase 2's entry/exit criteria should reference C1/C2 output as the
   code-side spine rather than assume SKA builds it. Sequencing: SKA Phase 0 and Phase 1
   (Wiki + Jira, no code dependency) can proceed in parallel regardless; Phase 2 (code +
   test layer) should be planned to consume the structural map and access mechanism.

2. **The GitLab vs Bitbucket question is now unavoidable.** Smart Discovery assumes the
   Sonata code estate lives on **GitLab** (the open item names the GitLab administrator as
   the one to provision the read-only service account). SKA's entire code layer assumes
   **Bitbucket** (`CLAUDE.md`, `04-data-sources/bitbucket.md`, Phase 2). These are
   incompatible assumptions about the same estate. Resolve before Phase 2: which system
   holds the Sonata product repos, and does the Bitbucket integration spec need to be
   rewritten as a GitLab one? (Flag added to `04-data-sources/bitbucket.md`.)

3. **Two different "impact assessments" now exist — disambiguate them.**
   - **SKA (Phase 3)**: *Upgrade impact assessment* — given a client + current/target
     trunk version, what changed and what's the client-specific impact/risk.
   - **Smart Discovery**: *change decomposition* — given a desired change, produce
     initiative/epic/story structure + a config-vs-build split.
   These are complementary (top-down from intent vs bottom-up from release diffs) and could
   eventually share a graph — but the shared name will cause confusion. The roadmap should
   keep them distinct: "Upgrade Impact Assessment" vs "Change Decomposition".

4. **Governance posture confirmed — and worth strengthening.** Smart Discovery's three
   preconditions (read-only credentials with no write path, VPN-restricted access, a named
   individual accountable for approving the access design) match SKA's CLAUDE.md
   non-negotiables and `06-governance/`. Worth adopting its *honest* framing of credential
   custody: client-side credentials "reduce routine and incidental exposure, not a hard
   boundary; a firmer boundary means a server-side build with its own decision." SKA's
   governance doc should say the same rather than imply hard isolation.

5. **Shared critical path = access provisioning.** The doc names the exact blocker
   (default GitLab roles yield no visibility; explicit project-level grants required; a
   named administrator + escalation route; provisioning to start before the phase formally
   begins). SKA Phase 2 needs the same grants. One request, one administrator, one
   escalation route — do not file two.

6. **Live-system context is a real gap in SKA's design.** SKA is a static-index assistant
   (freshness = poll cadence). C4 introduces querying the running instance. If it works,
   it's the natural answer to "is this wiki/Jira description actually true of the running
   system" — add as a Phase 3+/roadmap candidate, not v1.

## Risks this doc surfaces for SKA

- **Proposal status**: v0.2 draft for review, gated on six business decisions plus a
  critical-path open item (service account). SKA must not hard-depend on it yet — plan
  Phase 2 with a fallback (own access + own lightweight map) in case it stalls.
- **Retrieval quality at repository scale** is Smart Discovery's main engineering unknown
  (mitigated by making the structural map first-class and measuring hit rate during the
  spike, with a pre-built index held as fallback). SKA Phase 2 doesn't need full-code
  search, but it *does* need C1's map to be accurate for module tagging — treat C1
  accuracy as a Phase 3 precondition, not a given.
- **Tooling divergence**: the doc deliberately designs for portability across the
  Claude/Copilot tooling decision (access via skill files). SKA is Claude Code-specific.
  Fine for now, but keep the knowledge layer (markdown maps/skills) tool-agnostic so
  neither initiative strands the other.

## Open questions to take back to the initiative

1. **GitLab vs Bitbucket** — which system holds the Sonata product repos? (Blocks Phase 2
   tooling; see `04-data-sources/bitbucket.md`.)
2. If C1 produces a structural map, will it carry module/path tagging at the granularity
   SKA's client-impact filtering needs, and in a form SKA can import?
3. The proposal's open item "quantified benefit case — consultant hours per impact
   assessment" (Nick Fraser, due Week 4) overlaps SKA's Phase 3 success metric (days → under
   1 hour per assessment). Worth aligning both benefit cases to the same baseline so the
   60% cost-reduction target is measured once.
4. Review home: `catalogue-alignment.md` recommended the Upgrade Centre of Excellence
   accountability line as the KB's home; this proposal uses the fortnightly AI working
   group. Reconcile the two so SKA has a single ownership answer.
