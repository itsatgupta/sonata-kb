# Choosing the POC Enhancement

## Criteria for a good pilot feature
1. **Recently shipped** (last 2-3 trunk releases) — so the wiki/Jira/release-note trail
   is fresh and someone still remembers the details to grade answers.
2. **Fully documented** — has a wiki spec page, a Jira epic with stories + acceptance
   criteria, and a release note entry. If any of these is missing, pick a different
   feature — POC should prove the loop works, not fight documentation gaps on day one.
3. **Small and self-contained** — a single field, screen, calculation rule, or config
   option, not a cross-cutting change touching many modules.
4. **Has "before vs after" behavior** — ideally an enhancement that changed existing
   behavior (not a brand-new standalone feature), so you can also test the assistant's
   ability to explain a delta, which is a preview of Phase 3's core skill.
5. **A named SME is available** to write test questions and grade answers.

## Suggested process
1. Pull the last 3 release notes from wiki.
2. Shortlist 3-5 enhancement candidates meeting criteria 1-3.
3. Confirm documentation completeness for each (quick manual check).
4. Pick the one with clearest "before/after" story and most available SME time.
5. Write 20-30 test questions BEFORE building anything (avoid tuning the system to the
   test set after the fact) — mix of:
   - Direct fact lookup ("what does field X control")
   - Explanation ("why does this validation rule exist")
   - Before/after ("what changed", "would this affect a client on version Y")
   - Edge case / negative ("does this feature affect module Z" where the correct
     answer is "no" — tests the system doesn't hallucinate relevance)

## Template: candidate feature one-pager
```
Feature name:
Trunk release introduced:
Wiki page(s):
Jira epic/stories/defects:
Release note excerpt:
SME contact:
Why this is a good POC candidate:
```

## Selected POC candidates (2026-07)

### 1. searchEmployer SBS to support pagination (RLSI-6059)
```
Feature name: searchEmployer SBS to support pagination (RLSI-6059)
Trunk release introduced: Sonata 16.2
Wiki page(s): RLSI-6059 searchEmployer SBS to support pagination (space CliRln, page 973706490)
Jira epic/stories/defects: BASE-458832 (story), FEAT-9707 (work package), BASE-458836 (release note), BASE-458911 (schema change), BASE-460256 / BASE-460272 (defects)
Release note excerpt: BASE-458836 — "Operation searchEmployer now supports pagination & indexed sorting via new optional pagingRange element, improving scalability for Workplace Pension product, ensuring alignment with HMRC requirements"
SME contact: Pratigya
Why this is a good POC candidate: Recently shipped, small SBS enhancement adding an optional pagingRange element (default 20 results/page from result index 1, ordered by Employer Number); clean before/after delta; complete wiki + Jira + release-note trail.
```

### 2. Direct Uploads — saveExternalCorrespondence document size allowance (FEAT-10148 / LIBSON-3635)
```
Feature name: Direct Uploads — increase document size allowance for saveExternalCorrespondence SBS (LIBSON-3635)
Trunk release introduced: Sonata 16.6
Wiki page(s): LIBSON-3635: Direct Uploads - Increase document size allowance for saveExternalCorrespondence sbs (space CliStl, page 1001573493)
Jira epic/stories/defects: FEAT-10148 (work package), FEAT-10149 (IA), FEAT-10150 (design), BASE-464868 (story), BASE-464872 (release note), XRAY-80540 (tests)
Release note excerpt: BASE-464872 — "SBS saveExternalCorrespondence request enhanced to increase the maximum document upload size from 2MB to 10MB, improving the adviser and client experience on the client web platform"
SME contact: Sanjay Joshi
Why this is a good POC candidate: Tiny, self-contained change (single HLR/HLS, one hardcoded limit 2MB → 10MB); textbook before/after; complete documentation trail; RDA explicitly out of scope (already allows 10MB).
```
