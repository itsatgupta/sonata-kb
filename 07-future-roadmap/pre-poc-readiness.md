# Pre-POC Readiness — Client Profile & Upgrade-Impact Data Foundation

**Status:** Draft (2026-08-04) · **Owner:** KB/Upgrade CoE lead
**Complements:** `03-poc/phase-1-data-requirements.md` (Royal London UAR/ISA *support* handoff),
`03-poc/agent/upgrade_analyzer.py`, `02-phases/phase-3-impact-assessment.md`,
`08-central-upgrade-team-alignment/catalogue-alignment.md`.

## Why this exists

Before we invest in the *next* POC (Upgrade Impact Assessment, Phase 3), we must de-risk the
long-lead dependencies. `gap-analysis.md` and `phase-3-impact-assessment.md` both flag the
same thing: **Client Profile data doesn't exist as clean structured data anywhere** — it lives in
people's heads, config exports, and prior upgrade docs. This doc is the prep gate:

1. What we're preparing for and why (Sections 1–2).
2. **The complete ask-list to hand the consultancy team** for a pilot client (Section 3).
3. How each item feeds the build and its benefit (Section 4).
4. Pilot-client pick + sequencing (Sections 5–6).

Goal: by the time the next POC starts, we can answer **"this is that client's upgrade impact"**
— not "Sonata impact in general."

---

## 1. What we're preparing for

The next POC is **Upgrade Impact Assessment**: given a client, their current Sonata version, and a
target version, automatically draft *what changed + what's relevant to THIS client + what's risky*,
human-reviewed (never auto-approved — rule 3). Three things gate it: **Client Profile**, a
**validated fixVersion→trunk mapping / `jira_version_range`**, and **tenant-isolated content**.

---

## 2. The five readiness workstreams (checklist)

### WS1 — Client Profile Registry *(critical path, longest lead)*
- [ ] Pick **2–3 pilot clients** (start small/simple; Royal London is the documented one).
- [ ] One **SME workshop per pilot client** against the form in Section 3.
- [ ] Agree a template/table (start curated spreadsheet → later real table).
- [ ] Confirm whether a client **entitlement/config repository** already exists to ingest
      (gap-analysis Q2) vs. being built fresh.
- [ ] Capture **current version + licensed modules + customizations + prior upgrade history**.

### WS2 — Content readiness (close indexed-data gaps)
- [ ] Index **release notes 16.4** (page `1001572222`) and **16.5** (page `1007867808`) — currently NOT indexed.
- [ ] Build the **Bitbucket path→module lookup** (currently stubbed `"UNMAPPED"`).
- [ ] Wire **CART/X-ray** test coverage (Jira filter `103721`) for pilot modules.

### WS3 — Version-diff engine *(critical path)*
- [ ] **Validate fixVersion→trunk mapping** against actual release notes (open question in `04-data-sources/jira.md`).
- [ ] Build + test `jira_version_range` end-to-end on a real version pair (16.4 → 16.5).

