# Phase-wise Roadmap

| Phase | Name | Duration (typical) | Goal |
|---|---|---|---|
| 0 | POC | 3–4 weeks | Prove chat Q&A works end-to-end on ONE small feature area, with citations |
| 1 | Functional KB (Chat) | 6–8 weeks | Ingest full Wiki + Jira (read) for all modules; broad functional Q&A |
| 2 | Add Code + Test layer | 4–6 weeks | Ingest Bitbucket + X-ray; link entities into the graph; richer "how is this implemented/tested" answers |
| 3 | Upgrade Impact Assistant | 6–10 weeks | Version-diffing, client profiles, impact/risk reports |
| 4 | Voice Interface | 3–4 weeks | STT/TTS layer over existing chat backend, tone-tuned |
| 5 | Client-facing rollout + governance hardening | ongoing | Access control, per-client scoping, feedback loop, eval harness |
| 6 | Continuous improvement | ongoing | Auto-detect KB gaps, self-updating client profiles, proactive "your upgrade just got riskier" alerts |

Phases 0–3 can be sequential; **Phase 4 (voice) can run in parallel with Phase 2/3** since it's
purely a presentation-layer addition once chat is solid — don't gate voice behind impact
assessment.

## Why this order
- Start with the narrowest, most self-contained slice (Phase 0) to validate retrieval quality,
  citation trust, and org buy-in before investing in graph/version-diff complexity.
- Wiki + Jira (Phase 1) alone already unlocks most "how does X work" questions — code/test
  ingestion (Phase 2) is higher effort for a narrower payoff (mostly benefits impact
  assessment and deep technical questions), so it's sequenced after functional Q&A is solid.
- Upgrade Impact Assessment (Phase 3) is the highest-value, highest-effort piece — it needs
  Phase 1+2's indexed history to already exist, plus new work: client profiles and an
  impact-scoring model. It's deliberately not the POC.
- Voice (Phase 4) is cheap once chat works — it's UX, not new knowledge engineering.

See individual phase files for entry/exit criteria and detailed scope.

## Adjacent initiative: Smart Discovery — Foundation Phase (Centralised Upgrade Team)

A parallel AI proposal from the Centralised Upgrade Team (v0.2 draft, 27 Jul 2026; lead
Tamoor Malik) de-risks — and partially overlaps — this roadmap. Full mapping:
`08-central-upgrade-team-alignment/smart-discovery-alignment.md`.

| Its component | Weeks | Relationship to this roadmap |
|---|---|---|
| **C1** Sonata structural map (`agents.md`, module/path taxonomy) | 1–4 | The module taxonomy + path→module map Phases 1–2 need — consume it, don't rebuild |
| **C2a/b** Read-only access mechanism (GitLab; 2-week spike → build) | 1–5 | The code-access route Phase 2 rides on; same read-only governance posture |
| **C3** Bravura skill pack (central markdown skills, SpecKit) | 3–6 | Institutional home for the shared knowledge layer; answers the ownership-model question |
| **C4** NL query over SBS services (read-only, live system) | 5–8 | New live-system capability — candidate Phase 3+ addition, not v1 |
| **C5** Read-only GraphQL layer (candidate only) | post-foundation | Watch, don't build |

Sequencing implications:

- **Phase 0 and Phase 1 are unaffected** (Wiki + Jira only) — run in parallel.
- **Phase 2 should consume C1 + C2 output** rather than duplicate code access and module
  mapping. It's a *draft* proposal — hold a fallback (own access + own lightweight map) in
  case it stalls, but don't pre-build against it.
- **Resolve the GitLab vs Bitbucket question before Phase 2** — Smart Discovery assumes the
  Sonata estate is on GitLab; this roadmap's code layer assumes Bitbucket
  (see `04-data-sources/bitbucket.md`).
- Keep this roadmap's "Upgrade Impact Assessment" (version-diff) distinct from Smart
  Discovery's "change decomposition" (change-request → initiative/epic/story) — same word,
  different questions.
