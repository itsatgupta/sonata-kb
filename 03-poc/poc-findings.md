# POC Findings — from SME grading & eval runs

**Last updated:** 2026-08-01
Companion to `03-poc/PROGRESS-STATUS.md`. Failure modes and data-quality findings that feed the
Phase-1 backlog (`02-phases/phase-1-functional-kb.md`), plus the go/no-go result for the graded
feature-1 eval.

---

## Feature 1 — searchEmployer SBS pagination (RLSI-6059, Sonata 16.2) — PASS

- Eval: `agent/eval/test_questions.md` (27 questions) → `agent/eval/results.csv`.
- SME grading (Pratigya): **27/27 Correct, 27/27 citations present → 100% correct-with-citation.**
- Go/no-go threshold (≥80%, i.e. ≥22/27): **PASS.**
- No `wrong` / `partial` / `hallucinated_citation` rows.
- Two rows the grading briefing flagged as "likely wrong/partial" came back **Correct**. Both are
  defensible; the underlying data issues are recorded below so they don't resurface in Phase 1.

### Watch rows (graded Correct — data-quality findings)

1. **Q26 — "fixVersion of the searchEmployer pagination release-note ticket"**
   - Expected gist: Sonata 16.2 (BASE-458836, the official release note).
   - The assistant answered with the **porting** release note (BASE-458827, Sonata 16.3) and the
     **clone story** release note (BASE-458857, Sonata 16.1), but did **not** surface the official
     BASE-458836 (16.2). Three release-note tickets exist for this one feature, so "the release-note
     ticket" is genuinely ambiguous.
   - → Phase-1: teach retrieval to rank the official (non-porting, non-clone) release note first, or
     disambiguate in the question/answer.
2. **Q18 — "Does searchEmployer support searching by Employer External Reference?"**
   - The IA struck the external-ref enhancements (wiki sections **SEF-01**, **SFC-02**) out of scope.
   - The assistant answered "Yes — since Sonata 6.0" (BASE-112902), correctly distinguishing the
     *existing capability* from the *struck-through enhancement scope*, and cited the struck-through
     sections. The SME judged this Correct.
   - → Phase-1: the question wording ("does the *enhancement* support…") is ambiguous; reword or accept.

---

## Failure modes / data findings (feed Phase-1 backlog)

1. **Jira free-text search is unreliable on this DC instance.** `text ~` returned nothing even for
   exact summary strings. `jira_search` now uses `summary ~ / description ~` and does **not**
   default-scope to a single project (that was hiding BASE/FEAT tickets). Side effect: cross-project
   free-text now surfaces out-of-pilot tickets (e.g. the **LIBSON-3635 helpdesk ticket**, with extra
   facts like "web upload limit →100MB") — answers can drift outside the pilot's scope. Judge per-answer.
2. **BASE tickets are mostly empty shells** (no descriptions, no populated acceptance-criteria field).
   Substance lives in the wiki IA pages. `customfield_22644` is the real Acceptance Criteria field id.
3. **Release-note ambiguity (feature 1)** — see Q26 above: BASE-458836 (16.2, official) vs
   BASE-458827 (16.3, porting) vs BASE-458857 (16.1, clone). The assistant picked the porting note on
   the fixVersion question.
4. **External-ref out-of-scope nuance (feature 1)** — see Q18 above: the enhancement struck
   searching-by-external-ref out of scope, but the capability has existed since Sonata 6.0
   (BASE-112902). Question phrasing must distinguish "capability" from "enhancement scope".
5. **Wiki typo**: the Direct Uploads page consistently misspells the operation as
   `saveExternalCorespondence`.
6. **Security**: the Jira PAT and wiki token have appeared in chat transcripts. Rotate the Jira PAT
   hardcoded in `~/.claude/mcp.json` (consider `{env:...}` substitution). `.env` is gitignored — never commit it.

---

## Cost finding

- Feature-2 eval (21 questions): **45 API calls · 687,145 input · 10,384 output · 77,616 cache-read →
  ~$2.25 @ Sonnet**.
- Cost is driven almost entirely by **input context** (retrieved wiki chunks), not model output.
- Levers if costs matter (pending decision, not yet applied): cap chunk text sent to the model
  (~1500 chars), reduce `wiki_search` default results, lower `max_tokens`.

---

## Feature 2 — Direct Uploads saveExternalCorrespondence size allowance (FEAT-10148 / LIBSON-3635, Sonata 16.6) — **DEFERRED**

- Eval: `agent/eval/test_questions_directupload.md` (21 questions) → `agent/eval/results_directupload.csv`
  (20/21 cited).
- **Status: deferred (2026-08-01)** — feature-1 (searchEmployer pagination) is the single go-forward POC
  enhancement; Sanjay Joshi's grading is parked. Wiki index, eval set, and briefing
  (`agent/eval/GRADING-BRIEFING.md`, which flags 3 rows for specific judgment and the general LIBSON-3635
  helpdesk-ticket drift) are kept intact for a future run.
