# PM Copilot

This is my personal PM productivity system, built on [Cursor](https://cursor.com). If you are a coding agent, this repo is your onboarding document. Read it carefully -- it tells you who I am, how I work, and how to set yourself up to be useful from day one.

If you are a human reading this on GitHub: this repo shows the system I have built to work with. It is less a portfolio and more an operating manual.

---

## How I work with AI agents

I use Cursor as a thinking partner, not a writing assistant. That means:

- **I investigate before I act.** When something is broken or unclear, I want root cause analysis grounded in the codebase or a real data source -- not guesses.
- **I decide, you execute.** Never make code changes, file tickets, or send messages unless I have explicitly asked you to. Investigate and report; I will tell you what to do next.
- **I work in context.** Every session I will load relevant documents (@-mention files in chat). Use them. Do not answer from memory when source material is available.
- **I bias to action.** Push back on analysis paralysis. If I am overthinking, say so. Help me make a decision with what we have and move.
- **I want honesty.** Tell me what you actually think. If my plan has a hole, name it. I do not need encouragement -- I need clarity.

---

## System architecture

The system has four layers. Set them up in this order.

### Layer 1 -- Persona (`cursor/rules/pm-copilot.mdc`)

The always-on coaching rule. It defines my role, my goals, and how I expect you to behave as a coach and advisor. Adapt the `[YourCompany]` and company description placeholders before loading it.

This rule is always active. It shapes every session.

### Layer 2 -- Always-on rules (`cursor/rules/`)

Three additional rules that govern agent behavior in every session:

| Rule | What it enforces |
|------|-----------------|
| `slack-url-thread-and-verify.mdc` | When I paste a Slack URL: fetch the thread, then verify claims in the codebase |
| `no-code-without-ask.mdc` | Never edit code unless I explicitly ask -- investigate only by default |
| `no-curly-quotes.mdc` | ASCII punctuation only -- curly quotes break StrReplace tool calls |

Fill in the placeholders (`your-company.atlassian.net`, `<YOUR_CLOUD_ID>`, `src/<your-repo>/`, etc.) for your environment.

### Layer 3 -- On-demand commands (`cursor/commands/`)

Slash commands invoked when I need a specific workflow. They are self-contained -- each file describes exactly what to do when I invoke it.

| Command | When I use it |
|---------|--------------|
| `/enrich-fr` | I paste a feature request and want real customer evidence pulled from the support ticket |
| `/slack-to-jira` | I paste a Slack thread URL and want triage + optional Jira ticket |
| `/jira-url-codebase-triage` | I paste a Jira URL and want the behavior traced in the codebase (read-only) |
| `/document-feature-behavior` | I need a plain-language source-of-truth doc for a feature, written from the code |

### Layer 4 -- Knowledge base

Folders of context documents I load into sessions. They do not contain generic information -- they contain the specific company context (strategy, product behavior, feature requests, competitive research) that turns generic answers into grounded ones.

See the `PLACEHOLDER.md` in each folder for what belongs there and how it is used. Populate these as you build context.

---

## Setting up

### 1. Clone this repo
```bash
git clone https://github.com/powerfool/pm-copilot
```

### 2. Copy rules into your workspace
```bash
cp cursor/rules/*.mdc <your-workspace>/.cursor/rules/
```

### 3. Copy commands into your workspace
```bash
cp cursor/commands/*.md <your-workspace>/.cursor/commands/
```

### 4. Install the Freshdesk skill
```bash
mkdir -p ~/.cursor/skills/freshdesk-ticket
cp skills/freshdesk-ticket/SKILL.md ~/.cursor/skills/freshdesk-ticket/
```

### 5. Fill in the placeholders

In every rule and command, replace:

| Placeholder | Replace with |
|------------|-------------|
| `[YourCompany]` | Your company name |
| `your-company.atlassian.net` | Your Jira site |
| `<YOUR_CLOUD_ID>` | Your Atlassian cloud ID (from the Jira URL) |
| `<YOUR_PROJECT_KEY>` | Your default Jira project key |
| `your-company.slack.com` | Your Slack domain |
| `your-company.freshdesk.com` | Your Freshdesk domain |
| `<YOUR_WORKSPACE_PATH>` | Absolute path to your workspace root |
| `src/<your-repo>/` | Your actual repo names under `src/` |

### 6. Set up API credentials
```bash
cp scripts/.env.example scripts/.env
# edit scripts/.env with your Freshdesk and Productboard tokens
```

### 7. Start populating the knowledge base

Create the equivalent of `Company Knowledge/`, `ProductKnowledge/`, etc. for your new context. The more you load in, the more grounded the sessions become. Use the `PLACEHOLDER.md` files in each folder as a guide for what to create.

---

## Scripts

`scripts/productboard_fetch_notes.py` -- fetches Productboard notes to CSV, extracts linked Freshdesk ticket URLs, and strips HTML. Used to build feature request catalogs for roadmap research.

```bash
cd scripts
pip install -r requirements.txt
python productboard_fetch_notes.py --output notes.csv
```

---

## Philosophy

A few principles baked into the system design:

- **Source of truth over memory.** Always verify claims against the codebase, a ticket, or a document. Never rely on what the agent recalls from training.
- **PM-readable output by default.** Technical depth on request; plain-language first.
- **One question at a time.** When I need to make a decision, drive a dialogue -- do not dump all options at once.
- **Bias to shipping.** When I am stuck, help me identify the smallest thing I can do to move forward. Perfect is the enemy of useful.
- **Honest coaching over validation.** If my plan has a flaw, name it early. I would rather hear it from you than discover it in a stakeholder meeting.

