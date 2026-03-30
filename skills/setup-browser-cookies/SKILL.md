---
name: setup-browser-cookies
preamble-tier: 1
version: 1.0.0
description: |
 Import cookies from your real Chromium browser into the headless browse session.
 Opens an interactive picker UI where you select which cookie domains to import.
 Use before QA testing authenticated pages. Use when asked to "import cookies",
 "login to the site", or "authenticate the browser". (OpenGStack)
allowed-tools:
 - Bash
 - Read
 - AskUserQuestion
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

## Preamble (run first)

```bash
_UPD=$(~/.claude/skills/opengstack/bin/opengstack-update-check 2>/dev/null || .claude/skills/opengstack/bin/opengstack-update-check 2>/dev/null || true)
[ -n "$_UPD" ] && echo "$_UPD" || true
mkdir -p ~/.opengstack/sessions
touch ~/.opengstack/sessions/"$PPID"
_SESSIONS=$(find ~/.opengstack/sessions -mmin -120 -type f 2>/dev/null | wc -l | tr -d ' ')
find ~/.opengstack/sessions -mmin +120 -type f -exec rm {} + 2>/dev/null || true
_CONTRIB=$(~/.claude/skills/opengstack/bin/opengstack-config get OpenGStack_contributor 2>/dev/null || true)
_PROACTIVE=$(~/.claude/skills/opengstack/bin/opengstack-config get proactive 2>/dev/null || echo "true")
_PROACTIVE_PROMPTED=$([ -f ~/.opengstack/.proactive-prompted ] && echo "yes" || echo "no")
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
_SKILL_PREFIX=$(~/.claude/skills/opengstack/bin/opengstack-config get skill_prefix 2>/dev/null || echo "false")
echo "PROACTIVE: $_PROACTIVE"
echo "PROACTIVE_PROMPTED: $_PROACTIVE_PROMPTED"
echo "SKILL_PREFIX: $_SKILL_PREFIX"
source <(~/.claude/skills/opengstack/bin/opengstack-repo-mode 2>/dev/null) || true
REPO_MODE=${REPO_MODE:-unknown}
echo "REPO_MODE: $REPO_MODE"
_LAKE_SEEN=$([ -f ~/.opengstack/.completeness-intro-seen ] && echo "yes" || echo "no")
echo "LAKE_INTRO: $_LAKE_SEEN"
_TEL_START=$(date +%s)
_SESSION_ID="$$-$(date +%s)"
if [ "${_TEL:-off}" != "off" ]; then
fi
# zsh-compatible: use find instead of glob to avoid NOMATCH error
 if [ -f "$_PF" ]; then
 fi
 rm -f "$_PF" 2>/dev/null || true
 fi
 break
done
# Learnings count
eval "$(~/.claude/skills/opengstack/bin/opengstack-slug 2>/dev/null)" 2>/dev/null || true
_LEARN_FILE="${OPENGSTACK_HOME:-$HOME/.OpenGStack}/projects/${SLUG:-unknown}/learnings.jsonl"
if [ -f "$_LEARN_FILE" ]; then
 _LEARN_COUNT=$(wc -l < "$_LEARN_FILE" 2>/dev/null | tr -d ' ')
 echo "LEARNINGS: $_LEARN_COUNT entries loaded"
else
 echo "LEARNINGS: 0"
fi
# Check if CLAUDE.md has routing rules
_HAS_ROUTING="no"
if [ -f CLAUDE.md ] && grep -q "## Skill routing" CLAUDE.md 2>/dev/null; then
 _HAS_ROUTING="yes"
fi
_ROUTING_DECLINED=$(~/.claude/skills/opengstack/bin/opengstack-config get routing_declined 2>/dev/null || echo "false")
echo "HAS_ROUTING: $_HAS_ROUTING"
echo "ROUTING_DECLINED: $_ROUTING_DECLINED"
```

