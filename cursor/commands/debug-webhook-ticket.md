# debug-webhook-ticket
This command will be available in chat with /debug-webhook-ticket

Fetch a Freshdesk support ticket and analyze it for webhook payload or automation issues. Use when a customer reports wrong/missing data in a webhook or when support needs help debugging what the payload actually sends.

## Input

The user provides a Freshdesk ticket number or full ticket URL. Examples:
- `/debug-webhook-ticket 341800`
- `/debug-webhook-ticket https://your-company.freshdesk.com/a/tickets/341800`

## Context

- Freshdesk API credentials are stored in `<your-workspace>/scripts/.env` as `FRESHDESK_API_KEY`
- Freshdesk subdomain: `your-company.freshdesk.com`
- Webhook payload behavior is documented in your workspace's `webhook-payload-by-trigger.md` (trigger-specific payload keys, what is always present, what is stripped)

## Your Task

### Step 1: Resolve ticket ID
- If the user provided a URL, extract the ticket number from it (e.g. `/a/tickets/341800` -> `341800`).
- If only a number was provided, use it as the ticket ID.

### Step 2: Fetch ticket data via API
Load the API key from `<your-workspace>/scripts/.env`, then make two API calls:

```bash
# Ticket metadata (subject, requester, description)
curl -s -u "$FRESHDESK_API_KEY:X" "https://your-company.freshdesk.com/api/v2/tickets/{ticket_id}"

# Full conversation thread
curl -s -u "$FRESHDESK_API_KEY:X" "https://your-company.freshdesk.com/api/v2/tickets/{ticket_id}/conversations"
```

Parse both responses to get:
- `description_text` (original customer message)
- Each conversation message: `from_email`, `created_at`, `body_text`, and whether it is `incoming` (customer) or agent/support

### Step 3: Analyze the issue
From the ticket description and thread, determine:

1. **What the customer says they receive** -- Exact payload shape or fields they quoted (e.g. relative file path, missing keys).
2. **What they expected** -- From the automation UI preview, help docs, or API docs if they mentioned it.
3. **What actually happens** -- If support or the customer confirmed something (e.g. "that URL returns 404", "we don't support that").
4. **Compare to internal docs** -- If the issue is about webhook payload, read `webhook-payload-by-trigger.md` and check:
   - Does the documented payload for that trigger include the field in question?
   - Is the field documented as a relative path, a full URL, or not documented at all?
5. **Support accuracy** -- Did support give incorrect guidance (e.g. wrong URL pattern that 404s)? Note it.

### Step 4: Report (no code changes)
Provide a short analysis that includes:

- **Trigger/context** -- Which automation trigger or flow the ticket is about (e.g. assessment-submitted, file upload).
- **Payload issue (if any)** -- Whether there is a real payload/doc bug: e.g. we send a relative path with no way to resolve it, we document X but send Y, or we don't document file fields at all.
- **Support/UX notes** -- Wrong workaround given, or doc gap that could be fixed in help center or in-app copy.
- **Product conclusion** -- One or two sentences: is this a bug, a doc gap, or a feature request (e.g. "need downloadable file URL in webhook")?

Do **not** write or change code. Only analyze and report.

## Important Guidelines

1. **Use exact quotes** when summarizing what the customer or support said (e.g. "that link leads to a 404").
2. **Cite the doc** -- When comparing to `webhook-payload-by-trigger.md`, reference the relevant trigger and table.
3. **Flag wrong support guidance** -- If support suggested something that the customer then said doesn't work, state it clearly so product can correct internal playbooks or docs.
4. **One ticket per invocation** -- If the user provides multiple ticket numbers, analyze each and report separately; you may fetch all in parallel.

## Output

- A concise analysis (trigger, what's wrong or missing, doc/support accuracy, product conclusion).
- If the ticket could not be fetched (404, auth error), say so and do not guess.
