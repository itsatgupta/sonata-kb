# Phase 1 Scoping Strategy: Client-First, Feature-Segmented Approach

**Status:** Recommendation (pre-Phase-1 kickoff)  
**Context:** POC succeeded on 1 feature. Phase 1 must scale without:
- Choking Wiki/Jira with bulk ingestion
- Building a 6-month data pipeline before proving ROI
- Hitting performance cliffs from hitting source APIs on every query

**Your concern is valid:** Enumerating all Wiki spaces + all Jira projects in EMEA/APAC with N clients × M features each = analysis paralysis + infrastructure thrashing. **We need a different phase sequencing.**

---

## Recommended Approach: "Client Cohort" Model (NOT "Whole Product" Model)

Instead of:
- **Bad:** Ingest ALL wiki + ALL Jira → build index for "every module" → hope it answers questions

Do:
- **Good:** Pick 1–2 high-value clients (1 EMEA, 1 APAC ideally) → enumerate **their** modules/features → ingest those scoped chunks → measure Q&A quality & query performance → iterate → then expand

### Why this works

1. **Bounded scope**: "What features does Client A use?" is answerable via SME interview (2–3 hours) + config review. "What features does Sonata have?" is a 2-week rabbitehole.
2. **Performance proven early**: Real query volume on real client questions (not synthetic test sets) reveals caching/DB issues before scale.
3. **ROI visible fast**: Within 4 weeks, Client A's support team is using the bot → you have proof of life before investing in EMEA + APAC rollout.
4. **Mitigates political risk**: You're not asking Wiki/Jira teams to approve a "vacuum all our content" project; you're asking them to export a focused slice per client.

---

## Phase 1 Revised: Three Parallel Workstreams (12–14 weeks total)

### WS1: Data Architecture & Storage Layer (Weeks 1–4, ongoing)

**What to build:**
- **Hybrid retrieval backbone** (not just vector search):
  - Vector store for semantic search (chunks, embeddings)
  - Graph layer for entity relationships + versioning
  - Metadata layer for filtering (client ID, module, fix version, date ranges)
  
**Technology recommendation:**
- **Vector store**: Use what Bravura already licenses (Elasticsearch, Pinecone, Weaviate). If nothing, use **PostgreSQL + pgvector** (open-source, no new procurement, works with hybrid queries).
- **Graph layer**: Start lightweight — **PostgreSQL with JSON columns** or lightweight graph queries (not Neo4j unless you already use it).
- **NOT a full RAG database yet** — you're building the *structure* that RAG systems sit on top of. Think: "indexed chunks + metadata + relationships."

