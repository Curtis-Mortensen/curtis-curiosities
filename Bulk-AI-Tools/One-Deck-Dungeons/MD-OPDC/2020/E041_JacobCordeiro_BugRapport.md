# E041_JacobCordeiro_BugRapport

_Source: `E041_JacobCordeiro_BugRapport.pdf`_
_Processed: 2026-06-28T07:26:57.904Z_
_Model: `gemini-3.1-flash-lite` (medium reasoning)_

## Transcription

### Visual Description
The page is designed to look like a technical manual or a field report. It features a clean, professional layout dominated by a muted teal-and-white color palette on a white background. At the top, the title "Bug Rapport" is written in a bold, sans-serif font, accompanied by illustrations of small, insect-like "ambit" creatures.

The document is organized into columns: the outer edges contain gameplay instructions, lore, and definitions, while the central area features a flowchart-style map representing three towers. The overall aesthetic is "industrial horror"—clinical, sterile, and slightly ominous.

***

### Transcription of Text

**Bug Rapport**
*by Jacob Cordeiro*

**Lore**
There are three towers built along the snowy mountains. They receive radio signals for unknown purposes. Ambits are giant vermin improved by motors and plastic, programmed with simple roles. Some might be told to kill all intruders, even while others throw a party in the same room. The players are technicians who aren't paid nearly enough. Their job is to inspect the towers, and optionally, to get out alive.

**Setup**
Distribute these tools between the players.
*   **Welder:** Helps to attach cables. A decent weapon.
*   **Laptop:** Helps to reprogram electronics and ambits.
*   **Magnet:** Helps to climb, and messes with electronics.
*   **Hook:** Reaches objects from afar. A decent weapon.
*   **Railgun:** Fires small objects, including ends of cables.
*   **Instrument:** Entertains ambits. May have other uses.

**Ambits**
Every ambit has an organic body and one of many wild personalities, but they're enhanced and sometimes controlled by servos and microcontrollers with mysterious purpose. Their mechanical parts—wiry limbs, or plastic exoskeletons, or elaborate wings and weapons—sometimes take over the ambit's actions. Ambits may be reasonable and helpful, but they can’t speak, or resist the commands given by their roles. The players must be careful not to activate them.

**Goal**
Every minute a packet arrives, a radio signal containing a random (d6) number that’s picked up by the top of a tower and travels to the bottom. Each room also has a number, as shown on the map. The players’ goal is to “unlock” as many rooms as possible, by sending each one a packet with a matching number.

Every room has a locker, an outlet, and a console. The locker provides items, weapons, information, and other rewards when the room is unlocked. The outlet allows rooms to be linked by electrical cables (see the map) which can be removed and reconnected. The console is how players decide what happens to a packet as it passes through the room. Each console can have one of the following commands:
*   **NOP:** (default) The packet is sent on to the floor below.
*   **WAIT:** The packet stays in place until further notice.
*   **SUM:** The packet stays in place until a second packet arrives. Then the two numbers are added together.
*   **COPY:** The packet moves through, and a copy of the packet is sent through the cable attached to this room.
*   **DEL:** The packet is deleted.

*Each operation takes a few seconds to process. Characters may spend hours of in-game time to solve a puzzle with brute force. Give them a time limit!*

**Rooms**
Each room on the map is labeled with the room number (see "Goal"). It also suggests the room type, the game mechanic players might find, and the hazard they might face. Each suggestion is just one word, which the game master can interpret however they want. For a one-session game, try using 3 mechanics and 3 hazards, briefly mentioning other features to establish atmosphere. One hazard may expand into an overarching threat.

*   *Note:* The room's function. "Canteen" could refer to an abandoned mess hall, or a food pile made by ambits.
*   *Note:* A new game mechanic. "Music" could mean that ambits' behavior is affected by the music playing in this room.
*   *Note:* A room hazard. "Guards" could mean that a few of the ambits turn to "kill mode" if the players trip security.

*The danger escalates as the players complete their goals. Near the end of the game, players should be rushing between safe rooms, swinging from cables, and making desperate plans to solve the last few puzzles.*

***

### Description of the Map
The map is a directed graph representing three vertical "towers." Each tower is a column of six stacked boxes (rooms).

**The Nodes (Rooms):**
Each room is represented by a rectangle containing four lines of information:
1.  **Number:** The ID number required to unlock the room.
2.  **Room Name:** The title of the area.
3.  **Mechanic:** Indicated by a head icon.
4.  **Hazard:** Indicated by a warning triangle icon.

**The Columns:**
*   **Left Tower:** Top to bottom: 45 (Radio Station/Hints/Surveillance), 12 (Hangar/Trade/Mischief), 200 (Laboratory/Scavenge/Hunter), 1081 (Lobby/Buried/Darkness), 8 (Basement/Debris/Sleepers), 5040 (Generator/Circuits/Electricity).
*   **Middle Tower:** Top to bottom: 10 (Lookout/Injured/Blizzard), 33 (Workshop/Copycat/Limbs), 9 (Lounge/Helpers/Scouts), 1024 (Offices/Music/Projectiles), 7 (Staff Room/Malfunction/Guards), 121 (Boiler/Lonely/Burnout).
*   **Right Tower:** Top to bottom: 923 (???/Boss/Boss), 31 (Canteen/Persuade/Collapse), 15 (Storage/Party/Mayhem), 10 (Factory/Climb/Weaponizing), 27 (Hive/Production/Mutiny), 600 (Panic Room/Bulkhead/Freezing).

**The Cables:**
*   Each room has a thick black line extending from its side (the outlet) to another room in an adjacent column.
*   These represent the "cables" mentioned in the rules. They allow packets to jump from one tower to another.
*   For example, there is a connection from the "Hangar" in the left tower to the "Workshop" in the center tower. There are also connections branching out from the "Offices" and "Staff Room" to various rooms in the right tower.
*   The lines create a complex, crisscrossing web between the three towers, suggesting that players must physically move to re-link these cables to direct the numerical "packets" to the correct target rooms.
title: Bug Rapport
summary: Players are underpaid technicians inspecting three radio towers filled with insect-like 'ambits' that may be hostile or friendly. They must unlock rooms by routing numbered packets through a network of consoles and cables.
rooms: 18
resolutions: Combat, Diplomacy, Puzzles, Stealth, Roleplay, Traps, Exploration, Social
concept_originality: 8.5
mechanics_originality: 9.0
interesting_details: 8.0
map_quality: 7.5
humor: 2.5
content_rating: PG-13
rated_at: 2026-06-28T07:36:28.110Z
model: deepseek/deepseek-v4-flash
