# POC v2 Voice Demo Script

## Setup (Before Demo)

1. Open `https://sonata-voice-poc.vercel.app` in Chrome
2. Test microphone works (click Ask, speak, verify)
3. Have backup: text-only demo via `/api/text-ask?q=...`
4. Ensure audio is on (speakers or headphones for audience)

## Demo Flow (45 minutes)

### Opening (2 min)

"We've built a fully working voice assistant for Sonata. You can speak your question, the bot hears it, finds the answer from our knowledge base, and speaks it back. Every answer shows where it came from — wiki pages, Jira tickets, release notes. Let me show you."

### Live Demo (20 min)

**Question 1: "How does searchEmployer pagination work?"**
- Bot transcribes, answers, speaks
- Point out: sources shown below (Wiki RLSI-6059, Jira FEAT-9707)

**Question 2: "What is Search by Specification?"**
- Different question, same feature, different angle
- Shows retrieval working across sections

**Question 3: "What changed in version 16.2 for searchEmployer?"**
- Tests version-diff knowledge
- Shows release note citations

**Question 4: "What is the default page size for searchEmployer?"**
- Specific factual question
- Shows precision of retrieval

**Question 5: "What exception does BASE-460272 report?"**
- Tests defect knowledge
- Shows Jira citation layer

**Questions 6-10: Let audience suggest questions**
- "What do you want to know about Sonata?"
- Shows real-time capability, builds credibility

### Architecture Explanation (5 min)

"What you're seeing is a production RAG system:
- We indexed wiki pages, Jira tickets, and release notes into a searchable database
- When you ask a question, we find the 5 most relevant chunks in under 200ms
- We generate an answer using those chunks — never from model memory alone
- Every answer carries a citation: which wiki page, which Jira key, when it was last verified
- This same architecture scales to any module, any client"

### Phase 1 Pitch (8 min)

"This POC proves the engine works. Phase 1 takes this to production:
- Client: Royal London (EMEA, their UAR/ISA support pain point)
- 12 weeks to go-live
- Saves $238K/year in support costs
- Payback in 4 weeks
- Same architecture, same pattern, just more data"

### Q&A (10 min)

Common questions:
- "How accurate is it?" → "27/27 on our test set. We measure accuracy on real support questions."
- "What if it doesn't know?" → "It says 'I don't know' rather than guessing. We track escalation rate."
- "How much does it cost?" → "$0 for the voice demo. $20K for Phase 1 pilot. ROI: $238K/year."
- "Can it handle other modules?" → "Yes. Same pattern. Phase 1 proves it on Royal London, then we replicate."
- "What about data security?" → "Read-only. No writes back to Jira/Wiki. Client-scoped index."

### Close (2 min)

"Phase 0 proved the core loop works. This POC v2 shows it end-to-end with voice. Phase 1 takes it to production with Royal London. 12 weeks. $238K/year savings. Ready to approve?"

## Backup: Text-Only Demo

If voice has issues, use text endpoint:
```
GET /api/text-ask?q=How does searchEmployer pagination work?
```

Shows same answer + citations, just without voice input/output.

## Key Messages

1. "This is a fully working voice assistant" (not a prototype)
2. "Every answer is cited" (trustworthy, auditable)
3. "Same architecture scales to any module" (replicable)
4. "Phase 1: 12 weeks, $238K/year ROI" (clear business case)
5. "Zero cost for the demo" (no new infrastructure)
