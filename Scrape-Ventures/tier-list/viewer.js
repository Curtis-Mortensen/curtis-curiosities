/**
 * STS2 tier-list viewer logic.
 * Fetches JSON from data/ and assets/, then renders methodology, character tier rows,
 * and hover tooltips with card metadata from Spire Codex. Serve tier-list/ over HTTP —
 * opening index.html as file:// blocks fetch().
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

/** Load all viewer JSON over HTTP from the tier-list folder. */
async function loadData() {
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

/** Build the large card preview panel (full art + metadata). */
function fillCardPreview(previewEl, card, fullSrc, metaBySlug) {
  previewEl.replaceChildren();

  const art = document.createElement("img");
  art.className = "card-preview-art";
  art.src = fullSrc;
  art.alt = card.name;
  previewEl.appendChild(art);

  const meta = metaBySlug[card.slug];
  if (meta) {
    const panel = document.createElement("div");
    panel.className = "card-preview-meta";

    const title = document.createElement("p");
    title.className = "card-preview-title";
    title.textContent = meta.name || card.name;
    panel.appendChild(title);

    const stats = document.createElement("p");
    stats.className = "card-preview-stats";
    const parts = [meta.cost, meta.type, meta.rarity].filter(Boolean);
    stats.textContent = parts.join(" · ");
    panel.appendChild(stats);

    if (meta.keywords?.length) {
      const keywords = document.createElement("p");
      keywords.className = "card-preview-keywords";
      keywords.textContent = meta.keywords.join(", ");
      panel.appendChild(keywords);
    }

    if (meta.description) {
      const desc = document.createElement("p");
      desc.className = "card-preview-desc";
      desc.textContent = meta.description;
      panel.appendChild(desc);
    }

    previewEl.appendChild(panel);
  }
}

/** Place the preview to the right of the cursor, clamped inside the viewport. */
function positionCardPreview(previewEl, event) {
  const gap = 14;
  const pad = 20;
  const width = previewEl.offsetWidth || 320;
  const height = previewEl.offsetHeight || 420;

  let left = event.clientX + gap;
  let top = event.clientY - 24;

  // Stay on screen with padding — slide inward instead of flipping to the left of the cursor.
  left = Math.min(left, window.innerWidth - width - pad);
  left = Math.max(left, pad);
  top = Math.min(top, window.innerHeight - height - pad);
  top = Math.max(top, pad);

  previewEl.style.left = `${left}px`;
  previewEl.style.top = `${top}px`;
}

/** One shared preview that follows the pointer over any card thumbnail. */
function setupCardPreview(metaBySlug) {
  const previewEl = document.getElementById("card-preview");
  if (!previewEl) {
    return;
  }

  let activeEntry = null;

  const showForEntry = (entry, event) => {
    const slug = entry.dataset.slug;
    const card = { name: entry.dataset.name, slug };
    const fullSrc = entry.dataset.fullSrc;
    fillCardPreview(previewEl, card, fullSrc, metaBySlug);
    previewEl.hidden = false;
    previewEl.setAttribute("aria-hidden", "false");
    positionCardPreview(previewEl, event);
    activeEntry = entry;
  };

  const hide = () => {
    previewEl.hidden = true;
    previewEl.setAttribute("aria-hidden", "true");
    activeEntry = null;
  };

  document.addEventListener("mouseover", (event) => {
    const entry = event.target.closest(".card-entry");
    if (!entry || entry.classList.contains("is-hidden")) {
      if (!event.relatedTarget?.closest?.(".card-entry")) {
        hide();
      }
      return;
    }
    if (entry !== activeEntry) {
      showForEntry(entry, event);
    }
  });

  document.addEventListener("mousemove", (event) => {
    if (activeEntry && event.target.closest(".card-entry") === activeEntry) {
      positionCardPreview(previewEl, event);
    }
  });

  document.addEventListener("mouseout", (event) => {
    const from = event.target.closest(".card-entry");
    const to = event.relatedTarget?.closest?.(".card-entry");
    if (from && from !== to) {
      hide();
    }
  });

  window.addEventListener("scroll", hide, { passive: true });
}

/** One card thumbnail with a findable name label beneath it. */
function createCardEntry(card, manifestPaths, metaBySlug) {
  const { thumb, full } = imageSources(card, manifestPaths);

  const entry = document.createElement("div");
  entry.className = "card-entry";
  entry.dataset.slug = card.slug;
  entry.dataset.name = card.name;
  entry.dataset.fullSrc = full;
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

  entry.append(thumbImg, name);
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

/** Pair each nav link with its on-page section for scroll-spy and smooth jumps. */
function navSectionPairs(navEl) {
  return [...navEl.querySelectorAll('a[href^="#"]')]
    .map((link) => {
      const id = link.getAttribute("href").slice(1);
      return { link, section: document.getElementById(id) };
    })
    .filter((pair) => pair.section);
}

/** Highlight whichever section is currently in view while scrolling. */
function setupCharacterNavScrollSpy(navEl) {
  const pairs = navSectionPairs(navEl);
  if (pairs.length === 0) {
    return;
  }

  const setActive = (activeLink) => {
    for (const { link } of pairs) {
      const isActive = link === activeLink;
      link.classList.toggle("is-active", isActive);
      link.toggleAttribute("aria-current", isActive);
    }
  };

  const pickActiveFromScroll = () => {
    const header = document.querySelector(".site-header");
    const cutoff = (header?.offsetHeight ?? 0) + 8;

    let active = pairs[0];
    for (const pair of pairs) {
      if (pair.section.getBoundingClientRect().top <= cutoff) {
        active = pair;
      }
    }
    setActive(active.link);
  };

  const observer = new IntersectionObserver(
    () => pickActiveFromScroll(),
    {
      root: null,
      rootMargin: "-20% 0px -65% 0px",
      threshold: 0,
    },
  );

  for (const { section } of pairs) {
    observer.observe(section);
  }

  pickActiveFromScroll();
  window.addEventListener("hashchange", pickActiveFromScroll);
}

/** Smooth in-page jumps that respect the sticky header offset. */
function setupNavSmoothScroll(navEl) {
  navEl.addEventListener("click", (event) => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || !navEl.contains(link)) {
      return;
    }

    const id = link.getAttribute("href").slice(1);
    const target = document.getElementById(id);
    if (!target) {
      return;
    }

    event.preventDefault();
    target.scrollIntoView({ behavior: "smooth", block: "start" });
    history.pushState(null, "", `#${id}`);
    link.classList.add("is-active");
    for (const other of navEl.querySelectorAll("a.is-active")) {
      if (other !== link) {
        other.classList.remove("is-active");
        other.removeAttribute("aria-current");
      }
    }
    link.setAttribute("aria-current", "true");
  });
}

