# jira-url-codebase-triage

This command will be available in chat with `/jira-url-codebase-triage`

## Purpose

For **product managers and support**: given a **Jira issue URL** (for example `https://your-company.atlassian.net/browse/SUP-24881`), fetch the ticket from Jira, then **search this workspace codebase in read-only mode** to see whether the reported behavior lines up with existing product code. Deliver a **plain-language answer** suitable for internal notes or customer-facing context. **Do not write, edit, or suggest code changes** unless the user explicitly asks for engineering work.

## Input

The user provides one or more Jira URLs, or an issue key (e.g. `SUP-24881`). Examples:

- `/jira-url-codebase-triage https://your-company.atlassian.net/browse/SUP-24881`
- `/jira-url-codebase-triage SUP-24881`

## Jira site

- **cloudId:** `<YOUR_CLOUD_ID>`
- Use the **Atlassian MCP** tools: primarily `getJiraIssue` with `responseContentFormat: "markdown"` when you want readable text for the model.
- **Comments are required:** always request the `comment` field (e.g. pass `fields` including `"comment"` on `getJiraIssue`, not description-only). If `comment.total` is greater than the number of comments returned, fetch the rest via Jira so thread context is not missed.

### Parse URL to issue key

From `browse` links: path segment after `/browse/` is the key (e.g. `SUP-24881`).

From board links: use `selectedIssue=` query param if present.

If only a key is given, use it as `issueIdOrKey`.

## Step 1: Fetch the Jira issue (including comments)

1. Call `getJiraIssue` with `cloudId`, `issueIdOrKey`, and **`fields` that include `"comment"`** (and other fields you need, e.g. summary, status, description, priority). Do not rely on a fetch that omits comments.
2. Summarize for the user **without developer jargon**:
   - Summary, status, type, priority (if present)
   - What the reporter / description says is wrong or requested
   - **All issue comments** (chronological): who, date, gist; paste **exact** internal error strings or customer pushback when they change triage (e.g. log lines, "Required option...", Freshdesk ticket ids)
   - Any linked issues, labels, or components if useful for context

If the MCP returns an auth error, tell the user to sign in to the Atlassian MCP and retry. Do not invent ticket content.

## Step 2 (optional): Related Jira issues

If it helps triage duplicates or engineering ownership, run **one or two** narrow `searchJiraIssuesUsingJql` queries using distinctive words from the ticket summary or description. Keep result sets small (e.g. `maxResults` 10-20). This step is optional when the user only wants a codebase read.

## Step 3: Search the codebase (read-only)

1. **Scope:** Product code lives under `/` (e.g. `/<frontend-repo>/`, `/<backend-repo>/`). Prefer searching there; avoid treating the workspace root as a single git repo.
2. Use **semantic search** and **exact-text search** with terms from the **description and comments**: feature names, UI labels, error strings, integration names, webhook trigger names, API paths, etc.
3. Goal: answer **whether** the codebase contains logic that could explain the behavior (expected limitation, known path, feature flag, etc.), **not** to design a fix.
4. **Do not** modify files, open PRs, or paste large code blocks unless a short snippet helps explain behavior to a PM.

## Step 4: Answer format (for PM / support)

Reply with:

1. **Ticket in one line** -- Key, summary, status.
2. **What the customer / reporter is asking** -- Bullet points in plain language.
3. **Comments / thread** -- Short bullets if any comments exist (internal findings vs customer reply). Align or contrast with the description.
4. **Codebase signal** -- One of: **Likely product behavior** (with brief why), **Unclear / needs engineering** (what is missing), or **No strong match** (what you searched for). Include **file paths only** as pointers, not implementation tutorials. Incorporate **comment-derived** error strings or hypotheses when relevant.
5. **Confidence** -- High / medium / low, and one sentence why.
6. **Suggested next step** -- e.g. escalate to the team, check docs, confirm reproduction with customer, link existing issue -- **no code**.

## Guardrails

- **No code changes** and no prescriptive "change this function" instructions unless the user explicitly requests engineering implementation.
- If the ticket is empty or vague, say so and list **one** clarifying question for the user to ask the reporter.
- Quote ticket text **exactly** when it helps retrieval later (short phrases).
