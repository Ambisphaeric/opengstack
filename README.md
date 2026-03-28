# OpenGStack

> **npm:** `npm install github:Ambisphaeric/opengstack`

Open source engineering workflow skills for AI coding assistants. No telemetry, no tracking.

Forked from [garrytan/gstack](https://github.com/garrytan/gstack) with telemetry and YC references removed.

## What is this?

Skills that give AI agents structured roles for software development. Each skill is a specialist: CEO reviewer, eng manager, designer, QA lead, release engineer, debugger, and more.

## Available Skills

| Skill | What it does |
|-------|--------------|
| `/office-hours` | Brainstorm your product idea before you write code. |
| `/plan-ceo-review` | CEO-level review: find the 10-star product in the request. |
| `/plan-eng-review` | Lock architecture, data flow, edge cases, and tests. |
| `/plan-design-review` | Rate each design dimension 0-10, explain what a 10 looks like. |
| `/design-consultation` | Build a complete design system from scratch. |
| `/design-review` | Design audit + fix loop with atomic commits. |
| `/review` | Pre-landing PR review. Finds bugs that pass CI but break in prod. |
| `/investigate` | Systematic root-cause debugging. |
| `/qa` | Open a real browser, find bugs, fix them, re-verify. |
| `/qa-only` | Same as /qa but report only — no code changes. |
| `/ship` | Run tests, review, push, open PR. One command. |
| `/land-and-deploy` | Merge PR, deploy, verify health. |
| `/document-release` | Update all docs to match what you just shipped. |
| `/retro` | Weekly retro with per-person breakdowns and shipping streaks. |
| `/browse` | Headless browser — real Chromium, real clicks, ~100ms/command. |
| `/setup-browser-cookies` | Import cookies from your real browser for authenticated testing. |
| `/careful` | Warn before destructive commands (rm -rf, DROP TABLE, force-push). |
| `/freeze` | Lock edits to one directory. Hard block, not just a warning. |
| `/guard` | Activate both careful + freeze at once. |
| `/unfreeze` | Remove directory edit restrictions. |
| `/autoplan` | Run all reviews sequentially with auto-decisions. |
| `/codex` | OpenAI Codex CLI wrapper for code review. |
| `/canary` | Post-deploy monitoring. |
| `/benchmark` | Performance regression detection. |
| `/cso` | Security audit. |

## Installation

### npm (recommended)

```bash
npm install github:Ambisphaeric/opengstack
```

Then copy skills to your AI assistant's skills directory:

```bash
cp -r node_modules/opengstack/* ~/.claude/skills/opengstack/
```

### Git clone

```bash
git clone https://github.com/Ambisphaeric/opengstack.git ~/.claude/skills/opengstack
```

### Browse Setup (optional)

```bash
cd ~/.claude/skills/opengstack/browse
./setup
```

Requires `bun`: `curl -fsSL https://bun.sh/install | bash`

## No Telemetry

This fork removes all telemetry, analytics, and tracking from the original gstack. Your usage data stays on your machine.

## Syncing from Upstream

This repo auto-syncs hourly from `garrytan/gstack` via GitHub Actions. Filters are applied to remove telemetry and YC references.

To sync manually:

```bash
git remote add upstream https://github.com/garrytan/gstack.git
git fetch upstream main
git merge upstream/main
./scripts/filter_skills.py .
./scripts/cleanup.py .
git commit -m "chore: sync from upstream"
```

## License

MIT
