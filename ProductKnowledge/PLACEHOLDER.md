# ProductKnowledge

This folder held code-derived product behavior references -- documents written by reading the codebase and translating it into plain-language sources of truth. They were used to ground the AI agent in how features actually work, rather than how they are documented externally.

## Contents (not included -- company confidential)

- **Platform architecture context** -- v3 vs v4 architecture differences, useful for triage and routing support questions to the right team
- **Epic summaries** -- plain-language summaries of large engineering epics (e.g. marketing analytics tracking, SSO attribute mapping) written after reading the implementation
- **Automation schema references** -- documented fields and behavior of key data models (e.g. automation rule access attributes)
- **Feature behavior docs** -- source-of-truth behavioral references for specific features (coupon codes, downgrade enforcement, email notification settings, learner email sending logic)
- **Engineering review Q&As** -- questions and answers from engineering review sessions, captured as reference for future PM decisions

## How it was used

These files were the PM equivalent of internal technical docs -- written to bridge the gap between engineering implementation and PM/support understanding. They were @-mentioned in Cursor when:
- Triaging a support ticket that might be a real bug vs expected behavior
- Writing acceptance criteria that referenced actual system behavior
- Onboarding support agents to edge cases
