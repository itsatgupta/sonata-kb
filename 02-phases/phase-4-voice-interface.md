# Phase 4 — Voice Interface

Can run in parallel with Phase 2/3 — it's a presentation-layer addition, not new knowledge
engineering, once chat (Phase 1) is stable.

## Goal
Let users ask questions by voice and optionally have answers read back in a smooth,
natural, conversational tone — not a robotic text-to-speech dump of a table.

## Scope
- STT input (speech → text → same chat pipeline).
- Response formatting pass before TTS:
  - Strip tables/code/markdown, convert to short spoken sentences.
  - Numbers/versions read naturally ("version thirteen point one", not "v13.1" verbatim).
  - Long answers offered as a spoken summary + "would you like the full detail in chat".
- Voice is **opt-in per response**, not forced — e.g. "Want me to read that out loud?"
  matches the requirement for a "smoother tone... if they want to listen."
- Same citations/source-grounding as chat — voice doesn't relax the accuracy bar.

## Exit criteria
- Voice round-trip works for the same test question set used in Phase 0/1 evals.
- User testing confirms tone/pacing feels natural, not robotic (qualitative sign-off,
  not just a technical pass).
