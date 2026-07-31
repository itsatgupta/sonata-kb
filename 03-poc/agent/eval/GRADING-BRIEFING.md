# Grading Briefing — Sonata KB POC eval sets

This POC has **two pilot features**, each with its own eval run and its own SME:

| Feature | Eval file | Questions | Citations | SME |
|---|---|---|---|---|
| 1. searchEmployer SBS pagination (RLSI-6059, Sonata 16.2) | `eval/results.csv` | 27 | 27/27 | Pratigya |
| 2. Direct Uploads — saveExternalCorrespondence size allowance (FEAT-10148/LIBSON-3635, Sonata 16.6) | `eval/results_directupload.csv` | 21 | 20/21 | Sanjay Joshi |

---

## How to grade (same for both files)

For **every row**, fill the `score_manual` column with exactly one of:

| Score | Means |
|---|---|
| `correct` | Right answer **and** the citation points to a real source that supports it |
| `partial` | Right idea, but wrong/incomplete source, or a key nuance is missing |
| `wrong` | The answer is incorrect |
| `hallucinated_citation` | The answer cites a source that doesn't exist, or asserts a fact the cited source does not contain |

**Golden rule — don't just read the answer.** Open the cited wiki section / Jira key and confirm it actually says what the answer claims. The entire point of this POC is that every answer is traceable to source. A `hallucinated_citation` on any row is a red flag, not a minor issue.

Also note any **failure modes** you hit while grading (ambiguous wiki, conflicting Jira-vs-wiki info, missing content) — they feed the Phase-1 data-quality backlog.

---

## Feature 1 — searchEmployer SBS pagination (Pratigya)

File: `eval/results.csv` — please score all 27 rows.

Two rows need your specific judgment:

1. **"What is the fixVersion of the searchEmployer pagination release-note ticket?"**
   - The assistant answered **BASE-458827** (a *Porting* release note, Sonata **16.3**).
   - The official release note for this feature is **BASE-458836** (Sonata **16.2**). Both tickets exist.
   - Decide whether citing the porting note is `partial` or `wrong`.

2. **"Does searchEmployer support searching by Employer External Reference?"**
   - The assistant said **"Yes, since Sonata 6.0"**, citing an old ticket (BASE-112902).
   - The IA explicitly struck searching-by-external-ref **out of scope for this enhancement** — expected answer is "No / out of scope."
   - Likely `wrong` or `hallucinated_citation`.

General watch: answers should use **wiki § SFC-04** (the pagination spec) and the right Jira keys, not general knowledge.

---

## Feature 2 — Direct Uploads saveExternalCorrespondence (Sanjay Joshi)

File: `eval/results_directupload.csv` — please score all 21 rows.

Three rows need your specific judgment:

1. **"Does this enhancement change the RDA upload functionality?"**
   - Expected: "No — RDA already allows 10MB, out of scope."
   - The answer was correct in intent but convoluted and dragged in an unrelated RDA ticket.

2. **"Does the change apply to the saveScheme or getMemberList operations?"**
   - The assistant asked for clarification and gave no citation. It did not fabricate, but it also did not answer — `partial` at best.

3. **"Does the LIBSON-3635 change affect the searchEmployer operation?"**
   - The answer drifts to a **"web upload limit 2MB → 100MB"** claim.
   - That fact comes from the **LIBSON-3635 helpdesk ticket**, not the indexed wiki page.
   - Judge whether it is out-of-scope noise (`partial`) or a fabricated-looking citation (`hallucinated_citation`).

General watch: several answers cite the **LIBSON-3635 helpdesk ticket** (with extra details) rather than the wiki spec page. Mark `partial` if the source is real but outside the feature's spec page; `hallucinated_citation` only if the claim isn't backed by the cited source.

---

## After grading — go/no-go (phase-0 exit)

- Count **`correct` only** — treat `partial` as not counted.
- Threshold: **≥80% correct with accurate citations**.
  - Feature 1: 27 rows → need **≥ 22 correct**.
  - Feature 2: 21 rows → need **≥ 17 correct**.
- Send the scored CSVs back to the engineering contact; they'll summarise the % correct and list every non-correct row for the phase-0 review.
