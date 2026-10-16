# Translation corrections — 15 October 2026

This update addresses [incorrect Dynamo Hatch names (#2)](https://github.com/Blucanillo/gregtech-leisure-english/issues/2), [missing GTMThings names (#3)](https://github.com/Blucanillo/gregtech-leisure-english/issues/3), and the shared-text corrections contributed by [sgiath in PR #1](https://github.com/Blucanillo/gregtech-leisure-english/pull/1).

## Item names and tooltips

The installed GTMThings/GTLCore/GTLAdditions language resources have 224 GTMThings English gaps across the supported packs, including the two names shown in issue #3. The resource pack now fills those gaps. It displays `gtmthings:me_export_buffer` as **ME Output Dual Hatch** and the EV 64A wireless input hatch as **64A EV Wireless Energy Hatch**.

The overrides also correct 43 upstream **Dynoma** spellings, 40 malformed `An` amp separators, and consistent names for the same families of energy and laser hatches. Each amperage is taken from its own registry key: for example, 67,108,863A and 67,108,864A remain distinct. No item is renamed in the registry and no machine behavior changes.

The original English energy-hatch tooltips also reverse the binding controls. The installed GTMThings 1.3.5.b implementation binds in `onUse` (right-click) and unbinds in `onLeftClick`; input/output and laser hatch tooltips now describe these controls correctly. The misspelled “unknow user” message is corrected as well.

Related huge-bus names, wireless computation labels, missing tooltips and terminal settings are translated too. Runtime formatting placeholders are preserved. The readable overrides are versioned beside a builder so these fixes can be reviewed without inspecting only a binary ZIP.

## Quest corrections and version boundaries

518 differing text fields were backported from sgiath's GTL1452 English only where the **same quest/task ID, field and original Chinese string** also exist in GTL1450. This includes corrected machine/material names, misleading wording, incomplete sentences and text that previously belonged to another entry. The edits retain the old book's IDs, tasks, rewards, dependencies, layout and formatting codes. Clickable JSON descriptions preserve all fields other than their displayed text.

Two reported numbers required checking the installed machine code rather than blindly copying the newer text:

- **Dyson Sphere:** GTL1450's original Chinese correctly says **10,000A MAX**. Its Core 1.2.2.8-fix2 calculates output as `V[MAX] * moduleCount * efficiency`. Core 1.2.3.2-fix3 adds a factor of two, explaining GTL1452's **20,000A MAX** description. The older value is retained.
- **Steam Oven:** the old Chinese quest says eight parallels, but the installed GTL1450 Core's `SteamParallelMultiblockMachineMixin` explicitly gives `STEAM_OVEN` **256** parallels and half base duration. Its dedicated quest is corrected to 256. Both quest books' general steam-machine summaries now mention this exception instead of implying all small steam multiblocks have eight parallels.

Including the Steam Oven correction and the two summary clarifications, the update changes **520 distinct text fields across 29 quest files**: 519 fields in GTL1450 and one summary field in GTL1452. One old-book summary was already part of the shared-text backport, so it is counted only once. They do not copy newer quests, rewards or machines into the older pack.

## Validation

Run `python maintenance/tools/verify_translations.py --baseline e4c4777` to compare this update against the merged PR #1 baseline. Optional `--mods` arguments check coverage against the two installed mod sets.

The checks cover all 97 quest files, retained non-text quest data, clickable component behavior, formatting codes, page-break markers, resource-pack integrity, duplicate/conflicting language keys, GTMThings missing names, amp labels, format placeholders, all 67 literal companion-script translation keys, unchanged JavaScript and unchanged original resource-pack payloads. The resource-pack build is deterministic.

The separate numeric scan of GTL1450 was reviewed against its Chinese source. Remaining differences are translations of written Chinese numerals, equivalent expressions such as “doubles,” normalized material names, and the documented Steam Oven correction.

This is static validation against the installed files and extracted implementations. It is not a fresh in-game or multiplayer test. Existing upstream quest-link problems, if any, are not altered by this text-only update. A visual check after enabling the rebuilt pack remains useful for final appearance.