If `PROACTIVE` is `"false"`, do not proactively suggest opengstack skills AND do not
auto-invoke skills based on conversation context. Only run skills the user explicitly
types (e.g., /qa, /ship). If you would have auto-invoked a skill, instead briefly say:
"I think /skillname might help here — want me to run it?" and wait for confirmation.
The user opted out of proactive behavior.

If `SKILL_PREFIX` is `"true"`, the user has namespaced skill names. When suggesting
or invoking other opengstack skills, use the `/opengstack-` prefix (e.g., `/opengstack-qa` instead
of `/qa`, `/opengstack-ship` instead of `/ship`). Disk paths are unaffected — always use
`~/.claude/skills/opengstack/[skill-name]/SKILL.md` for reading skill files.

If output shows `UPGRADE_AVAILABLE <old> <new>`: read `~/.claude/skills/opengstack/opengstack-upgrade/SKILL.md` and follow the "Inline upgrade flow" (auto-upgrade if configured, otherwise AskUserQuestion with 4 options, write snooze state if declined). If `JUST_UPGRADED <from> <to>`: tell user "Running opengstack v{to} (just updated!)" and continue.

If `LAKE_INTRO` is `no`: Before continuing, introduce the Completeness Principle.
Tell the user: "opengstack follows the **Boil the Lake** principle — always do the complete
thing when AI makes the marginal cost near-zero. Read more: "
Then offer to open the essay in their default browser:

```bash
open 
touch ~/.opengstack/.completeness-intro-seen
```

Only run `open` if the user says yes. Always run `touch` to mark as seen. This only happens once.

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
```

Then commit the change: `git add CLAUDE.md && git commit -m "chore: add opengstack skill routing rules to CLAUDE.md"`

If B: run `~/.claude/skills/opengstack/bin/opengstack-config set routing_declined true`
Say "No problem. You can add routing rules later by running `opengstack-config set routing_declined false` and re-running any skill."

This only happens once per project. If `HAS_ROUTING` is `yes` or `ROUTING_DECLINED` is `true`, skip this entirely.

## Voice

**Tone:** direct, concrete, sharp, never corporate, never academic. Sound like a builder, not a consultant. Name the file, the function, the command. No filler, no throat-clearing.

**Writing rules:** No em dashes (use commas, periods, "..."). No AI vocabulary (delve, crucial, robust, comprehensive, nuanced, etc.). Short paragraphs. End with what to do.

The user always has context you don't. Cross-model agreement is a recommendation, not a decision — the user decides.

## Contributor Mode

If `_CONTRIB` is `true`: you are in **contributor mode**. At the end of each major workflow step, rate your opengstack experience 0-10. If not a 10 and there's an actionable bug or improvement — file a field report.

**File only:** opengstack tooling bugs where the input was reasonable but opengstack failed. **Skip:** user app bugs, network errors, auth failures on user's site.

**To file:** write `~/.opengstack/contributor-logs/{slug}.md`:
```
# {Title}
**What I tried:** {action} | **What happened:** {result} | **Rating:** {0-10}
## Repro
1. {step}
## What would make this a 10
{one sentence}
**Date:** {YYYY-MM-DD} | **Version:** {version} | **Skill:** /{skill}
```
Slug: lowercase hyphens, max 60 chars. Skip if exists. Max 3/session. File inline, don't stop.

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

Run this bash:

```bash
_TEL_END=$(date +%s)
_TEL_DUR=$(( _TEL_END - _TEL_START ))

## Plan Status Footer

When you are in plan mode and about to call ExitPlanMode:

1. Check if the plan file already has a `## opengstack REVIEW REPORT` section.
2. If it DOES — skip (a review skill already wrote a richer report).
3. If it does NOT — run this command:

\`\`\`bash
~/.claude/skills/opengstack/bin/opengstack-review-read
\`\`\`

Then write a `## opengstack REVIEW REPORT` section to the end of the plan file:

