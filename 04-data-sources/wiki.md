# Data Source: Wiki (Design/Arch/Tech Specs + Release Notes)

## What we ingest
- All spaces/pages under Sonata design, architecture, and tech spec areas.
- Release notes pages specifically (tag/track separately from general spec pages —
  they have different structure and are the backbone of the version-diff feature).

## Structure to preserve, not flatten
- Page hierarchy (parent/child) — informs module taxonomy.
- Page metadata: space, last-modified date, last-modified-by, labels/tags.
- Any existing labels that map to modules/components — audit what's already tagged
  before inventing a new taxonomy from scratch.

## Chunking approach
- Chunk by heading/section, not fixed token windows — specs are structured documents
  and section boundaries usually align with meaningful units (avoid splitting a table
  or a single rule description across chunks).
- Keep a "page + section" citation granularity so answers can link to the specific
  section, not just the page.

## Refresh cadence
- Target: reflect edits within 24h for general specs; release-notes pages should be
  picked up within 1h of publish (webhook if the wiki platform supports it, else
  frequent polling) since "what's new" queries are time-sensitive right after a release.

## Freshness/trust handling
- Every ingested page carries its last-modified date; answers should surface "as of
  [date]" so staleness is visible rather than silently trusted.
- Flag pages not updated in a long time relative to a linked Jira issue's resolution
  date — signal of possible doc drift, useful both to the retrieval layer (lower
  confidence) and as a documentation-debt report for Phase 1.

## Open questions
- Which wiki platform (Confluence vs other)? Determines API/export mechanism.
- Are release notes structured/consistent enough to parse the fixVersion↔Jira key
  list programmatically, or free text requiring an LLM extraction pass?