**Why NOT "hit Wiki/Jira every query":**
- ❌ Latency: API round-trips = 500ms–2s per query (unacceptable for chat)
- ❌ Rate limits: Jira/Wiki have strict API throttles; every user query burns quota
- ❌ Cost: API calls at scale = $$ (you paid ~$0.11/question to Claude in POC; don't spend $0.50/question just fetching Jira)
- ✅ Instead: **Cache strategically** — ingest daily/on-demand, update index incrementally, query only the index

### WS2: Pilot Client Cohort Selection & SME Workshop (Weeks 1–3)

**Pick 2 pilot clients:**
1. One from EMEA (e.g., mid-sized, uses ~8–12 Sonata modules)
2. One from APAC (different feature set, validates regional variation)

**Run a 2-hour SME workshop per client to enumerate:**
- Which modules they use (searchEmployer, account reconciliation, payroll, etc.)
- Which features are critical (the 80/20 — usually 5–7 out of 40+ modules)
- Known pain points / gaps in existing documentation

**Outcome**: A scoped "client feature set" (CSV: Module | Used Y/N | Criticality | Known gaps)

### WS3: Scoped Ingestion & Feature-Level Indexing (Weeks 4–10)

**Per pilot client, ingest only:**

| Source | Scope | Effort | Notes |
|--------|-------|--------|-------|
| **Wiki** | Pages tagged with client's modules only (e.g., "searchEmployer", "payroll") | 1–2 eng-weeks | Filter by wiki space + page properties/labels |
| **Jira** | Epics/stories/defects for those modules, last 3 releases + current | 1 eng-week | JQL: `component in (searchEmployer, payroll) AND fixVersion in (v11.5, v11.6, v12.0, v12.1) ORDER BY fixVersion DESC` |
| **Bitbucket** | PRs touching those modules, last 6 months | 1–2 eng-weeks | Module→file mapping, then filter PRs by files touched |
| **X-ray** | Tests linked to those Jira stories | 1 eng-week | Stub for now; Phase 2 scope |

**Do NOT ingest:**
- Pages tagged "internal-only", "deprecated", "research"
- Jira issues from 5+ releases ago (noise, not actionable)
- All of Bitbucket (massive; filter ruthlessly)

### WS4: Index Architecture & Query Performance (Weeks 6–12, overlap with WS3)

**Build:**
1. **Chunk strategy for Wiki**: By section (not whole page). Example: searchEmployer page → chunks for "What is SBS?", "How to configure pagination", "Known limitations", each with parent page context.
2. **Embedding strategy**: Embed chunk + parent context (so embeddings carry "what module is this?" + "what page?").
3. **Metadata indexing**: Every chunk carries `{client_id, module, fix_version, page_url, last_updated}`.
4. **Caching layer**: Cache retrieved chunks + re-ranker output (most queries repeat).

**Query performance targets:**
- Single semantic query (no filters): <200ms
- Filtered query (e.g., "searchEmployer module, v12.0 only"): <300ms
- Composed query (e.g., "version diff for Client A from v11.5→v12.1"): <1s

**If targets missed:**
- Add read replicas for vector store
- Index aggressively (Jira keys, module names, version ranges)
- Move to Elasticsearch if PostgreSQL pgvector is bottleneck

### WS5: Q&A Eval Set (Per-Client) & Iterative Refinement (Weeks 8–14)

**For each pilot client:**
- Work with their support/BA team to collect 30–50 real questions they get asked
- Run evals (same as POC: % correct, % cited, % hallucinated)
- **Target: ≥80% correct with accurate citations**
- Iterate on retrieval (better chunking, re-ranking) not just model tweaks

**Success criteria:**
- Client A support team uses bot for 20% of inbound queries (measured)
- Time-to-answer drops from 5 min (manual) to 30s (bot + human review)
- SME escalation rate: <10% of queries

---

## Database Architecture (Answering Your "Vector DB?" Question)

### What you're building: **Structured + Semantic Hybrid Index**

```
┌─────────────────────────────────────────────────────────────┐
│ PostgreSQL (or Elasticsearch)                               │
├─────────────────────────────────────────────────────────────┤
│ Chunks table:                                               │
│  - id, text, embedding (pgvector), module, fix_version      │
│  - client_id (filter: which clients use this chunk)         │
│  - wiki_page_id, jira_key, pr_id (entity links)            │
│  - last_updated, source_type (wiki|jira|bitbucket)         │
├─────────────────────────────────────────────────────────────┤
│ Entities table:                                             │
│  - Feature/Module: id, name, owning_team, modules_it_owns  │
│  - Client profile: id, name, region, modules_used,         │
│    current_version, customizations                         │
│  - Release: version, date, included_jira_keys              │
├─────────────────────────────────────────────────────────────┤
│ Relationships:                                              │
│  - Chunk ← → Jira key (1:many, a story has multiple chunks)│
│  - Jira key ← → PR id (linked PRs)                         │
│  - Jira key ← → Test (X-ray)                               │
│  - Release ← → Jira keys in that release                    │
│  - Client ← → Modules (entitlements)                        │
└─────────────────────────────────────────────────────────────┘
```

### NOT a "full RAG database" yet, but the foundation

- **Vector search**: `SELECT * FROM chunks WHERE embedding <-> query_embedding < distance_threshold ORDER BY distance LIMIT 5`
- **Metadata filtering**: Same query but `WHERE client_id = $1 AND module = $2 AND fix_version >= $3`
- **Graph traversal** (Phase 3): `Find all Jira keys in version range → resolve to modules → check if Client A uses them → fetch risk scores`

### Ingestion frequency

- **Wiki**: Once daily (off-peak, ~1 hour)
- **Jira**: Once daily + on-demand for "latest issue" scenarios
- **Bitbucket**: Once weekly (large volume; full scan is slow)
- **X-ray**: Once weekly

**No "real-time sync" needed** — chat answers don't need <1min freshness; daily is fine.

---

## Why This Avoids Your Concerns

| Your Concern | This Approach | Why It Works |
|---|---|---|
| "Enumerating all Wiki/Jira will take forever" | Pick 2 clients + their modules only (~10–15 modules per client) | 80/20 rule: 80% of support questions about 20% of features |
| "Will choke Wiki/Jira with bulk exports" | Scoped queries per client/module | Jira JQL is designed for this; Wiki spaces are usually module-aligned anyway |
| "Performance issues at scale" | Measure on real traffic first (2 clients × their question load) | Find bottlenecks early; fix architecture, not just indexes |
| "Are we building RAG?" | Hybrid index (vector + metadata + graph) | Not a generic RAG database; structured specifically for Sonata's use case |
| "Hitting APIs every query" | Cache, index, query the cache | Vector stores are designed for this |
| "Regional/feature variation" | Start with 1 EMEA + 1 APAC client | Variations handled by client_id + module metadata filters |

---

## Revised Phase 1 Timeline

| Timeline | Workstream | Output |
|---|---|---|
| **Weeks 1–3** | WS1 setup + WS2 SME workshops | Data architecture + 2 client feature profiles |
| **Weeks 4–6** | WS3 scoped ingestion (client 1) | Index of Client A's modules (Wiki + Jira) |
| **Weeks 7–9** | WS4 perf tuning + WS5 eval | <300ms queries, ≥80% correctness on real questions |
| **Weeks 10–12** | WS3 ingestion (client 2) + WS5 expand | Client B indexed + both clients in pilot use |
| **Weeks 12–14** | Refinement + readiness for Phase 2 | Documented architecture, team trained, ready to expand |

**Total: 12–14 weeks** (vs. the original 6–8 week estimate, because this is **cautious**, **measured scale**, not a "build it all fast and hope" approach).

---

## Phase 2 Then Becomes: "Expand to N Clients"

Once you've proven architecture + Q&A quality on 2 clients, Phase 2 is **template replication**:
- For each new client: run 2-hour SME workshop + apply same ingestion template → client's data added to shared index (with client_id filtering)
- Add new modules as they're discovered (most clients use 70% overlap + 30% custom)

**Phase 2 can be much faster** (4–6 weeks for 10 clients) because the hard part (architecture + patterns) is proven.

---

## What You Tell Stakeholders

*"POC proved the core loop works on 1 feature. Phase 1 takes a measured approach: pick 2 pilot clients (1 EMEA, 1 APAC), ingest their actual feature set (10–15 modules each), and validate Q&A quality + performance on real support traffic. This de-risks scale-out. Once proven, Phase 2 replicates the template across N clients in parallel. **No full-product ingest**, no infrastructure thrashing, ROI visible in 12 weeks."*

---

## Open Questions to Resolve Now

1. **Which 2 pilot clients?** (You pick — ideally not your most complex, but representative of regional variation)
2. **Client profile data location**: Where does Bravura track "Client X uses modules Y, Z"? (Existing system, SME interviews, config exports?)
3. **PostgreSQL + pgvector vs. existing vector DB?** (Do you already use Elasticsearch/Pinecone/etc.?)
4. **Ingestion infrastructure**: Can you self-host (EC2, K8s) or use managed (Pinecone, Weaviate Cloud)?

---

## Next Step

This strategy trades **breadth** (all modules, all clients) for **depth** (proven architecture, measured expansion). It's the safe path for a large, fragmented product. Ready to move forward with this scoping, or do you want to adjust?
