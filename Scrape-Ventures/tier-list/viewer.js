/**
 * STS2 tier-list viewer logic.
 * Prefers baked window.TIER_DATA (file:// friendly); falls back to fetch() when developing
 * without re-running build-viewer.py. Builds character sections, tier rows, and search.
 */

const TIER_ORDER = ["S", "A", "B", "C", "D", "TBD"];

const tierLabelClass = {
  S: "tier-label--s",
  A: "tier-label--a",
  B: "tier-label--b",
  C: "tier-label--c",
  D: "tier-label--d",
  TBD: "tier-label--tbd",
};

/** Load tier data from baked script tag or JSON files over HTTP. */
async function loadData() {
  if (window.TIER_DATA?.tiers && window.TIER_DATA?.manifest) {
    return window.TIER_DATA;
  }

  const [tierRes, manifestRes] = await Promise.all([
    fetch("data/tier-lists.json"),
    fetch("assets/manifest.json"),
  ]);

  if (!tierRes.ok) {
    throw new Error(`tier-lists.json: HTTP ${tierRes.status}`);
  }
  if (!manifestRes.ok) {
    throw new Error(`manifest.json: HTTP ${manifestRes.status}`);
  }

  return {
    tiers: await tierRes.json(),
    manifest: await manifestRes.json(),
  };
}

/** Resolve local thumb/full paths, falling back to remote iconUrl. */
function imageSources(card, manifestPaths) {
  const local = manifestPaths[card.slug];
  return {
    thumb: local?.thumb || card.iconUrl,
    full: local?.full || card.iconUrl,
  };
}

/** Necrobinder keeps an empty TBD row for parity with Mobalytics. */
function shouldShowTierRow(tierKey, cards, characterSlug) {
  if (cards.length > 0) {
    return true;
  }
  return tierKey === "TBD" && characterSlug === "necrobinder";
}

/** One card thumbnail with hover preview and a findable name in the DOM. */
function createCardEntry(card, manifestPaths) {
  const { thumb, full } = imageSources(card, manifestPaths);

  const entry = document.createElement("div");
  entry.className = "card-entry";
  entry.dataset.slug = card.slug;
  entry.dataset.name = card.name;
  entry.tabIndex = 0;

  const thumbImg = document.createElement("img");
  thumbImg.className = "card-thumb";
  thumbImg.src = thumb;
  thumbImg.alt = "";
  thumbImg.loading = "lazy";
  thumbImg.decoding = "async";

  const name = document.createElement("span");
  name.className = "card-name";
  name.textContent = card.name;

  const hoverImg = document.createElement("img");
  hoverImg.className = "card-hover";
  hoverImg.src = full;
  hoverImg.alt = card.name;

  entry.append(thumbImg, name, hoverImg);
  return entry;
}

/** S/A/B/C/D (and optional empty TBD) row for one character. */
function createTierRow(tierKey, cards, characterSlug, manifestPaths) {
  const row = document.createElement("div");
  row.className = "tier-row";
  row.dataset.tier = tierKey;

  const label = document.createElement("span");
  label.className = `tier-label ${tierLabelClass[tierKey] || ""}`;
  label.textContent = tierKey;

  const grid = document.createElement("div");
  grid.className = "tier-cards";

  if (cards.length === 0) {
    grid.classList.add("tier-cards--empty");
    grid.textContent = "No cards yet";
  } else {
    for (const card of cards) {
      grid.appendChild(createCardEntry(card, manifestPaths));
    }
  }

  row.append(label, grid);
  return row;
}

/** Full section for one character: title + tier rows. */
function createCharacterSection(character, manifestPaths) {
  const section = document.createElement("section");
  section.className = "character-section";
  section.id = character.anchorId;
  section.dataset.character = character.character;

  const heading = document.createElement("h2");
  heading.textContent = character.title;
  section.appendChild(heading);

  for (const tierKey of TIER_ORDER) {
    const cards = character.tiers[tierKey] || [];
    if (!shouldShowTierRow(tierKey, cards, character.character)) {
      continue;
    }
    section.appendChild(
      createTierRow(tierKey, cards, character.character, manifestPaths),
    );
  }

  return section;
}

/** Jump links across the sticky header. */
function buildCharacterNav(characters, navEl) {
  navEl.replaceChildren();
  for (const character of characters) {
    const link = document.createElement("a");
    link.href = `#${character.anchorId}`;
    link.textContent = character.character;
    navEl.appendChild(link);
  }
}

/** Hide non-matching cards; dim empty tier rows during search. */
function applySearch(query) {
  const normalized = query.trim().toLowerCase();
  const entries = document.querySelectorAll(".card-entry");
  let firstMatch = null;

  for (const entry of entries) {
    const name = entry.dataset.name.toLowerCase();
    const slug = entry.dataset.slug.toLowerCase();
    const matches =
      !normalized || name.includes(normalized) || slug.includes(normalized);

    entry.classList.toggle("is-hidden", !matches);
    entry.classList.remove("is-match");

    if (matches && normalized && !firstMatch) {
      firstMatch = entry;
      entry.classList.add("is-match");
    }
  }

  for (const row of document.querySelectorAll(".tier-row")) {
    const visible = row.querySelectorAll(".card-entry:not(.is-hidden)");
    const isEmptyTier = row.querySelector(".tier-cards--empty");
    row.classList.toggle("is-empty", !isEmptyTier && visible.length === 0);
  }

  if (firstMatch) {
    firstMatch.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

/** Wire search input after the page is rendered. */
function setupSearch() {
  const input = document.getElementById("search-input");
  input.addEventListener("input", () => applySearch(input.value));
}

/** Fill the page once JSON is loaded. */
function renderViewer(tierData, manifest) {
  const main = document.getElementById("tier-list-main");
  const meta = document.getElementById("meta-count");
  const manifestPaths = manifest.paths || {};

  main.replaceChildren();
  buildCharacterNav(tierData.characters, document.getElementById("character-nav"));

  for (const character of tierData.characters) {
    main.appendChild(createCharacterSection(character, manifestPaths));
  }

  const fetched = tierData.fetchedAt
    ? new Date(tierData.fetchedAt).toLocaleDateString()
    : "unknown date";
  meta.textContent = `${tierData.cardCount} cards · updated ${fetched}`;

  setupSearch();
}

/** Boot: fetch data, render, or show a helpful error. */
async function init() {
  const main = document.getElementById("tier-list-main");

  try {
    const { tiers, manifest } = await loadData();
    renderViewer(tiers, manifest);
  } catch (err) {
    main.innerHTML = "";
    const msg = document.createElement("p");
    msg.className = "load-error";
    msg.textContent =
      `Could not load tier list data (${err.message}). ` +
      "Run: python3 tier-list/scrape/build-viewer.py — or serve over HTTP for dev.";
    main.appendChild(msg);
  }
}

init();