- If the output contains review entries (JSONL lines before `---CONFIG---`): format the
 standard report table with runs/status/findings per skill, same format as the review
 skills use.
- If the output is `NO_REVIEWS` or empty: write this placeholder table:

\`\`\`markdown
## opengstack REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | \`/plan-ceo-review\` | Scope & strategy | 0 | — | — |
| Codex Review | \`/codex review\` | Independent 2nd opinion | 0 | — | — |
| Eng Review | \`/plan-eng-review\` | Architecture & tests (required) | 0 | — | — |
| Design Review | \`/plan-design-review\` | UI/UX gaps | 0 | — | — |

**VERDICT:** NO REVIEWS YET — run \`/autoplan\` for full review pipeline, or individual reviews above.
\`\`\`

**PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one
file you are allowed to edit in plan mode. The plan file review report is part of the
plan's living status.

# Setup Browser Cookies

Import logged-in sessions from your real Chromium browser into the headless browse session.

## CDP mode check

First, check if browse is already connected to the user's real browser:
```bash
$B status 2>/dev/null | grep -q "Mode: cdp" && echo "CDP_MODE=true" || echo "CDP_MODE=false"
```
If `CDP_MODE=true`: tell the user "Not needed — you're connected to your real browser via CDP. Your cookies and sessions are already available." and stop. No cookie import needed.

## How it works

1. Find the browse binary
2. Run `cookie-import-browser` to detect installed browsers and open the picker UI
3. User selects which cookie domains to import in their browser
4. Cookies are decrypted and loaded into the Playwright session

## Steps

### 1. Find the browse binary

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
1. Tell the user: "opengstack browse needs a one-time build (~10 seconds). OK to proceed?" Then STOP and wait.
2. Run: `cd <SKILL_DIR> && ./setup`
3. If `bun` is not installed:
 ```bash
 if ! command -v bun >/dev/null 2>&1; then
 BUN_VERSION="1.3.10"
 BUN_INSTALL_SHA="bab8acfb046aac8c72407bdcce903957665d655d7acaa3e11c7c4616beae68dd"
 tmpfile=$(mktemp)
 curl -fsSL "https://bun.sh/install" -o "$tmpfile"
 actual_sha=$(shasum -a 256 "$tmpfile" | awk '{print $1}')
 if [ "$actual_sha" != "$BUN_INSTALL_SHA" ]; then
 echo "ERROR: bun install script checksum mismatch" >&2
 echo " expected: $BUN_INSTALL_SHA" >&2
 echo " got: $actual_sha" >&2
 rm "$tmpfile"; exit 1
 fi
 BUN_VERSION="$BUN_VERSION" bash "$tmpfile"
 rm "$tmpfile"
 fi
 ```

### 2. Open the cookie picker

```bash
$B cookie-import-browser
```

This auto-detects installed Chromium browsers and opens
an interactive picker UI in your default browser where you can:
- Switch between installed browsers
- Search domains
- Click "+" to import a domain's cookies
- Click trash to remove imported cookies

Tell the user: **"Cookie picker opened — select the domains you want to import in your browser, then tell me when you're done."**

### 3. Direct import (alternative)

If the user specifies a domain directly (e.g., `/setup-browser-cookies github.com`), skip the UI:

```bash
$B cookie-import-browser comet --domain github.com
```

Replace `comet` with the appropriate browser if specified.

### 4. Verify

After the user confirms they're done:

```bash
$B cookies
```

Show the user a summary of imported cookies (domain counts).

## Notes

- On macOS, the first import per browser may trigger a Keychain dialog — click "Allow" / "Always Allow"
- On Linux, `v11` cookies may require `secret-tool`/libsecret access; `v10` cookies use Chromium's standard fallback key
- Cookie picker is served on the same port as the browse server (no extra process)
- Only domain names and cookie counts are shown in the UI — no cookie values are exposed
- The browse session persists cookies between commands, so imported cookies work immediately
