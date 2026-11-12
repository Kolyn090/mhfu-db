# Schema changelog

Record structural changes only. For each change, include its status (Planned or Completed), affected files, fields added, removed or modified, field types and meanings, compatibility implications, and implementation date when known.

## Completed — Weapon image separation

- Files affected include `Weapons/weapons.json` and the new `Weapons/weapon-images.json`.
- The `image` field was removed from all 1,500 weapon records. The new file preserves all 1,500 mappings in their original order.
- Each image mapping contains three strings. `name` is the weapon name, `type` is the weapon class, and `image` is the existing image path.
- This is an intentional breaking change for consumers that previously read `image` directly from `Weapons/weapons.json`.

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
| `definition-offset` | Integer | Binary offset of the item definition |
| `name-offset` | Integer | Offset of the localized item name |
| `description-offset` | Integer | Offset of the localized item description |
| `item-type` | Integer | Internal item classification |
| `toolbelt-flags` | Integer | Internal toolbelt behavior flags |
| `flags` | Integer | Additional internal item flags |
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

### Item Combinations — Expanded Recipe Definitions

**Status:** Completed  
**Affected file:** `Items/items-combine.json`

Expanded combination recipes using data extracted from the original English MHFU game binaries.

**New fields:**

| Field | Type | Description |
|---|---|---|
| `recipe-id` | Integer | Internal combination recipe identifier |
| `weights` | Array of integers | Stored weights associated with the recipe's output quantities |
| `definition-offset` | Integer | Binary offset of the recipe definition |
| `rate-id` | Integer | Internal combination success-rate identifier |
| `quantity-id` | Integer | Internal output-quantity table identifier |
| `quantity-offset` | Integer | Binary offset of the output-quantity definition |
| `flags` | Integer | Internal recipe flags |
| `alternate-index` | Integer | Internal alternate recipe index |

**Existing fields retained:**

`name`, `type`, `materialA`, `materialB`, `chance`, `min`, `max`

**Other changes:**

- Preserved the existing player-friendly recipe information.
- Added internal identifiers for linking recipes to game definitions.
- Added quantity weights for representing output-quantity distributions.
- Included source offsets for traceability and future reverse engineering.

**Compatibility:** This is an additive schema change. Existing consumers that ignore unknown fields should continue working without modification.

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
| `raw-flags` | Integer | Raw armor definition flags |
| `raw-recipe-flags` | Integer | Raw armor forging recipe flags |
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
