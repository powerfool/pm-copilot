# ProductKnowledge

This folder is for code-derived product behavior references -- documents you write by reading the codebase and translating it into plain-language sources of truth. Use the `/document-feature-behavior` command to generate them.

## What belongs here

- **Platform architecture context** -- how major platform versions or layers differ; useful for triage and routing support questions to the right team
- **Epic summaries** -- plain-language summaries of large engineering epics written after reading the implementation
- **Data model references** -- documented fields and behavior of key data models (e.g. automation rule schemas, access attributes)
- **Feature behavior docs** -- source-of-truth behavioral references for specific features; cover edge cases, defaults, and what support should tell customers
- **Engineering review Q&As** -- questions and answers from engineering review sessions, captured as reference for future PM decisions

## How to use it

@-mention these files when you need the agent to reason about how something actually works, not how it is documented externally:

- Triaging a support ticket: "Is this a real bug or expected behavior? See @ProductKnowledge/feature-name-behavior.md"
- Writing acceptance criteria: "Given @ProductKnowledge/automation-schema.md, what edge cases should I cover?"
- Onboarding support agents to non-obvious behavior

The `/document-feature-behavior` command will guide you through creating these files from the codebase. Run it when a feature comes up repeatedly in support tickets or engineering reviews.