/** Arrow keys move focus between nav links; Enter follows the focused hash. */
function setupNavKeyboard(navEl) {
  navEl.addEventListener("keydown", (event) => {
    const links = [...navEl.querySelectorAll("a")];
    const index = links.indexOf(document.activeElement);
    if (index === -1) {
      return;
    }

    let next = -1;
    if (event.key === "ArrowRight" || event.key === "ArrowDown") {
      next = (index + 1) % links.length;
    } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
      next = (index - 1 + links.length) % links.length;
    } else if (event.key === "Home") {
      next = 0;
    } else if (event.key === "End") {
      next = links.length - 1;
    }

    if (next >= 0) {
      event.preventDefault();
      links[next].focus();
    }
  });
}

/** Wire scroll-spy, smooth jumps, and keyboard nav after links are in the DOM. */
function setupCharacterNav(navEl) {
  setupNavSmoothScroll(navEl);
  setupNavKeyboard(navEl);
  setupCharacterNavScrollSpy(navEl);
}

/** Scroll position saved when the user first types in search; restored when cleared. */
let preSearchScrollY = null;

/** Hide non-matching cards; dim empty tier rows during search. */
function applySearch(query) {
  const normalized = query.trim().toLowerCase();
  const isActive = normalized.length > 0;

  if (isActive && preSearchScrollY === null) {
    preSearchScrollY = window.scrollY;
  }

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

  if (!isActive) {
    if (preSearchScrollY !== null) {
      const restoreY = preSearchScrollY;
      preSearchScrollY = null;
      requestAnimationFrame(() => {
        window.scrollTo({ top: restoreY, behavior: "smooth" });
      });
    }
    return;
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
  const navEl = document.getElementById("character-nav");
  buildCharacterNav(tierData.characters, navEl);

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

  setupCharacterNav(navEl);
  setupSearch();
  setupCardPreview(metaBySlug);

  if (location.hash) {
    const target = document.getElementById(location.hash.slice(1));
    if (target) {
      requestAnimationFrame(() => {
        target.scrollIntoView({ behavior: "auto", block: "start" });
      });
    }
  }
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
      "Serve locally: cd tier-list && python3 -m http.server 8080";
    main.appendChild(msg);
  }
}

init();
