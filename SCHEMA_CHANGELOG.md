# Schema changelog

Record structural changes only. For each change, include its status (Planned or Completed), affected files, fields added, removed or modified, field types and meanings, compatibility implications, and implementation date when known.

### Items — Expanded Item Definitions

**Status:** Completed  
**Affected file:** `Items/items.json`

Expanded item records using data extracted from the original English MHFU game binaries.

**New fields:**

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Internal game item ID |
| `buy-price` | Integer | Item purchase price in zenny |
| `pt` | Integer | Treasure points associated with the item |
| `pickup-sound` | Integer | Internal pickup sound identifier |
| `item-type` | Integer | Internal item classification |
| `icon-id` | Integer | Internal icon identifier |
| `color-id` | Integer | Internal color identifier |
| `ammo-bits` | Integer | Internal ammunition-related bit flags |
| `decoration-id` | Integer | Internal decoration identifier |

**Existing fields retained:**

`name`, `description`, `rare`, `carry-max`, `icon`, `color`, `selling-price`

⚠️ `description` now includes special characters such as new line and color code that are exactly used in game. 
- `\n` is new line character
- `~C05(Word)` means to paint the words in the parenthesis yellow.

**Other changes:**

- `rare` now uses the extracted game's `raw_rarity` value.
- `carry-max` uses the extracted `stack_size` value.
- `selling-price` uses the game's `sell_value` (zenny).
- `icon` and `color` retain readable labels where matching metadata exists; unmatched values may be `null`.
- Item descriptions preserve the original game's line breaks.
- Item records now include internal metadata useful for further research and development.

**Compatibility:** Additive fields are generally backward-compatible, but existing field values, description formatting, and nullable icon/color values may affect consumers. The change from previous rarity values to extracted values should be reviewed by dependent applications.

### Item Combinations — Expanded Recipe Definitions and Menu Positions

**Status:** Completed  
**Affected file:** `Items/items-combine.json`

Expanded combination recipes using data extracted from the original English MHFU game binaries.

The dataset now includes internal recipe identifiers, output quantity weights, and page positions corresponding to the in-game combination list.

**New fields:**

| Field | Type | Description |
|---|---|---|
| `recipe-id` | Integer | Internal combination recipe identifier |
| `weights` | Array of integers | Probability weights associated with the recipe's output quantities |
| `page` | Integer | Page number in the in-game combination list |
| `page-index` | Integer | Recipe position within its combination list page |

**Existing fields retained:**

`name`, `type`, `materialA`, `materialB`, `chance`, `min`, `max`

**Other changes:**

- Preserved existing recipe names, types, ingredients, success rates, and output quantity ranges.
- Added internal recipe IDs for linking combinations to game definitions.
- Added quantity weights for representing output-quantity distributions.
- Included page numbers and indices to identify recipes within the in-game combination list.

**Compatibility:**

The documented additions extend the existing recipe structure. Consumers using the original recipe fields can continue accessing those fields without modification.

### Skills — Added Internal Identifiers

**Status:** Completed  
**Affected file:** `Skills/skills.json`

Expanded skill activation records using identifiers extracted from the original English MHFU game binaries.

**New fields:**

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Internal identifier of the activated skill effect |
| `category-id` | Integer | Internal identifier of the skill-point category |

**Existing fields retained:**

- `name` — Activated skill name
- `skill-point` — Skill-point category name
- `points` — Required activation threshold

**Compatibility:** This is an additive schema change. Existing fields and their meanings remain unchanged. Consumers that ignore additional JSON properties should continue working normally.

### Armors — Expanded Armor Definitions and Image Separation

**Status:** Completed  
**Affected files:**
- `Armors/armors.json`
- `Armors/armors-image.json`

Expanded armor records using information extracted from the original English MHFU game binaries, and separated project-maintained armor images from the main dataset.

**New fields in `armors.json`:**

| Field | Type | Description |
|---|---|---|
| `armor-id` | Integer | Internal armor identifier |
| `forge-id` | Integer | Internal forging identifier |
| `raw-menu-index` | Integer | Internal forging menu index |
| `blacksmith-page` | Integer or null | Page number in the blacksmith's armor forging menu |
| `blacksmith-index` | Integer or null | Position within the blacksmith menu page |
| `felyne-vendor-page` | Integer or null | Page number in the Felyne armor vendor's shop menu |
| `felyne-vendor-index` | Integer or null | Position within the Felyne vendor menu page |

For the four menu-position fields, `null` indicates that the armor is not listed in the corresponding vendor's menu.

**Removed fields from `armors.json`:**

- `image-male`
- `image-female`

**New image dataset:**

`Armors/armors-image.json` stores:
- `part` — Armor equipment slot
- `name` — Armor name
- `image-male` — Project-maintained male armor image path
- `image-female` — Project-maintained female armor image path

**Existing fields retained:**

`part`, `name`, `rare`, `price`, `hunter-type`, `defense`, `skill-points`, `description`, `slots`, `fire-res`, `water-res`, `thundr-res`, `dragon-res`, `ice-res`, `materials`, `sex`

**Description formatting:**

`description` now preserves special characters from the original game text, including `\n` for line breaks.

**Other changes:**

