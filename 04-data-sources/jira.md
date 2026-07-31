# Data Source: Jira

## What we ingest
- Epics, stories, defects — summary, description, acceptance criteria, comments
  (optional, may be noisy — evaluate value vs noise in POC), fixVersion(s), component(s),
  labels, status, linked issues, linked PRs (if Bitbucket-Jira integration populates this).

## Why structured fields matter more here than free text
Jira's real value for this system is its **structured metadata** (fixVersion, component,
type, status) — this is what makes version-diff and impact-assessment queries possible.
Keep these as first-class filterable fields in the index, not just embedded text.

## Chunking approach
- One issue = one primary chunk (summary + description + acceptance criteria), with
  metadata attached. Large description/comment threads may need secondary chunking,
  but don't split acceptance criteria across chunks — it's usually a discrete, important unit.

## Refresh cadence
- Daily incremental sync via JQL query on updated date, or webhook on issue
  create/update/transition if available.

## Version mapping (critical for Phase 3)
- Build and validate a clean mapping of **fixVersion → trunk release** — confirm this is
  1:1 and consistently applied across teams/projects before relying on it for impact
  assessment. Inconsistent fixVersion hygiene is a common real-world gotcha — audit early.

## Open questions
- Which Jira project(s)/boards cover Sonata specifically (vs other Bravura products)?
- Is component tagging consistent enough across teams to use directly for module-level
  impact filtering, or does it need a normalization pass?
