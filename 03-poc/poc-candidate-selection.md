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
