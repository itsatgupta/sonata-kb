# Phase 2 — Code + Test Layer (Bitbucket + X-ray)

## Goal
Add the "ground truth" layers — actual code changes and actual test coverage — and
link them into the entity graph, so the system can answer deeper technical questions
and (critically) support Phase 3's impact assessment with real change data, not just
narrative release notes.

## Scope
- Ingest Bitbucket: PR metadata (linked Jira key, files/modules touched, merge date,
  target branch/release) — **not full source code search** in v1; that's a much larger
  undertaking (semantic code search) and isn't needed for impact assessment, which cares
  about "what modules changed," not "how".
- Ingest X-ray: test cases linked to stories, pass/fail history per release.
- Entity graph now fully connects: Wiki spec ↔ Jira story ↔ PR/code module ↔ test.
- New capability: "what test coverage exists for feature X" / "was this defect covered
  by a regression test".

## Out of scope
- Full source-code semantic search / "explain this function" (separate initiative if
  ever needed — different tooling, e.g. code-aware embeddings over the Bitbucket repos).
- Automated test generation.

## Entry criteria
- Phase 1 complete and stable in production/pilot use.
- Bitbucket + X-ray API access confirmed (see `04-data-sources/`).

## Exit criteria
- Entity graph traversal working: given a Jira key, resolve to PRs and tests in one query.
- Module/component tagging on Bitbucket PRs validated as accurate enough to trust for
  Phase 3's client-impact filtering (this is the main quality bar to hit here).

## Related initiative: Smart Discovery foundation (don't duplicate)
The Centralised Upgrade Team's *Smart Discovery – Foundation Phase* proposal (see
`08-central-upgrade-team-alignment/smart-discovery-alignment.md`) plans to build the
code-estate structural map (agents.md) and the read-only access mechanism this phase
needs. Plan Phase 2 to **consume** those outputs rather than rebuild them; hold a
fallback (own access + own lightweight map) since the proposal is still a draft.
Entry criterion to add: confirm whether the Sonata estate is on Bitbucket or GitLab
before committing to this phase's Bitbucket tooling.
