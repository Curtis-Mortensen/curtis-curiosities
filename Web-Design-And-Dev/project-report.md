# Project Report: Pleasant Noise

## Purpose

This project is a **portfolio website for an up-and-coming band**. The goal is to give the band a polished public presence where fans can discover releases, learn about the artists, and eventually read news or blog posts — while keeping day-to-day content management simple for non-developers.

The codebase is built on the [Sanity + React Router template](https://github.com/SimeonGriggs/sanity-react-router-template), adapted and extended for that use case. The band-facing site and the content studio live in one application, deployed together (currently targeting Vercel).

---

## Why Sanity (and this structure)

The template’s README describes a batteries-included setup. For a band portfolio, that structure pays off in several concrete ways:

### Embedded Studio (`/studio`)

Sanity Studio runs inside the same React Router app at `/studio`. Band members or a manager can log in and update content without touching code or a separate admin tool.

### Visual Editing and Presentation

Using [Presentation](https://www.sanity.io/docs/presentation) and [@sanity/react-loader](https://www.sanity.io/docs/react-loader), authenticated editors can browse the live site from within Studio, click into sections, and edit fields with **real-time preview**. That matters for a band site where layout and imagery are part of the brand.

### Pre-configured content model (Record Collection)

The default schema is already oriented around music:

| Content type | Role on a band site |
|---|---|
| **Home** (singleton) | Site title, hero heading, global branding |
| **Record** | Albums/singles with cover art, release date, track listing, rich editorial copy |
| **Artist** | Band members or collaborators |
| **Genre** | Tags for browsing and filtering |
| **Track** (object) | Per-song title and duration on a record |

Records are grouped in Studio (Details, Editorial, Tracks) and support Portable Text, images with hotspots, and references to artists and genres — a solid fit for release pages without custom CMS work.

### Authoring quality-of-life

- **Portable Text** — Rich release notes and bios as structured data, not brittle HTML.
- **Image URL builder** — CDN-backed artwork via asset IDs (see `RecordCover`).
- **Decorated inputs** — e.g. track duration stored as seconds but shown in minutes in Studio.
- **Dynamic OG images** — Share cards for records via `/resource/og`.
- **Typed, validated queries** — Zod schemas ensure the front end always receives content in the expected shape.

### Front-end mutations (example)

The template’s like/dislike buttons on record pages demonstrate how fan interactions can write back to Sanity (with an editor token). That pattern could extend to mailing-list signups, RSVP counts, or similar later.

### Deployment

The stack (React Router 7, Vite, Vercel preset) is aligned with low-friction hosting — important for a small band project without dedicated ops.

---

## Changes made so far

Work on this repo has focused on **extending the content model** and **operational polish**, while keeping the core record-centric site intact.

### Content model extensions

- **`article` schema** — Title, slug, author reference, publish date, main image, excerpt, body (Portable Text), and tags. Intended for band news, tour diaries, or press posts.
- **`author` schema** — Name and bio for article bylines.
- **Studio sidebar** — Articles and Authors added to the desk structure alongside Home, Records, Artists, and Genres.

These types exist in Sanity and can be authored today; they are **not yet wired to public routes** on the website (see planned work below).

### Preview and live content

Preview handling was simplified so public content updates and in-Studio previews work without extra secret configuration across Sanity and Vercel (session/view tokens for drafts were a pain point in earlier attempts). Loaders use `loadQueryOptions` to switch between `published` and `previewDrafts` perspectives when preview mode is active.

### Analytics

[Vercel Analytics](https://vercel.com/docs/analytics) was added in `app/root.tsx` to get basic traffic insight on the deployed site.

### Tooling

The project was migrated to **pnpm** (workspace layout in `pnpm-workspace.yaml`) for dependency management consistency with the monorepo-style Sanity scripts.

### Minor housekeeping

Line-ending normalization (`.gitattributes`), and small Studio structure tweaks (icons for new document types).

---

## Intended changes (not yet implemented)

These are the main gaps between “template + schemas” and a complete band portfolio:

1. **Article pages on the website** — Routes, GROQ queries, Zod types, and components to list and display articles (and link authors).
2. **Presentation locations for articles** — Extend `app/sanity/presentation/resolve.ts` so Visual Editing can deep-link to `/articles/:slug` (or similar).
3. **Home page beyond records** — Optionally surface featured release, latest article, or tour CTA from the `home` singleton.
4. **Artist profile pages** — Optional `/artists/:slug` routes if the band wants dedicated member pages.
5. **Branding pass** — Replace placeholder favicon, typography, and copy with the band’s identity (“Pleasant Noise” in `package.json` is a working title).
6. **OG preview for articles** — Mirror the record OG preview tab in Studio if articles become share-heavy.

None of the above require replacing Sanity or the template architecture; they build on what is already there.

---

## Current site surface

| Route | Status |
|---|---|
| `/` | Record catalog (home) |
| `/records/:slug` | Individual release with tracks, editorial content, like/dislike |
| `/studio` | Embedded Sanity Studio |
| `/resource/preview`, `/resource/og`, `/resource/toggle-theme` | Supporting resource routes |

Articles and authors are **Studio-only** until front-end routes are added.

---

## Summary

The project uses Sanity’s structure — singleton home curation, relational records/artists/genres, embedded Studio, and Visual Editing — as a practical CMS for a band portfolio. Records and the existing release UX are production-ready patterns from the template; recent work added **articles and authors** in the CMS and **analytics** on deploy, with **article pages and deeper band branding** as the natural next steps.

For setup, seeding demo content, and feature details, see [README.md](./README.md).
