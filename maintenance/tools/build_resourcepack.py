"""Rebuild each version's existing resource pack with the readable JSON overrides."""
from pathlib import Path
import json
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT=Path(__file__).resolve().parents[2]

def build():
    for version in ('1450','1452'):
        pack=ROOT/version/f'resourcepacks/GTL{version}-English-resourcepack.zip'
        with ZipFile(pack) as z:
            assert z.testzip() is None
            files={n:z.read(n) for n in z.namelist() if not n.endswith('/')}
        for source in (ROOT/'maintenance/resourcepack_overrides').rglob('*.json'):
            relative=source.relative_to(ROOT/'maintenance/resourcepack_overrides').as_posix()
            updates=json.loads(source.read_bytes())
            merged=json.loads(files.get(relative,b'{}'));merged.update(updates)
            files[relative]=(json.dumps(merged,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
        temporary=pack.with_suffix('.zip.tmp')
        with ZipFile(temporary,'w',ZIP_DEFLATED,compresslevel=9) as z:
            for name,payload in sorted(files.items()):
                info=ZipInfo(name,(1980,1,1,0,0,0));info.compress_type=ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,payload,compresslevel=9)
        with ZipFile(temporary) as z:assert z.testzip() is None
        temporary.replace(pack)
        print(f'Built {pack.relative_to(ROOT)}: {len(files)} files')

if __name__=='__main__':build()
