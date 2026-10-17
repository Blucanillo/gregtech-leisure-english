"""Exercise the installed FTB, GuideME and Minecraft/Forge text parsers.

These tests use the real installed libraries but do not launch Minecraft or
modify either reference instance. Compile outputs and logs stay in a temp dir.
"""
from pathlib import Path
from zipfile import is_zipfile
import argparse,json,os,shutil,subprocess,tempfile

ROOT=Path(__file__).resolve().parents[2]
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference-1450',type=Path,required=True)
    parser.add_argument('--reference-1452',type=Path,required=True)
    parser.add_argument('--libraries',type=Path,required=True,help='Minecraft launcher libraries directory')
    parser.add_argument('--java-bin',type=Path,required=True,help='JDK 21+ bin directory')
    args=parser.parse_args();lib=args.libraries;install=lib.parent
    java=args.java_bin/('java.exe'if os.name=='nt'else'java');javac=args.java_bin/('javac.exe'if os.name=='nt'else'javac')
    base=json.loads((install/'versions/1.20.1/1.20.1.json').read_text(encoding='utf-8'))
    forge=json.loads((install/'versions/forge-47.4.16/forge-47.4.16.json').read_text(encoding='utf-8'))
    common=[]
    def add(p):
        assert p.is_file()and is_zipfile(p),p
        if p not in common:common.append(p)
    for name in ['forge-1.20.1-47.4.16-client.jar','forge-1.20.1-47.4.16-universal.jar']:add(lib/'net/minecraftforge/forge/1.20.1-47.4.16'/name)
    for name in ['client-1.20.1-20230612.114412-srg.jar','client-1.20.1-20230612.114412-extra.jar']:add(lib/'net/minecraft/client/1.20.1-20230612.114412'/name)
    for kind in ['fmlcore','fmlloader','javafmllanguage','mclanguage','lowcodelanguage']:
        add(lib/f'net/minecraftforge/{kind}/1.20.1-47.4.16/{kind}-1.20.1-47.4.16.jar')
    for entry in base['libraries']+forge['libraries']:
        artifact=entry.get('downloads',{}).get('artifact')or{}
        if artifact.get('path'):
            p=lib/artifact['path']
            if p.is_file()and is_zipfile(p):add(p)
    references={'1450':args.reference_1450,'1452':args.reference_1452}
    versions={}
    sources=[ROOT/'maintenance/tools/native'/name for name in ['GuideParserProbe.java','FrontmatterProbe.java','QuestParserProbe.java','LanguageProbe.java']]
    with tempfile.TemporaryDirectory(prefix='gtl-native-apis-')as temporary:
        work=Path(temporary)
        compile_cp=common+[next((args.reference_1452/'mods').glob('guideme-*.jar')),next((args.reference_1452/'mods').glob('ftb-library-*.jar'))]
        subprocess.run([str(javac),'-proc:none','-cp',os.pathsep.join(map(str,compile_cp)),'-d',str(work),*map(str,sources)],cwd=work,check=True,capture_output=True)
        for version,inst in references.items():
            guide=next((inst/'mods').glob('guideme-*.jar'));ftb=next((inst/'mods').glob('ftb-library-*.jar'))
            cp=os.pathsep.join(map(str,[work,guide,ftb,*common]));folder=ROOT/version
            tests={
                'markdown':['GuideParserProbe',str(folder/'kubejs/assets/ae2/ae2guide'),str(work/f'ast-{version}')],
                'frontmatter':['FrontmatterProbe',str(folder/'kubejs/assets/ae2/ae2guide')],
                'quests':['QuestParserProbe',str(folder/'config/ftbquests/quests'),str(inst/'config/ftbquests/quests')],
                'language':['LanguageProbe',str(folder/f'resourcepacks/GTL{version}-English-resourcepack.zip'),str(lib/'net/minecraftforge/forge/1.20.1-47.4.16/forge-1.20.1-47.4.16-universal.jar')],
            }
            results={}
            for name,arguments in tests.items():
                process=subprocess.run([str(java),'-cp',cp,*arguments],cwd=work,capture_output=True,text=True,encoding='utf-8')
                if process.returncode:raise RuntimeError(f'{version}/{name}: {process.stdout}\n{process.stderr}')
                results[name]=process.stdout.strip()
            versions[version]={'guideme':guide.name,'ftb_library':ftb.name,'results':results}
    print(json.dumps({'result':'PASS','scope':'Real parser/component API execution; not a full game launch','versions':versions},indent=2))

if __name__=='__main__':main()
