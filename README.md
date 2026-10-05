# GregTech Leisure English Translation

For GTL1450.

An English translation package for an existing GregTech Leisure GTL1450 instance. It includes translated FTB Quests content, KubeJS item names and tooltips, and a companion resource pack.

This is an add-on package. Install the GTL1450 modpack separately before using it. Use a matching GTL1450 instance; compatibility with other modpack versions has not been established.

## Contents

```text
config/
  ftbquests/quests/                  Translated quest definitions
kubejs/
  startup_scripts/item.js           Item registrations and translated names
  startup_scripts/tips.js           Translated item tooltips
  client_scripts/tips.js            Client-side tooltips
resourcepacks/
  GTL1450-English-resourcepack.zip   English language resources
```

## Installation

1. Fully close Minecraft and back up the instance, including any worlds. Keep copies of the existing `config/ftbquests/quests/` directory and the three KubeJS files listed above so you can restore them later.
2. Locate the GTL1450 instance folder using your launcher's instance-folder option. This is the folder containing the instance's `config`, `kubejs`, and `resourcepacks` directories.
3. Copy this package's `config`, `kubejs`, and `resourcepacks` folders into that instance folder. Merge the folders and replace the matching files when prompted. Keep unrelated instance files. Do not copy the outer `AIO` folder into the instance.
4. Keep `GTL1450-English-resourcepack.zip` zipped inside `resourcepacks/`.
5. Launch Minecraft. In **Options > Resource Packs**, enable **GTL1450 English**. Give it higher priority than other packs that replace the same translations.
6. Set the game language to **English (US)**, then fully exit and restart Minecraft.

A full restart is required for the KubeJS startup scripts. Reloading only the quest book does not apply the whole package.

## Installing individual components

- **Quest book:** Install `config/ftbquests/quests/` to use the translated quest definitions.
- **Language resources:** Enable the resource-pack ZIP to use its English language entries.
- **Item names and tooltips:** Install the three KubeJS scripts together with the resource pack. The scripts depend on its translation keys; missing resources can cause raw keys to appear instead of English text.

## Multiplayer use

Server administrators should back up and review the quest definitions before installing them. They include command rewards with `elevate_perms: true`, such as teleportation, night vision, and `/ftbultimine serverconfig`. The last command opens Ultimine's server configuration screen. Review that reward against your server's permission policy before making the quest book available to players.

Coordinate quest and startup-script changes with the server administrator. Players must enable the English resource pack on their own clients.

## Troubleshooting

- **Raw translation keys:** Check that the resource pack is enabled, has suitable priority, and is installed in the same instance as the KubeJS scripts. Fully restart the game.
- **Quest book still in Chinese:** Check that `config/ftbquests/quests/` was copied into the active instance and that the game language is English (US). On multiplayer servers, ask the administrator to check the server's quest definitions.
- **Script errors or unexpected item behavior:** Confirm that the instance matches GTL1450 and that other custom scripts do not conflict with the replaced files. Restore the backup if necessary.

## Removing the package

Close Minecraft. Restore the original quest directory and the three KubeJS scripts from your backup, then disable or remove `GTL1450-English-resourcepack.zip`. Restart the game.

## Credits

- **English translation:** blucanillo, assisted by DeepSeek V4.1 Flash and ChatGPT Astra 6.
- **Original modpack:** [GregTech Leisure](https://www.curseforge.com/minecraft/modpacks/gregtech-leisure), published by nutant233, and its contributors.
- **Included mods:** Their respective authors and contributors.

This is an unofficial community translation. AI-assisted text may contain translation errors.

## Attribution and licensing

This package builds on GregTech Leisure and its included mod content. No standalone redistribution license is included. Check the original project's permissions and preserve any required third-party notices when redistributing or adapting the files.
