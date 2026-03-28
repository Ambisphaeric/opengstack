---
name: opengstack
preamble-tier: 1
version: 1.0.0
description: |
  Open source engineering workflow skills for AI coding assistants. QA testing,
  code review, design review, planning, shipping, and more. Use when asked to
  test a site, review code, plan features, or ship to production.
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion

---

## Preamble

No telemetry. No tracking. Just skills.

## Voice

**Tone:** direct, concrete, sharp, never corporate, never academic. Sound like a builder, not a consultant. Name the file, the function, the command. No filler, no throat-clearing.

**Writing rules:** No em dashes (use commas, periods, "..."). No AI vocabulary (delve, crucial, robust, comprehensive, nuanced, etc.). Short paragraphs. End with what to do.

The user always has context you don't. Cross-model agreement is a recommendation, not a decision — the user decides.

## Completion Status Protocol

When completing a skill workflow, report status using one of:
- **DONE** — All steps completed successfully. Evidence provided for each claim.
- **DONE_WITH_CONCERNS** — Completed, but with issues the user should know about. List each concern.
- **BLOCKED** — Cannot proceed. State what is blocking and what was tried.
- **NEEDS_CONTEXT** — Missing information required to continue. State exactly what you need.

### Escalation

It is always OK to stop and say "this is too hard for me" or "I'm not confident in this result."

Bad work is worse than no work. You will not be penalized for escalating.
- If you have attempted a task 3 times without success, STOP and escalate.
- If you are uncertain about a security-sensitive change, STOP and escalate.
- If the scope of work exceeds what you can verify, STOP and escalate.

Escalation format:
```
STATUS: BLOCKED | NEEDS_CONTEXT
REASON: [1-2 sentences]
ATTEMPTED: [what you tried]
RECOMMENDATION: [what the user should do next]
```

## Plan Status Footer

When you are in plan mode and about to call ExitPlanMode, write a `## REVIEW REPORT` section to the end of the plan file:

```markdown
## REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | 0 | — | — |
| Codex Review | `/codex review` | Independent 2nd opinion | 0 | — | — |
| Eng Review | `/plan-eng-review` | Architecture & tests | 0 | — | — |
| Design Review | `/plan-design-review` | UI/UX gaps | 0 | — | — |

**VERDICT:** NO REVIEWS YET — run `/autoplan` for full review pipeline, or individual reviews above.
```

# browse: QA Testing & Dogfooding

Persistent headless Chromium. First call auto-starts (~3s), then ~100-200ms per command.
Auto-shuts down after 30 min idle. State persists between calls (cookies, tabs, sessions).

## SETUP (run this check BEFORE any browse command)

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
B=""
[ -n "$_ROOT" ] && [ -x "$_ROOT/.claude/skills/opengstack/browse/dist/browse" ] && B="$_ROOT/.claude/skills/opengstack/browse/dist/browse"
[ -z "$B" ] && B=~/.claude/skills/opengstack/browse/dist/browse
if [ -x "$B" ]; then
  echo "READY: $B"
else
  echo "NEEDS_SETUP"
fi
```

If `NEEDS_SETUP`:
1. Tell the user: "browse needs a one-time build (~10 seconds). OK to proceed?" Then STOP and wait.
2. Run: `cd ~/.claude/skills/opengstack/browse && ./setup`
3. If `bun` is not installed:
   ```bash
   if ! command -v bun >/dev/null 2>&1; then
     curl -fsSL https://bun.sh/install | bash
   fi
   ```

## IMPORTANT

- Use the compiled binary via Bash: `$B <command>`
- Browser persists between calls — cookies, login sessions, and tabs carry over.
- Dialogs (alert/confirm/prompt) are auto-accepted by default — no browser lockup.
- **Show screenshots:** After `$B screenshot`, `$B snapshot -a -o`, or `$B responsive`, always use the Read tool on the output PNG(s) so the user can see them.

## QA Workflows

> **Credential safety:** Use environment variables for test credentials.

### Test a user flow (login, signup, checkout, etc.)

```bash
# 1. Go to the page
$B goto https://app.example.com/login

# 2. See what's interactive
$B snapshot -i

# 3. Fill the form using refs
$B fill @e3 "$TEST_EMAIL"
$B fill @e4 "$TEST_PASSWORD"
$B click @e5

# 4. Verify it worked
$B snapshot -D
$B is visible ".dashboard"
$B screenshot /tmp/after-login.png
```

### Verify a deployment

```bash
$B goto https://yourapp.com
$B text
$B console
$B network
$B screenshot /tmp/prod-check.png
```

### Test responsive layouts

```bash
$B goto https://yourapp.com
$B responsive /tmp/layout
```

## Snapshot System

```
-i        --interactive           Interactive elements only with @e refs
-c        --compact               Compact tree
-d <N>    --depth                 Limit tree depth
-s <sel>  --selector             Scope to CSS selector
-D        --diff                  Diff against previous snapshot
-a        --annotate             Annotated screenshot with labels
-o <path> --output               Output path for annotated screenshot
-C        --cursor-interactive   Cursor-interactive @c refs
```

## Command Reference

### Navigation
| Command | Description |
|---------|-------------|
| `goto <url>` | Navigate to URL |
| `back` | History back |
| `forward` | History forward |
| `reload` | Reload page |
| `url` | Print current URL |

### Reading
| Command | Description |
|---------|-------------|
| `accessibility` | Full ARIA tree |
| `forms` | Form fields as JSON |
| `html [selector]` | innerHTML |
| `links` | All links |
| `text` | Cleaned page text |

### Interaction
| Command | Description |
|---------|-------------|
| `click <sel>` | Click element |
| `fill <sel> <val>` | Fill input |
| `hover <sel>` | Hover element |
| `press <key>` | Press key |
| `scroll [sel]` | Scroll element into view |
| `select <sel> <val>` | Select dropdown option |
| `upload <sel> <file>` | Upload file |
| `viewport <WxH>` | Set viewport size |
| `wait <sel|--networkidle|--load>` | Wait for condition |

### Inspection
| Command | Description |
|---------|-------------|
| `attrs <sel>` | Element attributes as JSON |
| `console [--errors]` | Console messages |
| `cookies` | All cookies |
| `css <sel> <prop>` | Computed CSS value |
| `is <prop> <sel>` | State check (visible/hidden/enabled/disabled) |
| `js <expr>` | Run JavaScript expression |
| `network` | Network requests |
| `storage [set k v]` | localStorage/sessionStorage |

### Visual
| Command | Description |
|---------|-------------|
| `diff <url1> <url2>` | Text diff between pages |
| `pdf [path]` | Save as PDF |
| `responsive [prefix]` | Screenshots at mobile/tablet/desktop |
| `screenshot [--viewport] [selector] [path]` | Save screenshot |

### Snapshot
| Command | Description |
|---------|-------------|
| `snapshot [flags]` | Accessibility tree with @e refs |

### Tabs
| Command | Description |
|---------|-------------|
| `newtab [url]` | Open new tab |
| `closetab [id]` | Close tab |
| `tab <id>` | Switch to tab |
| `tabs` | List open tabs |

### Server
| Command | Description |
|---------|-------------|
| `connect` | Launch headed browser with extension |
| `disconnect` | Return to headless mode |
| `status` | Health check |
| `stop` | Shutdown server |
| `restart` | Restart server |
