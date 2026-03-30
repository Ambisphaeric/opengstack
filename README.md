# OpenGStack

AI engineering workflow skills for Claude/opencode. No telemetry. No tracking.

## Installation

```bash
npm install -g opengstack
```

Skills auto-install to `~/.claude/skills/` via symlink.

## CLI

```bash
opengstack --help # Show all commands
opengstack --list # List available skills
opengstack --install # Re-install skills (if needed)
```

## Usage

In opencode/Claude, type any skill name with `/`:

| Command | What it does |
|---------|--------------|
| `/office-hours` | Brainstorm before building |
| `/plan-ceo-review` | CEO-level strategic review |
| `/plan-eng-review` | Lock architecture & edge cases |
| `/plan-design-review` | Rate design decisions 0-10 |
| `/design-consultation` | Build a design system from scratch |
| `/design-shotgun` | Generate multiple design variants |
| `/design-html` | Production HTML with Pretext |
| `/design-review` | Design audit + fix loop |
| `/review` | Pre-landing PR review |
| `/investigate` | Root-cause debugging |
| `/qa` | Open browser, find bugs, fix, verify |
| `/qa-only` | QA report only — no code changes |
| `/ship` | Run tests, review, push, open PR |
| `/land-and-deploy` | Merge PR, deploy, verify health |
| `/document-release` | Update docs post-ship |
| `/retro` | Weekly engineering retrospective |
| `/browse` | Headless browser (real Chromium) |
| `/setup-browser-cookies` | Import cookies for auth testing |
| `/setup-deploy` | One-time deploy configurator |
| `/connect-chrome` | Launch Chrome with side panel |
| `/careful` | Warn before destructive ops |
| `/freeze` | Lock edits to one directory |
| `/guard` | Activate careful + freeze |
| `/unfreeze` | Remove directory restrictions |
| `/autoplan` | Run all reviews auto-decisioned |
| `/codex` | OpenAI Codex CLI wrapper |
| `/canary` | Post-deploy monitoring |
| `/benchmark` | Performance regression detection |
| `/cso` | Security audit |
| `/learn` | Manage project learnings |

## Why opengstack?

Forked from gstack with telemetry and vendor references removed. Your usage stays local.

## License

MIT
