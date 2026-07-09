/*
  One-time helper: open Microsoft Edge so you can log into DriveThruCards.

  ELI5: A real Edge window opens (the browser you already use). Log in
  as a partner. When you can see the deck tools, come back to the
  terminal and press Enter. Your login stays in auth/edge-profile/
  so later runs reuse the same Edge profile — you can watch it work.

  Related files:
  - auth/edge-profile/ is written here (gitignored)
  - src/browser.js opens that same profile for batch runs
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
  fs.mkdirSync(config.edgeProfileDir, { recursive: true });

  console.log(`Opening Microsoft Edge with profile:\n  ${config.edgeProfileDir}\n`);

  const context = await chromium.launchPersistentContext(config.edgeProfileDir, {
    channel: config.browserChannel,
    headless: false,
    slowMo: 50,
    viewport: null,
  });

  const page = context.pages()[0] || (await context.newPage());
  await page.goto(config.deckIndexUrl, { waitUntil: 'domcontentloaded' });

  console.log(`
Log in with your DriveThru partner account in the Edge window.
When you can see the deck builder / partner tools (not just a login popup),
return here.
`);
  await ask('Press Enter to keep this Edge profile and close the window… ');

  // Optional backup snapshot of cookies/localStorage (profile folder is the source of truth).
  fs.mkdirSync(path.dirname(config.authStatePath), { recursive: true });
  await context.storageState({ path: config.authStatePath });
  console.log(`Edge profile ready at ${config.edgeProfileDir}`);
  console.log(`Also wrote cookie snapshot to ${config.authStatePath}`);
  await context.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
