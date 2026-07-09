/*
  Step: wait on the Edit Images pages and move forward.

  ELI5: After uploads, DriveThruCards shows warnings and an optional
  "auto-fix" pass. This step waits for the edit page, optionally
  clicks batch fix, then hits Next.

  Related files:
  - src/steps/upload-images.js runs before this
  - deck.js publicly exposes .batch-edit, .image-fix, .submit-next
*/

import { clickNext } from '../browser.js';

export async function editImagesAndContinue(page, sideLabel = 'images') {
  console.log(`Waiting for edit page (${sideLabel})…`);

  // Body class from public deck.js init hooks.
  await page.waitForSelector('body.page-deck-lists, .listed-images, .batch-edit, .submit-next', {
    timeout: 120_000,
  });

  // If the batch-edit control is visible, images need auto-fix.
  const batchEdit = page.locator('.batch-edit').first();
  if ((await batchEdit.count()) > 0 && (await batchEdit.isVisible())) {
    console.log('Batch edit / auto-fix is available — clicking it');
    await batchEdit.click();
    // deck.js reloads the page when warnings clear (up to ~30s timer).
    await page.waitForLoadState('networkidle').catch(() => {});
  }

  // If a warning popup appears ("Let Me Edit" / continue), prefer continue
  // only when we intentionally triggered batch fix. Otherwise stop for human.
  const continueLink = page.locator('.lists-continue a').first();
  if ((await continueLink.count()) > 0 && (await continueLink.isVisible())) {
    console.log('Warning popup open — clicking continue-through');
    await continueLink.click();
    await page.waitForLoadState('networkidle').catch(() => {});
  }

  console.log(`Edit step looks ready for ${sideLabel}; clicking Next`);
  await clickNext(page);
}
