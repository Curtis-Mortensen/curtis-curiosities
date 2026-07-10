/*
  Step: assemble cards by pairing backs and fronts from batch.json.

  ELI5: On the last builder step you check which back and which front
  make a card, then click "Add Card(s) to Deck". This script walks the
  pairing list from organize-batches.js and does that for you.

  Related files:
  - cards/batches/*/batch.json is the pairing table
  - deck.js uses .checkboxes-backs / .checkboxes-fronts / .submit-add
*/

export async function assembleDeck(page, batch) {
  console.log(`Assembling ${batch.cardCount} card(s) for ${batch.batchId}`);

  await page.waitForSelector('body.page-deck-assemble, .checkboxes-backs, .checkboxes-fronts', {
    timeout: 120_000,
  });

  for (const pair of batch.pairs) {
    // Clear previous checks so we add one pair at a time.
    // (Safer than multi-select until we confirm how the UI multiplies.)
    await page.locator('.checkboxes-backs input:checked').uncheck().catch(() => {});
    await page.locator('.checkboxes-fronts input:checked').uncheck().catch(() => {});

    // Match checkbox labels / nearby text to the uploaded file name.
    // These locators will likely need tightening after a headed dry run.
    const backBox = page
      .locator('.checkboxes-backs label, .checkboxes-backs li, .checkboxes-backs tr')
      .filter({ hasText: pair.backFile.replace(/\.[^.]+$/, '') })
      .locator('input[type="checkbox"]')
      .first();

    const frontBox = page
      .locator('.checkboxes-fronts label, .checkboxes-fronts li, .checkboxes-fronts tr')
      .filter({ hasText: pair.frontFile.replace(/\.[^.]+$/, '') })
      .locator('input[type="checkbox"]')
      .first();

    if ((await backBox.count()) === 0 || (await frontBox.count()) === 0) {
      throw new Error(
        `Could not find checkboxes for ${pair.backFile} + ${pair.frontFile}. ` +
          'Open headed mode and adjust selectors in src/steps/assemble-deck.js',
      );
    }

    await backBox.check();
    await frontBox.check();

    const addButton = page.locator('.submit-add, input[value*="Add Card"]').first();
    await addButton.click();
    console.log(`Added pair #${pair.order}: ${pair.backFile} + ${pair.frontFile}`);
  }

  // Finish when the deck has rows.
  const finish = page.locator('.submit-wrapper-finish input, .submit-wrapper-finish button, input[value*="Finish"]').first();
  await finish.click();
}