### WS4 — Ownership & operating model
- [ ] Decision: KB lives as a capability **under the Upgrade Centre of Excellence** (per
      `catalogue-alignment.md` #6), not a standalone side project.
- [ ] Capture **baseline effort/cost per catalogue deliverable** (needed to measure the 60% reduction target).
- [ ] Adopt the catalogue's **RACI** (Accountable roles keep sign-off).

### WS5 — Tenant isolation & governance (before client-facing use)
- [ ] Specify a **per-client namespace/tenant contract** (extend `WIKI_NAMESPACE`) so an EMEA client
      never sees an APAC client's corpus.
- [ ] Define the **sign-off workflow** (draft → human approve); outputs stay local files only.

---

## 3. THE ASK — data request for the consultancy team (pilot client: Royal London)

Hand this section to the consultancy team. Fill the blanks; mark "✓ have" for anything already in the
POC (listed here) so they only close gaps — don't re-supply known data.

> **Scope note (read first):** per `catalogue-alignment.md`, the assistant answers *"what changed and
> what's the like-for-like migration impact"* for subscription clients — **not** "should we adopt new
> features." Please don't gather feature-adoption/roadmap material; it's out of scope for this prep.

### A. Identity & environment
| # | Please provide | Pilot value |
|---|---|---|
| A1 | Client legal entity + region + operating countries | Royal London (EMEA/UK) |
| A2 | Instance(s): env URLs, # instances, dev/UAT/prod | — |
| A3 | Current Sonata version (production) | ✓ have: v16.1 (from `phase-1-data-requirements.md`; confirm) |
| A4 | Full version history installed to date | — |
| A5 | Support/contract tier (e.g., Premium, SLA) | — |

### B. Versions & fixVersion→trunk mapping *(critical)*
| # | Please provide | Note |
|---|---|---|
| B1 | Ordered list of trunk releases between two versions (e.g., 16.2→16.5) | ✓ have release-note page IDs for 16.4/16.5 |
| B2 | Confirmed **fixVersion→trunk release** mapping for the client's releases | **open question** in `04-data-sources/jira.md` |
| B3 | Planned/committed upgrade version + target quarter | ✓ have: c/w v16.2 planned (Q4) for UAR feature |

### C. Module / license / entitlement usage
| # | Please provide | Note |
|---|---|---|
| C1 | Licensed modules/components list (or entitlement export) | ✓ have: UAR, ISA, Payroll, GL (from `phase-1-data-requirements.md`) |
| C2 | Which modules are **actually in production use** vs licensed | **critical** — often differs |
| C3 | Whether a config/entitlement data source exists to ingest (vs. build fresh) | gap-analysis Q2 |
| C4 | Config/parameter exports (safe to share / anonymized) | — |

### D. Customizations & config deltas *(highest risk — customization overlap drives upgrade risk)*
| # | Please provide | Note |
|---|---|---|
| D1 | Change-request / custom-code inventory (Jira project keys) | ✓ have: project `RLSI` (Royal London defects) |
| D2 | Which Sonata components carry client-specific code/config (Bitbucket repos/modules) | needs path→module map (WS2) |
| D3 | Prior-upgrade documents showing what was customized last time | — |
| D4 | Any known deviations from stock behaviour | — |

### E. Regulatory / regional overlay
| # | Please provide | Note |
|---|---|---|
| E1 | Regulatory jurisdictions that affect this client (UK/EU for EMEA) | Royal London = UK (PRIIPs/RDR/ISA rules) |
| E2 | Region-specific rules the assistant must be careful not to generalise from | rule 4 — flag as data-gaps, never guess |

### F. Upgrade & defect history
| # | Please provide | Note |
|---|---|---|
| F1 | Prior version-to-version jumps + issues encountered | ✓ have defect tracker project `RLSI`; Jira filter `90250` |
| F2 | Historical defect density per module/version | feeds risk scoring |
| F3 | Known open blockers on the current version | — |

### G. Test coverage (CART / X-ray)
| # | Please provide | Note |
|---|---|---|
| G1 | CART test sets per module/version | ✓ have Jira filter `103721` |
| G2 | X-ray test execution status per module | Phase 2 scope; `xray_search` stubbed |

### H. Contacts & access (RACI + source access)
| # | Please provide | Note |
|---|---|---|
| H1 | Named: delivery lead, account manager, technical SME, QA lead | ✓ have SMEs: Pratigya, Sanjay Joshi |
| H2 | Access needed: Jira (filters `103721`, `90250`, project `RLSI`), Wiki (pages `1001572222`, `1007867808`), Bitbucket, X-ray | all **read-only** (rule 2) |
| H3 | Do-not-contact list / authorisation path for client-specific data | — |

---

## 4. Where each item feeds the build → benefit

| Item | Feeds | Benefit |
|---|---|---|
| A/B (versions, mapping) | `jira_version_range` (WS3) | ~80% of upgrade-impact answers |
| C/D (modules, customisations) | Client Profile relevance + risk scoring | per-client, not generic — the differentiator |
| E (regulatory) | regional overlay | safe EMEA/APAC use, rule-4 compliant |
| F/G (defects, tests) | risk model + recommended test-suite plan | actionable draft, not just a diff |
| H (contacts/RACI) | WS4 ownership + sign-off | accountability; no invented roles |

---

## 5. Pilot-client pick

**Recommended: Royal London** — the POC is grounded here (project `RLSI`, SME input, feature set
searchEmployer + Direct Uploads already eval'd). Stanlib is a valid alternative (a fix-version detail
already appears in the eval data) but the RLSI content is richer. If the goal is a *quick, low-risk*
first Client Profile, pick the smaller/simpler instance to bootstrap the template before tackling a
large one.

---

## 6. Sequencing — next 1–2 weeks

1. **Week 1:** send Section 3 (with A–H) to the consultancy for Royal London; simultaneously open WS2 (index 16.4/16.5) + WS3 (validate version mapping).
2. **Week 2:** run the Client Profile **SME workshop**; confirm fixVersion→trunk mapping; agree WS4 ownership with the Upgrade CoE.
3. **Gate:** WS1 + WS3 complete before the next POC starts. WS2/WS4/WS5 parallel.

---

*Update this file as items are closed (tick the boxes) and log progress in `PROGRESS-STATUS.md`.*