- Armor descriptions preserve original in-game line breaks.
- Game-derived armor properties and forging metadata are stored independently of project-maintained images.
- Internal identifiers allow future links to armor crafting and upgrade information.
- Blacksmith and Felyne vendor menu positions are stored separately.
- Armor pieces unavailable through a particular vendor have `null` for both corresponding menu-position fields.

**Compatibility:**

- Removing `image-male` and `image-female` from `armors.json` is an intentional breaking change. Consumers must now read `armors-image.json`.
- The four vendor-position fields are additive. Consumers can use them to locate armor in the corresponding in-game menus.
- Applications displaying armor descriptions should support embedded newline characters.

### Gathering — Quest-Specific Gathering Spots and Loot Probabilities

**Status:** Completed  
**Affected file:** `gathering_spots.json`

Introduced a new quest-specific gathering dataset extracted from the original MHFU game files.

Unlike the existing map-based gathering dataset, which records observed collectible items, the new dataset provides individual gathering spot definitions for each quest, including coordinates, interaction properties, internal game metadata, and exact collectible outcome probabilities.

**The existing map-based gathering dataset remains available and unchanged.** Both datasets are maintained independently because they serve different purposes.

**New record structure:**

| Field | Type | Description |
|---|---|---|
| `quest-id` | Integer | Identifier of the quest associated with the gathering spot |
| `quest-title` | String | English quest title |
| `map` | String | Map and environment variant |
| `area-index` | Integer | Area identifier within the map |
| `stage-index` | Integer | Internal stage identifier |
| `spot-index` | Integer | Gathering spot index |
| `method` | String | Gathering method, such as `mine` |
| `x` | Number | Gathering spot X coordinate |
| `y` | Number | Gathering spot Y coordinate |
| `z` | Number | Gathering spot Z coordinate |
| `interaction-radius` | Number or null | Interaction radius, when available |
| `stored-uses` | Integer | Raw number of uses stored in the gathering node data |
| `outcomes` | Array | Possible collectible items and their probabilities |

**Outcome structure:**

| Field | Type | Description |
|---|---|---|
| `name` | String | Collectible item name |
| `chance` | Number | Probability weight expressed as a percentage |

**Key features:**

- Gathering spots are associated with specific quests rather than only maps.
- Each spot includes its location coordinates and gathering method.
- Every spot contains its own collectible outcome table with exact probabilities.
- Gathering outcomes may differ between quests sharing the same map or area.
- Internal node parameters and source offsets are retained for future reverse engineering.
- Optional interaction-radius values may be `null` when unavailable.
- The original map-based gathering dataset remains available for simpler collectible lookups.

**Dataset differences:**

- **Existing gathering dataset:** Provides map-based gathering information derived from observed collectibles.
- **`gathering_spots.json`:** Provides detailed, quest-specific gathering spot definitions and their collectible outcome probabilities.

Although the original dataset may theoretically be derived from the new data, reproducing it accurately would require additional processing and reconciliation across quests. Both datasets are therefore retained.

**Compatibility:**

This is an **additive dataset change**, not a breaking change.

Existing consumers can continue using the original gathering dataset without modification.

Applications requiring quest-specific gathering locations, interaction metadata, or exact collectible probabilities can use `gathering_spots.json` independently.

### Monster Spawns — Expanded Spawn Data and Setup Conditions

**Status:** Completed  
**Affected files:**
- `monster-spawns-flat.json`
- `monster-spawn-conditions.json`

Expanded quest-specific monster spawn records with raw power codes, spawn setup memberships, movement information, and conditions governing small-monster setup changes.

**Spawn data fields:**

| Field | Type | Description |
|---|---|---|
| `power-code` | Integer | Raw monster power code |
| `setup-slots` | Array of integers or null | Small-monster setup configurations containing the spawn |
| `possible-areas` | Array of integers or null | Possible large-monster movement areas |
| `areas-complete` | Boolean or null | Whether movement-area data is complete |
| `areas-source` | Array of strings, optional | Sources of movement-area information |
| `size` | Object or null | Monster size-roll eligibility and possible size percentages |

**Spawn condition fields:**

| Field | Type | Description |
|---|---|---|
| `defeat-count-triggers` | Array of objects | Monster defeat conditions for changing setups |
| `carried-item-triggers` | Array of objects | Carried-item conditions for changing setups |
| `target-setup-slot` | Integer | Setup activated when a condition is satisfied |
| `minimum-matching-defeats` | Integer | Required cumulative monster defeats |
| `minimum-carried-quantity` | Integer | Required item quantity |

**Existing fields retained:**

`quest-id`, `quest-title`, `map-id`, `map`, `monster-id`, `monster`, `type`, `area-index`, `stage-id`, `initial-xyz`, `facing-raw`, `defeat-budget`

**Other changes:**

- Covers 551 quests and 16,750 monster spawn records.
- Includes 47 defeat-count triggers and 110 carried-item triggers.
- Small-monster configurations start at slot `0` and progress to higher slots.
- Large-monster spawns are independent of small-monster setup switching.

**Compatibility:** The updated spawn data includes `power-code` and uses `setup-slots` for individual spawn membership. Consumers should use the condition dataset to determine when the active small-monster setup changes.
