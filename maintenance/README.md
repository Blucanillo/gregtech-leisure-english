# Translation maintenance

This folder contains support files for maintaining the translation. Players do not need to copy it into their Minecraft instance.

- `docs/`: [correction notes](docs/translation-fixes-2026-10-15.md).
- `resourcepack_overrides/`: readable GTMThings language fixes included in the distributed resource pack.
- `tools/`: resource-pack builder and translation checks.

From a Git checkout, run these commands at the repository root after editing the overrides:

```text
python maintenance/tools/build_resourcepack.py
python maintenance/tools/verify_translations.py
```

The builder updates `resourcepacks/GTL1450-English-resourcepack.zip`. The verifier checks both quest books, known name/value regressions, formatting, clickable quest actions and script translation keys. To compare quest changes with a previous revision, pass `--baseline <commit>`.

For language-coverage checks against installed mods, pass `--mods "path/to/instance/mods"`. This option can be supplied for both supported versions. The checks read installed files without modifying them.
