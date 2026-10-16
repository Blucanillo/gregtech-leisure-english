"""Check quest safety, known regressions, language coverage and the built ZIP.

Run from any directory. Optional --mods arguments audit the installed GTMThings,
GTLCore, GTLAdditions and GTCEu language resources without modifying an instance.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile

from quest_snbt import Document, display_fields, lookup, without_component_text, without_display_text


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "resourcepacks/GTL1450-English-resourcepack.zip"
HAN = re.compile(r"[\u3400-\u9fff]")
FORMAT = re.compile(r"&[0-9a-fk-or]", re.I)
PLACEHOLDER = re.compile(r"%(?:\d+\$)?[sdif]")


def json_unique(pairs):
    out = {}
    for key, value in pairs:
        assert key not in out, f"Duplicate JSON key: {key}"
        out[key] = value
    return out


def load_json(data):
    return json.loads(data, object_pairs_hook=json_unique)


def git_bytes(ref, relative):
    return subprocess.check_output(["git", "show", f"{ref}:{relative}"], cwd=ROOT)


def validate_changes(before, after, label):
    assert without_display_text(before.value) == without_display_text(after.value), f"Gameplay data changed: {label}"
    before_fields = {path: value for _, _, path, value in display_fields(before.value)}
    after_fields = {path: value for _, _, path, value in display_fields(after.value)}
    assert before_fields.keys() == after_fields.keys(), f"Text field structure changed: {label}"
    count = 0
    for path, original in before_fields.items():
        translated = after_fields[path]
        if original == translated:
            continue
        count += 1
        assert Counter(FORMAT.findall(original)) == Counter(FORMAT.findall(translated)), f"Formatting codes changed: {label} {path}"
        for marker in ("{@pagebreak}",):
            assert original.count(marker) == translated.count(marker), f"Quest marker changed: {label} {path}"
        try:
            component = json.loads(original)
        except ValueError:
            continue
        if isinstance(component, (dict, list)):
            updated = json.loads(translated)
            assert without_component_text(component) == without_component_text(updated), f"Clickable component behavior changed: {label} {path}"
    return count


def quest_by_item(document, item):
    return next(q for q in document.value["quests"] if any(t.get("item") == item for t in q.get("tasks", [])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="HEAD", help="Existing Git revision to compare with")
    parser.add_argument("--mods", action="append", type=Path, default=[], help="Optional installed mods folder; may be supplied twice")
    args = parser.parse_args()
    counts = {}
    changed_strings = 0
    for prefix in ("config/ftbquests/quests", "GTL1452/config/ftbquests/quests"):
        files = sorted((ROOT / prefix).rglob("*.snbt"))
        expected = 48 if prefix.startswith("config/") else 49
        assert len(files) == expected, (prefix, len(files), expected)
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            text = path.read_text(encoding="utf-8-sig")
            assert not HAN.search(text), f"Chinese remains in English quests: {relative}"
            assert "\ufffd" not in text, f"Invalid replacement character: {relative}"
            document = Document(text)
            baseline = Document(git_bytes(args.baseline, relative).decode("utf-8-sig"))
            changed_strings += validate_changes(baseline, document, relative)
        counts[prefix] = len(files)

        steam = Document((ROOT / prefix / "chapters/77F8039ACE718C6C.snbt").read_text(encoding="utf-8"))
        steam_text = " ".join(quest_by_item(steam, "gtceu:steam_oven")["description"])
        assert "256 parallels" in steam_text, f"Steam Oven regression: {prefix}"
        dyson = Document((ROOT / prefix / "chapters/576CB57EB6B77F84.snbt").read_text(encoding="utf-8"))
        dyson_text = " ".join(quest_by_item(dyson, "gtceu:dyson_sphere")["description"])
        expected_amps = "10000A" if prefix.startswith("config/") else "20000A"
        assert expected_amps in dyson_text, f"Version-specific Dyson value changed: {prefix}"

    # This work must not change the shared item registration or tooltip logic.
    for path in (ROOT / "kubejs").rglob("*.js"):
        relative = path.relative_to(ROOT).as_posix()
        # Git may convert line endings on Windows; compare the actual script text.
        assert path.read_bytes().replace(b"\r\n", b"\n") == git_bytes(args.baseline, relative).replace(b"\r\n", b"\n"), f"Script behavior changed: {relative}"

    override_path = ROOT / "maintenance/resourcepack_overrides/assets/gtmthings/lang/en_us.json"
    overrides = load_json(override_path.read_text(encoding="utf-8"))
    with ZipFile(PACK) as archive:
        assert archive.testzip() is None, "Corrupt resource pack"
        names = archive.namelist()
        assert len(names) == len(set(names)), "Duplicate resource-pack entries"
        assert all(not n.startswith(("/", "\\")) and ".." not in Path(n).parts for n in names), "Unsafe ZIP entry"
        assert load_json(archive.read("assets/gtmthings/lang/en_us.json")) == overrides, "Build ZIP does not contain current overrides"
        combined = {}
        for name in names:
            if name.endswith("/lang/en_us.json"):
                mapping = load_json(archive.read(name))
                for key, value in mapping.items():
                    assert isinstance(value, str), key
                    assert not HAN.search(value), f"Chinese remains in English resource: {key}"
                    assert not re.search(r"Dynoma|\d+An\u00a7", value, re.I), f"Known spelling/spacing bug: {key}"
                    if key in combined:
                        assert combined[key] == value, f"Conflicting duplicate language key: {key}"
                    combined[key] = value
        # Existing language assets and pack metadata must retain their exact payloads.
        import io
        with ZipFile(io.BytesIO(git_bytes(args.baseline, "resourcepacks/GTL1450-English-resourcepack.zip"))) as old_archive:
            for name in old_archive.namelist():
                if name.endswith("/") or name == "assets/gtmthings/lang/en_us.json":
                    continue
                assert archive.read(name) == old_archive.read(name), f"Unrelated resource changed: {name}"

    def plain(text):
        return re.sub(r"\u00a7[0-9a-fk-or]", "", text, flags=re.I)

    expected = {
        "block.gtmthings.me_export_buffer": "ME Output Dual Hatch",
        "block.gtmthings.ev_64a_wireless_energy_input_hatch": "64A EV Wireless Energy Hatch",
        "block.gtmthings.ev_16a_wireless_energy_output_hatch": "16A EV Wireless Dynamo Hatch",
        "block.gtmthings.iv_67108863a_wireless_laser_source_hatch": "67108863A IV Wireless Laser Source Hatch",
        "block.gtmthings.iv_67108864a_wireless_laser_target_hatch": "67108864A IV Wireless Laser Target Hatch",
    }
    for key, value in expected.items():
        assert plain(combined[key]) == value, f"Reported-name regression: {key}"
    for kind in ("input", "output", "target", "source"):
        instruction = combined[f"gtmthings.machine.wireless_energy_hatch.{kind}.tooltip"]
        assert instruction.startswith("Right-click") and "left-click to unbind" in instruction, f"Reversed binding controls: {kind}"
    for key, value in overrides.items():
        match = re.search(r"_(\d+)a_wireless_", key)
        if match:
            assert plain(value).startswith(match.group(1) + "A "), f"Amperage changed: {key}"
        assert value != key, f"Raw language key in display text: {key}"

    referenced = set()
    for path in (ROOT / "kubejs").rglob("*.js"):
        referenced.update(re.findall(r'[\"\x27](gtl1450\.[^\"\x27\r\n]+)[\"\x27]', path.read_text(encoding="utf-8")))
    assert not referenced - combined.keys(), f"Missing script translations: {referenced - combined.keys()}"

    coverage = {}
    for folder in args.mods:
        english, chinese = {}, {}
        for jar in folder.glob("*.jar"):
            if not any(name in jar.name.lower() for name in ("gtceu", "gtlcore", "gtladditions", "gtmthings")):
                continue
            with ZipFile(jar) as archive:
                for name in archive.namelist():
                    target = english if name.endswith("/lang/en_us.json") else chinese if name.endswith("/lang/zh_cn.json") else None
                    if target is not None:
                        for key, value in load_json(archive.read(name)).items():
                            if "gtmthings." in key:
                                target[key] = value
        english.update(combined)
        missing = [key for key in chinese if key not in english or HAN.search(english[key])]
        assert not missing, f"Missing GTMThings English in {folder}: {missing}"
        for key, source in chinese.items():
            if key in overrides:
                assert PLACEHOLDER.findall(source) == PLACEHOLDER.findall(overrides[key]), f"Tooltip placeholders changed: {key}"
        remaining = [key for key, value in english.items() if re.search(r"Dynoma|\d+An\u00a7", value, re.I)]
        assert not remaining, f"Upstream typos still visible in {folder}: {remaining}"
        coverage[str(folder)] = len(chinese)

    print(json.dumps({"result": "PASS", "quest_files": counts, "changed_display_strings": changed_strings,
                      "gtmthings_overrides": len(overrides), "script_translation_keys": len(referenced),
                      "installed_gtmthings_keys_checked": coverage,
                      "gameplay_data": "unchanged", "clickable_actions": "unchanged", "scripts": "unchanged"}, indent=2))


if __name__ == "__main__":
    main()
