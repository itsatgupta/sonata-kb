# POC Progress & Handoff Status

**Last updated:** 2026-08-02
**Read this first in any new session** — it records where the POC stands, what is verified,
what is blocked, and the exact commands to continue. The repo is otherwise explained in
`README.md`, `CLAUDE.md`, and `SETUP-AND-EXECUTION-GUIDE.md`.

**Where we left off (this session):** **Phase-0 exit COMPLETE** (27/27 Correct, SME sign-off).
**POC v2 Voice DEPLOYED & WORKING**:
- **Backend**: Render (https://sonata-kb.onrender.com) — Whisper STT + orchestrator + wiki index deployed
- **Frontend**: Vercel (https://sonata-kb.vercel.app) — Voice + Text chat with polished UI
- **Voice pipeline**: Whisper transcribes → orchestrator answers → Web Speech speaks back (verified)
- **Text chat**: 3 modes — Direct ($0, raw chunks), OpenAI (~$0.001, GPT-3.5), Claude (~$0.11)
- **UI**: Gradient header, Chat Bot / Voice Bot sections, hover tooltips, query history, mode selector
- **OpenAI API key**: Set in Render env vars (for cheap text queries)
- **Wiki index data**: Committed to git (`data/wiki.json` + `data/wiki_directupload.json`)

**Data Sources Discovered (for Upgrade + Defect POCs):**
- **CART tests**: Jira filter `103721` — Xray test sets per module/version (accessible)
- **Defect tracker**: Jira filter `90250` — incidents, service requests (accessible)
- **Royal London defects**: Project `RLSI` — defects, incidents with components (accessible)
- **Wiki release notes**: 16.4 (`page_id: 1001572222`), 16.5 (`page_id: 1007867808`) — NOT YET INDEXED
- **Upgrade catalogue alignment**: `08-central-upgrade-team-alignment/catalogue-alignment.md` — defines exact deliverables to produce

**Upgrade Analysis POC Status:**
- `upgrade_analyzer.py` created (backend module)
- `/api/upgrade-analysis` endpoint added to `main.py`
- **BLOCKER**: Wiki release notes (16.4, 16.5) not indexed yet — need ingestion before POC works
- **Jira access confirmed**: fixVersion values are "Raglan 14.9 R12/R13" (not "v16.4/v16.5")

**Defect Triage POC Status:**
- Data sources confirmed (RLSI project, CART filter, defect tracker)
- Not yet built — starts after Upgrade Analysis POC

**Known issues:**
- Whisper transcription slightly off on domain terms (expected — semantic retrieval still works)
- Wiki index only has searchEmployer page — release notes need ingestion

**Next:** Ingest release notes (16.4, 16.5) → build Upgrade Analysis POC → then Defect Triage POC

**This session also captured:** a proposed **Defect Triage Assistant** workstream
(`07-future-roadmap/defect-triage-assistant.md`) and a **Support / service-desk triage agent**
persona (`05-personas-and-usecases/personas-and-usecases.md`) — a later-phase, same-app
capability gated on client-attribution data and draft-then-approve write governance.

---

## The two pilot features

The POC started with **two** small pilot features in parallel. **Feature 1 is the single go-forward
enhancement** (graded & passed); **feature 2 is deferred** — its wiki index, eval set, and briefing
remain intact for a future run.

### Feature 1 — searchEmployer SBS pagination (RLSI-6059, Sonata 16.2)
- Wiki page: `RLSI-6059 searchEmployer SBS to support pagination` (space CliRln, id **973706490**)
- Jira: BASE-458832 (story), FEAT-9707 (work package), BASE-458836 (release note, 16.2),
  BASE-458911 (schema change), BASE-460256 / BASE-460272 (defects)
- SME: **Pratigya**
- Index namespace: `wiki` → `data/wiki.json` (17 chunks)
- Eval: `eval/test_questions.md` (27 questions) → `eval/results.csv` — **27/27 Correct (100%), go/no-go PASS** (SME-graded)
- Key spec: optional `pagingRange` element; default 20 results/page from index 1; ordered by Employer Number (sloc_code)

### Feature 2 — Direct Uploads: saveExternalCorrespondence size allowance (FEAT-10148 / LIBSON-3635, Sonata 16.6) — **DEFERRED**
- Wiki page: `LIBSON-3635: Direct Uploads - Increase document size allowance for saveExternalCorrespondence sbs` (space CliStl, id **1001573493**)
- Jira: FEAT-10148 (work package), FEAT-10149 (IA), FEAT-10150 (design), BASE-464868 (story),
  BASE-464872 (release note, 16.6)
- SME: **Sanjay Joshi**
- Index namespace: `wiki_directupload` → `data/wiki_directupload.json` (15 chunks)
- Eval: `eval/test_questions_directupload.md` (21 questions) → `eval/results_directupload.csv` — **20/21 cited, awaiting grading**
- Key change: hardcoded upload limit **2MB → 10MB**; RDA already at 10MB (out of scope); existing error message must be maintained
- **Grading instructions:** `eval/GRADING-BRIEFING.md` (rubric + the specific rows each SME must judge + 80% go/no-go thresholds)

---

## What is built & verified (working against the real systems)

| Area | State |
|---|---|
| Jira access | `helpdesk.bravurasolutions.com`, Jira **Server/DC**, Bearer-PAT auth. api/3 → api/2 fallback (Server soft-404s api/3 with HTML 200). Verified: search, version-range endpoint, citations. |
| Confluence access | `wiki.bravurasolutions.com`, Bearer-PAT. Page fetch/ingest verified. |
| `.env` loading | `config/env.py` → `load_env()`; wired into `tools/__init__.py`, `orchestrator.py`, `ingestion/wiki_ingest.py`. Also **strips Claude Code's inherited `ANTHROPIC_BASE_URL` localhost proxy** so the POC reaches the real API (this was the cause of the long-running `401 invalid_api_key` — the key was fine). |
| Chunking | `retrieval/chunking.py` supports ATX **and setext** headings (Confluence→markdownify uses setext; without it a page collapses to 1 chunk). |
| Index | `VectorIndex.add()` now **replaces** the namespace (was appending → duplicate chunks on re-ingest). |
| Namespaces | `WIKI_NAMESPACE` env / `--namespace` arg on `wiki_ingest.py` and `run_eval.py`; `--questions` / `--results` args on `run_eval.py`. |
| Orchestrator | **Prompt caching** (system + last tool) and **usage tracking** (`usage_summary()`) added. Model default `claude-sonnet-5`. |
| Eval harness | `run_eval.py` lazy-imports orchestrator so `WIKI_NAMESPACE` is honoured; UTF-8 CSV/stdout (Windows cp1252 was crashing runs on `≤`/`→`). |

## Measured eval cost (feature 2, 21 questions)

45 API calls · 687,145 input tokens · 10,384 output tokens · 77,616 cache-read → **~$2.25 @ Sonnet**.
Cost is driven almost entirely by **input context** (retrieved wiki chunks), not model output.
If costs matter: cap chunk text sent to the model (~1500 chars), reduce `wiki_search` default results,
and lower `max_tokens`. Not yet applied — pending decision.

---

## Known issues / data findings (feed the Phase-1 backlog)

1. **Jira free-text search is unreliable on this DC instance**: `text ~` returned nothing even for exact
   summary strings. `jira_search` now uses `summary ~ / description ~` and does **not** default-scope to a
   single project (that was hiding BASE/FEAT tickets). Side effect: cross-project free-text now surfaces
   out-of-pilot tickets (e.g. the **LIBSON-3635 helpdesk ticket**, with extra facts like "web upload limit
   →100MB") — answers can drift outside the pilot's scope. Judge per-answer.
2. **BASE tickets are mostly empty shells** (no descriptions, no populated acceptance-criteria field).
   Substance lives in the wiki IA pages. `customfield_22644` is the real Acceptance Criteria field id.
3. **Release-note ambiguity (feature 1)**: BASE-458836 (Sonata 16.2, official) vs BASE-458827
   (Sonata 16.3, porting). The assistant picked the porting note on the fixVersion question.
4. **Feature-1 negative question**: "Does searchEmployer support searching by Employer External Reference?"
   was answered "Yes, since Sonata 6.0" (old ticket BASE-112902); the enhancement struck external-ref
   searching **out of scope**. Expected "No".
5. **Wiki typo**: the Direct Uploads page consistently misspells the operation as `saveExternalCorespondence`.
6. **Security**: the Jira PAT and wiki token have appeared in chat transcripts. Rotate the Jira PAT that is
   hardcoded in `~/.claude/mcp.json` (consider `{env:...}` substitution). `.env` is gitignored — never commit it.

---

## Current position & pending

- **Repo**: pushed to GitHub (`https://github.com/itsatgupta/sonata-kb`, branch `master`, in sync at
  `6d942bf`). Includes PROGRESS-STATUS.md, the CLAUDE.md pointer, and the filled candidate one-pagers.
- **Feature 1 (Pratigya)**: graded — **27/27 Correct (100%)**, go/no-go **PASS**, **live demo delivered
  & sign-off obtained (Pratigya happy)**. Findings in `03-poc/poc-findings.md`. Single go-forward POC enhancement.
- **Feature 2 (Sanjay Joshi)**: **deferred** — grading on `eval/results_directupload.csv` parked; wiki
  index, eval set, and briefing kept intact for a future run.
- **Next**: **begin Phase-1 execution** — 1) enumerate Wiki spaces + Jira projects for full ingestion;
  2) kick off the Feature/Module taxonomy SME workshop (the long pole); 3) add Jira bulk-ingestion +
  generalize `wiki_ingest.py`; 4) apply POC cost levers; 5) rotate the Jira PAT in `~/.claude/mcp.json`.
  Full plan: `02-phases/phase-1-implementation-plan.md`.
