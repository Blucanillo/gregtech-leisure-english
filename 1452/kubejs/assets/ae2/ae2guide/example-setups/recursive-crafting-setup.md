---
navigation:
  parent: example-setups/example-setups-index.md
  title: Recursive Crafting
  icon: minecraft:netherite_upgrade_smithing_template
---

# Recursive Crafting Setup

As explained under [autocrafting](../ae2-mechanics/autocrafting.md), the crafting planner cannot handle recipes whose main output is also an ingredient. For example, it cannot plan the duplication recipe for a <ItemLink id="minecraft:netherite_upgrade_smithing_template" />.

One solution is to use a <ItemLink id="level_emitter" /> as a [pattern](../items-blocks-machines/patterns.md).

The level emitter can then activate a small crafting setup. This example duplicates a <ItemLink id="minecraft:netherite_upgrade_smithing_template" />.

<RecipeFor id="minecraft:netherite_upgrade_smithing_template" />

***

## Configuration

* <ItemLink id="interface" /> (1): stock the other required ingredients, diamonds and netherrack.
* <ItemLink id="level_emitter" /> (2): filter for a Netherite Upgrade Smithing Template, install a crafting card, and select "emit redstone to craft item".
* The first <ItemLink id="import_bus" /> (3): filter for the interface's stocked items. Install a redstone card and select "active with signal".
* The first <ItemLink id="storage_bus" /> (4) must have a *higher* [priority](../ae2-mechanics/import-export-storage.md#storage-priority) than the second storage bus.
* <ItemLink id="molecular_assembler" /> (5): insert a template duplication pattern and manually insert one smithing template.


* The second <ItemLink id="import_bus" /> (6): default configuration.
* The second <ItemLink id="storage_bus" /> (7): filter for a Netherite Upgrade Smithing Template and set a *lower* [priority](../ae2-mechanics/import-export-storage.md#storage-priority) than the first storage bus.

## How It Works

1. With a <ItemLink id="crafting_card" /> installed and "emit redstone to craft item" selected, the <ItemLink id="level_emitter" /> acts as a [pattern](../items-blocks-machines/patterns.md). The Netherite Upgrade Smithing Template appears in the [terminal](../items-blocks-machines/terminals.md) as an [autocraftable](../ae2-mechanics/autocrafting.md) item.
2. A crafting request from a player or the system activates the level emitter.
3. The first <ItemLink id="import_bus" /> is activated by the emitter and extracts ingredients from the <ItemLink id="interface" />.
4. The only <ItemLink id="storage_bus" /> that can accept those ingredients is the one on the assembler.
5. The <ItemLink id="molecular_assembler" />, which already contains one template, receives the ingredients and crafts two templates.
6. The second <ItemLink id="import_bus" /> extracts one template.
7. The first storage bus has a higher priority, so the template returns to the assembler.
8. The second <ItemLink id="import_bus" /> extracts the other template.
9. The assembler cannot accept another template, so this one enters the lower-priority storage bus and goes into the interface.
10. The <ItemLink id="interface" />, which is not configured to stock templates, returns it to the main network.
