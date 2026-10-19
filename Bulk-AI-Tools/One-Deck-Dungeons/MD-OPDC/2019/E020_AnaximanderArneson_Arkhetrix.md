# E020_AnaximanderArneson_Arkhetrix

_Source: `E020_AnaximanderArneson_Arkhetrix.pdf`_
_Processed: 2026-06-28T07:21:27.250Z_
_Model: `gemini-3.1-flash-lite` (medium reasoning)_

## Transcription

This document, titled **Arkhetrix**, is a one-page tabletop roleplaying game (TTRPG) concept designed with a distinct "retro-hacker" aesthetic.

### Visual Overview
The page mimics the appearance of a 1980s or 90s green-and-white computer terminal. The background is solid black with monospaced, light-colored text and lines. The header features prominent ASCII art of the title "Arkhetrix," and the entire layout is strictly column-based. It uses ASCII characters (plus signs, hyphens, pipes, and tildes) to construct tables, grids, and decorative avatars, creating a cohesive, lo-fi cyberpunk atmosphere.

---

### Transcription

**[Header ASCII Art: Arkhetrix]**
*Anaximander Arneson (https://sites.google.com/site/arkhe-rpg)*

**2081 AD, ace netrunners are hacking a military-grade system looking for Arkhetrix's megacorp secrets.** Relying on topnotch cyberware, they tap their minds directly to the cyberspace. Offensive security countermeasures are deployed, preventing them from jacking out safely... The only way out lies deep in.

**Cyberspace:**
The cyberspace is an VR maze of layered cell-grids, each with 1 entry, 3 exits and a damaged (unpassable) sector. PCs start at layer 1 and need to find their way to layer 4. The GM can determine the correct exit by rolling 1d3 in secret for each layer. Each time the (whole) group takes the correct exit, rotate the board 90º clockwise and access the next layer. Otherwise, rotate the board counter-clockwise and re-enter the previous layer (or re-enter layer 1 if already at layer 1).

**Avatars:**
In Arkhetrix’s cyberspace, PCs are represented by avatars, with:
* 10 Connection Points (CP) and
* 10 Execution Points (EP).
Bonuses may apply at GM’s discretion.
If dropped to 0 CP, PCs are derezzed. Otherwise, a PC commands 2 different actions each round:
* Move 1 cell
* Move up to 2 cells
* Regain 1 EP (capped at maximum)
* Code (an exploit)
* Execute (an exploit)

**Exploits:**
Coding an exploit costs 1 permanent EP (effectively reducing the PC's maximum), and allows to execute it unlimitedly. Coding fixes effects and cost in EP, for each EP (required for execution) an exploit gains:
* +2 cell range
* +1 target (friend or foe)
And choose between effects(*):
* +1d6 CP damage
* +2 CP increase
* +2 cell (forced) movement
(*) Distribute EP between effects and effects between different targets.

**Intruder Countermeasure Entities (ICE):**
AI software protects the system, spawning ICE to repel intruders. ICE have 1 CP and a damage reduction of 1. At the beginning of each round in layer N, spawn N+1 ICE. Roll 1d10 and 1d8, then place an ICE in the corresponding cell. Ignore an spawn on top of an existing ICE and activate it instead, also ignore spawns in the damaged sector.
At the end of each round, every ICE in play activates and moves 3 cells towards the PC closest to it (avoiding collisions with other ICE). When entering a cell occupied by another ICE or PC (including during spawn), ICE are automatically dropped to 0 CP. At 0 CP, ICE explode damaging friend and foes in the central and adjacent cells for 1d6 CP. Every time PCs move between layers reset existing ICE.

**Arkhetrix Restricted Knowledgebase (ARK):**
At layer 4 place the ARK (occupying a 3x3 area) fixed at the center of the grid. The ARK has 40 CP and a damage reduction of 2. Immediately after each PC's turn, the ARK activates an ICE or spawns a new one if there are none in play. ICE spawned in ARK's cells are ignored, activating the ARK instead. When dropped to 0 CP, the ARK is hacked, the paydata retrieved, and PCs may disconnect safely.

*Arkhetrix is released under the Creative Commons Attribution-Share Alike 3.0 Unported Licence. http://creativecommons.org/licenses/by-sa/3.0*

---

### Map Description for Play
The cyberspace board is represented as a **10x8 grid** (10 rows down, 8 columns across). 

*   **The Grid Layout:**
    *   **Rows:** Numbered 1 through 10 from top to bottom.
    *   **Columns:** Numbered 1 through 8 from left to right.
    *   **The Damaged Sector:** Occupying a 2x2 space in the lower-middle section, specifically at intersection of **Rows 6 & 7, Columns 6 & 7**. This is marked on the map with tilde (`~~~~`) borders and bracketed symbols (`[@#$%&]`), signifying it is impassable.
*   **Access Points:**
    *   **Entry:** Located on the left side, situated between rows 5 and 6.
    *   **Exit 1:** Located at the top, centered between columns 4 and 5.
    *   **Exit 2:** Located on the right side, situated between rows 5 and 6.
    *   **Exit 3:** Located at the bottom, centered between columns 4 and 5.
*   **Key Mechanics for Navigation:**
    *   **Rotation:** This is the most critical aspect of the map. Because the board rotates 90° clockwise upon a success or counter-clockwise upon a failure, the relative positions of the Exits and the "Damaged Sector" will shift constantly. 
    *   **Pro Tip for Play:** If playing physically, use a piece of paper for the grid and rotate it physically on the table. If playing digitally, ensure your map layer can be rotated easily in your VTT (Virtual Tabletop).
    *   **Layer 4 (ARK):** At the final stage, a 3x3 square is placed in the center of the board (Rows 4-6, Columns 3-5). This is the "boss" object that players must deplete to 0 CP to win.
title: Arkhetrix
summary: Arkhetrix is a one-page cyberpunk hacking dungeon where netrunners navigate a rotating virtual maze to hack a megacorp's system. Players manage avatars with connection and execution points, code exploits, and fight ICE to reach the final ARK.
rooms: 4
resolutions: Combat, Puzzles, Exploration
concept_originality: 9.5
mechanics_originality: 9.0
interesting_details: 9.0
map_quality: 8.0
humor: 1.0
content_rating: PG
rated_at: 2026-06-28T07:35:41.801Z
model: deepseek/deepseek-v4-flash
