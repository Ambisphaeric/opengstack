#!/usr/bin/env node

/**
 * opengstack CLI - Install and manage AI workflow skills
 * Usage: opengstack [options]
 * Example: opengstack --install
 */

const fs = require('fs');
const path = require('path');

const PKG_DIR = path.dirname(__dirname);
const SKILLS_SOURCE = path.join(PKG_DIR, 'skills');

function getSkillDescription(skillName) {
 const skillPath = path.join(SKILLS_SOURCE, skillName, 'SKILL.md');
 if (!fs.existsSync(skillPath)) return '';
 
 const content = fs.readFileSync(skillPath, 'utf8');
 const match = content.match(/description:\s*\|?\s*([^\n]+)/);
 return match ? match[1].trim() : '';
}

function showHelp() {
 console.log(`
opengstack - AI Engineering Workflow Skills

Usage: opengstack [options]

Options:
 -h, --help Show this help message
 -l, --list List all available skills
 -i, --install Install skills to ~/.config/opencode/skills/,
 ~/.claude/skills/, and ~/.agents/skills/

In opencode/Claude, use /slash commands:
 /ship, /qa, /review, etc.
`);
}

function listSkills() {
 console.log('\nAvailable skills:\n');
 
 if (!fs.existsSync(SKILLS_SOURCE)) {
 console.error('❌ No skills/ folder found');
 process.exit(1);
 }
 
 fs.readdirSync(SKILLS_SOURCE).forEach(skillName => {
 const skillPath = path.join(SKILLS_SOURCE, skillName, 'SKILL.md');
 if (!fs.existsSync(skillPath)) return;
 
 const content = fs.readFileSync(skillPath, 'utf8');
 const match = content.match(/description:\s*\|?\s*([^\n]+)/);
 let description = '';
 if (match) {
 description = match[1].trim().substring(0, 60);
 if (description.length === 60) description += '...';
 }
 console.log(` ${skillName.padEnd(20)} ${description}`);
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

 // Check if skill exists in package
 const skillPath = path.join(SKILLS_SOURCE, command, 'SKILL.md');
 if (!fs.existsSync(skillPath)) {
 console.error(`Unknown command: ${command}`);
 console.error('Run "opengstack --help" for available commands');
 process.exit(1);
 }

 // Print instructions for using the skill
 console.log(`\n🎯 Skill: ${command}`);
 console.log(`📍 Location: ${skillPath}`);
 console.log(`\nTo use this skill in opencode/Claude, type:`);
 console.log(` /${command}\n`);
 console.log('The skill instructions will be loaded automatically.\n');
}

main();
