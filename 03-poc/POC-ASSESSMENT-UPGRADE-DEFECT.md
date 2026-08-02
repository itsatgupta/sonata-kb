# POC Assessment: Upgrade Analysis + Defect Triage
## Can We Build These? What Do We Need?

**Date:** 2026-08-02
**Context:** POC v2 voice is working. User asks: can we build similar POCs for:
1. Upgrade Impact Analysis (compare 2 releases)
2. Defect Triage (identify similar defects across clients)

---

## POC 1: Upgrade Impact Analysis

### What It Does
Compare two trunk releases (e.g., v16.1 → v16.2) and produce:
- **Architecture changes**: New APIs, deprecated endpoints, config changes
- **Technology changes**: Library upgrades, DB schema changes, infra changes
- **Functionality changes**: New features, enhanced features, removed features
- **Impact analysis**: Breaking changes, client-specific risk, effort estimate
- **Gap analysis**: What changed that clients need to know about

### What We Already Have

| Component | Status | Source |
|---|---|---|
| Wiki search | ✅ Working | `wiki_tool.py` — searches design/arch/tech-spec pages |
| Jira search | ✅ Working | `jira_search()` — filter by fixVersion range |
| Release notes | ✅ Ingested | `data/wiki.json` has release note content |
| Chunking + embedding | ✅ Working | `retrieval/chunking.py` + `retrieval/index.py` |
| Hybrid search | ✅ Working | `tools/wiki_tool.py` — semantic + keyword |
| Claude synthesis | ✅ Working | `orchestrator.py` — generates answers from chunks |

### What We Need to Build

| Component | Effort | Data Required |
|---|---|---|
| **Version-diff JQL** | 2 hours | Jira: `fixVersion in (v16.1, v16.2)` — already have JQL skills |
| **Release note extraction** | 4 hours | Wiki: parse release notes by version — need structured release notes |
| **Change categorization** | 8 hours | Logic to tag changes as arch/tech/func/impact — can use Claude |
| **Impact scoring** | 8 hours | Risk model (breaking vs additive) — need SME input on categories |
| **Report generation** | 4 hours | Markdown/PDF output — straightforward |
| **Total** | ~26 hours (~1 week) | |

### Data We Need

```
For comparing v16.1 vs v16.2:

1. Jira issues in that range:
   JQL: project = SONATA AND fixVersion in ("v16.1", "v16.2") ORDER BY fixVersion
   → Already have JQL skills, can query live

2. Release notes per version:
   Wiki pages tagged "release notes" for v16.1 and v16.2
   → Need: which wiki spaces have release notes?
   → Can search with: wiki_search("release notes v16.2")

3. Bitbucket PRs (Phase 2, optional for POC):
   PRs merged between v16.1 and v16.2 release dates
   → Need: Bitbucket API access (already configured in .env)

4. Known client impact (optional):
   Which clients are on v16.1? What modules do they use?
   → This is Phase 3 data (client profiles) — skip for POC
```

### Can We Do a POC? **YES — 1 week**

**Minimal POC scope:**
1. User inputs: "Compare v16.1 and v16.2"
2. System queries Jira for issues in that range
3. System searches wiki for release notes
4. Claude synthesizes: "Here's what changed: 5 new features, 3 bug fixes, 2 breaking changes..."
5. Output: Structured report with categories

**What wins stakeholders:**
- "Show me what changed between two releases in 30 seconds" (vs. 2 hours manual)
- Cites every change to its Jira ticket and wiki page
- Categorizes as breaking/additive/informational

---

## POC 2: Defect Triage Assistant

### What It Does
When support raises a defect:
1. **Search historical defects** — "Has this been reported before for any client?"
2. **Find similar issues** — semantic search over defect descriptions
3. **Check if fixed** — "Was this fixed in a later release?"
4. **Suggest triage** — "This looks like BASE-459103, reported for Client X, fixed in v16.2"
5. **If new** — Help draft defect with proper format, initial analysis, impact assessment

### What We Already Have

| Component | Status | Source |
|---|---|---|
| Jira defect search | ✅ Working | `jira_search()` — search by summary/description |
| Wiki search | ✅ Working | Search for known issues, workarounds |
| Semantic search | ✅ Working | Find similar text across Jira descriptions |
| Claude synthesis | ✅ Working | Generate triage recommendations |
| Historical data | ✅ Partial | Jira has defect history (need client tagging) |

### What We Need to Build

| Component | Effort | Data Required |
|---|---|---|
| **Defect similarity search** | 4 hours | Jira: `issuetype = Defect ORDER BY created DESC` |
| **Client attribution matching** | 8 hours | Need: which defects are tagged to which clients |
| **Fix-version lookup** | 4 hours | "Was this fixed?" → check fixVersion on similar defects |
| **Triage recommendation** | 8 hours | Claude: "This looks like X, suggest assign to Y, priority Z" |
| **Defect draft generation** | 4 hours | Auto-fill: summary, description, steps, expected vs actual |
| **Total** | ~28 hours (~1 week) | |

### Data We Need

