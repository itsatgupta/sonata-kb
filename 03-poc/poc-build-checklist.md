# POC Build Checklist (for Claude Code / engineering)

- [ ] Confirm read-only API access: Wiki space(s) for the pilot feature, Jira project/filter
      for its epic+stories+defects
- [ ] Export/ingest: wiki page(s) as markdown/HTML → chunk → embed
- [ ] Export/ingest: Jira issues (summary, description, acceptance criteria, comments,
      fixVersion, linked issues) → chunk → embed, keep structured fields as metadata
      (don't just flatten to text — you'll want to filter by fixVersion/type later)
- [ ] Build a minimal entity link: Jira key mentioned in wiki page ↔ actual Jira issue
      (regex on key pattern, e.g. `PROJ-1234`, is enough for POC)
- [ ] Stand up hybrid retrieval (keyword + vector) over this small corpus
- [ ] Build minimal chat UI (internal, no auth complexity needed for POC) — a simple
      web chat is enough, in Claude Code this can literally be a small React/HTML artifact
      or app calling your retrieval backend
- [ ] Every answer must include a citation (wiki page title/section OR Jira key) —
      no exceptions, this is the trust mechanism
- [ ] Run the pre-written test question set, score each answer (correct / partially
      correct / wrong / hallucinated-citation), log failures with reason
- [ ] Write up findings: what worked, what didn't, what's needed to scale to Phase 1

## Suggested repo layout once POC code exists
```
sonata-kb/
├── 03-poc/
│   ├── ingestion/        # small scripts: wiki_fetch.py, jira_fetch.py
│   ├── index/            # embedding + chunking logic
│   ├── app/              # minimal chat backend + UI
│   └── eval/             # test_questions.md, results.csv
```
