# Phase 1 Execution: Single-Client, Single-Feature Model
## With Complete System Workflow & Stakeholder Narrative

**Context:** POC proved the loop on 1 feature (searchEmployer). Phase 1 proves it on 1 client's 1 most-critical feature, then replicates that pattern.

---

## Part 1: Why This Sequencing (Stakeholder Perspective)

### The Pitch

*"The POC proved the core engine works. Phase 1 takes zero risk: pick one real client (say, EMEA bank), their #1 pain-point feature (e.g., 'How does searchEmployer work?'), implement end-to-end (data→ index → chat → eval), measure success with their support team, and ship. Once that's working, we have a replicable playbook: each new client/feature takes 3–4 weeks. By end of 2026, we're covering 10 clients × 3–5 features each. No guessing, no paralysis."*

**Why one client, one feature?**
- ✅ Scope is **bounded and achievable** (not "all Sonata")
- ✅ Success is **measurable** (Client A's support team says "this works")
- ✅ Risk is **contained** (if it fails, it's 1 client, 1 feature; we learn and adjust)
- ✅ ROI is **immediate** (Client A's support cost drops in week 12)
- ✅ Expansion is **predictable** (each new feature = same 3–4 week template)

---

## Part 2: Complete End-to-End Workflow (Data → Stakeholder Presentation)

### **The System After Client 1 Implementation**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         STAKEHOLDER-FACING DASHBOARD                         │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ "searchEmployer" feature · Client EMEA Bank · v12.0 & v12.1           │ │
│  ├────────────────────────────────────────────────────────────────────────┤ │
│  │ 📊 Metrics:                                                             │ │
│  │   • 427 questions answered in support chat this week                   │ │
│  │   • 89% accuracy (vs. baseline: manual lookup by SME)                 │ │
│  │   • Avg response time: 0.8 sec (vs. baseline: 15 min manual)           │ │
│  │   • SME escalation rate: 11% (questions bot flagged as "I don't know") │ │
│  │                                                                         │ │
│  │ 📈 Support Team Feedback:                                              │ │
│  │   • "Reduced our searchEmployer tickets by 35%"                       │ │
│  │   • "Answers are accurate enough to hand to clients"                  │ │
│  │   • "Time to resolution dropped from 20 min to 3 min"                 │ │
│  │                                                                         │ │
│  │ 🔗 Citation & Trustworthiness:                                         │ │
│  │   • Every answer links back: Wiki page § section · Jira story · Date  │ │
│  │   • Last indexed: today 14:32 UTC                                      │ │
│  │   • Known gaps: 3 Confluence pages marked "review needed"              │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

                                      ↓ (Data flow)

┌─────────────────────────────────────────────────────────────────────────────┐
│                          CHAT INTERFACE (Support Team)                       │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Q: "What's the difference between SBS and non-SBS searchEmployer?"    │ │
│  │                                                                         │ │
│  │ Bot: SBS (Search by Specification) is a pagination mode for searches  │ │
│  │      that return >1000 results. It divides results into chunks...     │ │
│  │                                                                         │ │
│  │ 📎 Sources:                                                            │ │
│  │   • Wiki: RLSI-6059 searchEmployer SBS to support pagination          │ │
│  │     § "What is Search by Specification?" [edited 2 days ago]         │ │
│  │   • Jira: FEAT-9707 (accepted) · BASE-458832 (deployed v16.2)         │ │
│  │   • Release note: "v16.2 adds SBS pagination support"                 │ │
│  │                                                                         │ │
│  │ 👤 Follow-up: "Show me config" → retrieves YAML from linked Bitbucket │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

                                      ↓ (Query flow)

┌─────────────────────────────────────────────────────────────────────────────┐
│                        RAG INDEX (the "database")                            │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ PostgreSQL + pgvector (or Elasticsearch)                              │ │
│  │                                                                         │ │
│  │ Chunks table (10,000 rows for Client EMEA Bank, searchEmployer):      │ │
│  │  ┌─────┬──────────────────────┬────────────┬────────┬──────────────┐ │ │
│  │  │ id  │ text                 │ embedding  │ module │ source_type  │ │ │
│  │  ├─────┼──────────────────────┼────────────┼────────┼──────────────┤ │ │
│  │  │ 1   │ "SBS is a mode..."   │ [0.2, ...] │ search │ wiki         │ │ │
│  │  │ 2   │ "Config: page_size"  │ [0.15,...] │ search │ wiki         │ │ │
│  │  │ 3   │ "Fixed: StackOverf"  │ [0.3, ...] │ search │ jira         │ │ │
│  │  │ ... │ [8,997 more]         │ ...        │ ...    │ ...          │ │ │
│  │  └─────┴──────────────────────┴────────────┴────────┴──────────────┘ │ │
│  │                                                                         │ │
│  │ Metadata:                                                              │ │
│  │  • client_id: "emea_bank_001"                                         │ │
│  │  • feature: "searchEmployer"                                          │ │
│  │  • fix_version: ["v16.0", "v16.1", "v16.2"]                         │ │
│  │  • wiki_page_id: "973706490" (RLSI-6059 searchEmployer SBS)          │ │
│  │  • jira_keys: ["BASE-458832", "FEAT-9707", "BASE-460272"]            │ │
│  │  • last_updated: "2026-08-01 14:32 UTC"                              │ │
│  │  • freshness: "24h" (wiki ingested daily)                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  Retrieval logic (on every query):                                         │
│    1. Embed user question → semantic vector                                │
│    2. SELECT * FROM chunks WHERE                                           │
│       embedding <-> query_vec < distance_threshold AND                    │
│       client_id = 'emea_bank_001' AND                                     │
│       feature = 'searchEmployer'                                           │
│       ORDER BY distance LIMIT 5                                            │
│    3. Re-rank by recency (prefer "edited 2 days ago" > "edited 6m ago")   │
│    4. Return top 3 chunks + metadata (wiki link, Jira key, dates)         │
└─────────────────────────────────────────────────────────────────────────────┘

                                      ↓ (Ingest flow)

┌─────────────────────────────────────────────────────────────────────────────┐
│                     SOURCE SYSTEMS (Wiki, Jira, Bitbucket)                  │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ Wiki (Confluence):                                                      │ │
│  │  • Space: "CliRln" (Client Release Notes)                              │ │
│  │  • Pages: "RLSI-6059 searchEmployer SBS" + 8 related pages            │ │
│  │  • Last ingest: daily, 14:00 UTC (captures edits from previous 24h)   │ │
│  │                                                                         │ │
│  │ Jira (Issues):                                                          │ │
│  │  • Query: component="searchEmployer" AND fixVersion in ("v16.0", ...)  │ │
│  │  • Returns: 47 tickets (stories, defects, tasks)                      │ │
│  │  • Last ingest: daily, 14:30 UTC                                       │ │
│  │                                                                         │ │
│  │ Bitbucket (PRs):                                                        │ │
│  │  • Files touched: src/EmployerSearch.java, src/SBSPaginator.java      │ │
│  │  • PRs: 23 merged in last 6 months (only for searchEmployer module)   │ │
│  │  • Last ingest: weekly, Sunday 02:00 UTC                              │ │
│  │                                                                         │ │
│  │ Metadata connections:                                                  │ │
│  │  • Jira BASE-458832 ← links to → PR #8342 (merged)                   │ │
│  │  • Jira BASE-458832 ← appears in → Release note (v16.2)              │ │
│  │  • Wiki RLSI-6059 ← references → Jira FEAT-9707                      │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Part 3: Yes, This IS a RAG System (Clarification)

**RAG = Retrieval-Augmented Generation**

```
User question
    ↓
[Retrieve] from index → top 5 chunks + metadata
    ↓
[Augment] prompt with chunks: "Answer based on: [chunk1], [chunk2], ..."
    ↓
[Generate] answer via Claude + citation layer
    ↓
Final answer with sources
```

**What we're NOT doing** (common RAG mistakes):
- ❌ Hitting Wiki/Jira APIs on every query (slow, rate-limited)
- ❌ Storing raw pages (unstructured, bad embeddings)
- ❌ Generic RAG (no client filtering, version filtering, etc.)

**What we ARE doing** (production RAG):
- ✅ **Structured retrieval**: Chunks + rich metadata (client_id, module, version, dates)
- ✅ **Cached index**: Query the index, not APIs (fast, scalable)
- ✅ **Client-scoped**: Only retrieve searchEmployer docs for Client EMEA Bank
- ✅ **Entity linking**: Chunks know their Jira key, wiki page, PR context
- ✅ **Citation layer**: Every answer shows "from Wiki page X, verified 2 days ago"

**The database we're building:**
- PostgreSQL (or Elasticsearch) with:
  - Vector embeddings (for semantic search)
  - Full-text search (for keyword matching)
  - Metadata indexes (for client_id, module, version filters)
  - Relationships (chunk ↔ Jira ↔ PR ↔ Test)

This is a **production RAG backend**, not a "simple vector search" or a generic LLM knowledge base.

---

## Part 4: Phase 1 Execution Timeline (Client 1, Feature 1)

### **Weeks 1–2: Onboarding & Scoping**

| Day | Task | Owner | Output |
|---|---|---|---|
| **1–2** | Kick-off workshop with Client EMEA Bank support team | Product + SME | "searchEmployer is our #1 pain point" (confirmed) |
| **3–4** | Enumerate searchEmployer docs: which Wiki pages, which Jira tickets, which releases | Engineering | CSV: 8 wiki pages, 47 Jira tickets, v15.8–v16.2 in scope |
| **5–10** | Collect 40–50 real support questions from Client EMEA Bank | Support team | Question set for eval (from last 6 months of tickets) |

**Stakeholder narrative:** "We're starting with the feature Client EMEA Bank complains about most. Scope is intentionally narrow: searchEmployer feature, 1 client, 3–4 releases. This buys confidence."

---

### **Weeks 3–6: Data Ingest & Index Build**

| Week | Task | Owner | Output |
|---|---|---|---|
| **3** | Export searchEmployer wiki pages from Confluence; chunk by section | Engineering | 150 chunks (each tagged with module, page_id, last_edited date) |
| **3** | Query Jira for searchEmployer tickets (component="searchEmployer", fixVersion in ...) | Engineering | 47 issues extracted (summaries, descriptions, acceptance criteria, links) |
| **4** | Embed chunks using Claude embeddings (or open-source); load into PostgreSQL + pgvector | Engineering | Index created: 150 wiki chunks + 47 Jira chunks (∼200 total), searchable |
| **4–5** | Ingest Bitbucket PRs touching searchEmployer files | Engineering | 23 PRs linked to Jira tickets (change tracking) |
| **5–6** | Build re-ranking layer: prefer recent chunks, boost cited tickets | Engineering | Retrieval pipeline: <200ms per query |

**Stakeholder narrative:** "We're building a fast, client-scoped search engine on top of the docs Client EMEA Bank already has. No API calls on every query—we cache once daily and serve from our index."

---

### **Weeks 7–10: Q&A, Eval, Iteration**

| Week | Task | Owner | Output |
|---|---|---|---|
| **7** | Run eval set (40–50 questions collected in week 2) against the index | Engineering | % correct, % cited accurately, % hallucinations |
| **7–8** | If <80% correct: diagnose failures (bad chunks? re-ranking issue? embedding issue?) | Engineering | Root cause analysis + iteration plan |
| **8–9** | Iterate (better chunking, re-ranking tweaks, metadata filtering) | Engineering | ≥80% correct on eval set |
| **9–10** | Deploy live: Client EMEA Bank support team gets access to chat interface | Support + Engineering | Private beta with Client EMEA Bank (10 support agents) |

**Stakeholder narrative:** "We're measuring on their real questions. If it doesn't hit 80% accuracy, we iterate until it does. No shipping until we're confident."

---

### **Weeks 11–12: Live Pilot & Metrics**

| Week | Task | Owner | Output |
|---|---|---|---|
| **11–12** | Monitor live usage: how many questions? accuracy on real queries? SME satisfaction? | Support + Engineering | Weekly metrics dashboard (throughput, accuracy, SME feedback) |
| **12** | Iterate on any live issues (hallucinations, missing docs, etc.) | Engineering | Production-ready system |

**Live metrics tracked:**
- **Questions/week**: How many searchEmployer questions are support agents asking the bot?
- **Accuracy**: Spot-check 50 answers; measure correctness + citation quality
- **Escalation rate**: % of questions where bot says "I don't know" (target: <15%)
- **Resolution time**: Support agent time-to-answer (vs. baseline: 20 min manual → target: 3 min bot + human review)
- **Satisfaction**: Support team survey ("Does this help?" Yes/No/Sometimes)

**Stakeholder narrative:** "After 3 months, Client EMEA Bank's support team is using the bot for 30–40% of searchEmployer questions. Resolution time dropped 85%. Total cost of ownership: 1 engineer for 3 months + cloud compute. ROI: 1 support FTE saved per year per client."

---

## Part 5: Stakeholder Presentation After Client 1 (End of Week 12)

### **Slide 1: The Pilot Success**

```
"searchEmployer" for Client EMEA Bank (3-month pilot)

📊 Results:
  • 427 questions answered (37% of searchEmployer traffic)
  • 89% accuracy (verified by support team)
  • 0.8 sec response time (vs. 20 min manual lookup)
  • 35% reduction in support tickets
  
✅ Why it matters:
  • Real client, real traffic, real ROI
  • Proven architecture (no guessing)
  • 1 support FTE saved/year/client

💰 Cost: 1 engineer (3 months) + $500/month compute
   Payback: Month 4 (1 FTE saved)
```

### **Slide 2: The Replicable Template**

```
Pattern proven: each new client/feature follows same 12-week playbook

Client A: searchEmployer (DONE)  ✅
     ↓
Client A: payroll (12 weeks)
     ↓
Client B: searchEmployer (12 weeks, faster 2nd time)
     ↓
Client B: payroll (12 weeks)
     ...

By Dec 2026: 4 clients × 2 features each = 8 live pilots
By Q2 2027: 10 clients × 3–5 features each = expansion mode
```

### **Slide 3: What's Inside (Technical)**

```
System Architecture (demystified for stakeholders):

1. **Data Ingest** (daily):
   - Grab wiki pages about searchEmployer
   - Grab Jira tickets about searchEmployer
   - Break into chunks, embed them, store in index

2. **Query Engine** (per question):
   - User asks bot: "How does SBS work?"
   - Bot finds 5 similar chunks from index (<200ms)
   - Bot generates answer using those chunks + Claude
   - Bot shows sources: "From wiki page X (edited 2d ago)"

3. **Quality Assurance**:
   - Every chunk carries last-updated date (builds trust)
   - Chunks carry Jira key/wiki link (traceability)
   - Support team can mark answers as "right" or "wrong" (feedback loop)

This is production RAG: structured, fast, auditable.
```

### **Slide 4: Why This De-Risks Scale**

| Risk | Old Approach | New Approach |
|---|---|---|
| **Time to ROI** | 6–12 months | 3 months |
| **Infrastructure unknown** | Build first, test at scale | Tested on real client |
| **Political friction** | "Give us everything" | "Give us searchEmployer" |
| **Failure mode** | Entire project fails | Pivot to next client/feature |
| **Expansion** | Unclear how to scale | Clear template: repeat 12 weeks |

### **Slide 5: Next Steps (Your Question: How Many Clients?)**

```
Proven Approach:
  1 client at a time
  1 feature at a time
  12-week cycle
  Measure, iterate, replicate

Proposed 2026 Roadmap:
  Q3: Client A, Feature 1 (searchEmployer) ✅
  Q4: Client A, Feature 2 (payroll) + Client B, Feature 1 (searchEmployer)
  Q1 2027: Expand to 4–5 clients (parallel pipelines)
  Q2 2027: Tooling + automation (faster cycles, <8 weeks per client)

Ask: Which client next? Which is their #2 pain point after searchEmployer?
```

---

## Part 6: Why ONE Client, ONE Feature, Per Cycle?

| Dimension | One-at-a-time | All-at-once |
|---|---|---|
| **Risk** | Isolated (1 client fails, others unaffected) | Systemic (if architecture breaks, all fail) |
| **Feedback loop** | Fast (Client A tells you in week 3 if it's wrong) | Slow (discover problems after 3 months of building) |
| **Confidence** | Built incrementally (3 months → 6 months → 1 year proven) | All-or-nothing (hope it works) |
| **Team morale** | Quick wins (one success per quarter) | Grinding (invisible progress for months) |
| **Scope creep** | Bounded ("just searchEmployer") | Unbounded ("everything") |
| **Expansion speed** | Actually FASTER (proven playbook, repeat 12 weeks) | Slower (still building for first client while trying to scale) |

---

## Part 7: Your Question: "Why RAG?"

**The alternative** (that we rejected):
- ❌ Store everything in model memory (Claude's context) → hits token limits after 2–3 features
- ❌ Call Wiki/Jira APIs on every query → 500ms–2s latency, rate-limited, expensive
- ❌ Generic LLM knowledge base → no client scoping, no version filtering, hallucinations

**Why RAG** (what we're doing):
- ✅ Fast (<200ms), scalable, auditable retrieval
- ✅ Client/feature/version filtering (not "everything")
- ✅ Citation layer (sources are explicit, not hallucinated)
- ✅ Incremental updates (daily ingest, not retraining)
- ✅ Cost-effective (PostgreSQL + pgvector, not expensive embeddings vendor)

RAG is the right architecture for a knowledge assistant grounded in multiple source systems. We're just being **smart** about building it (client-scoped, feature-scoped, measured iteration).

---

## Summary for Your Decision

**Your concern:** "One client at a time will take forever."  
**Reality:** One client at a time is actually FASTER to scale because:
1. You prove the playbook (3 months)
2. You replicate it in parallel (12 weeks → 8 weeks → 6 weeks per client as tooling improves)
3. By month 12, you're at 4–5 clients
4. By month 18, you're at 8–10 clients

vs.

**"All clients/all features at once":**
1. You're stuck building the "perfect" system for 6 months
2. No real feedback until then
3. When it fails (and it will), you're stuck rearchitecting everything

**Go with one client, one feature, 12-week cycles. That's how production AI systems scale.**

Ready to pick Client 1?
