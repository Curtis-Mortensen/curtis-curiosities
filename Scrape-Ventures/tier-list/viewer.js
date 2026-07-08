/**
 * STS2 tier-list viewer logic.
 * Prefers baked window.TIER_DATA (file:// friendly); falls back to fetch() when developing
 * without re-running build-viewer.py. Renders methodology, character tier rows, and
 * hover tooltips with card metadata from Spire Codex.
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

/** Load all viewer JSON — baked inline or fetched over HTTP during dev. */
async function loadData() {
  if (window.TIER_DATA?.tiers && window.TIER_DATA?.manifest) {
    return window.TIER_DATA;
  }

  const [tierRes, manifestRes, methodologyRes, metadataRes] = await Promise.all([
    fetch("data/tier-lists.json"),
    fetch("assets/manifest.json"),
    fetch("data/methodology.json"),
    fetch("data/card-metadata.json"),
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
    methodology: methodologyRes.ok ? await methodologyRes.json() : null,
    cardMetadata: metadataRes.ok ? await metadataRes.json() : null,
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

/** Build the hover tooltip: full art plus cost / type / rarity / description. */
function createCardHover(card, fullSrc, metaBySlug) {
  const hover = document.createElement("div");
  hover.className = "card-hover";
  hover.setAttribute("role", "tooltip");

  const art = document.createElement("img");
  art.className = "card-hover-art";
  art.src = fullSrc;
  art.alt = card.name;
  hover.appendChild(art);

  const meta = metaBySlug[card.slug];
  if (meta) {
    const panel = document.createElement("div");
    panel.className = "card-hover-meta";

    const title = document.createElement("p");
    title.className = "card-hover-title";
    title.textContent = meta.name || card.name;
    panel.appendChild(title);

    const stats = document.createElement("p");
    stats.className = "card-hover-stats";
    const parts = [meta.cost, meta.type, meta.rarity].filter(Boolean);
    stats.textContent = parts.join(" · ");
    panel.appendChild(stats);

    if (meta.keywords?.length) {
      const keywords = document.createElement("p");
      keywords.className = "card-hover-keywords";
      keywords.textContent = meta.keywords.join(", ");
      panel.appendChild(keywords);
    }

    if (meta.description) {
      const desc = document.createElement("p");
      desc.className = "card-hover-desc";
      desc.textContent = meta.description;
      panel.appendChild(desc);
    }

    hover.appendChild(panel);
  }

  return hover;
}

/** One card thumbnail with hover preview and a findable name in the DOM. */
function createCardEntry(card, manifestPaths, metaBySlug) {
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

  entry.append(
    thumbImg,
    name,
    createCardHover(card, full, metaBySlug),
  );
  return entry;
}

/** S/A/B/C/D (and optional empty TBD) row for one character. */
function createTierRow(tierKey, cards, characterSlug, manifestPaths, metaBySlug) {
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
      grid.appendChild(createCardEntry(card, manifestPaths, metaBySlug));
    }
  }

  row.append(label, grid);
  return row;
}

/** Full section for one character: title + tier rows. */
function createCharacterSection(character, manifestPaths, metaBySlug) {
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
      createTierRow(tierKey, cards, character.character, manifestPaths, metaBySlug),
    );
  }

  return section;
}

/** Mobalytics-style S–D methodology blurb at the top of the page. */
function createMethodologySection(methodology) {
  if (!methodology) {
    return null;
  }

  const section = document.createElement("section");
  section.className = "methodology-panel";
  section.id = "methodology";

  const details = document.createElement("details");
  details.open = true;

  const summary = document.createElement("summary");
  summary.textContent = "Tier methodology";
  details.appendChild(summary);

  const body = document.createElement("div");
  body.className = "methodology-body";

  if (methodology.intro) {
    const intro = document.createElement("p");
    intro.textContent = methodology.intro;
    body.appendChild(intro);
  }

  if (methodology.disclaimer) {
    const disclaimer = document.createElement("p");
    disclaimer.className = "methodology-disclaimer";
    disclaimer.textContent = methodology.disclaimer;
    body.appendChild(disclaimer);
  }

  if (methodology.evaluation) {
    const evaluation = document.createElement("p");
    evaluation.textContent = methodology.evaluation;
    body.appendChild(evaluation);
  }

  if (methodology.multiplayerNote) {
    const mp = document.createElement("p");
    mp.className = "methodology-note";
    mp.textContent = methodology.multiplayerNote;
    body.appendChild(mp);
  }

  const tierList = document.createElement("dl");
  tierList.className = "methodology-tiers";

  for (const tier of methodology.tiers || []) {
    if (tier.tier === "TBD") {
      continue;
    }

    const dt = document.createElement("dt");
    const badge = document.createElement("span");
    badge.className = `methodology-tier-badge ${tierLabelClass[tier.tier] || ""}`;
    badge.textContent = tier.label || tier.tier;
    dt.appendChild(badge);

    const dd = document.createElement("dd");
    dd.textContent = tier.description;

    tierList.append(dt, dd);
  }

  body.appendChild(tierList);
  details.appendChild(body);
  section.appendChild(details);
  return section;
}

/** Jump links across the sticky header. */
function buildCharacterNav(characters, navEl) {
  navEl.replaceChildren();

  const methodLink = document.createElement("a");
  methodLink.href = "#methodology";
  methodLink.textContent = "Methodology";
  navEl.appendChild(methodLink);

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
function renderViewer(data) {
  const tierData = data.tiers;
  const manifest = data.manifest;
  const main = document.getElementById("tier-list-main");
  const meta = document.getElementById("meta-count");
  const manifestPaths = manifest.paths || {};
  const metaBySlug = data.cardMetadata?.cards || {};

  main.replaceChildren();
  buildCharacterNav(tierData.characters, document.getElementById("character-nav"));

  const methodologySection = createMethodologySection(data.methodology);
  if (methodologySection) {
    main.appendChild(methodologySection);
  }

  for (const character of tierData.characters) {
    main.appendChild(createCharacterSection(character, manifestPaths, metaBySlug));
  }

  const fetched = tierData.fetchedAt
    ? new Date(tierData.fetchedAt).toLocaleDateString()
    : "unknown date";
  const metaCount = Object.keys(metaBySlug).length;
  meta.textContent = `${tierData.cardCount} cards · ${metaCount} with metadata · updated ${fetched}`;

  setupSearch();
}

/** Boot: load data, render, or show a helpful error. */
async function init() {
  const main = document.getElementById("tier-list-main");

  try {
    const data = await loadData();
    renderViewer(data);
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
