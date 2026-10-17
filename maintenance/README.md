# Translation maintenance

Players install only the contents of their matching `1450` or `1452` folder.

- `resourcepack_overrides/`: readable language corrections merged into both packs without dropping existing keys. Keys used by different installed builds were checked independently.
- `tools/build_resourcepack.py`: deterministic rebuilding of both version-labelled ZIPs.
- `tools/verify_translations.py`: separate reference hash, quest, script behavior, language, namespace-order and guide-link checks. Requires Python with PyYAML, Node.js 24 (including its bundled Acorn parser) and Git. References are read-only.
- `tools/script_behavior_probe.cjs`: exercises item registration and tooltip callbacks, including wrapped Java strings, all universal tiers and dynamic language-key lookups. Native runtime testing remains authoritative for Java/Rhino integration.
- `tools/verify_native_apis.py`: executes the installed GuideME/FTB Library parsers and native Minecraft/Forge language formatters. Requires a Java 21 JDK and the matching Minecraft/Forge library directory. It compiles probes in temporary folders and does not launch the game.
- `tools/native/TranslationRuntimeAudit.java`: the source of the separate test-only Forge mod used for full Minecraft tests. It scans names, creates a **new world**, scans normal/advanced tooltips, compiles the translated AE2 pages, saves representative screenshots and closes the test client. Compile against the matching Forge/Minecraft/GuideME libraries and package with a `javafml` mods.toml only for a disposable test instance. Never add it to either installation package or an existing player instance.
- `docs/version-source-manifest.json`: exact reference hashes and the Git baseline.
- `docs/`: scope, consistency findings and saved file/native/full-game reports. The October 15 report describes the layout at that earlier date; current installation instructions are in the root README.

Run from the repository root, replacing the example paths:

```powershell
python maintenance/tools/build_resourcepack.py
python maintenance/tools/verify_translations.py --reference-1450 "X:/instances/GTL1450" --reference-1452 "X:/instances/GTL1452"
python maintenance/tools/verify_native_apis.py --reference-1450 "X:/instances/GTL1450" --reference-1452 "X:/instances/GTL1452" --libraries "X:/minecraft/Install/libraries" --java-bin "C:/Program Files/Eclipse Adoptium/jdk-21/bin"
```

The static, behavioral and native parser tools complement full-game checks. Neither alone proves every possible item state or gameplay interaction. Keep each version's source data separate, even where shared translations currently match.
