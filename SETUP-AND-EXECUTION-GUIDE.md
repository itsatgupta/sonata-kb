# Setup & Execution Guide — Claude Code, POC → Production

This is the operational companion to `README.md` and `CLAUDE.md`. It tells you exactly
what to click/type, in order, to go from an empty machine to a working POC, and then
how to progress phase by phase toward production.

---

## Part A — One-time setup

### A1. Install Claude Code
1. Requires Node.js (LTS) installed first — check with `node -v`; install from
   nodejs.org if missing.
2. Install: `npm install -g @anthropic-ai/claude-code`
3. Verify: `claude --version`
4. Authenticate: run `claude` once in any folder and follow the login prompt
   (Anthropic Console account or Claude subscription, depending on your org's setup).

### A2. Get this repo onto your machine
1. Unzip `sonata-kb.zip` into your working directory, e.g.:
   ```
   mkdir -p ~/projects && cd ~/projects
   unzip sonata-kb.zip
   cd sonata-kb
   ```
2. Turn it into a git repo now, even before writing more code — you want history from day one:
   ```
   git init
   git add .
   git commit -m "Initial Sonata KB plan + POC scaffold"
   ```
3. Push to your org's Bitbucket/GitHub so the Centralised Upgrade Team can collaborate:
   ```
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

### A3. Open it in Claude Code
```
cd ~/projects/sonata-kb
claude
```
Claude Code will automatically read `CLAUDE.md` at the repo root on startup — that's
why it exists at the root and not buried in a subfolder. You should see it acknowledge
the project context (citation rules, read-only rules, Phase 2 stubs) when you ask it
anything about the codebase.

**Sanity check prompt to run first:**
> "Read CLAUDE.md and the 03-poc folder, then summarize what's already built and what's
> stubbed, in your own words."

If Claude's summary matches what's in `README.md`'s "buildable POC agent" section, you're
correctly set up.

### A4. Configure credentials (do this before any real ingestion)
1. In Claude Code:
   ```
   cd 03-poc/agent
   cp config/env.example.txt .env
   ```
2. Open `.env` and fill in real values — you'll need, at minimum for the POC:
   - `ANTHROPIC_API_KEY`
   - `WIKI_BASE_URL` + `WIKI_API_TOKEN` (read-only token/service account — ask your
     wiki admin for a read-only API token, don't use a personal admin token)
   - `JIRA_BASE_URL` + `JIRA_USER_EMAIL` + `JIRA_API_TOKEN` (same — read-only service
     account preferred)
3. Add `.env` to `.gitignore` immediately (create the file if it doesn't exist):
   ```
   echo ".env" >> .gitignore
   echo "data/" >> .gitignore
   git add .gitignore && git commit -m "Ignore secrets and local index data"
   ```
4. Install Python dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

**You can ask Claude Code to do steps A4.3-A4.4 for you** — e.g. "set up a Python
virtualenv here and install requirements.txt" — it has bash access and will just do it.

---

## Part B — Phase 0: POC (weeks 1-4)

### B1. Pick the pilot feature
1. Open `03-poc/poc-candidate-selection.md` in Claude Code and ask:
   > "Help me shortlist 3-5 recent Sonata enhancements that meet the criteria in this
   > document. I'll paste in the last 3 release notes." (paste actual release note text)
2. Pick one, fill in the "candidate feature one-pager" template at the bottom of that
   file with real details (wiki page IDs, Jira keys, SME contact).
3. Commit it: `git add 03-poc/poc-candidate-selection.md && git commit -m "Select POC pilot feature"`

### B2. Write the test questions BEFORE building anything
1. Open `03-poc/agent/eval/test_questions.md`.
2. With your SME, write 20-30 real questions per the categories already templated
   (direct fact, explanation, before/after, negative/edge case).
3. Ask Claude Code:
   > "Read eval/test_questions.md's format instructions and help me draft 25 test
   > questions for [pilot feature name], based on this release note and Jira epic text: [paste]"
4. Commit this file **before** touching ingestion code — this order matters (avoids
   unconsciously tuning the system to a test set written after seeing its behavior).

### B3. Ingest the pilot feature's wiki pages
```
cd 03-poc/agent
source venv/bin/activate
python ingestion/wiki_ingest.py --page-id <id1> --page-id <id2>
```
- If your wiki isn't Confluence-compatible, tell Claude Code:
  > "Our wiki is [platform name] with this API shape: [paste API docs/example response].
  > Update ingestion/wiki_ingest.py and tools/wiki_tool.py's _fetch_from_wiki_api to match,
  > keeping the same WikiChunk output shape."
- Verify it worked: `ls data/` should show `wiki.json` with your chunks.

### B4. Confirm Jira access works
```
python -c "from tools.jira_tool import jira_search; print(jira_search(query='<a term from your pilot feature>', max_results=3))"
```
If this errors, the error message will tell you what's misconfigured (bad token, wrong
base URL, wrong project key) — paste the error to Claude Code and ask it to help debug.

### B5. Run the chatbot
```
python orchestrator.py
```
Ask it a few of your test questions manually first, informally, before running the
full eval — this is where you catch obvious wiring issues fast.

### B6. Run the full eval
```
python eval/run_eval.py
```
- Open the generated `eval/results.csv`.
- Have your SME fill in the `score_manual` column (correct / partial / wrong /
  hallucinated_citation) for every row.
- Ask Claude Code to help summarize:
  > "Read eval/results.csv and compute the % correct, and list every row where
  > score_manual is 'wrong' or 'hallucinated_citation' so I can look at why."

### B7. Go/no-go decision
Check against `02-phases/phase-0-poc.md` exit criteria:
- ≥80% correct with accurate citations?
- Every answer traceable to a specific source?
- SME sign-off obtained?
- Findings doc written (failure modes observed)?

Write the findings as `03-poc/poc-findings.md` (new file) — ask Claude Code:
> "Based on eval/results.csv and our discussion, draft 03-poc/poc-findings.md
> summarizing what worked, what failed and why, and what Phase 1 needs to fix."

**If yes → proceed to Phase 1. If no → iterate on retrieval/chunking/prompt before
scaling scope, not after.**

---

## Part C — Phase 1: Functional KB, all modules (weeks 5-12)

1. With the Centralised Upgrade Team, run the SME workshop mentioned in
   `02-phases/phase-1-functional-kb.md` to define the Feature/Module taxonomy — do
   this as a real working doc, e.g. `01-architecture/module-taxonomy.md` (new file).
2. Extend `ingestion/wiki_ingest.py` to bulk-ingest by space rather than page-by-page:
   > "Add a --space flag to wiki_ingest.py that lists and ingests all pages in a given
   > Confluence space, with pagination, instead of requiring individual page IDs."
3. Extend Jira ingestion similarly — add a `jira_ingest.py` for bulk indexing if you
   want Jira content in the same vector index as wiki (currently `jira_tool.py` queries
   Jira live via JQL rather than pre-indexing — decide if you also want a searchable
   Jira text index for free-text queries beyond structured JQL).
4. Add the feedback capture mechanism from `06-governance/governance-and-evaluation.md`
   — a simple thumbs up/down + comment, logged to a file or lightweight DB table.
5. Re-run eval, now against a broadened question set spanning modules.
6. Exit gate: coverage across major modules + accuracy threshold + escalation-rate baseline
   logged (see `02-phases/phase-1-functional-kb.md`).

---

## Part D — Phase 2: Code + Test layer (weeks 13-18, can start once Phase 1 is stable)

1. Get Bitbucket + X-ray API access (read-only service accounts).
2. Build the path→module mapping table with engineering — this is the actual hard
   part of this phase. Store it as data, e.g. `04-data-sources/module-mapping.json`,
   not hardcoded in `bitbucket_tool.py`.
3. Implement `tools/bitbucket_tool.py`'s `bitbucket_search` (currently raises
   `NotImplementedError`) and `tools/xray_tool.py`'s `xray_search` (currently returns
   empty) — ask Claude Code to implement each against your actual API docs.
4. Validate entity linking: given a Jira key, can you resolve to its PRs and tests in
   one traversal? Write a small test script proving this before calling Phase 2 done.

---

## Part E — Phase 3: Upgrade Impact Assessment (weeks 19-28)

This is where `08-central-upgrade-team-alignment/catalogue-alignment.md` becomes your
spec — go back to it before starting this phase.

1. **Client profile bootstrap** — start with 2-3 pilot clients (smaller/simpler first).
   Run SME workshops with account/delivery teams; mine existing SOT records per the
   catalogue's "Configuration Alignment Service." Store as structured data, e.g.
   `05-personas-and-usecases/client-profiles/<client>.json` (gitignore or encrypt if
   sensitive — see governance doc).
2. Implement `generate_impact_draft()` in `tools/jira_tool.py` (currently raises
   `NotImplementedError`) — it composes `jira_version_range()` + client profile +
   risk-tagging.
3. Define the risk-scoring model WITH the delivery/upgrade team (don't invent it
   solo) — starting dimensions are listed in `02-phases/phase-3-impact-assessment.md`.
4. Build report generation — ask Claude Code to use the `docx` skill to render the
   final impact assessment as a Word doc matching the catalogue's existing deliverable
   format, if one exists to match against.
5. Pilot end-to-end with your 2-3 client/version pairs; get delivery-team sign-off that
   risk categorization is directionally trustworthy.
6. **Track effort/time saved per deliverable** against the baseline you gathered from
   the Upgrade Team (see catalogue-alignment.md's "open question") — this is your real
   evidence toward the 60% cost-reduction goal.

---

## Part F — Phase 4: Voice (can run in parallel with Phase 2/3)

1. Pick an STT/TTS provider (org-approved) and add a thin wrapper module,
   `03-poc/agent/voice/voice_io.py` — STT converts speech to text and calls `orchestrator.ask()`
   unchanged; a response formatter strips markdown/tables before TTS.
2. Test against the same eval question set, spoken — confirm tone/pacing with real users,
   not just a technical pass (see `02-phases/phase-4-voice-interface.md` exit criteria).

---

## Part G — Phase 5+: Governance hardening & rollout

1. Before ANY client-facing exposure: implement the access-control/entitlement model
   from `06-governance/governance-and-evaluation.md` — role-based scoping, and hard
   isolation between clients' data. Treat this as a security review, not a feature.
2. Move the local TF-IDF index (`retrieval/index.py`) to your org's real vector store —
   it was always meant to be swapped out once you're past a single pilot feature's scale.
3. Formalize ownership per `catalogue-alignment.md`'s recommendation (Upgrade Centre of
   Excellence) rather than leaving this an unowned side project.
4. Keep the eval harness running continuously — every model/prompt/retrieval change
   gets re-scored before merge, not just at each phase gate.

---

## Quick reference: what to ask Claude Code at each stage

| You want to... | Ask Claude Code... |
|---|---|
| Understand current repo state | "Read CLAUDE.md and README.md and summarize current status" |
| Adapt a tool to your real API | "Here's our [system]'s API shape: [paste]. Update tools/[x]_tool.py to match." |
| Debug a failing call | Paste the exact error/traceback and ask "why is this failing and how do I fix it" |
| Move to the next phase | "Read 02-phases/phase-N.md and tell me what's still missing before I can call this phase done" |
| Check citation discipline isn't slipping | "Run eval/run_eval.py and flag any row where citation_present is False" |
