# GregTech Leisure English Translation

For GTL1450 and for [GregTech Leisure 1.4.5.2 from CurseForge](https://www.curseforge.com/minecraft/modpacks/gregtech-leisure/files/8903963) (GTL1452).

## Supported versions

- **GTL1450 custom:** the older pack from [this Google Drive folder](https://drive.google.com/drive/folders/1Ga_w-TmDKNru0me1kAM_gXyedz_Ne4-x). Install the root `config` folder.
- **GTL1452:** [GregTech Leisure 1.4.5.2 from CurseForge](https://www.curseforge.com/minecraft/modpacks/gregtech-leisure/files/8903963). Install `GTL1452/config` instead.

The two versions have different quest books. Keep them separate; do not install the GTL1452 quests over GTL1450. The root `kubejs` scripts and English resource pack are shared by these two supported versions. Compatibility with other pack versions or newer GTLCore/GTLAdditions builds has not been established.

This is an add-on translation package: install the matching modpack separately first. It includes translated FTB Quests, KubeJS item names and tooltips, and a companion resource pack. The resource pack also supplies missing GTMThings names and corrects misspelled Dynamo Hatch names.

## Contents

```text
config/
  ftbquests/quests/                  Translated quest definitions (GTL1450)
GTL1452/
  config/ftbquests/quests/           Translated quest definitions (CurseForge 1.4.5.2)
kubejs/
  startup_scripts/item.js           Item registrations and translated names
  startup_scripts/tips.js           Translated item tooltips
  client_scripts/tips.js            Client-side tooltips
resourcepacks/
  GTL1450-English-resourcepack.zip   English language resources
```

## Installation

1. Fully close Minecraft and back up the instance, including any worlds. Keep copies of the existing `config/ftbquests/quests/` directory and the three KubeJS files listed above so you can restore them later.
2. Locate the GTL1450 or GTL1452 instance folder using your launcher's instance-folder option. This is the folder containing the instance's `config`, `kubejs`, and `resourcepacks` directories.
3. Copy this package's `kubejs` and `resourcepacks` folders into that instance folder. Then copy the `config` folder for your version: `config` for GTL1450, or `GTL1452/config` for CurseForge 1.4.5.2. Merge the folders and replace the matching files when prompted. Keep unrelated instance files. Do not copy the outer `AIO` folder or the `GTL1452` folder itself into the instance.
4. Keep `GTL1450-English-resourcepack.zip` zipped inside `resourcepacks/`. When updating, replace the previous copy instead of keeping multiple versions enabled.
5. Launch Minecraft. In **Options > Resource Packs**, enable **GTL1450 English**. Give it higher priority than other packs that replace the same translations.
6. Set the game language to **English (US)**, then fully exit and restart Minecraft.

A full restart is required for the KubeJS startup scripts. Reloading only the quest book does not apply the whole package.

## Installing individual components

- **Quest book:** Install `config/ftbquests/quests/` (GTL1450) or `GTL1452/config/ftbquests/quests/` (CurseForge 1.4.5.2) to use the translated quest definitions.
- **Language resources:** Enable the resource-pack ZIP to use its English language entries.
- **Item names and tooltips:** Install the three KubeJS scripts together with the resource pack. The scripts depend on its translation keys; missing resources can cause raw keys to appear instead of English text.

## Multiplayer use

Server administrators should back up and review the quest definitions before installing them. They include command rewards with `elevate_perms: true`, such as teleportation, night vision, and `/ftbultimine serverconfig`. The last command opens Ultimine's server configuration screen. Review that reward against your server's permission policy before making the quest book available to players.

Coordinate quest and startup-script changes with the server administrator. Players must enable the English resource pack on their own clients.

## Troubleshooting

- **Raw translation keys:** Check that the resource pack is enabled, has suitable priority, and is installed in the same instance as the KubeJS scripts. Fully restart the game.
- **Quest book still in Chinese:** Check that the quest directory for your version (`config/ftbquests/quests/` or `GTL1452/config/ftbquests/quests/`) was copied into the active instance and that the game language is English (US). On multiplayer servers, ask the administrator to check the server's quest definitions.
- **Script errors or unexpected item behavior:** Confirm that the instance matches GTL1450 or CurseForge 1.4.5.2 and that other custom scripts do not conflict with the replaced files. Restore the backup if necessary.

## Removing the package

Close Minecraft. Restore the original quest directory and the three KubeJS scripts from your backup, then disable or remove `GTL1450-English-resourcepack.zip`. Restart the game.

## Credits

- **English translation:** blucanillo, assisted by DeepSeek V4.1 Flash and ChatGPT Astra 6.
- **CurseForge 1.4.5.2 quest book and shared quest wording corrections:** [sgiath](https://github.com/sgiath), assisted by Claude Opus 5.5, based on blucanillo's GTL1450 translation. The matching shared-text corrections were also backported to GTL1450; version-specific mechanics remain separate.
- **Original modpack:** [GregTech Leisure](https://www.curseforge.com/minecraft/modpacks/gregtech-leisure), published by nutant233, and its contributors.
- **Included mods:** Their respective authors and contributors.

This is an unofficial community translation. AI-assisted text may contain translation errors.

## Attribution and licensing

This package builds on GregTech Leisure and its included mod content. No standalone redistribution license is included. Check the original project's permissions and preserve any required third-party notices when redistributing or adapting the files.

## Checking and rebuilding

The readable GTMThings fixes are in `resourcepack_overrides/assets/gtmthings/lang/en_us.json`. After editing them, run:

```text
python tools/build_resourcepack.py
python tools/verify_translations.py
```

The first command updates the distributed resource-pack ZIP. The second checks both quest books, known name/value regressions, formatting, clickable quest actions and script translation keys. To compare local quest changes with a previous revision, pass `--baseline <commit>`. For an additional language-coverage check against installed mods, pass `--mods "path/to/instance/mods"`; this option can be supplied for both supported versions.

The `tools` and `resourcepack_overrides` folders are for maintaining the translation; players only need the installation folders listed above. See [the correction notes](docs/translation-fixes-2026-10-15.md) for the reported issues, version-specific decisions and validation limits.
