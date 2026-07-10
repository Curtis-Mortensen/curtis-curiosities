/*
  Waiting helpers for DriveThruCards' slow server jobs.

  ELI5: Playwright does NOT have to "sleep for 10 minutes and hope."
  It can watch the webpage and only continue when something real
  changes — a new URL, a new button, a spinner going away. These
  helpers do that, and they print a heartbeat so you know it is
  still patiently waiting (color fix / sheet render / publish can
  each take around 10 minutes).

  Related files:
  - docs/plan-explainer.html explains this in plain language
  - src/steps/edit-images.js and export-pdf.js call these helpers
  - src/config.js holds the long timeout numbers
*/

import { config } from './config.js';

/**
 * Print "still waiting…" every heartbeat so a 10-minute job does not
 * look like a frozen script.
 */
function startHeartbeat(label, startedAt) {
  return setInterval(() => {
    const mins = ((Date.now() - startedAt) / 60_000).toFixed(1);
    console.log(
      `…still waiting for ${label} (${mins} min so far; DTC jobs often take ~10 min)`,
    );
  }, config.waitHeartbeatMs);
}

/**
 * Wait until the page URL changes in a way we care about.
 * Example: leaving /images/back/ and landing on an edit/lists URL.
 */
export async function waitForUrlChange(page, { match, label, timeoutMs } = {}) {
  const timeout = timeoutMs ?? config.longJobTimeoutMs;
  const startedAt = Date.now();
  const beat = startHeartbeat(label || 'URL change', startedAt);
  try {
    if (typeof match === 'function') {
      await page.waitForURL(match, { timeout });
    } else if (match instanceof RegExp) {
      await page.waitForURL(match, { timeout });
    } else if (typeof match === 'string') {
      await page.waitForURL((url) => url.href.includes(match), { timeout });
    } else {
      // Any navigation away from the current URL.
      const from = page.url();
      await page.waitForURL((url) => url.href !== from, { timeout });
    }
    const mins = ((Date.now() - startedAt) / 60_000).toFixed(1);
    console.log(`OK — ${label || 'URL change'} after ${mins} min → ${page.url()}`);
  } finally {
    clearInterval(beat);
  }
}

/**
 * Wait until a selector appears (page "shifted" into a new UI state).
 */
export async function waitForSelectorAppear(page, selector, { label, timeoutMs, state = 'visible' } = {}) {
  const timeout = timeoutMs ?? config.longJobTimeoutMs;
  const startedAt = Date.now();
  const beat = startHeartbeat(label || selector, startedAt);
  try {
    await page.locator(selector).first().waitFor({ state, timeout });
    const mins = ((Date.now() - startedAt) / 60_000).toFixed(1);
    console.log(`OK — saw ${label || selector} after ${mins} min`);
  } finally {
    clearInterval(beat);
  }
}

/**
 * Wait until busy/loading UI goes away (spinners, block overlays, "please wait").
 * If none of the busy selectors exist, returns quickly — that is fine.
 *
 * Each selector is checked on its own. We cannot join CSS and text= engines
 * into one comma list reliably in Playwright.
 */
export async function waitForBusyToClear(page, { label = 'busy UI to clear', timeoutMs } = {}) {
  const timeout = timeoutMs ?? config.longJobTimeoutMs;
  const deadline = Date.now() + timeout;

  // Soft poll: give overlays a moment to appear after a click.
  await page.waitForTimeout(500);

  const anyBusyVisible = async () => {
    for (const sel of config.busySelectors) {
      const loc = page.locator(sel);
      const n = await loc.count();
      for (let i = 0; i < n; i += 1) {
        if (await loc.nth(i).isVisible().catch(() => false)) return true;
      }
    }
    return false;
  };

  if (!(await anyBusyVisible())) {
    console.log(`No busy indicators found for "${label}" — continuing`);
    return;
  }

  const startedAt = Date.now();
  const beat = startHeartbeat(label, startedAt);
  try {
    while (Date.now() < deadline) {
      if (!(await anyBusyVisible())) {
        const mins = ((Date.now() - startedAt) / 60_000).toFixed(1);
        console.log(`OK — ${label} after ${mins} min`);
        return;
      }
      await page.waitForTimeout(2_000);
    }
    throw new Error(`Timed out waiting for ${label} (${Math.round(timeout / 60_000)} min)`);
  } finally {
    clearInterval(beat);
  }
}

/**
 * After clicking something that starts a long DTC job:
 * 1) optionally notice busy UI
 * 2) wait for a success signal (selector and/or URL match)
 *
 * This is the main "detect when the webpage shifts" entry point.
 */
export async function waitForPageShift(page, {
  label,
  successSelector,
  urlMatch,
  timeoutMs,
  alsoWaitForBusyClear = true,
} = {}) {
  const timeout = timeoutMs ?? config.longJobTimeoutMs;
  console.log(`Waiting for page shift: ${label} (timeout ${Math.round(timeout / 60_000)} min)`);

  if (alsoWaitForBusyClear) {
    // Soft: busy UI may appear a moment after the click.
    await page.waitForTimeout(1_000);
    await waitForBusyToClear(page, { label: `${label} (busy clear)`, timeoutMs: timeout });
  }

  if (urlMatch) {
    await waitForUrlChange(page, { match: urlMatch, label: `${label} (URL)`, timeoutMs: timeout });
  }

  if (successSelector) {
    await waitForSelectorAppear(page, successSelector, {
      label: `${label} (UI)`,
      timeoutMs: timeout,
    });
  }
}
