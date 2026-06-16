This command will be available in chat with /slack-to-jira

## Hard rule: Jira

**Do not create a Jira ticket unless Dimitris explicitly asks you to** (e.g. "create the ticket", "file this in Jira", "open <PROJECT>-..."). Never auto-create tickets at the end of analysis.

---

## Summary (intended flow)

When Dimitris pastes a Slack conversation URL:

1. **Fetch the thread** using Slack MCP `conversations_replies` (paginate with `cursor` until empty). Follow workspace rules for parsing `channel_id` and `thread_ts` from the URL.
2. **Analyze:** Perform root cause analysis by searching the codebase (`src/` repos). Separate **facts verified in code** from **interpretation or Slack-only claims**.
3. **Respond for a PM:** Deliver a concise, actionable summary that helps Dimitris **reply in Slack**:
   - What was reported and who cares (customer/internal)
   - Whether this looks like a bug, a product limitation, misconfiguration, or needs more data
   - Suggested wording he can paste or adapt (professional, not code-dump)
   - Impact level (HIGH / MEDIUM / LOW) and any urgency signals
4. **Interview (if there is a real issue):** Use a dialogue. Ask **one question at a time** about how the issue should be handled (scope, priority, comms to customers, acceptance criteria, owner). Do not rush to solutions; align on intent first.
5. **Jira (only after explicit request):** After Dimitris asks for a ticket **and** confirms **which Jira project** it should live in, propose creating the issue (or draft the full ticket body for him to paste). Default project suggestion may be the integrations project, but **never assume** -- confirm the project key.

---

## Instructions (detail)

### 1. Fetch the Slack conversation

- Parse `channel_id` and `thread_ts` from the URL (see Quick Reference).
- Use `conversations_replies` with the correct server/tool schema from the MCP descriptor.
- If the thread is long, paginate until no more messages.

### 2. Root cause analysis (codebase)

- Search relevant repos under `/` (see workspace git layout).
- Compare implementations when relevant (e.g. v3 vs v4).
- Cite file paths (and line numbers when helpful) for engineering follow-up, but **keep the first response PM-readable** -- no walls of code unless Dimitris asks for technical depth.

### 3. PM-first output

- Lead with what to do next and what to say in Slack.
- Call out gaps, risks, and what would need repro or product decision.
- Respect `pm-copilot`: bias to action, challenge assumptions when useful.

### 4. Interview before any ticket

- If resolution is not obvious, ask how Dimitris wants to handle it (fix vs doc vs defer), one question at a time.

### 5. Jira creation (only when explicitly requested)

- Confirm: **project key**, issue type (Bug / Story / Support Issue / other), and title.
- Use the Atlassian MCP `createJiraIssue` tool with the configured `cloudId` when creating, **after** project is confirmed.
- Ticket body (when requested) should include: reporter, Slack link, impact, expected vs actual, repro, technical pointers (paths), testing notes -- but only **after** he asked for the ticket.

---

## Additional context

- **JIRA project (suggested default):** `https://your-company.atlassian.net/jira/software/c/projects/<YOUR_PROJECT_KEY>/`
- **cloudId:** `<YOUR_CLOUD_ID>`
- Prioritize customer impact and clear next steps for Dimitris, Support, and Engineering.

---

## Quick Reference

**Slack URL format:**
```
https://your-company.slack.com/archives/{CHANNEL_ID}/p{TIMESTAMP}
```

**Parse to:**

- `channel_id`: segment after `/archives/` (e.g. C01B64CGVF1)
- `thread_ts`: from `p{TIMESTAMP}` -- first 10 digits = Unix seconds, remainder (usually 6 digits) after a dot (e.g. `p1762285076339219` -> `1762285076.339219`)

**Common issue types (when filing Jira):**

- Bug: defects or unexpected behavior
- Story: new features or enhancements
- Support Issue: customer-reported problems

**Priority guidelines:**

- HIGH: onboarding, revenue, or core functionality at risk
- MEDIUM: UX pain, workarounds exist
- LOW: minor or edge cases
