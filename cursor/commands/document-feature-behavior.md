# document-feature-behavior
This command will be available in chat with /document-feature-behavior

Create a source-of-truth document for a feature's behavior, edge cases, and design decisions. The user will tell you which feature to document and point you to the relevant repositories.

## Audience

**Support agents, PMs, and anyone explaining behavior to customers.** The document is written in plain language -- no code, no technical jargon. It explains *what* the system does and *why*, not *how* it is implemented.

## Your process

Follow these steps in order. Do not skip ahead.

### Step 1 -- Ask the user what to document
Ask the user:
1. What feature or feature area should be documented?
2. Which repositories contain the relevant code? (server, client, or both)
3. Are there any existing technical docs or specs to start from?

Then explore the codebase:
- Read existing technical docs in the repositories (e.g. `Technical_Documentation.md`, summaries, specs) for context.
- Use `Grep` and targeted `Read` calls to find: validation constants, service logic, enum values, edge case handling, UI constraints.
- Do not rely on UI descriptions alone -- the document's value is what is *not* obvious from the UI.

### Step 2 -- Propose the document structure
- Create the `.md` file with **section headings only**. No content yet.
- Present the structure to the user for review and ask them to confirm or adjust before filling anything in.
- Default location: workspace root (e.g. `feature-name-behavior-and-decisions.md`). Ask the user if they prefer a different path.

### Step 3 -- Fill sections one at a time
- Wait for the user to tell you which section(s) to fill next.
- Fill one section (or small group of subsections) at a time.
- After each fill, briefly confirm what was written and ask if the user wants changes before moving on.

### Step 4 -- Writing formula (apply to every section)
For each section you fill, cover these in order:
1. **What it does** -- plain English description of the behavior
2. **How it works** -- step-by-step if the behavior has multiple stages, no code references
3. **Edge cases** -- what happens when inputs are missing, invalid, out of range, or unexpected
4. **What support should tell customers** -- a ready-to-use explanation or Q&A pair

Not every section needs all four -- use judgment. A simple behavior may only need #1 and #3.

## Writing rules (always follow)

- No code snippets, class names, method names, or queue names in the output
- No passive voice like "it can be configured to..." -- be specific about what actually happens and what the defaults are
- Always document the *default* behavior when a setting is not configured
- For every limit or threshold (min, max, timeout): state the value, what error the user sees, and whether it fires at build time or runtime
- For every status or state: what it means, how to distinguish it from similar statuses, and whether it is actionable
- Cross-reference related sections (e.g. "see section 4.3") rather than repeating content
- Use tables for lists of limits, statuses, or options -- they are easier to scan than bullet lists
- Add **PM notes** (in blockquotes with italic text) when the user provides commentary on a decision -- these should read differently from the rest of the document

## Document structure template

Use this as a starting point. Adapt section names to fit the feature.

```
# [Feature Name] -- Behavior & Decisions (Source of Truth)

## 1. Document scope and audience
## 2. [Core model / terminology]
## 3. [Feature area 1]
  ### 3.1 What it does
  ### 3.2 [Key behavior]
  ### 3.3 Edge cases
## 4. [Feature area 2]
  ...
## N-1. Error handling and validation
## N. References and related docs
```
