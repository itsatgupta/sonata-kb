# Data Source: X-ray (Testing)

## What we ingest (Phase 2)
- Test cases: key, title, steps summary, linked story/requirement, module/component tag.
- Test execution history: pass/fail per release/test plan, linked defects if a test
  failure was logged as a bug.

## Why it matters for both use cases
- Functional Q&A: "is there a regression test for X" / "how is this validated".
- Impact assessment: coverage gaps are a risk signal — a changed area with thin test
  coverage is higher risk for a client upgrade, independent of the change's own size.

## Refresh cadence
- Sync test execution results after each trunk release's test cycle completes —
  doesn't need to be real-time.

## Open questions
- X-ray API access model (Jira plugin API vs standalone) — confirm your instance's setup.
- Are tests reliably tagged to component/module today, or does this need cleanup
  (same risk as Jira component tagging — likely needs a normalization pass).
