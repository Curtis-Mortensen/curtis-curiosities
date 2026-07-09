/*
  This file is the shared settings for the whole automator.

  ELI5: Think of it as a sticky note with the website address, folder
  paths, the 130-card limit, and how long we are willing to wait for
  DriveThru's slow "fix colors / render sheet / publish" jobs.

  Related files:
  - src/run-batch.js uses these URLs and paths when driving Edge
  - src/organize-batches.js uses maxCardsPerBatch as a default
  - src/waits.js uses the long-job timeout + heartbeat settings
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
  // Persistent Edge profile = you log in once in a real Edge window.
  edgeProfileDir: path.join(ROOT, 'auth', 'edge-profile'),
  // Optional cookie snapshot (legacy / backup); profile folder is preferred.
  authStatePath: path.join(ROOT, 'auth', 'storage-state.json'),
  cardsDir: path.join(ROOT, 'cards'),
  batchesDir: path.join(ROOT, 'cards', 'batches'),
  outputDir: path.join(ROOT, 'output'),

  // Use installed Microsoft Edge, in a visible window you can watch.
  browserChannel: 'msedge',
  headless: false,
  slowMoMs: 250,

  // Short navigations (clicking Next between ready pages).
  navigationTimeoutMs: 120_000,

  // DTC server-side jobs observed ~10 minutes each (color correct,
  // render sheet, publish). Give them 20 minutes before failing.
  longJobTimeoutMs: 20 * 60 * 1000,
  waitHeartbeatMs: 30_000,

  uploadSettleMs: 2_000,

  // Selectors that often mean "server is still working."
  // Hardened later against the live DOM; extras are ignored if absent.
  busySelectors: [
    '.batch-wait',
    '.blockUI',
    '.blockOverlay',
    '.loading',
    '.spinner',
    'img[src*="loader"]',
    'text=/please wait/i',
    'text=/processing/i',
    'text=/rendering/i',
    'text=/auto-?correct/i',
  ],
};