- **Open decisions**: apply eval cost levers (truncate chunks, lower `max_tokens`) before any re-run;
  rotate the Jira PAT in `~/.claude/mcp.json` (security).

## After SME grading — action plan

1. **Consolidate & score** — done (feature 1: 27/27 Correct, 100%). Feature 2 deferred.
2. **Go/no-go** — **PASS** on feature 1 (≥22/27 threshold; 27/27). Phase-0 exit criterion met.
3. **Write `03-poc/poc-findings.md`** — done (findings + data-quality backlog).
4. **Demo / sign-off** — **DONE**: live demo delivered to Pratigya; she is happy (sign-off obtained).
5. **If a feature fails** — n/a (feature 1 passed; no re-run needed).
6. **Phase 1 planning** — draft done (`02-phases/phase-1-implementation-plan.md`); **execution is the
   next step** — SME workshop for the taxonomy is the long pole, start it early.

---

## Useful commands (run from `03-poc/agent`, venv at `03-poc/agent/venv`)

```bash
# Jira sanity
venv/Scripts/python.exe -c "from tools.jira_tool import jira_search; print(jira_search(jql='project = SON ORDER BY updated DESC', max_results=3))"

# Wiki ingest (feature 1 / feature 2)
venv/Scripts/python.exe ingestion/wiki_ingest.py --namespace wiki --page-id 973706490
venv/Scripts/python.exe ingestion/wiki_ingest.py --namespace wiki_directupload --page-id 1001573493

# Eval run (any feature)
venv/Scripts/python.exe eval/run_eval.py --namespace wiki --questions eval/test_questions.md --results eval/results.csv
venv/Scripts/python.exe eval/run_eval.py --namespace wiki_directupload --questions eval/test_questions_directupload.md --results eval/results_directupload.csv

# Live smoke question
venv/Scripts/python.exe -c "from orchestrator import ask; print(ask('What is the default page size for searchEmployer?')[0])"
```

---

## Environment notes

- Always run from `03-poc/agent` (imports assume it is on `sys.path`).
- Credentials live in `03-poc/agent/.env` (gitignored). Token shapes: Jira PAT (`MTMw…`), wiki PAT (`MjM5…`), Anthropic `sk-ant-api03-…`.
- Anthropic account had a low-balance (`400 credit balance is too low`) episode; a $10 top-up resolved it. If you see that error again, check billing before debugging code.
