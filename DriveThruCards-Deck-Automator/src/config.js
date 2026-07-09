/*
  This file is the shared settings for the whole automator.

  ELI5: Think of it as a sticky note with the website address, folder
  paths, and the 130-card limit. Other scripts import these numbers
  instead of hard-coding them in five places.

  Related files:
  - src/run-batch.js uses these URLs and paths when driving the browser
  - src/organize-batches.js uses maxCardsPerBatch as a default
*/

import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(__dirname, '..');

export const config = {
  // Partner tools host that serves the deck builder.
  baseUrl: 'https://tools.drivethrucards.com',

  // Logged-out deep links bounce here; after login you usually land on
  // a deck session URL like /builder/deck/images/back/<id>.
  deckIndexUrl: 'https://tools.drivethrucards.com/builder/deck',

  // Example deep link from the user (session-specific; will 302 if stale).
  exampleBackUploadUrl:
    'https://tools.drivethrucards.com/builder/deck/images/back/6a4ff5a3138d6',

  // Builder hard stop for this project unless a live session shows otherwise.
  maxCardsPerBatch: 130,

  // Image rules from the upload notes panel.
  maxFileBytes: 5 * 1024 * 1024,
  recommendedWidth: 825,
  recommendedHeight: 1125,

  // Local paths.
  authStatePath: path.join(ROOT, 'auth', 'storage-state.json'),
  cardsDir: path.join(ROOT, 'cards'),
  batchesDir: path.join(ROOT, 'cards', 'batches'),
  outputDir: path.join(ROOT, 'output'),

  // Slow, watchable defaults for first dry runs.
  headless: false,
  slowMoMs: 250,
  navigationTimeoutMs: 60_000,
  uploadSettleMs: 2_000,
};
