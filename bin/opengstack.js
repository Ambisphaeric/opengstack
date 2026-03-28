#!/usr/bin/env node

/**
 * OpenGStack CLI - Run skills directly from command line
 * Usage: opengstack <skill-name> [args...]
 * Example: opengstack ship
 */

const fs = require('fs');
const path = require('path');

const PKG_DIR = path.dirname(__dirname);
const SKILLS_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.claude', 'skills');

// Map of skill names to their directories
const skillMap = {
  'ship': 'ship',
  'qa': 'qa',
  'qa-only': 'qa-only',
  'review': 'review',
  'investigate': 'investigate',
  'design-review': 'design-review',
  'plan-ceo-review': 'plan-ceo-review',
  'plan-eng-review': 'plan-eng-review',
  'plan-design-review': 'plan-design-review',
  'office-hours': 'office-hours',
  'design-consultation': 'design-consultation',
  'design-shotgun': 'design-shotgun',
  'document-release': 'document-release',
  'retro': 'retro',
  'browse': 'browse',
  'setup-browser-cookies': 'setup-browser-cookies',
  'setup-deploy': 'setup-deploy',
  'careful': 'careful',
  'freeze': 'freeze',
  'guard': 'guard',
  'unfreeze': 'unfreeze',
  'autoplan': 'autoplan',
  'codex': 'codex',
  'canary': 'canary',
  'benchmark': 'benchmark',
  'cso': 'cso',
  'connect-chrome': 'connect-chrome',
  'land-and-deploy': 'land-and-deploy',
  'gstack-upgrade': 'gstack-upgrade'
};

function showHelp() {
  console.log(`
OpenGStack - AI Engineering Workflow Skills

Usage: opengstack <command> [options]

Commands:
  ship              Ship workflow: test, review, push, PR
  qa                Open browser, find bugs, fix, verify
  qa-only           QA report only — no code changes
  review            Pre-landing PR review
  investigate       Root-cause debugging
  design-review     Design audit + fix loop
  plan-ceo-review   CEO-level strategic review
  plan-eng-review   Lock architecture & edge cases
  plan-design-review Rate design decisions 0-10
  office-hours      Brainstorm before building
  design-consultation Build a design system from scratch
  design-shotgun    Generate multiple AI design variants
  document-release  Update docs post-ship
  retro             Weekly engineering retrospective
  browse            Headless browser (real Chromium)
  setup-browser-cookies Import cookies for auth testing
  setup-deploy      Configure deployment settings
  careful           Warn before destructive ops
  freeze            Lock edits to one directory
  guard             Activate careful + freeze
  unfreeze          Remove directory restrictions
  autoplan          Run all reviews auto-decisioned
  codex             OpenAI Codex CLI wrapper
  canary            Post-deploy monitoring
  benchmark         Performance regression detection
  cso               Security audit
  connect-chrome    Launch Chrome with Side Panel
  land-and-deploy   Merge PR, deploy, verify health
  gstack-upgrade    Upgrade gstack to latest version

Options:
  -h, --help        Show this help message
  -l, --list        List all available skills
  -i, --install     Install skills to ~/.claude/skills/

In opencode/Claude, use /slash commands:
  /ship, /qa, /review, etc.
`);
}

function listSkills() {
  console.log('\nAvailable skills:\n');
  Object.entries(skillMap).forEach(([cmd, dir]) => {
    const skillPath = path.join(SKILLS_DIR, dir, 'SKILL.md');
    let description = '';
    if (fs.existsSync(skillPath)) {
      const content = fs.readFileSync(skillPath, 'utf8');
      const match = content.match(/description:\s*\|?\s*([^\n]+)/);
      if (match) {
        description = match[1].trim().substring(0, 60);
        if (description.length === 60) description += '...';
      }
    }
    console.log(`  ${cmd.padEnd(20)} ${description}`);
  });
  console.log('');
}

function installSkills() {
  console.log('Installing skills...');
  require('../scripts/install-skills.js');
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '-h' || command === '--help') {
    showHelp();
    process.exit(0);
  }

  if (command === '-l' || command === '--list') {
    listSkills();
    process.exit(0);
  }

  if (command === '-i' || command === '--install') {
    installSkills();
    process.exit(0);
  }

  const skillDir = skillMap[command];
  if (!skillDir) {
    console.error(`Unknown command: ${command}`);
    console.error('Run "opengstack --help" for available commands');
    process.exit(1);
  }

  // Check if skill is installed
  const skillPath = path.join(SKILLS_DIR, skillDir, 'SKILL.md');
  if (!fs.existsSync(skillPath)) {
    console.error(`Skill "${command}" not installed.`);
    console.error('Run: opengstack --install');
    process.exit(1);
  }

  // Print instructions for using the skill
  console.log(`\n🎯 Skill: ${command}`);
  console.log(`📍 Location: ${skillPath}`);
  console.log(`\nTo use this skill in opencode/Claude, type:`);
  console.log(`  /${command}\n`);
  console.log('The skill instructions will be loaded automatically.\n');
}

main();
