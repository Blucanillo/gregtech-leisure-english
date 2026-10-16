"""Rebuild the distributed ZIP with the readable resourcepack_overrides files."""

from pathlib import Path
import json
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "resourcepacks/GTL1450-English-resourcepack.zip"


def build():
    with ZipFile(PACK) as archive:
        if archive.testzip() is not None:
            raise ValueError("Existing resource pack is corrupt")
        files = {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
    for source in (ROOT / "maintenance/resourcepack_overrides").rglob("*.json"):
        relative = source.relative_to(ROOT / "maintenance/resourcepack_overrides").as_posix()
        payload = source.read_bytes()
        json.loads(payload.decode("utf-8"))
        files[relative] = payload
    temporary = PACK.with_suffix(".zip.tmp")
    with ZipFile(temporary, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for name, payload in sorted(files.items()):
            info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload, compresslevel=9)
    with ZipFile(temporary) as archive:
        if archive.testzip() is not None:
            raise ValueError("Rebuilt resource pack is corrupt")
    temporary.replace(PACK)
    print(f"Built {PACK.name}: {len(files)} files, {PACK.stat().st_size:,} bytes")


if __name__ == "__main__":
    build()
