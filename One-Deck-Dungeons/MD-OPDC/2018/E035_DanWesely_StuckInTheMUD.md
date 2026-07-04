# E035_DanWesely_StuckInTheMUD

_Source: `E035_DanWesely_StuckInTheMUD.pdf`_
_Processed: 2026-06-28T07:14:56.897Z_
_Model: `gemini-3.1-flash-lite` (medium reasoning)_

## Transcription

This document is a "One-Page Dungeon" design titled **"Stuck in the Mud"** by Dan Wesely. It is a minimalist, text-based RPG resource designed in a monospaced font. The layout is utilitarian, featuring a central ASCII-art map, a key for NPC locations, specific movement rules for non-player characters, a list of adventure hooks, and a detailed numbered legend describing each room in the dungeon.

***

### Transcribed Text

**STUCK IN THE MUD**
by Dan Wesely
https://sites.google.com/site/asciisandbox/

**Map Legend & NPC territory abbreviations**
b: Bear | f: Farmer | g: Guard | m: Merchant | n: Noble | o: Oracle | t: Townsfolk | u: Urchin | w: Wealthy Person

**Rules & Context:**
*   **Starting Point:** The players begin in room 11, where the only exit is East.
*   **Navigation:** Throughout the realm, exits are North, East, South, and West. Distances are not important in this realm.
*   **NPC Movement:** NPCs wander around their territory. One option is to place a marker for each NPC somewhere in their territory, then periodically roll a four-sided die (N, E, S, W) and move them if the room in that direction is in their territory.
*   **Event Ideas:**
    *   find an ancient artifact
    *   complete a quest from the king
    *   get killed by the bear or guard
    *   cause self-awareness by the NPCs

**Room Descriptions:**
*   **11 - E - Introductory Area:** A few signs are here to welcome the new players and describe the realm they are entering. No one in the rest of the map seems to think this is odd.
*   **12 - NE W - Town:** Folk go about their business, houses are old but in good repair. A sign warns of bears in the woods. A few necessities can be purchased or bartered.
*   **13 - NE W - In the Woods:** Trees and moss abound, but a clearing can almost be made out to the North. Wind whispers through the trees.
*   **14 - N W - Deeper in the Woods:** It's hard to tell which way is which, it is difficult to travel through so much growth. Even the air smells thick.
*   **21 - NE - Mansion:** Excessive ornamentation, locked cabinets and display cases with trophies. Stairs descend at the North end of the mansion.
*   **22 - NESW - Fields:** Rolling hills covered with a variety of local crops. Rows of trees to the East, and an formidable, gated home to the West.
*   **23 - N SW - Orchard:** Rows of well-kept trees, the fruit tastes good. A modest farmhouse stands to the North. This feels like a good place for a nap.
*   **24 - S - Bear's Cave:** A corner has a sleeping area. Thieves stashed their plunder here long ago. This bear has been terrorizing the townsfolk as long as they can remember.
*   **31 - S - Cellar:** Racks of wine and cheeses keeping cool. There might even be some rats down here causing problems.
*   **32 - N S - Path:** The road to the castle is a good place to meet travelers. The castle itself towers to the North.
*   **33 - ES - Farmhouse:** A simple little house that smells somewhere between fresh baking and old work clothes. The house overlooks the orchard, fields, and a small pond.
*   **34 - W - Pond:** A few birds are usually relaxing here. There are no fish to be seen, but a chorus of frogs is heard in the evening.
*   **41 - N - Guard Shack:** Castle guards usually wander the castle, but come here to train and rest. No lollygagging.
*   **42 - NES - Castle:** Visitors feel tiny at the entrance of the castle. Mud and wagon ruts make it difficult to walk. A makeshift encampment is to the East.
*   **43 - E W - Camp:** Travelling merchants like to bring their wares to the castle to fetch a higher price. Camping, they can be the first to sell to travelers.
*   **44 - W - Merchant's Tent:** One of the merchants may have interesting articles to sell. The tent smells of spices and incense. The merchant watches customers closely.
*   **51 - NES - Market:** Food and daily goods are sold here, bustling during the day. With all the shouting over prices and bumping into other market goers, this is a likely place to get pick pocketed.
*   **52 - NESW - Yard:** Good for meetings, or for parades and small festivals. Guards muster daily here. The noble is likely in the official-looking building to the North.
*   **53 - E W - Theatre:** The castle residents enjoy a good show. A regular troupe performs on this stage, but some days are amateur days where anyone can take the stage.
*   **54 - N W - Wall:** The castle wall protects the residents from unseen dangers. Stairs to the North lead up to a tower. Guards may not like civilians in their territory.
*   **61 - S - Slums:** The urchin's domain, not even the guards come here any more. Houses are little more than spare bits of fabric stretched over felled tree branches.
*   **62 - ES - Throne Room:** The noble sits on a simple but sturdy wooden chair. A look of concern, perhaps some bad news just came from the oracle.
*   **63 - W - Oracle's Library:** Books line the shelves in this musty room. Instruments and crystals sit near an open window. The oracle's notes sit on a table.
*   **64 - S - Tower:** The entire realm can be seen from here, if faintly. The map is bordered by seemingly impassible mountain peaks. One wonders how it sustains itself.

***

### Map Description for Navigation
The dungeon is organized as a **6x4 grid**, totaling 24 rooms. Each cell in the grid represents a numbered room. The numbering follows a coordinate system where the first digit represents the vertical row (1 at the bottom, 6 at the top) and the second digit represents the horizontal column (1 on the far left, 4 on the far right).

*   **Grid Layout:**
    *   **Row 6 (Top):** 61 (Slums), 62 (Throne Room), 63 (Oracle's Library), 64 (Tower)
    *   **Row 5:** 51 (Market), 52 (Yard), 53 (Theatre), 54 (Wall)
    *   **Row 4:** 41 (Guard Shack), 42 (Castle), 43 (Camp), 44 (Merchant's Tent)
    *   **Row 3:** 31 (Cellar), 32 (Path), 33 (Farmhouse), 34 (Pond)
    *   **Row 2:** 21 (Mansion), 22 (Fields), 23 (Orchard), 24 (Bear's Cave)
    *   **Row 1 (Bottom):** 11 (Intro), 12 (Town), 13 (Woods), 14 (Deeper in Woods)

*   **Connections:** The map uses horizontal and vertical ASCII line characters (`-` and `|`) to denote connected paths. A double equal sign (`===`) denotes a major path or thoroughfare between rooms.
*   **Visualizing NPC Territories:** Within the map boxes, you will see lowercase letters (e.g., `g`, `u`, `w`, `b`). These indicate the NPC types that can be found roaming those specific room areas. For instance, the Bear (`b`) is found in the cave (24) and woods (13, 14), while Guards (`g`) are generally found in the upper-middle section of the map (the castle/market area).
*   **The Perimeter:** The map is fully enclosed by ASCII box drawing characters, creating a sense of a contained realm, with no exits leading off the grid.
title: Stuck in the Mud
summary: A sandbox realm in a 6x4 grid where players navigate towns, woods, a castle, and more, with NPCs roaming their territories. Hooks include finding an artifact, completing a king's quest, or dealing with a bear.
rooms: 24
resolutions: Combat, Diplomacy, Fetch Quests, Roleplay, Exploration, Social
concept_originality: 6.5
mechanics_originality: 6.0
interesting_details: 7.0
map_quality: 5.0
humor: 2.0
content_rating: PG
rated_at: 2026-06-28T07:36:05.986Z
model: deepseek/deepseek-v4-flash
