# enrich-fr
This command will be available in chat with /enrich-fr

Enrich a feature request with extra context from the original Freshdesk ticket conversation: either **append to a markdown catalog** or **return context only in chat**.

## Modes (pick one per invocation)

### Mode A -- Catalog / document update

Use when the user is working in a feature-requests markdown file, references that file (for example `@<your-catalog-file.md>`), or asks to add enrichment **into the doc**.

- The catalog path is **not** fixed. Search the workspace for the relevant file if the user only names it or uses a partial path.
- For each ticket: find the FR block in **that** document (or the file the user specified), fetch Freshdesk, then **append** the enrichment block below the existing FR entry (after the ticket link line), using the format under Step 4.
- Do **not** alter existing FR text above the new block except for adding the new block.

### Mode B -- Conversation only (paste / no file edit)

Use when the user **pastes** the FR excerpt (or "the code of the FR") and there is **no** clear intent to modify a catalog file, or they explicitly want output **only in chat**.

- Extract Freshdesk ticket number(s) from: the pasted text (for example `[Ticket](https://your-company.freshdesk.com/a/tickets/XXXXXX)`), or ticket IDs given with the command.
- Fetch ticket data via API (same as Mode A).
- Produce the same **information** as the enrichment (requester, summary, quotes, relevance, workarounds) **in the conversation only**. Use the block format below as a **template for readability** in chat, but **do not** write or edit any file unless the user switches to Mode A.

**How to choose:** If the user @-mentions a file, has a catalog file in context, or says to update / append / add to the document, use Mode A. If they only paste FR content and ask to enrich, use Mode B.

## Input

- Ticket numbers after the command: `/enrich-fr 321203` or `/enrich-fr 321203 322751 325601`
- Optionally: pasted FR markdown, or a path / @ reference to the catalog file

## Context

- Typical catalog files are markdown documents listing feature requests; each FR often includes `[Ticket](https://your-company.freshdesk.com/a/tickets/XXXXXX)`
- Freshdesk API credentials are stored in `<your-workspace>/scripts/.env` as `FRESHDESK_API_KEY`
- Freshdesk subdomain: `your-company.freshdesk.com`

## Your Task

For each ticket number:

### Step 1: Locate context (Mode A only)

- Find the FR entry in the catalog file the user is using (search by ticket number).
- Read the existing FR entry to understand what was captured.

Skip file lookup in Mode B; use the pasted FR text for comparison in Step 3 where helpful.

### Step 2: Fetch ticket data via API

Load the API key from `<your-workspace>/scripts/.env`, then make two API calls:

```bash
# Ticket metadata (subject, requester, description)
curl -s -u "$FRESHDESK_API_KEY:X" "https://your-company.freshdesk.com/api/v2/tickets/{ticket_number}"

# Full conversation thread
curl -s -u "$FRESHDESK_API_KEY:X" "https://your-company.freshdesk.com/api/v2/tickets/{ticket_number}/conversations"
```

Parse both responses to extract:

- `description_text` from the ticket (original customer message)
- Each conversation message's `from_email`, `created_at`, and `body_text`

### Step 3: Extract the key information

From the ticket description and conversation thread, extract:

1. **Customer's actual words** -- Direct quotes that explain what they need and WHY (the pain point, the use case, the business context). Pick the 1-3 most revealing quotes.
2. **Use case context** -- What is the customer trying to accomplish? What workflow is broken or missing?
3. **Workaround mentions** -- Is the customer using any workaround today? (for example "we currently do this manually", "we use Zapier to...")
4. **Requester info** -- The requester's name / company from the ticket or email signatures
5. **Relevance check** -- Does the conversation actually match the FR summary (in the doc or in the paste)? If the FR summary is misleading or the ticket is actually about something else, note this clearly.

### Step 4: Write the enrichment (Mode A: file; Mode B: chat only)

Insert into the **catalog file** (Mode A only), directly below the existing FR entry (after the ticket link line), using this exact format:

```
  > **Enriched from ticket:**
  > **Requester:** [Name / Company if available]
  >
  > [1-2 sentence summary of the actual use case / pain point]
  >
  > Key quotes:
  > - "[Exact customer quote 1]"
  > - "[Exact customer quote 2]"
  >
  > [Optional: Workaround mentioned / Additional context / Relevance note]
```

In Mode B, output the same structured content in the assistant reply; do not append to files.

## Important Guidelines

1. **Preserve exact quotes** -- Use the customer's actual words. Don't paraphrase their quotes.
2. **Be concise** -- The enrichment should add signal, not noise. 3-8 lines max per FR.
3. **Flag mismatches** -- If the ticket conversation doesn't match the FR summary, say so clearly: `> **Relevance note:** The ticket is actually about [X], not [Y as summarized].`
4. **Flag irrelevant tickets** -- If the customer's request clearly doesn't belong to the Integrations Team, note: `> **Relevance note:** This ticket appears unrelated to integrations. Consider removing from catalog.`
5. **Multiple tickets** -- Process them one at a time. In Mode A, update the file after each ticket so progress isn't lost.
6. **Don't alter existing FR content (Mode A)** -- Only ADD the enrichment block below. Never modify the original FR text, metadata, or links.
7. **Skip boilerplate** -- Ignore agent signatures, footers, "Got Questions?" blocks, and portal links when extracting conversation content.
8. **Handle long threads** -- For tickets with 10+ messages, focus on: the original customer message, customer replies that clarify intent, and any agent replies that reveal useful context. Ignore back-and-forth pleasantries.

## Output

After processing all tickets:

- **Mode A:** Brief summary: how many tickets were enriched in the file, any mismatched or irrelevant flags, any tickets that could not be accessed (errors, 404s, etc.).
- **Mode B:** The enrichment content in chat for each ticket, plus the same kind of summary (counts, flags, access errors).
