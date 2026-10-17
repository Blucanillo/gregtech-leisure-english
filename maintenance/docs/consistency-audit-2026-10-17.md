# Consistency and translation audit — 17 October 2026

## References

- [Issue #2: Incorrect dynamo hatch names](https://github.com/Blucanillo/gregtech-leisure-english/issues/2).
- [Issue #3: Incorrect GTMThings names](https://github.com/Blucanillo/gregtech-leisure-english/issues/3).
- [sgiath's PR #1](https://github.com/Blucanillo/gregtech-leisure-english/pull/1), including shifted descriptions, truncation, material names, parallels and version-specific values.

Both issues were closed without discussion comments. The PR's substantive findings are in its description. No GitHub messages or changes were made during this audit.

## Findings fixed locally

1. Retained the earlier Dynamo spelling, amp-count and missing-name fixes. Fixed receiver spelling/grammar and Wireless Transfer sentence spacing. Duplicated the 40 corrected hatch values under the Additions jar's misspelled `gtmtings` namespace, preventing its language file from undoing the corrections.
2. Fixed the duplicated Steam Oven exception in the newer general steam-machine description. Both books now consistently say ME Toggle Bus, Huge Input Bus / Huge Input Dual Hatch and Parallel Control Hatch where those are the actual item names. Changed the ExtendedAE silicon-block warning from “cannot be used” to “cannot be crafted”, matching the removed recipe in each instance's own script. These are 19 additional quest display-field edits across both books.
3. Filled seven minor bundled-mod language gaps: FramedBlocks' Done button; two JER block-count settings; two LaserIO messages; the ME Requester tab label; and one ModernFix setting description. Filled the compatibility report's 11 GTCEu entries and 14 AE2 labels/unit-symbol entries.
4. Live registry checks found six EV wireless laser hatch names absent from both English and Chinese language tables. Added the three source/target amp pairs from their actual IDs. Also added Crystal Reader, Auto Dialer, Liquid Naquadah, Heavy Liquid Naquadah and Inaccessible Slot names. Both versions' installed builds were checked independently.
5. Real tooltips exposed hardcoded Chinese text that resource-pack key coverage cannot detect: digital-miner durations, Spacetime material hints and two old Chemical Energy Devourer boost lines. Exact native-component replacements translate these while preserving the original durations, quantities, styles and energy text. The newer generator's existing English text remains untouched.
6. Corrected a dynamic tooltip translation-key error and wrapped-Java-string behavior, preserving circuit color ramps and using LuV/OpV consistently. The final callback runs successfully in the actual KubeJS/Rhino engine, including the three digital miners.
7. Restored the exact Forge 47.4.16 deferred-work error template, including its newline and formatting code. Native Forge formatting, rather than ordinary Minecraft component formatting, verifies its extended arguments.
8. Translated and checked all 123 AE2 override pages per version, including four custom pages. Corrected missing diagrams, the export-bus recipe reference and six unavailable recipe panels. The latter now explain pack processing and direct the player to JEI; no recipes changed. Corrected six inherited English spelling errors per version. Full live compilation confirms the pages come from the KubeJS resource pack.

Each resource pack now contains 1,349 distinct language keys. The full version-update report describes the guide changes in more detail.

## Semantic and version checks

- Parsed all 97 quest files and compared non-display data against each version's own source. IDs, tasks, dependencies, commands, rewards, clickable actions and layout are preserved.
- Compared 2,960 Chinese-origin fields in 1450 with its archived Chinese quest book and 3,067 fields in 1452 with its own Chinese book. Reviewed 57 numeric candidates: written numerals, equivalent expressions, material identities and the documented Steam Oven exception. Dyson output remains **10,000A in 1450** and **20,000A in 1452**. Steam Oven is **256 parallels** in both checked builds.
- Reviewed repeated-English groups, material and machine titles, click controls and negations for shifted or incomplete descriptions. No further confirmed mismatch remained in the reviewed candidates. Red Granite and Tannin are the ordinary English material names. The newer Chinese title for `gtceu:ethylene_sulfide_bucket` incorrectly names a different chemical; the English retains the actual registered item's name, Ethylene Sulfide.
- All 19 installed KubeJS scripts were checked after applying each package's replacements. No Chinese remains in quoted display strings; comments are excluded. Item-registration mechanics match the source after removing only display names/tooltips from the parsed code. `misc.js` differs only in the approved message strings.
- English lookup covers 16,812 keys found in the old Chinese language tables and 18,129 in the newer tables, with no missing English entries or Chinese English-language values. Namespace-order checks ensure corrected names survive either order. Format arguments are retained.
- The newer Additions build's 80 default English guide pages contain no Chinese. Its intentionally separate Chinese-localized pages are excluded. No newer Additions guide or gameplay content was copied into 1450.

## Native and full-game verification

The actual GuideME 20.1.14/20.1.15 Markdown/frontmatter parsers, FTB Library 2001.2.12/2001.2.13 SNBT parsers, Minecraft components and Forge formatter all passed. The saved native report records the counts, including 1,336 Minecraft component keys and 13 Forge templates per version.

Both complete modpacks were then launched in separate disposable copies with the matching translation and newly generated worlds. No original save was copied. A test-only mod exercised the actual item registry, tooltip callbacks and guide compiler; it is absent from both installation packages.

| Check | 1450 | 1452 |
| --- | ---: | ---: |
| Registered item names | 18,669 | 18,766 |
| Normal + advanced fresh-world tooltip cases | 37,338 | 37,532 |
| Translated AE2 pages compiled | 123 | 123 |
| Remaining translation findings in those checks | 0 | 0 |

Three Stargate symbol tooltips require a connected client and fail if invoked at the title screen. All three were retested successfully in the fresh worlds. Representative native tooltips and seven guide pages per version were rendered for visual review. Runtime reports also check the previously reported spelling, amp counts, guide compiler errors and package hashes.

Reports: `verification-2026-10-17.json`, `native-api-verification-2026-10-17.json`, and `runtime-verification-2026-10-17.json`.

These results provide confidence in the checked translation packages, not proof of every possible gameplay or mod state. Held-key/NBT-dependent item states, multiplayer interactions and a complete progression playthrough were not exhaustively tested. Existing upstream recipe-registration, texture/model and Additions guide-navigation problems are outside this translation update. Original installed game files and saves remain unchanged; all changes are local for review.
