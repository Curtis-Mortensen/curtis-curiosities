# E061_GoblinsHenchman_RubiksCubeRandomDungeon

_Source: `E061_GoblinsHenchman_RubiksCubeRandomDungeon.pdf`_
_Processed: 2026-06-28T07:27:39.080Z_
_Model: `gemini-3.1-flash-lite` (medium reasoning)_

## Transcription

This document is a procedural generation tool designed for tabletop roleplaying games (like D&D). It uses a standard Rubik’s Cube to randomly determine the characteristics of a specific dungeon location.

### 1. Visual Description
The page is titled "Rubik’s Cube Random Dungeon." It is organized into clear sections:
*   **Header:** Features a colorful graphic of a partially scrambled Rubik’s Cube.
*   **Color Legend:** Lists the six aspects corresponding to the six colors of the cube faces (Blue, White, Green, Orange, Red, Yellow).
*   **Methodology:** Explains how to calculate points based on square configurations on each face. It provides visual examples of scoring patterns (L-shapes, lines).
*   **Example Sidebar:** Shows a real-world example of how a cube face might be calculated and what it generates.
*   **Main Table:** A large, comprehensive table that maps the calculated point totals to specific room descriptors.
*   **Footer:** Includes creative commons licensing information and the author's blog URL.

***

### 2. Transcription

**Title:** Rubik’s Cube Random Dungeon

**Color Legend:**
*   Blue square = Structure
*   White square = Exits
*   Green square = Dressing
*   Orange square = Special
*   Red square = Encounters
*   Yellow square = Reward

**METHOD:** Thoroughly jumble the cube and add up the points for each of the six aspects and refer to the table below.

**POSITIVE POINTS:** For each face, all squares matching the colour of the central square = +2 points (include the central square). For three-block shapes matching the colour of the central square = +1 (e.g., L-shape, 2 x L-shapes + line, diagonal line).

**NEGATIVE POINTS:** For three-block shapes *not* matching the colour of the central square = –3 points (e.g., L-shape, line).

**TABLE OF RESULTS: SIX ASPECTS OF THE DUNGEON LOCATION**

| Pts | Blue (Structure) | White (Exits) | Green (Dressing) | Orange (Special) | Red (Encounters) | Yellow (Reward) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ≤ 1 | way up/down | 3 | water/flooded | trap | robust | punitive |
| 2-3 | cavern/natural | 1 | smell/draft | feature/statue | wandering | handsome |
| 4-5 | room | - | - | - | - | - |
| 6-7 | passageway | 2 | sounds | flora/fauna | denizens | fair |
| 8-9 | collapsed area | concealed | odd lighting | puzzle/mystery | sanctuary/aid | objective |
| 10+ | special* | 4+ | ± temperature | secret way(s) | apex/boss | knowledge |

*\* = e.g. amphitheatre, boat, bridge, caldera, catacomb, chasm, dwelling, giant crystal geode, giant invertebrate burrow, lake, lava, midden, pit of corruption, portal, quarry, river, rope swing, sentient space, temple, waterfall etc.*

**Example Sidebar:**
*   Blue: 10+ (special)
*   White: ≤1 (3 exits)
*   Green: 10+ (± temperature)
*   Orange: 6 (flora/fauna)
*   Red: 7 (denizens)
*   Yellow: 4 (no treasure)
*   *Interpretation:* "Gnomes work at the forge; rats scurry away down the three exits"

***

### 3. Understanding the "Map" (How to use it)

Because this is a procedural generator rather than a fixed drawing, the "map" is the state of the cube itself. If you cannot see the cube, here is how you can use the system to generate a dungeon room:

**The Concept:**
A single dungeon location is defined by all six faces of your Rubik’s Cube simultaneously. Each face represents a specific "Aspect" of the room.

**The Steps to Generate a Room:**
1.  **Randomize:** Scramble your Rubik’s Cube.
2.  **Identify the Core:** For each of the six sides, look at the **center square**. This color tells you which aspect you are calculating for that face (e.g., if the center of a face is Blue, that face calculates your "Structure").
3.  **Calculate the Score:**
    *   Count the squares on that face that match the center color. Every matching square (including the center) is **+2 points**.
    *   Look for groups of three squares (L-shapes or straight lines) that match the center color. Each group adds **+1 point**.
    *   Look for groups of three squares that *do not* match the center color. Each group subtracts **-3 points**.
4.  **Reference the Table:** Take your total points for that face and look at the "Table of Results" row for that specific color. This tells you what is in the room.

**Example of an Interpretation:**
If your Blue face (Structure) scores "10+," the table says the structure is "special." Looking at the asterisk note, you might decide the room is a "giant crystal geode." If your White face (Exits) scores "≤1," the table says "3 exits." You now know you are in a giant crystal geode with three exits. You would repeat this for the other four colors to build the full "flavor" of the encounter.
title: Rubik’s Cube Random Dungeon
summary: Rubik's Cube Random Dungeon is a procedural generation tool that uses a Rubik's Cube to randomly determine aspects of a dungeon location by calculating points based on colored squares. Each face of the cube maps to a different room characteristic such as structure, encounters, or rewards.
rooms: 0
resolutions: Combat, Puzzles, Traps, Exploration, Social
concept_originality: 10.0
mechanics_originality: 8.5
interesting_details: 5.0
map_quality: 3.0
humor: 2.0
content_rating: G
rated_at: 2026-06-28T07:37:08.600Z
model: deepseek/deepseek-v4-flash