```
For defect triage:

1. Historical defects:
   JQL: project = SONATA AND issuetype = Defect ORDER BY created DESC
   → Need: 500+ defects with summaries, descriptions, fixVersions
   → Can query live via Jira API

2. Client attribution (THE HARD PART):
   How are defects tagged to clients?
   Options:
   a) Labels: defect has label "client:royal-london"
   b) Components: defect has component "UAR" (module-level, not client-level)
   c) Custom field: "Client" field on defect
   d) Description text: "Client X reported this..."
   
   → Need to check: Does Jira have a "Client" field on defects?
   → If no client field: POC limited to module-level matching

3. Known fixes:
   Which defects were fixed in which versions?
   → Jira fixVersion field — already available

4. Workaround documentation:
   Wiki pages listing known issues + workarounds
   → Can search: wiki_search("known issues")
```

### Can We Do a POC? **YES — but scope depends on client data**

**Minimal POC scope (no client attribution):**
1. User describes a defect: "searchEmployer throws NullPointerException when GL account has special chars"
2. System searches Jira for similar defects (semantic search)
3. Finds: "BASE-459103 — searchEmployer fails on special chars in GL account, fixed in v16.1"
4. Recommends: "This looks like BASE-459103. If client is on v16.1+, already fixed. If on v16.0, escalate."
5. If no match: Helps draft new defect with proper format

**What wins support team:**
- "I don't have to search Jira manually for 15 minutes"
- "Bot finds similar defects I didn't know existed"
- "Auto-drafts defect with proper format — saves 20 minutes per ticket"

**Full POC (with client attribution):**
- Same as above PLUS: "This defect was reported by Client A in March, fixed in v16.1. Client B (your caller) is on v16.0 — needs upgrade."
- This requires client-defect mapping data

---

## Comparison: Upgrade vs Defect POC

| Dimension | Upgrade Analysis | Defect Triage |
|---|---|---|
| **Data available** | ✅ Jira + Wiki ready | ⚠️ Need client attribution |
| **Effort** | ~1 week | ~1 week (minimal), ~2 weeks (full) |
| **Stakeholder impact** | High (architects, PM) | Very High (support team daily) |
| **Data dependency** | Low (release notes + Jira) | Medium (need defect-client mapping) |
| **Can demo immediately** | ✅ Yes | ⚠️ Partial (module-level only) |
| **Builds on POC v2** | ✅ Same architecture | ✅ Same architecture |

---

## Recommendation

### **Build Upgrade Analysis POC First (1 week)**

**Why:**
1. **Data is ready** — Jira + Wiki already indexed, just need version-diff queries
2. **Quick win** — 1 week to demo
3. **High impact** — Architects + PMs see value immediately
4. **No new data dependencies** — just query existing Jira/Wiki differently
5. **Natural progression** — POC v2 proved retrieval; this proves analysis

**Demo scenario:**
"Compare Sonata v16.1 and v16.2"
→ Bot produces: "5 new features, 3 bug fixes, 2 breaking changes, 1 deprecation. Here's the impact matrix..."

### **Then Build Defect Triage POC (1 week after)**

**Why:**
1. **Need to check**: Does Jira have a "Client" field on defects?
2. **If yes**: Full POC with client attribution (2 weeks total)
3. **If no**: Module-level POC (1 week), then add client data later
4. **Highest daily value** — support team uses this every ticket

**Demo scenario:**
"searchEmployer throws NullPointerException on special chars"
→ Bot: "Found similar: BASE-459103 (fixed v16.1). If client on v16.1+, already resolved. If not, see workaround: [link]. No match? Draft new defect: [template]"

---

## What You Need to Confirm

### For Upgrade Analysis POC:
1. **Which version pairs to test?** (e.g., v16.1 → v16.2)
2. **Where are release notes?** (Wiki pages? Jira release notes? Both?)
3. **What categories matter?** (Architecture, Technology, Functionality, Impact — or different?)

### For Defect Triage POC:
1. **Does Jira have a "Client" field on defects?** (Check: when you open a defect, is there a field saying which client reported it?)
2. **How many historical defects?** (500? 5000? Need enough for meaningful similarity search)
3. **What's the triage workflow today?** (Support gets call → searches Jira manually → escalates? → what happens?)

---

## Proposed Timeline

```
Week 1: Upgrade Analysis POC
  Day 1-2: Build version-diff JQL + release note extraction
  Day 3-4: Build report generator (categorized changes)
  Day 5: Test with v16.1 → v16.2, demo

Week 2: Defect Triage POC (after confirming Jira client data)
  Day 1-2: Build defect similarity search
  Day 3-4: Build triage recommendation + draft generator
  Day 5: Test with real defects, demo

Week 3: Polish + Integrate with Voice
  - Add voice to both POCs (same Whisper + Web Speech pattern)
  - Single unified demo: Voice + Upgrade + Defect Triage
```

---

## Cost

| Item | Cost |
|---|---|
| Upgrade POC | $0 (same Render/Vercel, same APIs) |
| Defect Triage POC | $0 (same stack) |
| Claude API (testing) | ~$5 (100 test queries × $0.05 avg) |
| **Total** | **~$5** |

---

## Bottom Line

**Can we do both?** YES.
**Can we do them now?** YES — data is largely available.
**Which first?** Upgrade Analysis (data ready, 1 week).
**Then?** Defect Triage (need to confirm client field in Jira).
**Cost?** ~$5 total. Same architecture as POC v2.
**Stakeholder impact?** Massive — three working demos in 2 weeks.
