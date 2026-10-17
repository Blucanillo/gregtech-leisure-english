# Version-separated translation update — 17 October 2026

## Installation layout and references

`1450` and `1452` each contain only `config`, `kubejs`, and `resourcepacks`, ready to merge into the matching instance. No shared installation folder is needed.

1450 was checked against Core 1.2.2.8-fix2 and Additions 2.6.5Custom; 1452 against Core 1.2.3.2-fix4 and Additions 3.3.1Custom. Both use Minecraft 1.20.1, Forge 47.4.16, GTCEu 1.4.4, GTMThings 1.3.5.b and AE2 15.4.10. Exact mod and source hashes are in `version-source-manifest.json`, including independently checked versions of GuideME, FTB Library, KubeJS, Stargate Journey and Sophisticated Storage.

## Included changes

- Retained the separate 48-file and 49-file quest books. The follow-up audit corrects 19 display fields across the two books: machine names, the wording about crafting the ExtendedAE silicon block, and the duplicated newer Steam Oven exception. Quest IDs, tasks, dependencies, rewards, commands and layout remain appropriate to each version. 1450 retains 10,000A Dyson output; 1452 retains 20,000A.
- Translated the 20 status-message source lines in each instance's own `misc.js`, preserving handlers, IDs, calculations, recipes and controls.
- Added 123 English AE2 pages per version: 119 native English counterparts with the pack's custom notes and frontmatter preserved, plus four translated pack-only pages. Both source trees and AE2 jars are byte-identical, verified independently.
- Preserved the available custom formation-plane examples. Replaced the main-network example's absent custom scene with the actual native scene and matching annotations, retaining the custom building notes as text. Removed references to missing diagrams on the four extra pages while retaining their configuration instructions and functional item references.
- Corrected the export-bus page's import-bus recipe/name error. Replaced six unavailable recipe panels with pack-specific instructions and JEI references, checked against each instance's recipe script and live guide compilation. Actual recipes are unchanged. Corrected six inherited native English spelling errors per version.
- Retained earlier GTMThings corrections and added missing GTCEu, AE2 and minor mod labels. Added names for six registered EV laser hatches and five previously unnamed auxiliary items/blocks.
- Fixed wrapped Java-string handling and invalid dynamic translation lookups in KubeJS tooltip callbacks. Visible voltage names use LuV/OpV. Translated the digital miners' hardcoded duration component, plus exact Chinese Spacetime and Chemical Energy Devourer literals where present. These replacements preserve numbers, energy text and styles. Exact matching leaves already-English or changed native text alone.
- Added the same 40 corrected hatch values under the Additions jar's misspelled `gtmtings` namespace, so its language file cannot undo the corrections through namespace loading order. Restored one inherited Forge error-message template to the exact Forge 47.4.16 format.

Each deterministic resource-pack ZIP contains 15 files and 1,349 distinct language keys. Its filename and description match its numbered installation folder. Pack format remains 15.

## Verification

The [consistency audit](consistency-audit-2026-10-17.md) records the findings and practical limits. Saved machine-readable reports cover file/behavior checks, real parser/component APIs, and full Minecraft runtime checks. Both installation folders remain local for review; nothing was committed, pushed or merged. Original installed instances, mod jars and saves were not changed, and no original world was copied into a test instance.
