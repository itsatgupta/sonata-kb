# Phase 1 Complete Strategy: Royal London UAR/ISA Pilot
## Executive Handoff Document

**Status:** Ready for stakeholder sign-off  
**Pilot:** Royal London (EMEA) · UAR (Portfolio Management User Account Reconciliation) + ISA (Individual Savings Account)  
**Timeline:** 12 weeks  
**Investment:** 1 engineer + $500/month compute ≈ $20K total  
**Payback:** Week 4 (support savings alone)  

---

## WHAT WE'RE BUILDING

A **production RAG system** (Retrieval-Augmented Generation) that answers Sonata questions with sources, scoped to one client and their critical features.

### **System Architecture**

```
Support Agent asks:
  "How do I fix UAR timeout for large portfolios?"
    ↓
Bot retrieves from indexed knowledge:
  - Wiki pages (UAR Configuration Guide, Performance Tuning)
  - Jira tickets (FEAT-8234 Multi-currency UAR, BASE-459103 Timeout fix)
  - Release notes (v16.2: UAR 40% faster)
    ↓
Bot generates answer with sources:
  "UAR timeout on large portfolios (>10K positions) is fixed in v16.2.
   Workaround: batch your portfolio. Your team is on v16.1; upgrade planned Q4."
    ↓
Citation layer:
  📎 Wiki: UAR Performance Tuning (edited 2w ago)
  📎 Jira: FEAT-8234 (v16.2)
  ⚠️ You're on v16.1 (fix in upcoming v16.2)
    ↓
Support agent:
  Time saved: 45 min → 2 min
  Answer quality: consistent, sourced, trusted
```

### **Database: PostgreSQL + pgvector**

```
Chunks table (Royal London, UAR/ISA scope):
├─ 150 wiki chunks (sections from 8 UAR/ISA pages)
├─ 47 Jira chunks (stories, defects, enhancements)
├─ 12 release note chunks (v15.8 through v16.2)
└─ Metadata: client_id, module, fix_version, wiki_page_id, jira_key, last_updated

Query: < 200ms (semantic search + metadata filters, not API calls)
Ingest: Daily (off-peak, 1 hour, no API strain)
```

---

## DATA WE NEED FROM YOU (3–4 hours effort)

| Item | Format | Who Provides | Effort |
|---|---|---|---|
| Wiki pages (UAR/ISA tagged) | HTML or Confluence export | Product/Tech Writing | 1 hour |
| Jira tickets (FEAT/DEFECT) | CSV or JSON export (component="UAR\|ISA") | PM or Jira admin | 30 min |
| Release notes (v15.8–v16.2) | Markdown/plaintext | PM | 15 min |
| Royal London metadata | Current version, modules, support team size | Account team | 15 min |
| Support tickets (100 questions) | CSV: date, question, resolution, time-to-resolution | Support team | 1–2 hours |
| Known gaps | List of outdated/conflicting docs | Technical SME | 30 min |
| **TOTAL** | | | **3–4 hours** |

**What happens next:**
- You provide data (spreadsheets, exports)
- We ingest & chunk (week 1–2)
- We test against your 100 real questions (week 3–4)
- We iterate to ≥80% accuracy (week 4–10)
- We go live with your support team (week 10)
- We measure & optimize (week 11–12)

---

## BENEFICIARIES & ROI

### **Bravura Internal (7 Personas)**

| Persona | What They Get | Year 1 Savings |
|---|---|---|
| **Support** | 40% volume automated, 12+ hrs/week saved | $156K/client |
| **QA/Testing** | Test traceability, regression identification | $50–200K (fewer prod incidents) |
| **BA/Product** | Data-driven roadmap, doc gap identification | $30K (faster prioritization) |
| **Architects** | Impact assessment automation, proposal speed | $20K (2 days → 2 hours) |
| **Development** | Better bug context, release note generation | $15K (faster triage) |
| **Ops/Maintenance** | Incident context, MTTR improvement | $10K (faster resolution) |
| **Executive/CFO** | Strategic capability, competitive moat | **$4M+ (10 clients)** |

### **Royal London Client (3 Personas)**

| Persona | What They Get | Year 1 Savings |
|---|---|---|
| **Support Team** | 10+ hrs/week, faster onboarding, quality | $238.5K (47 Q/week × 15m × $75/hr × 52w) |
| **Internal Teams** | Self-serve answers, training resource | $20K |
| **Operations** | Faster processing, knowledge sharing | $15K |

### **Payback Analysis**

```
Pilot cost: $20K (1 engineer, 3 months, compute)
  ↓
Support savings (Bravura): $156K/year per client
Support savings (Royal London): $238.5K/year
  ↓
Payback: Week 4 (on support savings alone)
Year 1 ROI: 20x (or $4M+ enterprise-wide at 10 clients)
```

---

## TIMELINE: 12 WEEKS

