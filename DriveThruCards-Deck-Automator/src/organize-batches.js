/*
  This script turns a card manifest into batch folders.

  ELI5: You list every card and which back art it uses. This program
  groups cards that share a back, packs them into folders of at most
  130 cards, and renames files to 001back.jpg / 001front.jpg so the
  DriveThruCards uploader is easy to follow.

  Related files:
  - cards/manifest.example.json shows the input shape
  - src/run-batch.js later reads each batch's batch.json
  - master-plan.md explains the batching rules in plain language
*/

import fs from 'node:fs';
import path from 'node:path';
import { config, ROOT } from './config.js';

function usageAndExit() {
  console.error('Usage: node src/organize-batches.js <manifest.json>');
  process.exit(1);
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function slugify(text) {
  return String(text)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 40) || 'back';
}

function resolveCardPath(manifestDir, relativePath) {
  return path.resolve(manifestDir, relativePath);
}

function copyAsJpegName(srcPath, destPath) {
  // We keep the original bytes; only the destination name is normalized.
  // DTC prefers JPG; renaming .png → .jpg is NOT a real conversion.
  fs.copyFileSync(srcPath, destPath);
}

/**
 * Expand qty into individual card slots so packing math is simple.
 * Each slot still remembers the original card id for the batch log.
 */
function expandSlots(cards) {
  const slots = [];
  for (const card of cards) {
    const qty = Number(card.qty ?? 1);
    for (let i = 0; i < qty; i += 1) {
      slots.push({
        id: card.id,
        front: card.front,
        back: card.back,
        slotIndex: i + 1,
        qtyInOriginal: qty,
      });
    }
  }
  return slots;
}

/**
 * Group slots by back path, then pack groups into batches ≤ maxCards.
 * A single oversized back-group is split across multiple batches.
 */
function packBatches(slots, maxCards, strategy) {
  if (strategy === 'single-deck') {
    const batches = [];
    for (let i = 0; i < slots.length; i += maxCards) {
      batches.push(slots.slice(i, i + maxCards));
    }
    return batches;
  }

  // Default: group-by-back, then first-fit into batches.
  const byBack = new Map();
  for (const slot of slots) {
    if (!byBack.has(slot.back)) byBack.set(slot.back, []);
    byBack.get(slot.back).push(slot);
  }

  const batches = [];
  let current = [];

  for (const [, group] of byBack) {
    let offset = 0;
    while (offset < group.length) {
      const room = maxCards - current.length;
      if (room === 0) {
        batches.push(current);
        current = [];
        continue;
      }
      const take = Math.min(room, group.length - offset);
      // Prefer keeping a whole group together when it fits.
      if (offset === 0 && group.length <= maxCards && group.length > room) {
        batches.push(current);
        current = [];
        continue;
      }
      current.push(...group.slice(offset, offset + take));
      offset += take;
      if (current.length === maxCards) {
        batches.push(current);
        current = [];
      }
    }
  }

  if (current.length) batches.push(current);
  return batches;
}

function writeBatch(batchIndex, slots, manifest, manifestDir, batchesDir) {
  const firstBackName = path.basename(slots[0].back, path.extname(slots[0].back));
  const batchId = `batch-${String(batchIndex).padStart(2, '0')}-${slugify(firstBackName)}`;
  const batchDir = path.join(batchesDir, batchId);
  const backsDir = path.join(batchDir, 'backs');
  const frontsDir = path.join(batchDir, 'fronts');
  ensureDir(backsDir);
  ensureDir(frontsDir);

  // Unique back files in this batch → upload once each.
  const uniqueBacks = new Map();
  const pairs = [];

  slots.forEach((slot, index) => {
    const n = String(index + 1).padStart(3, '0');
    const backSrc = resolveCardPath(manifestDir, slot.back);
    const frontSrc = resolveCardPath(manifestDir, slot.front);

    if (!fs.existsSync(backSrc)) {
      throw new Error(`Missing back image: ${backSrc}`);
    }
    if (!fs.existsSync(frontSrc)) {
      throw new Error(`Missing front image: ${frontSrc}`);
    }

    let backBatchName = uniqueBacks.get(slot.back);
    if (!backBatchName) {
      // First time we see this back in the batch: copy as NNN + shared key.
      // If several cards share it, later pairs reuse the same uploaded name.
      backBatchName = `${n}back${path.extname(backSrc).toLowerCase() || '.jpg'}`;
      copyAsJpegName(backSrc, path.join(backsDir, backBatchName));
      uniqueBacks.set(slot.back, backBatchName);
    }

    const frontBatchName = `${n}front${path.extname(frontSrc).toLowerCase() || '.jpg'}`;
    copyAsJpegName(frontSrc, path.join(frontsDir, frontBatchName));

    pairs.push({
      order: index + 1,
      cardId: slot.id,
      backFile: backBatchName,
      frontFile: frontBatchName,
      sourceBack: slot.back,
      sourceFront: slot.front,
      quantity: 1,
    });
  });

  const batchJson = {
    batchId,
    deckName: manifest.deckName ?? 'Untitled Deck',
    cardCount: pairs.length,
    uniqueBackCount: uniqueBacks.size,
    pairs,
    notes: [
      'Upload every file in backs/ on the Back Images step.',
      'Upload every file in fronts/ on the Front Images step.',
      'On Assemble, pair each front with its backFile from this list.',
      'quantity is always 1 here because qty was expanded into slots.',
    ],
  };

  fs.writeFileSync(path.join(batchDir, 'batch.json'), JSON.stringify(batchJson, null, 2));
  return batchJson;
}

function main() {
  const manifestArg = process.argv[2];
  if (!manifestArg) usageAndExit();

  const manifestPath = path.resolve(process.cwd(), manifestArg);
  const manifestDir = path.dirname(manifestPath);
  const manifest = readJson(manifestPath);
  const maxCards = Number(manifest.maxCardsPerBatch ?? config.maxCardsPerBatch);
  const strategy = manifest.batchStrategy ?? 'group-by-back';

  if (!Array.isArray(manifest.cards) || manifest.cards.length === 0) {
    throw new Error('manifest.cards must be a non-empty array');
  }

  const slots = expandSlots(manifest.cards);
  const packed = packBatches(slots, maxCards, strategy);

  const batchesDir = path.join(config.cardsDir, 'batches');
  // Fresh organize: wipe previous generated batches for this project folder.
  fs.rmSync(batchesDir, { recursive: true, force: true });
  ensureDir(batchesDir);

  const summary = [];
  packed.forEach((slotsInBatch, i) => {
    const batch = writeBatch(i + 1, slotsInBatch, manifest, manifestDir, batchesDir);
    summary.push({
      batchId: batch.batchId,
      cardCount: batch.cardCount,
      uniqueBackCount: batch.uniqueBackCount,
    });
    console.log(
      `Wrote ${batch.batchId} (${batch.cardCount} cards, ${batch.uniqueBackCount} unique backs)`,
    );
  });

  const summaryPath = path.join(batchesDir, 'summary.json');
  fs.writeFileSync(
    summaryPath,
    JSON.stringify(
      {
        deckName: manifest.deckName,
        strategy,
        maxCardsPerBatch: maxCards,
        totalCards: slots.length,
        batchCount: summary.length,
        batches: summary,
        sourceManifest: path.relative(ROOT, manifestPath),
      },
      null,
      2,
    ),
  );

  console.log(`Done. ${summary.length} batch(es). Summary: ${summaryPath}`);
}

main();
