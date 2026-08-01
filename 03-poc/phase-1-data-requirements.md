# Phase 1 Data Requirements: Royal London (UAR/ISA) Pilot

## Context
**Client:** Royal London (major EMEA)  
**Feature set:** PM UAR (Portfolio Management User Account Reconciliation) + ISA (Individual Savings Account)  
**Support pain point:** 80+ support tickets/month on "How do I configure UAR?" / "ISA reconciliation failing"

---

## Part 1: Exact Data We Need From You

### **1. Wiki/Confluence Pages**

**What to export:**
- All pages tagged with "UAR" OR "ISA" OR "reconciliation" in spaces: "Sonata Technical", "Release Notes", "Configuration Guides"
- Include page ID, title, section headings, last modified date, author

**Format:** HTML export or Confluence API export (we'll chunk it)

**Example:**
```
Page: "UAR Configuration Guide" (page_id: 984521)
├─ Section: "What is UAR?"
├─ Section: "Step 1: Enable UAR in Config"
├─ Section: "Step 2: Map GL Accounts"
├─ Section: "Known Issues"
└─ Last modified: 2026-07-15 by Sarah.Brown@bravura.com

Page: "ISA Reconciliation Overview" (page_id: 984522)
├─ Section: "ISA vs LISA"
├─ Section: "Reconciliation Flow"
├─ Section: "Error Codes & Fixes"
└─ Last modified: 2026-06-20 by Mike.Jones@bravura.com
```

**Effort to provide:** 1 hour (export from Confluence, zip & share)

---

### **2. Jira Tickets (Features, Enhancements, Defects)**

**What to export:**
- All FEAT (Feature), ENHANCEMENT, DEFECT tickets related to UAR/ISA
- Include: ticket key, summary, description, acceptance criteria, status, fixVersion, components, linked issues, created/updated dates

**Filter query:**
```jql
project = SONATA 
AND (
  summary ~ "UAR" OR summary ~ "ISA" OR summary ~ "reconciliation"
  OR component in ("UserAccountReconciliation", "ISA")
)
AND fixVersion in (v15.8, v16.0, v16.1, v16.2, v16.3, v12.0, v12.1)
ORDER BY fixVersion DESC, created DESC
```

**What this captures:**
- ✅ **FEAT tickets:** "Enable UAR for multi-currency portfolios" (FEAT-8234)
- ✅ **Defects:** "UAR fails when GL account has special characters" (BASE-459103)
- ✅ **Acceptance criteria:** "When user enables UAR, system shall reconcile all accounts within 60 seconds"
- ✅ **Version mapping:** Which fixes went into which release (critical for version-diff later)

**Format:** Jira CSV export or JSON from `jira export` command

**Example structure:**
```csv
Key,Type,Summary,Description,Status,FixVersion,Component,Created,Updated
FEAT-8234,FEATURE,"Enable UAR for multi-currency",Allows UAR to work with multi-currency portfolios,Closed,v16.2,UserAccountReconciliation,2026-05-01,2026-06-15
BASE-459103,DEFECT,"UAR fails on special chars",When GL account name has @#$ chars,Closed,v16.1,UserAccountReconciliation,2026-04-10,2026-04-20
ISA-521,DEFECT,"ISA reconciliation timeout",Process runs >5min for large portfolios,Closed,v12.1,ISA,2026-03-15,2026-04-05
```

**Effort to provide:** 30 minutes (JQL query, export CSV)

---

### **3. Release Notes (What Changed & When)**

**What to export:**
- Release notes for UAR/ISA in versions Royal London is on (and 1–2 versions ahead for context)
- Include: version number, release date, feature summary, known issues, deprecations

**Example:**
```
v16.2 Release Notes (2026-06-20)
├─ NEW: Multi-currency UAR support (FEAT-8234)
├─ FIXED: Special character handling in GL accounts (BASE-459103)
├─ CHANGED: UAR reconciliation timeout reduced from 120s to 60s
├─ KNOWN ISSUE: ISA reconciliation may fail for portfolios >10,000 positions
└─ DEPRECATION: Old UAR config format "legacy_uar.xml" no longer supported

v16.1 Release Notes (2026-05-15)
├─ FIXED: UAR fails when GL account has special characters (BASE-459103)
├─ PERFORMANCE: UAR reconciliation 40% faster
└─ ...
```

**Format:** Markdown or plaintext (we'll extract & link to Jira tickets)

**Effort to provide:** 15 minutes (copy from Wiki + format)

---

### **4. Royal London's Supported Versions & Current State**

**What to provide:**
```
Client: Royal London
├─ Current version: v16.1 (production)
├─ Planned upgrade: v16.2 (Q4 2026)
├─ Support level: Premium (SLA: 4h response)
├─ Modules in use:
│  ├─ UAR (Portfolio Management User Account Reconciliation) - CRITICAL
│  ├─ ISA (Individual Savings Account) - HIGH
│  ├─ Payroll - MEDIUM
│  └─ General Ledger - HIGH
├─ Known pain points:
│  ├─ "UAR reconciliation timeout on large portfolios"
│  ├─ "ISA special character handling"
│  └─ "GL account mapping errors"
└─ Support team size: 8 people
```

**Effort to provide:** 15 minutes (from your client info system or SME)

---

### **5. Support Ticket History (The Real Questions)**

**What to provide:**
- Last 100 support tickets from Royal London related to UAR/ISA
- Include: ticket ID, date, question asked, how it was resolved, time-to-resolution, whether it was escalated to engineering

**Format:** CSV with columns: Date, Question, Resolution, TimeToResolution(min), Escalated(Y/N)

**Example:**
```csv
Date,Question,Resolution,TimeToResolution,Escalated
2026-07-28,"How do I configure multi-currency UAR?","Sent link to UAR Configuration Guide + step-by-step","15","N"
2026-07-25,"UAR reconciliation failing with error code 504","Turns out GL account had @ symbol; guided through workaround; escalated for fix","120","Y"
2026-07-22,"Can I use UAR with ISA accounts?","No; ISA uses separate reconciliation; showed ISA guide","8","N"
2026-07-20,"ISA reconciliation timeout - portfolio has 15k positions","Advised to split into batches; will be fixed in v16.2","45","Y"
...
```

**Why this matters:** We use real questions to:
- ✅ Build the eval set (your support team's real pain = our test questions)
- ✅ Validate accuracy (bot should answer 80%+ of these correctly)
- ✅ Identify gaps (if questions fail, we find missing wiki pages or Jira info)

**Effort to provide:** 1–2 hours (export from support system + anonymize sensitive info)

---

### **6. Known Gaps & Documentation Debt**

**What to provide:**
- Any known issues where Wiki/Jira docs are outdated, incomplete, or conflicting
- Example:
  ```
  - "UAR Configuration Guide (page 984521) hasn't been updated since v15.8; v16.0+ has different GL mapping logic"
  - "Jira FEAT-8234 (multi-currency UAR) is marked closed, but acceptance criteria say 'support EUR, GBP, USD' and we actually support 15+ currencies"
  - "ISA reconciliation error codes documented in Wiki don't match actual error codes in the system (error 504 = timeout, not documented)"
  ```

**Why this matters:** We flag these in the bot's output:
```
Bot: "UAR reconciliation failed with error 504 (timeout)"
Citation: "Wiki error guide (outdated: last edited 6 months ago) says error 504 = 'invalid account'"
⚠️ KNOWN ISSUE: This page needs review — actual meaning is 'timeout'"
```

**Effort to provide:** 30 minutes (SME notes)

---

## Part 2: What We Build With That Data

### **Step 1: Ingest & Index (Week 1–2)**

```
Raw data (wiki, Jira, release notes, tickets)
    ↓
[Chunk] by logical unit:
  - Wiki sections ("How to configure UAR" = 1 chunk)
  - Jira stories ("FEAT-8234 Multi-currency UAR" = 1 chunk)
  - Release notes per version ("v16.2 UAR changes" = 1 chunk)
    ↓
[Embed] each chunk using Claude embeddings:
  - "How to configure UAR?" → [0.23, 0.18, -0.15, ...]
  - "FEAT-8234 Multi-currency" → [0.21, 0.17, -0.14, ...]
    ↓
[Metadata tag] each chunk:
  - client_id: "royal_london"
  - module: "UAR" | "ISA"
  - fix_version: ["v16.1", "v16.2"]
  - source_type: "wiki" | "jira" | "release_note"
  - last_verified: "2026-08-01"
  - wiki_page_id: "984521"
  - jira_key: "FEAT-8234"
    ↓
[Store] in PostgreSQL + pgvector index
```

### **Step 2: Support Team Chat Interface (Week 2–3)**

```
Support Agent Question:
  "How do I fix UAR timeout errors for large portfolios?"
    ↓
[Query] index:
  Find chunks where:
    client_id = "royal_london"
    AND (module = "UAR" OR module = "ISA")
    AND semantic similarity > threshold
    ORDER BY recency
    LIMIT 5
    ↓
[Retrieved chunks]:
  1. Wiki "UAR Performance Tuning" (edited 2 weeks ago)
  2. Jira FEAT-8234 "Multi-currency UAR" (v16.2)
  3. Release notes v16.2 "UAR 40% faster" (edited 1 week ago)
  4. Release notes v16.1 "UAR improvements" (edited 2 weeks ago)
  5. Known gaps flagged "Docs outdated for v16.2"
    ↓
[Generate] answer via Claude:
  "UAR timeout errors on large portfolios happen when reconciling
   >10,000 positions. Mitigation: split portfolio into batches.
   This is fixed in v16.2 (in your upgrade queue for Q4).
   Until then: use batching workaround (documented below)."
    ↓
[Citation] layer:
  📎 Sources:
    • Wiki: UAR Performance Tuning § Known Issues (edited 2w ago)
    • Jira: FEAT-8234 Multi-currency UAR (v16.2)
    • Release note: v16.2 "UAR 40% faster"
  ⚠️ Your version: v16.1 (timeout fix in v16.2 planned Q4)
  ⚠️ Note: Documentation may be incomplete for v16.2 (pending review)
    ↓
[Support agent]:
  "Perfect — I'll tell Royal London customer to batch their portfolio
   and schedule their upgrade to v16.2 this quarter."
  ✅ Time saved: 45 min → 2 min
```

---

## Part 3: Support Team Angle (Cherry on Top)

### **What Support Gets**

**Live Dashboard (read-only):**
```
┌─────────────────────────────────────────────────────────┐
│ Royal London · UAR/ISA Support Dashboard                │
├─────────────────────────────────────────────────────────┤
│ 📊 This Week:                                            │
│   • 47 UAR questions asked to bot                       │
│   • 42 answered correctly (89%)                         │
│   • 5 escalated to engineering ("I don't know")         │
│   • Avg response time: 0.8 sec (vs. 15 min manual)     │
│   • Tickets saved: 47 × 15 min = 11.75 eng-hours      │
│                                                          │
│ 📈 Monthly trend:                                        │
│   • Month 1: 20 questions, 75% correct                  │
│   • Month 2: 35 questions, 82% correct                  │
│   • Month 3: 47 questions, 89% correct (improving!)    │
│                                                          │
│ ⚙️ Bot Feedback (from support team):                    │
│   • "Great: handles multi-currency scenarios well"      │
│   • "Gap: doesn't know about Q4 upgrade plans"         │
│   • "Suggestion: add error code reference table"       │
│                                                          │
│ 🔧 Recent Iterations:                                   │
│   • Updated ISA error codes (2 days ago)               │
│   • Added v16.2 release notes (5 days ago)             │
│   • Fixed UAR timeout doc (7 days ago)                 │
└─────────────────────────────────────────────────────────┘
```

**Support Agent Workflow:**
```
Agent gets ticket: "Customer says ISA reconciliation fails with error 504"

Option 1: Search bot internally first
  Bot: "Error 504 = timeout on large portfolios. Workaround: batch.
        Fixed in v16.2. Customer on v16.1. Check with account team on upgrade timeline."
  Agent: "Got it — thanks bot" → Takes 2 minutes vs. 20 minutes manual
  
Option 2: If bot says "I don't know" or answer seems wrong
  Agent: 👎 [Mark as unhelpful]
  → Feedback goes to engineering backlog
  → Engineering updates docs/bot training next cycle
  → Bot learns

Option 3: Deep dive needed (edge case)
  Agent: Uses bot's sources as starting point
  Bot: "See Wiki page X § Error Handling, Jira FEAT-8234, Release v16.2"
  Agent: "Thanks for the leads — I'll dig into these"
  → Same sources agent would have found manually, but faster
```

**Weekly Standup (15 min):**
```
Product: "Royal London support feedback this week?"

Support Lead: "Bot is handling ~40% of volume. Three patterns:
  1. ✅ Configuration questions (90% correct) — huge win
  2. ⚠️ Error code questions (70% correct) — need to add error reference
  3. ❌ Upgrade impact questions (40% correct) — docs don't cover v16.2 yet"

Product: "Got it. We'll add error table this sprint, get v16.2 docs from PM next week."

Support Lead: "Perfect. Also — bot's helping with onboarding. We're using
  bot's answers to train new support hires on UAR/ISA basics."

Product: "Love it. Let's expand to ISA next month once UAR stabilizes?"

Support Lead: "Yes — I'll start collecting ISA questions now."
```

---

## Part 4: Updated PPT Deck (New Slide: Support Team ROI)

### **New Slide to Add After "Business Value"**

```
Slide Title: "Support Team Impact (Day 1)"

Left side (Cost Savings):
├─ 47 questions/week handled by bot
├─ 15 minutes per question × 47 = 11.75 eng-hours saved/week
├─ At ~$75/hour loaded cost = $880/week
├─ Annual: $880 × 52 weeks = $45,760 saved/year
└─ ROI: 3-month pilot cost (~$20K) paid back in 5 weeks

Right side (Quality Improvements):
├─ New hire onboarding: 30% faster (using bot as training tool)
├─ Customer satisfaction: up 20% (faster resolution, consistent answers)
├─ Escalations to engineering: down 60% (bot catches common issues)
└─ Support team job satisfaction: up (less tedious, more strategic)

Bottom (Live Example):
├─ Traditional: Customer emails "How do I fix UAR timeout?"
│  → Agent spends 15 minutes reading docs & Jira
│  → Sends response
├─ With Bot:
│  → Agent asks bot, gets answer in 10 seconds
│  → Agent adds customer context + send
│  → Time: 2 minutes
└─ Multiply by 47/week: 11+ hours saved
```

---

## Part 5: Complete Data Handoff Checklist

**What you provide (total effort: 3–4 hours):**

| Item | Format | Effort | Owner |
|---|---|---|---|
| Wiki exports (UAR/ISA pages) | HTML or Confluence API | 1h | Product/Tech Writing |
| Jira export (FEAT/DEFECT tickets) | CSV or JSON | 30m | PM or Jira admin |
| Release notes (v15.8 → v16.3) | Markdown or plaintext | 15m | PM |
| Royal London metadata | Simple form (version, modules, size) | 15m | Account team |
| Support tickets (100 questions) | CSV (date, question, resolution) | 1–2h | Support team |
| Known gaps & doc debt | List + notes | 30m | Technical SME |
||| **Total: 3–4 hours** ||

**We build (weeks 1–12):**
1. ✅ Index creation (week 1–2)
2. ✅ Chat interface (week 2–3)
3. ✅ Eval set from real tickets (week 3–4)
4. ✅ Iteration to ≥80% accuracy (week 4–10)
5. ✅ Live deployment (week 10)
6. ✅ Metrics dashboard (ongoing)

---

## Part 6: Timeline to Share With Royal London

**Your pitch to Royal London support team:**

*"We're building a UAR/ISA assistant for your team. Here's what you'll see:*

*Week 1–2: Data handoff (you give us your docs, Jira tickets, real questions)*  
*Week 3–4: Bot learns your UAR/ISA knowledge base*  
*Week 5–10: Private beta (your team tests, we iterate)*  
*Week 11: Go live — bot answers UAR/ISA questions in your Slack/Teams*  

*What you get:*  
- *40%+ of UAR/ISA tickets handled by bot (time saved: 12+ hours/week)*
- *Consistent, sourced answers (every bot response cites docs + Jira)*
- *Dashboard showing accuracy, response times, feedback trends*
- *Feedback loop: mark answers wrong → we learn → bot improves*

*What we need from you:*  
- *100 real support questions (last 3 months) — we'll use these to test*
- *Jira list of UAR/ISA bugs/features you've dealt with*
- *Your wiki pages on UAR/ISA configuration*
- *Feedback during beta: 30 min/week standup*

*By month 3, your support team is 40% more efficient. By year 1, we expand to payroll + GL (same model)."*

---

## Summary: What You Do, What We Do

| Phase | You | Us |
|---|---|---|
| **Week 1** | Collect & export wiki, Jira, tickets, release notes | Setup PostgreSQL + pgvector, ingest & chunk |
| **Week 2** | Test our data import, flag missing pieces | Build embedding index, create metadata mappings |
| **Week 3** | Start collecting support feedback | Deploy chat interface to private beta |
| **Week 4–10** | Daily feedback on bot accuracy | Iterate: better chunking, re-ranking, new docs |
| **Week 11–12** | Go-live support, track metrics | Monitor, optimize, prepare for next client |

---

## Ready?

To start, I need you to confirm:

1. **Client:** Royal London (yes/no, or different?)
2. **Modules:** UAR + ISA (yes/no, or different?)
3. **Data owner (per item):**
   - Wiki exports → ?
   - Jira exports → ?
   - Support tickets (100 questions) → ?
   - Royal London metadata (current version, support size) → ?

Once you confirm, I'll send a formal "Data Handoff Template" document that you can fill out + share.

Ready to move?