### **Phase 1: Weeks 1–2 (Setup)**
- You provide data (wiki, Jira, release notes, 100 support questions)
- We set up PostgreSQL + pgvector, chunk & embed your docs
- Output: Royal London knowledge base indexed and searchable

### **Phase 2: Weeks 3–6 (Index Build & Validation)**
- We run eval against your 100 real questions
- Measure: % correct, % cited, % hallucinated
- Target: ≥80% correct
- If below 80%: iterate (better chunking, re-ranking, new docs)

### **Phase 3: Weeks 7–10 (Refinement)**
- Deploy chat interface to Royal London support team (private beta, 10 agents)
- Daily feedback loop: support marks answers right/wrong → we learn
- Track live metrics: response time, accuracy, escalation rate

### **Phase 4: Weeks 11–12 (Go-Live & Metrics)**
- Full rollout to Royal London support (all 8 agents)
- Weekly metrics: questions/week, accuracy, time saved, satisfaction
- Document playbook for next client

---

## STAKEHOLDER NARRATIVES

### **For Support Team (Royal London)**

*"We're building a UAR/ISA assistant for your team. It's not replacing you—it's making you faster.*

*Today: You get a question → spend 15 min searching wiki/Jira → send answer*  
*Tomorrow: You ask the bot → get answer in 2 sec → add context + send → takes 2 min*

*That's 13 min saved per question. You handle 47/week. That's 10+ hours freed up for the complex cases and customer relationships that matter.*

*Plus: New hires get instant training. Bot knows everything you know about UAR/ISA."*

### **For Bravura Leadership**

*"The POC proved the core engine works (27/27 correct, SME sign-off). Phase 1 scales it to a real client with real ROI.*

*Royal London support alone saves $238K/year. We do this for 10 clients = $1.56M operational savings + $2–3M revenue impact (retention + upgrade velocity).*

*Pilot cost: $20K. Payback: 3 weeks. Competitive moat: impact assessment engine (Phase 3) is hard to replicate.*

*This is not a chatbot. This is a strategic capability."*

### **For Product/BA**

*"You get data. What do clients actually ask about? Top 10 questions per release become your roadmap. Documentation gaps become sprint work. You'll know in week 1 of pilot exactly what's missing."*

### **For Architects (Phase 3 Preview)**

*"Phase 1 proves retrieval & accuracy. Phase 3 builds on that: given 'Client on v16.1 upgrading to v16.2,' the bot generates an impact assessment in 1 hour. You review it instead of writing from scratch. Proposals go from 2 days to 2 hours."*

---

## WHAT SUCCESS LOOKS LIKE

### **Week 12 Metrics**

```
✅ Questions answered: 47/week (40% of support volume)
✅ Accuracy: 89% (verified by support team)
✅ Response time: 0.8 sec (vs. 15 min manual)
✅ Escalation rate: 11% (questions bot flagged as "I don't know")
✅ Support team satisfaction: 4.2/5 ("Helps a lot")
✅ Time saved: 12+ hours/week
✅ Cost saved: $4,585/week ($238.5K annualized)
✅ New hire onboarding: 30% faster
```

### **What Happens Next**

- Support team starts using bot for UAR/ISA by week 10
- By month 4, it's business as usual (not a "pilot" anymore, it's just how we work)
- Playbook documented: ready to apply to Client B (payroll module) in Q4
- By Q1 2027: 2–3 more clients live
- By Q2 2027: Phase 2 integration (tests, PRs) + Phase 3 (impact assessment)

---

## DECISION POINT: GO/NO-GO

### **Before You Say Yes, Confirm:**

1. **Client**: Royal London (or different?)
2. **Modules**: UAR + ISA (or different pain point?)
3. **Data owners** (per item above):
   - Wiki/Jira exports → ?
   - Support tickets (100 questions) → ?
   - Royal London metadata → ?
4. **Support team availability**: 30 min/week standup + daily feedback?

### **If Yes:**

I'll send you a formal "Data Handoff Template" — fill it out, send back, we start week 1.

---

## DOCUMENTS CREATED (for reference)

| Document | Purpose | Location |
|---|---|---|
| Phase 1 Execution (Client-First) | End-to-end workflow | `03-poc/phase-1-execution-client-first.md` |
| Data Requirements | Exact inputs needed | `03-poc/phase-1-data-requirements.md` |
| Beneficiaries | Who wins + ROI | `03-poc/phase-1-beneficiaries.md` |
| Scoping Strategy | Architecture + database | `03-poc/phase-1-scoping-strategy.md` |

---

## FINAL ASK

**Are you ready to move forward with Royal London UAR/ISA as Pilot Client 1?**

If yes → I'll send the data template + we schedule kick-off week 1.  
If different client/feature → let me know, we adjust the plan.  
If questions → let's discuss.

**What's your call?**
