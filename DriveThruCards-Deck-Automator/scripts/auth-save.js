/*
  One-time helper: open the deck builder and save your login cookies.

  ELI5: A browser window opens. You log into DriveThruCards as a
  partner. When you are clearly logged in, come back to the terminal
  and press Enter. We save the session so other scripts can reuse it.

  Related files:
  - auth/storage-state.json is written here (gitignored)
  - src/browser.js reads that file on later runs
*/

import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { chromium } from 'playwright';
import { config } from '../src/config.js';

function ask(question) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

async function main() {
  fs.mkdirSync(path.dirname(config.authStatePath), { recursive: true });

  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('Opening deck builder login surface…');
  await page.goto(config.deckIndexUrl, { waitUntil: 'domcontentloaded' });

  console.log(`
Log in with your DriveThru partner account in the browser window.
When you can see the deck builder (not the login popup), return here.
`);
  await ask('Press Enter to save the session… ');

  await context.storageState({ path: config.authStatePath });
  console.log(`Saved login state to ${config.authStatePath}`);
  await browser.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
