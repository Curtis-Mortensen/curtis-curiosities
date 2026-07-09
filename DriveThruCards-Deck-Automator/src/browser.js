/*
  Shared Playwright browser helpers.

  ELI5: Opens Chromium with your saved login cookie jar, and gives
  other step files a page they can click around on.

  Related files:
  - scripts/auth-save.js creates the cookie jar
  - src/run-batch.js is the main caller
*/

import fs from 'node:fs';
import { chromium } from 'playwright';
import { config } from './config.js';

export async function launchAuthedBrowser(options = {}) {
  if (!fs.existsSync(config.authStatePath)) {
    throw new Error(
      `Missing ${config.authStatePath}. Run: npm run auth:save`,
    );
  }

  const browser = await chromium.launch({
    headless: options.headless ?? config.headless,
    slowMo: options.slowMoMs ?? config.slowMoMs,
  });

  const context = await browser.newContext({
    storageState: config.authStatePath,
    acceptDownloads: true,
  });
  context.setDefaultTimeout(config.navigationTimeoutMs);

  const page = await context.newPage();
  return { browser, context, page };
}

export async function clickNext(page) {
  // The builder shows red "Next »" controls; class names vary by step.
  const next = page.locator('.submit-next, a:has-text("Next"), button:has-text("Next")').first();
  await next.click();
}

export async function clickBack(page) {
  const back = page.locator('a:has-text("Back"), button:has-text("Back")').first();
  await back.click();
}
