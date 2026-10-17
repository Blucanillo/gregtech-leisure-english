---
navigation:
  parent: example-setups/example-setups-index.md
  title: Bucket Emptier
  icon: minecraft:bucket
---

# Bucket Emptier

See also the [bucket filler](bucket-filler.md).

This setup uses a <ItemLink id="pattern_provider" />, so it works together with your [autocrafting](../ae2-mechanics/autocrafting.md) system.

Sometimes you need a fluid but can only produce it in buckets. Other mods may have a machine for this, such as Thermal Expansion's Fluid Transposer. When one is unavailable, vanilla offers a slightly less convenient solution: the <ItemLink id="minecraft:dispenser" />.

## Configuration

* <ItemLink id="pattern_provider" /> (1): set crafting lock to "while redstone signal is present", enable blocking mode, and insert the appropriate <ItemLink id="processing_pattern" />.


* <ItemLink id="interface" /> (2): default configuration.
* The first <ItemLink id="storage_bus" /> (3): default configuration.
* <ItemLink id="annihilation_plane" /> (4): has no GUI or configuration.
* <ItemLink id="import_bus" /> (5): filter for empty buckets.
  <ItemImage id="minecraft:bucket" scale="2" />
* The second <ItemLink id="storage_bus" /> (6): default configuration.

## How It Works

1. The <ItemLink id="pattern_provider" /> sends ingredients to the <ItemLink id="interface" />.
   (As an optimization, it actually inserts directly into the storage buses as though they were its own output faces. The items never enter the interface itself.)
2. The [pipe subnet](pipe-subnet.md#providing-to-multiple-places) carries the filled buckets to the <ItemLink id="minecraft:dispenser" />.
3. The <ItemLink id="minecraft:comparator" /> detects a bucket in the dispenser, activating it and locking the <ItemLink id="pattern_provider" />.
4. The dispenser empties the fluid into the world, leaving an empty bucket inside.
5. The <ItemLink id="import_bus" /> extracts the empty bucket. The <ItemLink id="storage_bus" /> sends it into the pattern provider and back to the main network.
6. The comparator detects that the dispenser is empty and unlocks the provider.
