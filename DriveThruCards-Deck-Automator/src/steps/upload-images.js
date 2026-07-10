/*
  Step: upload a folder of images on a Deck Builder upload page.

  ELI5: Finds the "choose files" control (or the drag-and-drop box)
  and feeds it every JPG/PNG in a folder. Used once for backs and
  once for fronts.

  Related files:
  - src/run-batch.js calls this for backs/ then fronts/
  - src/steps/edit-images.js runs after uploads finish
  - master-plan.md lists the CSS hooks we expect after login

  NOTE: Selectors are best-effort from public CSS + screenshots.
  Harden them during a headed dry run while logged in.
*/

import fs from 'node:fs';
import path from 'node:path';
import { config } from '../config.js';

function listImageFiles(dirPath) {
  return fs
    .readdirSync(dirPath)
    .filter((name) => /\.(jpe?g|png)$/i.test(name))
    .sort()
    .map((name) => path.join(dirPath, name));
}

/**
 * Upload every image in dirPath on the current builder page.
 * Prefers a hidden file input; falls back to clicking the dropzone text.
 */
export async function uploadImages(page, dirPath, label = 'images') {
  const files = listImageFiles(dirPath);
  if (files.length === 0) {
    throw new Error(`No jpg/png files found in ${dirPath}`);
  }

  for (const filePath of files) {
    const size = fs.statSync(filePath).size;
    if (size > config.maxFileBytes) {
      throw new Error(
        `${path.basename(filePath)} is ${size} bytes (max ${config.maxFileBytes})`,
      );
    }
  }

  console.log(`Uploading ${files.length} ${label} from ${dirPath}`);

  // Most modern upload widgets keep an <input type="file"> in the DOM.
  let fileInput = page.locator('input[type="file"]').first();
  if ((await fileInput.count()) === 0) {
    // Click the dropzone so the site injects / reveals the input.
    const dropzone = page.getByText(/drag and drop files here or click to upload/i);
    await dropzone.click();
    fileInput = page.locator('input[type="file"]').first();
  }

  // setInputFiles works even when the input is visually hidden.
  await fileInput.setInputFiles(files);

  // Give the table a moment to list thumbnails. A later edit step
  // should wait for real "ready" signals; this is only a soft pause.
  await page.waitForTimeout(config.uploadSettleMs);

  // Soft check: look for any uploaded thumbnail row if present.
  const uploaded = page.locator('.deck-uploaded img, .uploaded-images img, table img');
  if ((await uploaded.count()) > 0) {
    console.log(`Saw ${await uploaded.count()} thumbnail(s) after upload`);
  } else {
    console.log('No thumbnails detected yet — continue and verify in headed mode');
  }

  return files.map((f) => path.basename(f));
}
