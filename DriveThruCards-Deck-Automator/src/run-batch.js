/*
  Glue script: run one organized batch through the deck builder.

  ELI5: Reads a batch folder, opens a logged-in browser, uploads backs,
  uploads fronts, assembles pairs, and tries to download the PDF.

  Related files:
  - src/organize-batches.js creates the batch folder
  - src/steps/* do each wizard page
  - scripts/auth-save.js must be run once first
*/

import fs from 'node:fs';
import path from 'node:path';
import { config } from './config.js';
import { launchAuthedBrowser, clickNext } from './browser.js';
import { uploadImages } from './steps/upload-images.js';
import { editImagesAndContinue } from './steps/edit-images.js';
import { assembleDeck } from './steps/assemble-deck.js';
import { exportPdf } from './steps/export-pdf.js';

function parseArgs(argv) {
  const args = { batch: null, startUrl: null, dryStopAfter: null, mode: 'download' };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--batch') args.batch = argv[++i];
    else if (a === '--start-url') args.startUrl = argv[++i];
    else if (a === '--dry-stop-after') args.dryStopAfter = argv[++i];
    else if (a === '--mode') args.mode = argv[++i];
    else if (a === '--help' || a === '-h') args.help = true;
  }
  return args;
}

function usage() {
  console.log(`Usage:
  node src/run-batch.js --batch cards/batches/batch-01-shared-red [options]

Options:
  --start-url <url>       Deck session URL (default: config.deckIndexUrl)
  --dry-stop-after <step> Stop after: backs | edit-backs | fronts | edit-fronts | assemble
  --mode <mode>           Export next_step: download | make | update (default download)
`);
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.batch) {
    usage();
    process.exit(args.help ? 0 : 1);
  }

  const batchDir = path.resolve(process.cwd(), args.batch);
  const batchJsonPath = path.join(batchDir, 'batch.json');
  if (!fs.existsSync(batchJsonPath)) {
    throw new Error(`Missing batch.json in ${batchDir}. Run npm run organize first.`);
  }

  const batch = JSON.parse(fs.readFileSync(batchJsonPath, 'utf8'));
  if (batch.cardCount > config.maxCardsPerBatch) {
    throw new Error(
      `Batch ${batch.batchId} has ${batch.cardCount} cards; max is ${config.maxCardsPerBatch}`,
    );
  }

  const outputDir = path.join(config.outputDir, batch.batchId);
  fs.mkdirSync(outputDir, { recursive: true });

  const startUrl = args.startUrl || config.deckIndexUrl;
  const { browser, page } = await launchAuthedBrowser();

  const runLog = {
    batchId: batch.batchId,
    startedAt: new Date().toISOString(),
    startUrl,
    steps: [],
  };

  try {
    console.log(`Opening ${startUrl}`);
    await page.goto(startUrl, { waitUntil: 'domcontentloaded' });

    // If we landed on the index, the human (or a later improvement) must
    // click into "Create US Poker Deck…" / an existing deck session.
    // For MVP we accept a --start-url that already points at back upload.
    if (!/\/builder\/deck\/images\//.test(page.url())) {
      console.log(
        'Not on an images upload URL yet. Pass --start-url with your live ' +
          'back-upload link (like the …/images/back/<id> URL), or click into ' +
          'the beta tool in the headed window, then re-run.',
      );
    }

    // --- Backs ---
    const backs = await uploadImages(page, path.join(batchDir, 'backs'), 'backs');
    runLog.steps.push({ step: 'upload-backs', files: backs, at: new Date().toISOString() });
    if (args.dryStopAfter === 'backs') return finish(runLog, outputDir);

    await clickNext(page);
    await editImagesAndContinue(page, 'backs');
    runLog.steps.push({ step: 'edit-backs', at: new Date().toISOString() });
    if (args.dryStopAfter === 'edit-backs') return finish(runLog, outputDir);

    // --- Fronts ---
    const fronts = await uploadImages(page, path.join(batchDir, 'fronts'), 'fronts');
    runLog.steps.push({ step: 'upload-fronts', files: fronts, at: new Date().toISOString() });
    if (args.dryStopAfter === 'fronts') return finish(runLog, outputDir);

    await clickNext(page);
    await editImagesAndContinue(page, 'fronts');
    runLog.steps.push({ step: 'edit-fronts', at: new Date().toISOString() });
    if (args.dryStopAfter === 'edit-fronts') return finish(runLog, outputDir);

    // --- Assemble ---
    await assembleDeck(page, batch);
    runLog.steps.push({ step: 'assemble', at: new Date().toISOString() });
    if (args.dryStopAfter === 'assemble') return finish(runLog, outputDir);

    // --- Export ---
    const pdfPath = await exportPdf(page, outputDir, {
      mode: args.mode,
      productName: batch.deckName,
    });
    runLog.steps.push({ step: 'export', pdfPath, at: new Date().toISOString() });
    runLog.finishedAt = new Date().toISOString();
    finish(runLog, outputDir);
  } finally {
    await browser.close();
  }
}

function finish(runLog, outputDir) {
  runLog.finishedAt = runLog.finishedAt || new Date().toISOString();
  const logPath = path.join(outputDir, 'run-log.json');
  fs.writeFileSync(logPath, JSON.stringify(runLog, null, 2));
  console.log(`Wrote ${logPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
