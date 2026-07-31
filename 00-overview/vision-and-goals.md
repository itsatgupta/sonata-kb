# Vision & Goals

## Problem
Sonata knowledge is fragmented across four systems with no unified query layer:
- **Bitbucket** — actual behavior (source of truth, but noisy/low-level)
- **Wiki** — architecture, tech specs, release notes (authoritative narrative, but drifts from code)
- **Jira** — epics/stories/acceptance criteria/defects (the "why" and "what changed")
- **X-ray** — test coverage and expected behavior (the "how do we know it works")

No one place answers "how does feature X work in Sonata today", or "what changed for
client Y going from v11.3 to v12.6, and what's my impact/risk". Both questions today
require a senior engineer manually cross-referencing wiki + Jira + release notes + code diffs —
slow, inconsistent, and a bottleneck through a handful of SMEs.

## Two products, one knowledge spine

| Product | Question it answers | Primary user |
|---|---|---|
| **Sonata Functional Assistant** | "How does X work / where is Y configured / what does this field do" | Support, BA, QA, client-facing consultants, (later) clients |
| **Upgrade Impact Assistant** | "Client Z is on v11.4, upgrading to v13.1 — what changed, what's the risk, what's the effort" | Delivery/upgrade teams, architects, account leads |

Both are served by the **same underlying knowledge graph** — release-note deltas, Jira
history, and wiki/spec content are just different views over the same indexed corpus.

## Interface
- **Chat**: text Q&A, grounded answers with citations back to wiki page / Jira ticket / release note.
- **Voice**: same backend, TTS output in a natural/conversational tone, opt-in
  ("Would you like me to read that out loud?"), not forced on every response.

## Success metrics (initial)
- POC: >80% of test questions on the pilot feature answered correctly with correct source citation.
- Time to produce an upgrade impact assessment for a single client/version pair: reduced from
  days (manual) to under 1 hour (assisted) by Phase 3.
- SME escalation rate (bot says "I don't know, ask a human") tracked and trending down release over release.

## Non-goals for v1
- Not replacing Jira/wiki/Bitbucket as systems of record — this is a read-layer on top.
- Not auto-approving upgrade decisions — output is a decision-support report, human sign-off required.
- Not client-facing on day one — internal only until accuracy/governance is proven (see `06-governance/`).

## Glossary
- **Trunk release**: Sonata's monthly internal release train.
- **Client release / upgrade**: a specific client's jump from their current trunk baseline to a target trunk version, usually yearly.
- **RDA**: Sonata's rich desktop application client.
- **Impact assessment**: report of what functional/technical changes lie between two trunk versions, filtered to what a specific client actually uses/customizes.
