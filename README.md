# GregTech Leisure English Translation

Choose the folder matching your installed modpack. Each folder contains the installation files for its specific setup. The original CurseForge translation is preserved separately from the updated custom packages.

```text
1450/
  config/
  kubejs/
  resourcepacks/GTL1450-English-resourcepack.zip
1452/
  config/
  kubejs/
  resourcepacks/GTL1452-English-resourcepack.zip
1452-curseforge/
  config/
  kubejs/
  resourcepacks/GTL1450-English-resourcepack.zip
```

| Folder | Target setup |
| --- | --- |
| **1450** | GTL 1.4.5.0 custom, Core **1.2.2.8-fix2**, Additions **2.6.5Custom** |
| **1452** | Custom GTL 1.4.5.2 with Core **1.2.3.2-fix4**, Additions **3.3.1Custom** |
| **1452-curseforge** | Original unmodified CurseForge **1.4.5.2** release; sgiath's original PR #1 quest translation and its original companion files |

The two checked custom instances use Minecraft 1.20.1, GTCEu 1.4.4, AE2 15.4.10 and GTMThings 1.3.5.b. Other combinations need their own compatibility check.

**Use `1450` for the old custom setup, `1452` for the custom setup listed above, or `1452-curseforge` for the original CurseForge 1.4.5.2 setup. Install only one package.** Each folder supplies its own scripts and resource pack; you do not need files from the other folder.

## Installation

1. Close Minecraft and back up your instance. Locate its `.minecraft` folder, or the launcher instance folder containing `config`, `kubejs` and `resourcepacks`.
2. Open **1450**, **1452**, or **1452-curseforge**, matching your setup. Copy the **three folders inside it** (`config`, `kubejs`, `resourcepacks`) into the instance folder. Merge folders and replace matching files. Keep the resource-pack ZIP zipped.
3. Launch Minecraft, choose **English (US)**, and enable the matching **GTL1450 English** or **GTL1452 English** resource pack above other translation packs. If updating the custom **1452** setup from the previous shared package, disable/remove the old `GTL1450-English-resourcepack.zip` in that instance.
   For **1452-curseforge**, enable **GTL1450 English**: that historical filename is intentional and belongs to the original shared resource pack. Disable any other GTL English translation pack.
4. Fully exit Minecraft and restart it so the startup scripts are loaded.

**Keep the matching English resource pack enabled.** It supplies the KubeJS tooltip text as well as the translated mod labels.

Do not copy the outer `1450`, `1452`, or `1452-curseforge` folder itself into `.minecraft`. Server administrators should also install the matching quests and server/startup scripts; clients need the guide assets and resource pack.

## Original CurseForge translation

`1452-curseforge` restores [sgiath's original PR #1](https://github.com/Blucanillo/gregtech-leisure-english/pull/1) exactly: 49 quest files plus the three shared KubeJS scripts and resource-pack ZIP that its installation instructions specified. It targets [CurseForge 1.4.5.2](https://www.curseforge.com/minecraft/modpacks/gregtech-leisure/files/8903963), without the manual mod upgrades used by our custom setup.

This is a preserved original, including its original wording and limitations. It does not include our later fixes, AE2 manual translation or additional server messages. The custom-package runtime results below do not apply to this restored package; restoration was checked against the original Git files. See [restoration details](maintenance/docs/1452-curseforge-restoration.md).

## Included translations (custom packages)

- Version-specific quest books: **48 files for 1450**, **49 for 1452**. Quest IDs, tasks, rewards, commands, dependencies and layout are preserved for each version.
- KubeJS item names and tooltips, plus action messages for teleport slots, Time Twister, flight speed, night vision and Vajra controls.
- **123 English AE2 guide pages**, including the pack-added bucket-filling, bucket-emptying, recursive-crafting and Fluix Researcher pages. Available diagrams come from the installed AE2 version. Examples whose original diagrams were missing use text instructions instead.
- Resource packs with GTMThings name corrections, missing GTCEu entries, and AE2 guide/interface labels.

The 1450 and 1452 guide translations are the same because both checked instances contain byte-identical source pages and the same AE2 build. Each version was checked independently. The newer Additions build already supplies its own English guide.

## Verification and rollback

The October 2026 update passed separate file and native-parser checks for both versions, followed by real Minecraft tests in disposable copies with fresh worlds. These checked every registered item name, normal and advanced tooltips, and all 123 translated AE2 pages per version. The full findings and limits are in the [consistency audit](maintenance/docs/consistency-audit-2026-10-17.md). This translation does not fix the modpack's separate recipe-registration or Additions guide-navigation problems.

To undo installation, restore the overwritten `config` and `kubejs` files from your backup, remove the matching English resource-pack ZIP, and restart Minecraft.

## Credits

- **English translation:** blucanillo, with AI assistance.
- **1452 quest book and shared quest wording corrections:** [sgiath](https://github.com/sgiath), assisted by Claude, based on blucanillo's 1450 translation. Matching text corrections are retained in 1450 while its mechanics remain separate.
- **AE2 guide:** English text from the installed Applied Energistics 2 build and translations of the pack's additional material. Original content belongs to its authors.
- **Original modpack:** GregTech Leisure and its contributors; included mods belong to their respective authors.

This is an unofficial community translation. AI-assisted text may contain errors. No standalone redistribution license is included; preserve applicable upstream attribution and permissions.

Maintainer notes and checking tools are under [`maintenance/`](maintenance/README.md). Only the contents of your matching numbered folder belong in the game instance.
