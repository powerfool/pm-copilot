---
name: freshdesk-ticket
description: Fetch and analyze a Freshdesk support ticket when the user pastes a Freshdesk URL or ticket number. Triggers automatically on any your-company.freshdesk.com/a/tickets/ URL. Loads API key from scripts/.env, fetches ticket metadata and full conversation thread, then summarizes the issue and provides analysis. Optionally, after summarizing, ask whether to search the codebase to verify if the customer is describing a real product issue versus misunderstanding or third-party behavior.
---

# Freshdesk Ticket Analysis

Trigger: user pastes a URL matching `your-company.freshdesk.com/a/tickets/{id}` or provides a bare ticket number.

## Steps

### 1. Resolve ticket ID
Extract the numeric ID from the URL (e.g. `/a/tickets/341800` -> `341800`).

### 2. Load API key
Read `FRESHDESK_API_KEY` from `<your-workspace>/scripts/.env`.

### 3. Fetch ticket data (run in parallel)
```bash
curl -s -u "$FRESHDESK_API_KEY:X" "https://your-company.freshdesk.com/api/v2/tickets/{id}"
curl -s -u "$FRESHDESK_API_KEY:X" "https://your-company.freshdesk.com/api/v2/tickets/{id}/conversations"
```

### 4. Ask about codebase verification (before or right after the first summary)
**Stop and ask the user explicitly:** whether they want you to analyze the codebase (e.g. repos under `src/` in their workspace) to check whether the ticket describes an actual product behavior, limitation, or bug -- versus a configuration mistake, expected behavior, or something outside the product.

- If they **decline** or do not answer, finish with the ticket-only summary and analysis from step 5.
- If they **confirm**, search the relevant repo(s), trace behavior mentioned in the ticket, and add a short section to the report: **Codebase check** -- what you verified in code vs what remains uncertain or only from the ticket.

### 5. Report
Provide a concise summary:

- **Subject & requester** -- ticket title and who opened it
- **Issue** -- what the customer is reporting (use exact quotes)
- **Thread summary** -- key back-and-forth between customer and support, in order
- **Current status** -- open/pending/resolved and last action
- **Analysis** -- your assessment: is this a bug, a config issue, a feature request, or a misunderstanding? What is the likely next step?

Keep the report short. Use exact quotes from the ticket when summarizing what the customer or support said.

If the user did not opt in to codebase verification, omit the **Codebase check** section.
