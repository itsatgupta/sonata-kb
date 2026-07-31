# System Design

## Layered architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Interface Layer                                            │
│  Chat widget (web/Teams/Slack) · Voice bot (STT/TTS wrapper) │
└───────────────────────────▲───────────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────────┐
│  Orchestration Layer (agent)                                 │
│  Intent routing: "functional Q&A" vs "impact assessment"      │
│  vs "release note lookup" · conversation memory · citations   │
└───────────────────────────▲───────────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────────┐
│  Retrieval Layer                                              │
│  Hybrid search (vector + keyword + metadata filters)          │
│  Per-corpus retrievers: Wiki / Jira / Bitbucket / X-ray        │
│  Re-ranker · citation resolver                                │
└───────────────────────────▲───────────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────────┐
│  Knowledge Graph / Index Layer                                 │
│  - Document store (chunked, embedded) per source               │
│  - Entity graph: Feature ↔ Wiki page ↔ Jira epic/story ↔        │
│    code module/PR ↔ X-ray test ↔ release version               │
│  - Version timeline: trunk release N → N+1 → ... diffs         │
│  - Client profile: which modules/customizations each client uses│
└───────────────────────────▲───────────────────────────────────┘
                            │
┌───────────────────────────┴───────────────────────────────────┐
│  Ingestion Layer (per-source connectors, see 04-data-sources/) │
│  Bitbucket API · Wiki API (Confluence/other) · Jira API · X-ray API │
└─────────────────────────────────────────────────────────────┘
```

## Why an entity graph, not just RAG-over-documents
Plain vector search over wiki pages answers "explain feature X" reasonably well, but
**upgrade impact assessment is fundamentally a graph traversal problem**: given
version range [v_from, v_to], find all Jira stories/defects delivered in that range,
resolve to their linked wiki spec sections and code PRs, then filter to modules the
client actually uses. A pure semantic-search layer can't do the "in this version
range" and "for this client's configuration" filtering reliably — that needs
structured metadata (fix version, epic, component/module, client entitlement) sitting
alongside the embeddings. So: **hybrid** — vector search for "explain this concept",
structured graph queries for "what changed / what's affected."

## Key entities
| Entity | Source | Key attributes |
|---|---|---|
| Feature/Module | Wiki (curated) | name, owning team, related components |
| Wiki page | Wiki | title, space, last-updated, linked Jira keys |
| Epic/Story/Defect | Jira | key, fix version, component, acceptance criteria, linked PRs, status |
| Code change | Bitbucket | PR id, files touched, linked Jira key, merge date, target branch/release |
| Test | X-ray | test key, linked story, module, pass/fail history |
| Release | Wiki release notes + Jira fixVersion | version number, date, list of included Jira keys |
| Client profile | (new — needs to be built, see below) | current version, modules/customizations in use, past upgrade history |

**Client profile is the one entity that doesn't already exist anywhere as clean data.**
This is likely the single biggest piece of new work in the whole project — see
`03-poc/` and `07-future-roadmap/gap-analysis.md`.

## Retrieval strategy per question type
1. **"How does X work?"** → vector search over Wiki (primary) + Jira acceptance criteria
   (secondary, for edge-case behavior) → synthesize with citations.
2. **"What changed between v_a and v_b?"** → structured query: all Jira issues with
   fixVersion in (v_a, v_b] → group by component → pull release-note summaries →
   optionally pull linked wiki spec diffs.
3. **"What's the impact for Client Z upgrading v_a→v_b?"** → step 2's result, filtered/
   weighted by Client Z's module usage profile → risk-scored (see impact-scoring model
   in `02-phases/phase-3-impact-assessment.md`) → generated report.
4. **Voice variant of any of the above** → same pipeline, response passed through a
   TTS-friendly formatting pass (short sentences, no tables/code blocks, reads numbers
   and version strings naturally) before speech synthesis.

## Freshness / sync
- Wiki, Jira, Bitbucket, X-ray are all polled/webhooked on a schedule (see per-source
  spec docs) — target: index reflects wiki/Jira within 24h, release notes within 1h of
  publish (these matter most for "what's new" queries).
- Every answer carries a "last verified against source as of [date]" marker to build trust
  and expose staleness rather than hide it.

## Suggested initial tech choices (adjust to your existing stack)
- Embeddings + vector store: whatever your org already licenses (avoid a new procurement
  cycle for the POC) — Confluence/Jira/Bitbucket connectors are the hard part, not the vector DB.
- Orchestration: Claude with tool-use, one tool per data source + one "impact assessment" tool
  that composes graph queries server-side rather than asking the model to do multi-hop
  reasoning over raw retrieved chunks.
- Voice: any STT/TTS layer wrapping the same chat backend — do not build a parallel voice-only
  brain; voice is a presentation layer, not a separate assistant.
