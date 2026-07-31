# Personas & Use Cases

## Internal support/BA
- "What does the [field] on the [screen] do?"
- "Why does Sonata reject this transaction type?"
- "Which release introduced [behavior]?"

## QA/Test engineer
- "What acceptance criteria exist for [story]?"
- "Is there regression coverage for [feature]?"

## Delivery/upgrade team & architects
- "What changed between v11.4 and v13.1 in the dealing module?"
- "Client Z is upgrading — what's their risk profile?"
- "Which clients are affected by this recent defect fix?"

## Support / service-desk triage agent (later phase)
- "Has this defect been reported for another client before?"
- "Which existing tickets are the closest matches to this customer report?"
- "Here are the customer's replication steps — draft a base ticket with initial analysis."
- Triage flow: search historical defects → found? reference the existing ticket(s) /
  not found? draft a new base ticket (replication steps + analysis) for human approval.
  Write-back to Jira is always **draft-then-approve**, never auto-created.
  See `07-future-roadmap/defect-triage-assistant.md`.

## Account/client-facing consultants (later, client-facing phase)
- "Explain [feature] to a client in plain language."
- "What's new for our client in the last 3 releases relevant to what they use?"

## Voice-specific scenario
- User on the move / hands busy asks a quick functional question by voice, gets a short
  spoken answer, and can say "read me the full detail" or "send this to my chat" for
  the complete grounded/cited version.

## Sample end-to-end flow (impact assessment)
1. User: "What's the impact of Royal London upgrading from v11.4 to v13.1?"
2. System resolves Royal London's client profile (current version, modules in use).
3. System runs version-diff query for that release range.
4. System filters/weights changes by Royal London's module usage + customizations.
5. System generates a structured report: module → change → risk → recommended focus.
6. Delivery lead reviews, edits, finalizes — system output is a draft, not the final word.
