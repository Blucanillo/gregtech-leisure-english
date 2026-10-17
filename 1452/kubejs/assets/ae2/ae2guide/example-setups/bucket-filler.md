---
navigation:
  parent: example-setups/example-setups-index.md
  title: Bucket Filler
  icon: minecraft:water_bucket
---

# Bucket Filler

See also the [bucket emptier](bucket-emptier.md).

This setup uses a <ItemLink id="pattern_provider" />, so it works together with your [autocrafting](../ae2-mechanics/autocrafting.md) system.

Sometimes you need buckets of a fluid rather than the fluid itself. Other mods may have a machine for this, such as Thermal Expansion's Fluid Transposer. When one is unavailable, vanilla offers a slightly less convenient solution: the <ItemLink id="minecraft:dispenser" />.

**This setup is often unnecessary: fluid substitution in the [pattern encoding terminal](../items-blocks-machines/terminals.md#pattern-encoding-terminal) lets crafting recipes use fluids directly instead of buckets.**

## Configuration

* <ItemLink id="pattern_provider" /> (1): set crafting lock to "while redstone signal is present" and insert the appropriate <ItemLink id="processing_pattern" />.


* <ItemLink id="interface" /> (2): default configuration.
* The first <ItemLink id="storage_bus" /> (3): default configuration.
* <ItemLink id="formation_plane" /> (4): use an inverter card to exclude empty buckets.
  <Row><ItemImage id="minecraft:bucket" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
* <ItemLink id="import_bus" /> (5): use an inverter card to exclude empty buckets.
  <Row><ItemImage id="minecraft:bucket" scale="2" /><ItemImage id="inverter_card" scale="2" /></Row>
* The second <ItemLink id="storage_bus" /> (6): default configuration.

## How It Works

1. The <ItemLink id="pattern_provider" /> sends ingredients to the <ItemLink id="interface" />.
   (As an optimization, it actually inserts directly into the storage buses as though they were its own output faces. The items never enter the interface itself.)
2. The [pipe subnet](pipe-subnet.md#providing-to-multiple-places) carries empty buckets to the <ItemLink id="minecraft:dispenser" />, while the formation plane places the fluid in the world.
3. The <ItemLink id="minecraft:comparator" /> detects a bucket in the dispenser, activating it and locking the <ItemLink id="pattern_provider" />.
4. The dispenser collects the fluid, leaving a filled bucket inside.
5. The <ItemLink id="import_bus" /> extracts the filled bucket. The <ItemLink id="storage_bus" /> sends it into the pattern provider and back to the main network.
6. The comparator detects that the dispenser is empty and unlocks the provider.
