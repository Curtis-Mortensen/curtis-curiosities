/*
  Step: wait on the Edit Images pages and move forward.

  ELI5: After uploads, DriveThruCards may offer to auto-correct colors.
  That job can take around 10 minutes. We do NOT sleep blindly — we
  watch for busy UI to clear and for the edit page to look ready, with
  a heartbeat printed every 30 seconds so you know Edge is still waiting.

  Related files:
  - src/waits.js = the "detect when the page shifts" helpers
  - src/steps/upload-images.js runs before this
  - deck.js publicly exposes .batch-edit, .image-fix, .submit-next
*/

import { clickNext } from '../browser.js';
import { waitForBusyToClear, waitForPageShift, waitForSelectorAppear } from '../waits.js';
import { config } from '../config.js';

export async function editImagesAndContinue(page, sideLabel = 'images') {
  console.log(`Waiting for edit page (${sideLabel})…`);

  // Body class from public deck.js init hooks.
  await waitForSelectorAppear(
    page,
    'body.page-deck-lists, .listed-images, .batch-edit, .submit-next',
    { label: `edit page for ${sideLabel}`, timeoutMs: config.longJobTimeoutMs },
  );

  // If the batch-edit control is visible, images need auto-fix / color correct.
  const batchEdit = page.locator('.batch-edit').first();
  if ((await batchEdit.count()) > 0 && (await batchEdit.isVisible())) {
    console.log(
      'Batch edit / auto-correct is available — clicking it (may take ~10 minutes)',
    );
    await batchEdit.click();

    // deck.js may reload when warnings clear. Wait for busy UI + warnings gone.
    await waitForPageShift(page, {
      label: `auto-correct colors (${sideLabel})`,
      alsoWaitForBusyClear: true,
      // Success = no more .image-fix rows, or page reloaded into a clean list.
      successSelector: 'body.page-deck-lists, .listed-images, .submit-next',
      timeoutMs: config.longJobTimeoutMs,
    });

    // Extra: if danger/warning rows linger, keep waiting until they clear or timeout.
    const warnings = page.locator('.image-fix, tr.danger ul.warnings li.label-danger');
    if ((await warnings.count()) > 0) {
      console.log('Warnings still listed — waiting for them to clear…');
      await waitForBusyToClear(page, {
        label: `warning rows clear (${sideLabel})`,
        timeoutMs: config.longJobTimeoutMs,
      });
    }
  }

  // If a warning popup appears ("Let Me Edit" / continue), prefer continue
  // only when we intentionally triggered batch fix.
  const continueLink = page.locator('.lists-continue a').first();
  if ((await continueLink.count()) > 0 && (await continueLink.isVisible())) {
    console.log('Warning popup open — clicking continue-through');
    await continueLink.click();
    await waitForBusyToClear(page, {
      label: 'continue-through busy clear',
      timeoutMs: config.longJobTimeoutMs,
    });
  }

  console.log(`Edit step looks ready for ${sideLabel}; clicking Next`);
  await clickNext(page);
}
