/*
  Step: finish the export page and download the print PDF.

  ELI5: After assemble, the builder asks whether to make a new product,
  update an existing one, or just download. For automation dry runs we
  pick "download" and save the PDF into output/.

  Related files:
  - src/run-batch.js creates the output folder
  - deck.js shows next_step values: make | update | download
*/

import path from 'node:path';

export async function exportPdf(page, outputDir, options = {}) {
  const mode = options.mode ?? 'download';

  await page.waitForSelector('body.page-deck-export, input[name="next_step"], .content', {
    timeout: 120_000,
  });

  const radio = page.locator(`input[name="next_step"][value="${mode}"]`);
  if ((await radio.count()) > 0) {
    await radio.check();
    console.log(`Selected next_step=${mode}`);
  } else {
    console.log('next_step radios not found — continuing with whatever the page defaults to');
  }

  // Product name only matters for make/update; fill if present.
  if (mode === 'make' && options.productName) {
    const nameField = page.locator('.textfield-wrapper-new_product input, input[name*="new_product"]').first();
    if ((await nameField.count()) > 0) {
      await nameField.fill(options.productName);
    }
  }

  // Click the final submit / download control and catch a download if any.
  const submit = page.locator('input[type="submit"], button[type="submit"], a:has-text("Download")').last();

  const downloadPromise = page.waitForEvent('download', { timeout: 180_000 }).catch(() => null);
  await submit.click();
  const download = await downloadPromise;

  if (!download) {
    console.log('No download event yet — PDF may be linked on the next page');
    // Try a direct download link if the page exposes one.
    const link = page.locator('a[href*=".pdf"], a:has-text("Download")').first();
    if ((await link.count()) > 0) {
      const [dl] = await Promise.all([
        page.waitForEvent('download', { timeout: 180_000 }),
        link.click(),
      ]);
      const target = path.join(outputDir, dl.suggestedFilename());
      await dl.saveAs(target);
      console.log(`Saved PDF to ${target}`);
      return target;
    }
    throw new Error('Could not capture a PDF download. Inspect the export page in headed mode.');
  }

  const target = path.join(outputDir, download.suggestedFilename());
  await download.saveAs(target);
  console.log(`Saved PDF to ${target}`);
  return target;
}
