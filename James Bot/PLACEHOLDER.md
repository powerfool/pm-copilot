# James Bot

This folder runs your competitive intelligence system. Set it up once, then run it on a regular cadence to stay ahead of what competitors are shipping.

## What belongs here

- **intel-brief-prompt.md** -- the prompt used to generate periodic competitive integration briefs; structure it to cover new integrations, partnership announcements, API changes, and strategic signals from competitors
- **intel-source-registry.md** -- the curated list of sources to monitor: competitor changelog pages, product blogs, release notes, app marketplace listings, and community forums; update it as you discover new sources

## How to use it

On a weekly or bi-weekly cadence, feed the source registry to the agent along with the brief prompt to produce a competitive intel digest. Use the output to:

- Inform roadmap prioritization discussions
- Answer customer questions like "does [competitor] support X?"
- Spot feature parity gaps before they become a retention issue

## Getting started

1. Create `intel-source-registry.md` -- list the 5-10 most important competitor pages to watch (changelog, blog, integrations marketplace)
2. Create `intel-brief-prompt.md` -- define the output format you want (e.g. new integrations, removed features, pricing changes, strategic signals)
3. Run a session: "@James Bot/intel-source-registry.md -- generate this week's integration intel brief using @James Bot/intel-brief-prompt.md"

The name "James" is a reference to having a dedicated competitive intelligence analyst -- this folder is the AI-powered version.
