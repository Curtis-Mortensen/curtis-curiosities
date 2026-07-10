/*
  Shared Playwright browser helpers.

  ELI5: Opens YOUR installed Microsoft Edge in a normal window you can
  watch. It reuses a dedicated Edge profile folder so you can log in
  once and stay logged in. No invisible "headless" browser.

  Related files:
  - scripts/auth-save.js opens the same Edge profile for first login
  - src/run-batch.js is the main caller
  - src/waits.js handles the long "please wait" server jobs
*/

import fs from 'node:fs';
import { chromium } from 'playwright';
import { config } from './config.js';

/**
 * Launch headed Microsoft Edge with a persistent profile directory.
 * Returns { context, page, close } — persistent context has no separate browser object.
 */
export async function launchAuthedBrowser(options = {}) {
  fs.mkdirSync(config.edgeProfileDir, { recursive: true });

  const headless = options.headless ?? config.headless;
  if (headless) {
    console.warn('Headless mode is off by default so you can watch Edge. Proceeding anyway…');
  }

  // channel: 'msedge' = the Edge you already have installed on the machine.
  // launchPersistentContext = real profile folder (cookies, login) on disk.
  const context = await chromium.launchPersistentContext(config.edgeProfileDir, {
    channel: config.browserChannel,
    headless,
    slowMo: options.slowMoMs ?? config.slowMoMs,
    acceptDownloads: true,
    // null viewport = use the real window size (easier to watch).
    viewport: null,
  });

  context.setDefaultTimeout(config.navigationTimeoutMs);
  // Long server jobs (color fix / PDF render / publish) need a bigger ceiling.
  context.setDefaultNavigationTimeout(config.longJobTimeoutMs);

  const page = context.pages()[0] || (await context.newPage());

  return {
    context,
    page,
    async close() {
      await context.close();
    },
  };
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
