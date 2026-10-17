# Original CurseForge 1.4.5.2 translation restoration

Source: [sgiath's PR #1](https://github.com/Blucanillo/gregtech-leisure-english/pull/1), commit `9d6230902c0053ad77419fe7e2a9c457ff157e15`.

The 49 files under `GTL1452/config/` were restored to `1452-curseforge/config/`. The three shared `kubejs/` scripts and `resourcepacks/GTL1450-English-resourcepack.zip` were restored from that same commit, as required by its original README. All 53 file contents are byte-identical to their Git source. The historic resource-pack filename is intentional.

The quest translation is by sgiath, assisted by Claude, based on blucanillo's translation. The original shared scripts/resource pack are blucanillo's work. No later custom-package changes were applied to this copy.

This preserves the contribution for unmodified CurseForge 1.4.5.2; it is not a fresh full-game compatibility certification. The existing runtime reports cover only the custom packages in `1450` and `1452`. The original may retain issues fixed in those later packages.

Install only the three folders inside `1452-curseforge` into the matching instance, after backing them up. Enable its GTL1450 English pack, select English (US), and restart Minecraft. Do not overlay it with either custom translation package. Applying this translation does not undo previously installed custom mods; use an unmodified CurseForge profile.

`1452-curseforge-restoration.json` records every original path and SHA-256 hash. The custom-package build and verification tools continue to target only `1450` and `1452`; they must not rewrite this preserved original.
