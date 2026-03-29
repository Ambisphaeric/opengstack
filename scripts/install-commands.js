#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const os = require('os');

const COMMANDS_SOURCE = path.join(__dirname, '..', 'commands');
const TARGET_DIR = path.join(os.homedir(), '.config', 'opencode', 'commands');

function installCommands() {
  if (!fs.existsSync(COMMANDS_SOURCE)) {
    console.error('❌ No commands/ folder found in package');
    process.exit(1);
  }

  if (!fs.existsSync(TARGET_DIR)) {
    fs.mkdirSync(TARGET_DIR, { recursive: true });
  }

  let installed = 0;
  fs.readdirSync(COMMANDS_SOURCE).forEach(file => {
    if (!file.endsWith('.md')) return;

    const commandName = path.basename(file, '.md');
    const src = path.join(COMMANDS_SOURCE, file);
    const dest = path.join(TARGET_DIR, file);

    if (fs.existsSync(dest)) {
      console.log(`⚠️  /${commandName} already exists — skipping`);
      return;
    }

    fs.copyFileSync(src, dest);
    console.log(`✅ Installed native slash command: /${commandName}`);
    installed++;
  });

  if (installed === 0) {
    console.log('⚠️  No new commands installed (they already exist)');
  } else {
    console.log(`\n🎉 ${installed} native commands installed!`);
    console.log('Restart OpenCode → just type /qa directly (no /skills menu)');
  }
}

installCommands();
