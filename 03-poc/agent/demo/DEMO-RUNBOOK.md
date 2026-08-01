# Feature-1 Sign-off Demo — Runbook (live screen-share)

**Goal:** let Pratigya watch the assistant answer questions **live** against the real Wiki + Jira,
satisfying the phase-0 exit criterion ("one SME watches the assistant answer live"). Nothing is
deployed to a server — this runs from your machine and is shared over screen-share (Teams/Zoom/Meet).

Companion: `demo_questions.md` (what the 8 questions check) and `demo_transcript.md` (the run
produced today, as a backup if anything fails live).

## Before the session (5 min — do on the demo machine, not live)

1. Confirm the machine can reach the sources:
   - `03-poc/agent/.env` exists (gitignored) with Wiki / Jira / Anthropic tokens.
   - venv present: `03-poc/agent/venv/Scripts/python.exe`.
2. Pre-flight smoke — one question, ~10s, from `03-poc/agent`:
   ```
   venv/Scripts/python.exe -c "from orchestrator import ask; print(ask('What is the default page size for searchEmployer?')[0][:200])"
   ```
   If it errors (auth / network / billing), fix **before** the session — don't debug live.
3. Open a fresh terminal, `cd 03-poc/agent`. Close other tabs (keep the window clean for sharing).

## The live run (≈10 min)

Run the prepared 8-question set — it streams Q → A with citations:
```
venv/Scripts/python.exe demo/demo_run.py
```

Order and the talking point to call out at each step:

| # | Question | Point out |
|---|---|---|
| 1 | What does the optional pagingRange element do? | Direct spec answer, Wiki § SFC-04 citation |
| 2 | Default results per page if pagingRange omitted? | Precise default (20/page) with source |
| 3 | Why was pagination added? | Synthesised from Wiki + Jira, still cited |
| 4 | Would a client without pagingRange see a change? | Backward-compat delta — "No, optional, default applies" |
| 5 | Does it return Employer External References? | Out-of-scope honesty — says "No, dropped from scope", doesn't guess |
| 6 | Defect for 14 failing TDDs? | Jira lookup by description → BASE-460256 |
| 7 | Exception in BASE-460272? | Deep Jira defect detail, layered fault chain |
| 8 | Status of BASE-458911? | Jira status lookup → Closed, with fixVersion |

## Optional: free-form chat

After the prepared set, open interactive chat so Pratigya can ask her own question:
```
venv/Scripts/python.exe orchestrator.py
```
Suggested prompts if she wants ideas:
- "What changed in searchEmployer in Sonata 16.2?" (delta)
- "Will the pagingRange change affect my existing calls?" (backward-compat)
- "What defect was reported for SaveEmployerTest?" (Jira lookup)

## Key messages to emphasise

- **Every answer carries a `Wiki:` or `Jira:` citation** — no un-sourced claims. That is the trust
  mechanism this whole POC exists to prove.
- Where content is **out of scope**, it says so plainly rather than guessing.
- Answers come from the **indexed/live sources**, not model memory.
- The full eval set is **27/27 Correct**, graded by Pratigya herself — 100% against the ≥80% bar.

## If something fails live

- Fallback: `python orchestrator.py` and ask a single question.
- Worst case: open the committed `demo_transcript.md` — it is today's actual live run — and note it
  was produced live minutes ago.

## After the session — capture sign-off

- Get Pratigya's sign-off (verbal or in the call chat).
- Update `03-poc/PROGRESS-STATUS.md`: mark demo **done**, phase-0 exit **complete**, and begin
  Phase-1 (first steps at the end of `02-phases/phase-1-implementation-plan.md`).
