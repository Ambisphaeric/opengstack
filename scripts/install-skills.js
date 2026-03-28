#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const SKILLS_DIRS = [
  path.join(process.env.HOME || process.env.USERPROFILE, '.claude', 'skills'),
  path.join(process.env.HOME || process.env.USERPROFILE, '.config', 'opencode', 'skills')
];
const PKG_DIR = path.dirname(__dirname);

// List of skill directories
const skills = [
  'autoplan', 'benchmark', 'browse', 'canary', 'careful', 'codex',
  'connect-chrome', 'cso', 'design-consultation', 'design-review',
  'design-shotgun', 'document-release', 'freeze', 'gstack-upgrade',
  'guard', 'investigate', 'land-and-deploy', 'office-hours',
  'plan-ceo-review', 'plan-design-review', 'plan-eng-review',
  'qa', 'qa-only', 'retro', 'review', 'setup-browser-cookies',
  'setup-deploy', 'ship', 'unfreeze'
];

console.log('🔗 Installing OpenGStack skills...');

// Install to all skill directories
for (const SKILLS_DIR of SKILLS_DIRS) {
  console.log(`\n📁 Installing to ${SKILLS_DIR}...`);
  
  // Ensure skills directory exists
  if (!fs.existsSync(SKILLS_DIR)) {
    fs.mkdirSync(SKILLS_DIR, { recursive: true });
  }

  // Create symlinks for each skill
  let installed = 0;
  let skipped = 0;

  for (const skill of skills) {
    const srcPath = path.join(PKG_DIR, skill);
    const destPath = path.join(SKILLS_DIR, skill);

    if (!fs.existsSync(srcPath)) {
      console.warn(`⚠️  Skill not found: ${skill}`);
      skipped++;
      continue;
    }

    try {
      // Remove existing if it's a symlink
      if (fs.existsSync(destPath)) {
        const stat = fs.lstatSync(destPath);
        if (stat.isSymbolicLink()) {
          fs.unlinkSync(destPath);
        } else {
          console.log(`⏭️  Skipping ${skill} (already exists)`);
          skipped++;
          continue;
        }
      }

      // Create symlink
      fs.symlinkSync(srcPath, destPath, 'dir');
      console.log(`✓ ${skill}`);
      installed++;
    } catch (err) {
      console.error(`✗ ${skill}: ${err.message}`);
      skipped++;
    }
  }

  console.log(`\n✅ Installed ${installed} skills, skipped ${skipped}`);
}

console.log('\n🎯 Skills are now available in opencode/Claude');
