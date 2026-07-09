/*
  Step: finish the export page — download PDF or publish a product.

  ELI5: After assemble, you choose download, make a new product, or
  update one. Rendering the sheet and publishing each took ~10 minutes
  in real testing. Playwright waits for the page to shift (new URL,
  success text, or a download) instead of guessing with a fixed sleep.

  Related files:
  - src/waits.js explains / implements page-shift waiting
  - src/run-batch.js passes --mode download | make | update
  - deck.js shows next_step values: make | update | download
*/

import path from 'node:path';
import { config } from '../config.js';
import { waitForBusyToClear, waitForPageShift, waitForSelectorAppear } from '../waits.js';

export async function exportPdf(page, outputDir, options = {}) {
  const mode = options.mode ?? 'download';

  await waitForSelectorAppear(
    page,
    'body.page-deck-export, input[name="next_step"], .content',
    { label: 'export page', timeoutMs: config.navigationTimeoutMs },
  );

  const radio = page.locator(`input[name="next_step"][value="${mode}"]`);
  if ((await radio.count()) > 0) {
    await radio.check();
    console.log(`Selected next_step=${mode}`);
  } else {
    console.log('next_step radios not found — continuing with whatever the page defaults to');
  }

  // Product name only matters for make/update; fill if present.
  if ((mode === 'make' || mode === 'update') && options.productName) {
    const nameField = page
      .locator('.textfield-wrapper-new_product input, input[name*="new_product"]')
      .first();
    if ((await nameField.count()) > 0) {
      await nameField.fill(options.productName);
    }
  }

  const submit = page
    .locator('input[type="submit"], button[type="submit"], a:has-text("Download"), a:has-text("Publish")')
    .last();

  console.log(
    `Starting export mode="${mode}" — render/publish can take ~10 minutes. Watching Edge…`,
  );

  // For download mode, race a download event against a long page-shift wait.
  if (mode === 'download') {
    const downloadPromise = page
      .waitForEvent('download', { timeout: config.longJobTimeoutMs })
      .catch(() => null);

    await submit.click();
    await waitForBusyToClear(page, {
      label: 'sheet render / download busy clear',
      timeoutMs: config.longJobTimeoutMs,
    });

    const download = await downloadPromise;
    if (download) {
      const target = path.join(outputDir, download.suggestedFilename());
      await download.saveAs(target);
      console.log(`Saved PDF to ${target}`);
      return { mode, path: target };
    }

    console.log('No download event yet — looking for a PDF link on the result page');
    const link = page.locator('a[href*=".pdf"], a:has-text("Download")').first();
    await waitForSelectorAppear(page, 'a[href*=".pdf"], a:has-text("Download")', {
      label: 'PDF download link',
      timeoutMs: config.longJobTimeoutMs,
    });
    const [dl] = await Promise.all([
      page.waitForEvent('download', { timeout: config.longJobTimeoutMs }),
      link.click(),
    ]);
    const target = path.join(outputDir, dl.suggestedFilename());
    await dl.saveAs(target);
    console.log(`Saved PDF to ${target}`);
    return { mode, path: target };
  }

  // make / update (publish) — no file download required; wait for success UI.
  await submit.click();
  await waitForPageShift(page, {
    label: `publish (${mode})`,
    alsoWaitForBusyClear: true,
    successSelector: [
      'text=/success/i',
      'text=/published/i',
      'text=/complete/i',
      'text=/product/i',
      'a:has-text("Download")',
      'body.page-deck-export',
      'body.page-deck-index',
    ].join(', '),
    timeoutMs: config.longJobTimeoutMs,
  });

  console.log(`Publish/update flow finished (mode=${mode}). Check the Edge window for confirmation.`);
  return { mode, path: null, url: page.url() };
}
