# Data Source: Bitbucket

## What we ingest (Phase 2, not POC)
- PR metadata: id, title, description, author, merge date, target branch/release,
  linked Jira key(s) (parsed from branch name/PR title/commit message conventions —
  audit your team's actual convention first).
- Files/paths touched per PR → map to module/component via a path-to-module lookup
  table (needs to be built with engineering input — this mapping is the crux of
  making impact assessment accurate).

## What we deliberately don't ingest in v1
- Full source code content for semantic "explain this code" search — separate,
  larger initiative if ever justified (needs code-aware embeddings, much bigger corpus).

## API/access notes
- Use Bitbucket REST API (or Bitbucket Data Center API if self-hosted) with a read-only
  service account.
- Rate limits: batch pulls, incremental sync via merge-date watermark, not full re-pull
  each time.

## Refresh cadence
- Daily batch sufficient — code-change data isn't needed in real time for either chatbot
  use case.

## Open questions to resolve with engineering before Phase 2
- Is there already a consistent Jira-key-in-branch-name or commit-message convention?
  If not, linking PRs to Jira issues reliably may need the Jira side (issue → linked PR
  field, if your Jira/Bitbucket integration already populates this) instead of parsing text.
- Who owns/maintains the path→module mapping long-term as the codebase evolves?
- **Is the Sonata code estate actually on Bitbucket, or GitLab?** The Centralised
  Upgrade Team's Smart Discovery foundation proposal assumes GitLab (GitLab administrator
  provisions the read-only service account). If the product repos are on GitLab, this
  spec's Bitbucket REST/Data-Center assumption needs to be rewritten before Phase 2.
  See `08-central-upgrade-team-alignment/smart-discovery-alignment.md`.
