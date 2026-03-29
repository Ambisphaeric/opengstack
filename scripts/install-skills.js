#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const SKILLS_SOURCE = path.join(__dirname, '..', 'skills');
const TARGET_DIRS = [
  path.join(os.homedir(), '.config', 'opencode', 'skills'),     // OpenCode native
  path.join(os.homedir(), '.claude', 'skills'),                 // Claude compat
  path.join(os.homedir(), '.agents', 'skills')                  // other agents
];

function copyDir(src, dest) {
  // Create destination directory (including parents)
  fs.mkdirSync(dest, { recursive: true });
  
  fs.readdirSync(src).forEach(item => {
    const srcPath = path.join(src, item);
    const destPath = path.join(dest, item);
    
    if (fs.statSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  });
}

function installSkills() {
  if (!fs.existsSync(SKILLS_SOURCE)) {
    console.error('❌ No skills/ folder found in package');
    process.exit(1);
  }

  TARGET_DIRS.forEach(target => {
    // Ensure parent directories exist
    fs.mkdirSync(target, { recursive: true });

    fs.readdirSync(SKILLS_SOURCE).forEach(skillName => {
      const src = path.join(SKILLS_SOURCE, skillName);
      const dest = path.join(target, skillName);

      // Skip if not a directory
      if (!fs.statSync(src).isDirectory()) return;

      if (fs.existsSync(dest)) {
        console.log(`⚠️  Skill ${skillName} already exists — skipping`);
        return;
      }

      copyDir(src, dest);
      console.log(`✅ Installed skill: /${skillName}`);
    });
  });

  console.log('\n🎉 Skills installed! Restart OpenCode (just quit and restart the TUI).');
  console.log('Now just type /qa directly — no /skills menu needed.');
}

installSkills();
