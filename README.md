# PM Copilot

A personal productivity system built on top of [Cursor](https://cursor.com) to manage my work as a Product Manager on an Integrations team. It combines AI personas, slash commands, reusable rules, and scripts into a cohesive daily workflow.

## What this is

Over time I found myself repeating the same PM workflows: triaging support tickets, enriching feature requests, triage from Slack threads, analyzing product behavior from code. This repo captures the automation layer I built to do those faster and better.

It is not a generic framework -- it was built for my specific context. But the patterns, commands, and rules are all reusable and the structure can be adapted to any PM working in a product+engineering environment.

---

## System components

### `cursor/rules/`
Always-on Cursor rules that shape how the AI agent behaves in every session.

| Rule | Purpose |
|------|---------|
| `pm-copilot.mdc` | PM coaching persona: goals, coaching style, bias to action |
| `jira-mcp-fast-path.mdc` | Default Jira MCP configuration for fast ticket creation and retrieval |
| `slack-url-thread-and-verify.mdc` | Fetch a Slack thread, summarize it, then verify claims in the codebase |
| `git-repos-under-src.mdc` | Workspace layout: git repos live under `src/`, not the root |
| `no-code-without-ask.mdc` | Never change code unless explicitly asked -- investigation only by default |
| `no-curly-quotes.mdc` | ASCII punctuation only to prevent tool-call failures |

### `cursor/commands/`
Slash commands invoked on demand for specific PM workflows.

| Command | What it does |
|---------|-------------|
| `enrich-fr.md` | Pull a Freshdesk ticket and enrich a feature request entry with real customer evidence |
| `slack-to-jira.md` | Take a Slack thread URL, triage the issue, draft a Jira ticket |
| `jira-url-codebase-triage.md` | Take a Jira URL, trace the related behavior in the codebase (read-only) |
| `document-feature-behavior.md` | Generate a plain-language feature behavior doc from code |
| `debug-webhook-ticket.md` | Debug a webhook or automation issue from a Freshdesk ticket |
| `school-automation-analysis.md` | Analyze a school's automation JSON export to understand their setup |
| `extract-automation-use-cases.md` | Extract automation use cases from a customer analysis into a research catalog |
| `thought-partner.md` | Creative coaching session -- challenge assumptions, find paradoxes, generate options |

### `skills/freshdesk-ticket/`
An agent skill that auto-triggers on any Freshdesk ticket URL. Fetches the full ticket and conversation thread, summarizes the issue, and optionally verifies product behavior against the codebase.

### `scripts/`
Python tooling for research pipelines.

| Script | What it does |
|--------|-------------|
| `productboard_fetch_notes.py` | Fetches Productboard notes to CSV with Freshdesk URL extraction for FR research |
| `.env.example` | Template for required API credentials |

---

## Knowledge base structure

The repo preserves the folder structure of the knowledge base I maintained alongside this tooling. The actual documents are not included (company-confidential), but placeholders describe what each folder held.

- `Company Knowledge/` -- strategy docs, segment analyses, feature request catalogs, competitive research
- `changelog/` -- integration team release notes
- `ProductKnowledge/` -- code-derived product behavior references for LLM grounding
- `James Bot/` -- competitive intelligence prompts and source registry
- `docs/` -- PM how-to guides for using the commands

---

## How to adapt this

1. Copy `cursor/rules/` into your workspace's `.cursor/rules/` folder
2. Copy `cursor/commands/` into `.cursor/commands/`
3. Drop `skills/freshdesk-ticket/SKILL.md` into `~/.cursor/skills/freshdesk-ticket/`
4. Update the placeholders in the rules (`[YourCompany]`, `your-company.atlassian.net`, etc.) to match your environment
5. Run `scripts/productboard_fetch_notes.py` with your own API credentials (see `.env.example`)

---

## Author

Dimitris Tzortzis -- Senior Product Manager, Integrations
