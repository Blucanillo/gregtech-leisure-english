"""Read-only checks of the prepared translation and its matching installed references."""
from pathlib import Path
import argparse, collections, hashlib, io, json, posixpath, re, shutil, subprocess, sys, tempfile
from zipfile import ZipFile
import yaml

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'maintenance/tools'))
from quest_snbt import Document, display_fields, without_display_text, without_component_text
MESSAGES={'需要手持数据': 'Hold the data item in your hand', '结构错误': 'Invalid structure', '消耗了 ': 'Consumed ', ' EU，使机器运行时间减少了 ': ' EU, reducing machine processing time by ', '可使用次数：': 'Uses remaining: ', '坐标已保存至该槽位': 'Coordinates saved to this slot', '飞行速度重置': 'Flight speed reset', '飞行速度x': 'Flight speed x', '达到极限': 'Maximum reached', '夜视关闭': 'Night vision disabled', '夜视开启': 'Night vision enabled', '坐标槽位：10': 'Coordinate slot: 10', '坐标槽位：0': 'Coordinate slot: 0', '坐标槽位：': 'Coordinate slot: ', '速度：10': 'Speed: 10', '速度：': 'Speed: ', '磁力吸引：关闭': 'Magnetic attraction: disabled', '磁力吸引：打开': 'Magnetic attraction: enabled'}
MANIFEST=json.loads((ROOT/'maintenance/docs/version-source-manifest.json').read_text())
HAN=re.compile('[\u3400-\u9fff]')
def sha(b):return hashlib.sha256(b).hexdigest()
def git(p):return subprocess.check_output(['git','-c',f'safe.directory={ROOT.as_posix()}','show',f'{MANIFEST["baseline_commit"]}:{p}'],cwd=ROOT)
def obj(s):return yaml.safe_load(s.split('---',2)[1])
def unique(pairs):
    d={}
    for k,v in pairs:
        assert k not in d,('Duplicate JSON key',k)
        d[k]=v
    return d
def load(b):return json.loads(b,object_pairs_hook=unique)
def tags(s):return collections.Counter(re.findall(r'<(?:ItemLink|ItemImage|BlockImage|RecipeFor|ImportStructure|Video|GameScene|BoxAnnotation|DiamondAnnotation|IsometricCamera|BlockGrid)\b[^>]*>',s))
def anchors(s):
    out=set();counts=collections.Counter()
    for heading in re.findall(r'^#{1,6}\s+(.+)$',s,re.M):
        h=re.sub(r'<[^>]*>','',heading).strip().lower()
        h=re.sub(r'[^\w\s-]','',h).replace(' ','-')
        n=counts[h];counts[h]+=1;out.add(h+(f'-{n}' if n else ''))
    out.update(re.findall(r'(?:id|name)="([^"]+)"',s))
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference-1450',type=Path,required=True,help='Read-only reference instance for 1450')
    parser.add_argument('--reference-1452',type=Path,required=True,help='Read-only reference instance for 1452')
    args=parser.parse_args()
    instances={'1450':args.reference_1450,'1452':args.reference_1452}
    result={};warnings=[]
    for version,record in MANIFEST['versions'].items():
        folder=ROOT/version;inst=instances[version]
        assert {p.name for p in folder.iterdir()}=={'config','kubejs','resourcepacks'}
        assert not any(p.suffix=='.jar' or p.name=='saves' for p in folder.rglob('*'))
        for name,h in record['mods'].items():assert sha((inst/'mods'/name).read_bytes())==h
        for rel,h in record['source_files'].items():assert sha((inst/rel).read_bytes())==h,('Reference changed',version,rel)
        qp='config/ftbquests/quests/';prefix='' if version=='1450' else 'GTL1452/'
        qs=sorted((folder/qp).rglob('*.snbt'));assert len(qs)==record['quest_files']
        assert {p.relative_to(folder/qp).as_posix() for p in qs}=={p.relative_to(inst/qp).as_posix() for p in (inst/qp).rglob('*.snbt')}
        totalq=totalt=totalr=0
        for p in qs:
            rel=p.relative_to(folder).as_posix();data=p.read_bytes();text=data.decode('utf-8-sig')
            assert without_display_text(Document(data.decode('utf-8-sig')).value)==without_display_text(Document(git(prefix+rel).decode('utf-8-sig')).value),('Quest moved incorrectly',version,rel)
            a=Document(text);b=Document((inst/rel).read_text(encoding='utf-8-sig'))
            assert without_display_text(a.value)==without_display_text(b.value),('Quest gameplay mismatch',version,rel)
            fields={path:text for _,_,path,text in display_fields(a.value)}
            oldfields={path:text for _,_,path,text in display_fields(b.value)}
            assert fields.keys()==oldfields.keys()
            for path,t in fields.items():
                assert not HAN.search(t)
                assert collections.Counter(re.findall(r'(?:&|§)[0-9a-fk-or]|\{@pagebreak\}',t,re.I))==collections.Counter(re.findall(r'(?:&|§)[0-9a-fk-or]|\{@pagebreak\}',oldfields[path],re.I))
                try:c=json.loads(oldfields[path])
                except ValueError:continue
                if isinstance(c,(list,dict)):assert without_component_text(c)==without_component_text(json.loads(t))
            q=a.value.get('quests',[]) if isinstance(a.value,dict) else [];totalq+=len(q);totalt+=sum(len(v.get('tasks',[]))for v in q);totalr+=sum(len(v.get('rewards',[]))for v in q)
        scripts=list((folder/'kubejs').rglob('*.js'));assert len(scripts)==4
        for p in scripts:
            rel=p.relative_to(folder).as_posix();text=p.read_text(encoding='utf-8-sig')
            subprocess.run([shutil.which('node') or 'node','--check',str(p)],check=True,capture_output=True)
            if p.name=='misc.js':
                expected=(inst/rel).read_text(encoding='utf-8-sig')
                for old,new in MESSAGES.items():expected=expected.replace('"'+old+'"','"'+new+'"')
                assert text==expected,('Unexpected script change',version,rel)
            else:
                expected=git(rel).decode('utf-8-sig').replace('\r\n','\n')
                if rel=='kubejs/startup_scripts/tips.js':
                    helper='    function display_tier(tier) {\n        if (tier === "luv") return "LuV"\n        if (tier === "opv") return "OpV"\n        return tier.toUpperCase()\n    }\n'
                    expected=expected.replace('    if (!LDLib.isClient()) return\n','    if (!LDLib.isClient()) return\n'+helper,1)
                    duration_patch='    // Native GTMThings duration text is a literal child component. Keep the\n    // energy component, original duration, and styles; translate that child only.\n    var digitalMinerIds = ["gtmthings:lv_digital_miner", "gtmthings:mv_digital_miner", "gtmthings:hv_digital_miner"]\n    var tooltipItemId = String(event.getItemStack().getId())\n    if (digitalMinerIds.indexOf(tooltipItemId) >= 0) {\n        var digitalMinerLines = event.getToolTip()\n        for (var minerLineIndex = 0; minerLineIndex < digitalMinerLines.size(); minerLineIndex++) {\n            var minerSiblings = digitalMinerLines.get(minerLineIndex).getSiblings()\n            for (var minerChildIndex = 0; minerChildIndex < minerSiblings.size(); minerChildIndex++) {\n                var minerChild = minerSiblings.get(minerChildIndex)\n                var minerDuration = /^§7\\u6bcf\\u4e2a\\u65b9\\u5757\\u9700\\u8981§f(\\d+)§7\\u523b。$/.exec(String(minerChild.getString()))\n                if (minerDuration) {\n                    minerSiblings.set(minerChildIndex, Component.translatable("gtl1450.tooltip.digital_miner_ticks", minerDuration[1]).setStyle(minerChild.getStyle()))\n                }\n            }\n        }\n    }\n    // Some Core material/generator hints are native literal components too.\n    // Match the exact original text; changed wording/numbers in another version\n    // will not be overwritten by a stale translation.\n    if (tooltipItemId.indexOf("gtceu:") === 0 && (tooltipItemId.indexOf("spacetime") >= 0 || tooltipItemId === "gtceu:chemical_energy_devourer")) {\n        var literalTranslations = {"\\u00a77\\u7194\\u70bc\\u4e3a\\u6d41\\u4f53\\u7684\\u65f6\\u7a7a": "gtl1450.tooltip.spacetime_fluid_hint", "\\u63d0\\u4f9b\\u00a7f120mB/s\\u00a77\\u7684\\u6db2\\u6001\\u6c27\\uff0c\\u5e76\\u6d88\\u8017\\u00a7f\\u53cc\\u500d\\u00a77\\u71c3\\u6599\\u4ee5\\u4ea7\\u751f\\u9ad8\\u8fbe\\u00a7f1048576\\u00a77EU/t\\u7684\\u529f\\u7387\\u3002": "gtl1450.tooltip.chemical_devourer_oxygen", "\\u518d\\u989d\\u5916\\u63d0\\u4f9b\\u00a7f80mB/s\\u00a77\\u7684\\u56db\\u6c27\\u5316\\u4e8c\\u6c2e\\uff0c\\u5e76\\u6d88\\u8017\\u00a7f\\u56db\\u500d\\u00a77\\u71c3\\u6599\\u4ee5\\u4ea7\\u751f\\u9ad8\\u8fbe\\u00a7f4194304\\u00a77EU/t\\u7684\\u529f\\u7387\\u3002": "gtl1450.tooltip.chemical_devourer_tetroxide"}\n        var coreTooltipLines = event.getToolTip()\n        for (var coreLineIndex = 0; coreLineIndex < coreTooltipLines.size(); coreLineIndex++) {\n            var coreLine = coreTooltipLines.get(coreLineIndex)\n            var originalLiteral = String(coreLine.getString())\n            if (Object.prototype.hasOwnProperty.call(literalTranslations, originalLiteral)) {\n                coreTooltipLines.set(coreLineIndex, Component.translatable(literalTranslations[originalLiteral]).setStyle(coreLine.getStyle()))\n            }\n        }\n    }\n'
                    expected=expected.replace('    if (!LDLib.isClient()) return\n','    if (!LDLib.isClient()) return\n'+duration_patch,1)
                    expected=expected.replace('tier_line(suprachronal.toUpperCase())','tier_line(display_tier(suprachronal))')
                    expected=expected.replace('addtooltip("\\u00a7d" + magneto_resonatic.toUpperCase() + text("gtl1450.tooltip.circuit_suffix"))','event.getToolTip().add(Component.literal("\\u00a77\\u00a7d" + display_tier(magneto_resonatic) + text("gtl1450.tooltip.circuit_suffix")))')
                if version=='1452':
                    expected=expected.replace('GTL1450 English localisation patch (KubeJS companion), revision 5','GTL1452 English localisation patch (shared gtl1450 language-key namespace)')
                    expected=expected.replace('GTL1450-English-resourcepack.zip','GTL1452-English-resourcepack.zip')
                assert text.replace('\r\n','\n')==expected,('Unexpected companion-script change',version,rel)
            assert not HAN.search(text)
        with ZipFile(folder/f'resourcepacks/GTL{version}-English-resourcepack.zip') as z:
            assert z.testzip() is None
            assert len(z.namelist())==len(set(z.namelist()))
            assert load(z.read('pack.mcmeta'))['pack']['pack_format']==15
            pack={};pack_by_namespace={}
            for name in z.namelist():
                assert name=='pack.mcmeta' or name.endswith('/lang/en_us.json')
                if not name.endswith('/lang/en_us.json'):continue
                mapping=load(z.read(name));pack_by_namespace[name.split('/')[1]]=mapping
                for k,v in mapping.items():
                    assert isinstance(v,str) and not HAN.search(v) and '\ufffd' not in v
                    if k in pack:assert pack[k]==v
                    pack[k]=v
            with ZipFile(io.BytesIO(git('resourcepacks/GTL1450-English-resourcepack.zip'))) as base:
                for name in base.namelist():
                    if name=='assets/gtmthings/lang/en_us.json':
                        old=load(base.read(name));current=load(z.read(name))
                        assert all(current.get(k)==v for k,v in old.items()),('Existing GTMThings correction regressed',version)
                    elif name=='assets/kubejs/lang/en_us.json':
                        old=load(base.read(name));current=load(z.read(name))
                        assert all(current.get(k)==v for k,v in old.items()),('Existing KubeJS translation regressed',version)
                    elif name=='assets/minecraft/lang/en_us.json':
                        old=load(base.read(name));current=load(z.read(name))
                        native_template='fml.modloading.failedtoprocesswork'
                        for key,value in old.items():
                            if key!=native_template:assert current.get(key)==value,('Existing Minecraft language regressed',version,key)
                        assert current[native_template]=='{0,modinfo,name} ({0,modinfo,id}) encountered an error processing deferred work\n\u00a77{2,exc,msg}'
                    elif name!='pack.mcmeta':assert base.read(name)==z.read(name),('Existing language regressed',version,name)
        refs=set()
        for p in scripts:refs.update(re.findall(r'["\x27](gtl1450\.[^"\x27\r\n]+)["\x27]',p.read_text(encoding='utf-8')))
        assert not refs-pack.keys()
        for amps in (262144,1048576,4194304):
            for direction in ('source','target'):
                key=f'block.gtmthings.ev_{amps}a_wireless_laser_{direction}_hatch'
                assert pack[key]==f'{amps}A \u00a75EV\u00a7r Wireless Laser {direction.title()} Hatch',('Live-registry name regression',version,key)
        with tempfile.TemporaryDirectory(prefix='gtl-tooltip-behavior-')as temporary:
            langfile=Path(temporary)/'english.json';langfile.write_text(json.dumps(pack),encoding='utf-8')
            process=subprocess.run([shutil.which('node')or'node','--expose-internals',str(ROOT/'maintenance/tools/script_behavior_probe.cjs'),str(folder),str(inst),str(langfile)],check=True,capture_output=True,text=True)
            behavior=json.loads(process.stdout)
        langs={'en_us':{},'zh_cn':{}};modkeys={};english_by_namespace={}
        for jar in (inst/'mods').glob('*.jar'):
            with ZipFile(jar) as z:
                for name in z.namelist():
                    match=re.fullmatch(r'assets/[^/]+/lang/(en_us|zh_cn)\.json',name)
                    if not match:continue
                    try:d=json.loads(z.read(name))
                    except (ValueError,UnicodeError):continue
                    langs[match[1]].update(d)
                    if match[1]=='en_us':english_by_namespace.setdefault(name.split('/')[1],{}).update(d)
                    if match[1]=='zh_cn' and jar.name in record['mods']:modkeys.setdefault(jar.name,set()).update(d)
        for p in (inst/'kubejs/assets').rglob('*.json'):
            if p.parent.name=='lang' and p.stem in langs:
                mapping=json.loads(p.read_text(encoding='utf-8-sig'));langs[p.stem].update(mapping)
                if p.stem=='en_us':english_by_namespace.setdefault(p.parent.parent.name,{}).update(mapping)
        langs['en_us'].update(pack)
        for namespace,mapping in pack_by_namespace.items():english_by_namespace.setdefault(namespace,{}).update(mapping)
        for namespace,mapping in english_by_namespace.items():
            assert not any(HAN.search(str(value)) for value in mapping.values()),('Namespace contains Chinese English values',version,namespace)
            for key,value in mapping.items():
                if key in pack:assert value==pack[key],('Cross-namespace override can undo correction',version,namespace,key,value,pack[key])
        # Resource namespaces may be visited in either order. Every corrected
        # key must end up with the intended value in both orderings.
        for namespaces in (list(english_by_namespace),list(reversed(english_by_namespace))):
            merged={}
            for namespace in namespaces:merged.update(english_by_namespace[namespace])
            assert all(merged.get(key)==value for key,value in pack.items()),('Namespace order changes translation',version)
        missing_global=[k for k in langs['zh_cn'] if k not in langs['en_us'] or HAN.search(str(langs['en_us'][k]))]
        assert not missing_global,('Untranslated mod language keys',version,missing_global)
        assert not any(re.search(r'\bDynoma\b|\bDynom[ao]\b|\bReciver\b|\bunknow user\b',str(v),re.I) for k,v in langs['en_us'].items() if 'gtmthings.' in k),('GTMThings typo regression',version)
        for key,value in pack.items():
            source=langs['zh_cn'].get(key)
            if not source:continue
            placeholders=lambda t:collections.Counter(re.sub(r'\d+\$','',v)for v in re.findall(r'%(?:\d+\$)?[sdf]',t))
            assert placeholders(source)==placeholders(value),('Formatting argument changed',version,key)
        steam_text=(folder/'config/ftbquests/quests/chapters/77F8039ACE718C6C.snbt').read_text(encoding='utf-8')
        assert steam_text.count('The Steam Oven is an exception, with 256 parallels.')==1
        assert '256 parallels' in steam_text
        dyson=(folder/'config/ftbquests/quests/chapters/576CB57EB6B77F84.snbt').read_text(encoding='utf-8')
        assert ('10000A' if version=='1450' else '20000A') in dyson
        resources=(folder/'config/ftbquests/quests/chapters/ziyuan.snbt').read_text(encoding='utf-8')
        assert 'ME Toggle Bus/Machine Controller Cover' in resources and 'Trigger Bus' not in resources
        assert not any(HAN.search(str(v)) for v in langs['en_us'].values()),('Chinese remains in an English language value',version)
        lex=re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|`(?:\\.|[^`\\])*`')
        installed_scripts=list((inst/'kubejs').rglob('*.js'))
        for source_script in installed_scripts:
            replacement=folder/source_script.relative_to(inst)
            chosen=replacement if replacement.exists() else source_script
            for match in lex.finditer(chosen.read_text(encoding='utf-8-sig')):
                if match.group().startswith(('//','/*')):continue
                assert not HAN.search(match.group()),('Untranslated script literal',version,source_script.relative_to(inst),match.group())
        english_additions_pages=0
        additions=next((inst/'mods').glob('gtladditions-*.jar'))
        with ZipFile(additions) as z:
            for name in z.namelist():
                if name.startswith('assets/') and name.endswith('.md') and '/_zh_cn/' not in name:
                    assert not HAN.search(z.read(name).decode('utf-8-sig')),('Chinese remains in default Additions guide',version,name)
                    english_additions_pages+=1
        coverage={}
        for mod,keys in modkeys.items():
            missing=[k for k in keys if k not in langs['en_us'] or HAN.search(str(langs['en_us'][k]))]
            assert not missing,('Language gaps',version,mod,missing)
            coverage[mod]=len(keys)
        guide=folder/'kubejs/assets/ae2/ae2guide';original=inst/'kubejs/assets/ae2/ae2guide'
        files={p.relative_to(guide).as_posix():p.read_text(encoding='utf-8') for p in guide.rglob('*.md')}
        assert len(files)==123
        with ZipFile(next((inst/'mods').glob('appliedenergistics2-*.jar'))) as native:
            for rel,en in files.items():
                cn=(original/rel).read_text(encoding='utf-8')
                assert not HAN.search(en) and '\ufffd' not in en
                cm,em=obj(cn),obj(en);cm['navigation']['title']=em['navigation']['title'];assert cm==em,('Metadata drift',rel)
                # Only a native extra quantum-link mention differs from original
                # technical markup; all original scene coordinates/IDs survive.
                a,b=tags(cn),tags(en)
                recipe_display_replacements={'items-blocks-machines/certus_quartz_crystal.md': {'<Recipe id="misc/deconstruction_certus_quartz_block" />': 'The standard block-to-crystal crafting recipe is disabled in this pack. Consult JEI for GregTech material processing with <ItemLink id="gtceu:certus_quartz_gem" />. The remaining AE2 transformation recipe is shown below.'}, 'items-blocks-machines/certus_quartz_dust.md': {'<RecipeFor id="certus_quartz_dust" />': 'GregTech Leisure uses <ItemLink id="gtceu:certus_quartz_dust" /> in its material recipes. Consult JEI for its processing routes; the standard AE2 Inscriber recipe is unavailable.'}, 'items-blocks-machines/controller.md': {'<RecipeFor id="controller" />': 'GregTech Leisure replaces the standard controller recipe. Consult JEI for the current recipe for <ItemLink id="controller" />.'}, 'items-blocks-machines/ender_dust.md': {'<RecipeFor id="ender_dust" />': 'GregTech Leisure uses <ItemLink id="gtceu:ender_pearl_dust" /> in its material recipes. Consult JEI for its processing routes; the standard AE2 Inscriber recipe is unavailable.'}, 'items-blocks-machines/fluix_pearl.md': {'<RecipeFor id="fluix_pearl" />': 'GregTech Leisure makes <ItemLink id="fluix_pearl" /> in a Lightning Processor. Consult JEI for the current machine recipe.'}, 'items-blocks-machines/patterns.md': {'<RecipeFor id="blank_pattern" />': 'GregTech Leisure makes <ItemLink id="blank_pattern" /> in an Assembler, with several material options and output quantities. Consult JEI for the current machine recipes.'}}
                for old,new in recipe_display_replacements.get(rel,{}).items():
                    assert old in cn and new in en,('Recipe display fix regressed',version,rel)
                    a.subtract(tags(old));a.update(tags(new));a=+a
                missing=a-b
                extras={'example-setups/bucket-emptier.md','example-setups/bucket-filler.md','example-setups/recursive-crafting-setup.md','items-blocks-machines/fluix_researcher.md'}
                if rel=='example-setups/main-network.md':
                    native_text=native.read('assets/ae2/ae2guide/'+rel).decode();assert not tags(native_text)-b
                elif rel in extras:
                    assert not any(re.search(r'<(?:ItemLink|RecipeFor|BlockImage)\b',tag) for tag in missing),('Lost functional reference',rel,missing)
                else:assert not missing,('Lost guide markup',version,rel,dict(missing))
                if rel not in {'example-setups/main-network.md','items-blocks-machines/quantum_bridge.md'}:assert not b-a,('Unexpected guide markup',rel,b-a)
                stack=[]
                for m in re.finditer(r'<(/?)([A-Z][A-Za-z0-9]*)\b([^>]*?)>',en):
                    close,tag,rest=m.groups()
                    if close:assert stack and stack.pop()==tag,('Unbalanced guide tag',rel,tag)
                    elif not rest.rstrip().endswith('/'):stack.append(tag)
                assert not stack,(rel,stack)
                parent=em.get('navigation',{}).get('parent');assert not parent or parent in files,(rel,parent)
                links=re.findall(r'\]\(([^)]+)\)',en)+re.findall(r'<ImportStructure\b[^>]*src="([^"]+)"',en)
                for url in links:
                    if re.match(r'\w+://',url):continue
                    target,_,anchor=url.partition('#');target=posixpath.normpath(posixpath.join(posixpath.dirname(rel),target)) if target else rel
                    exists=target in files or (original/target).is_file() or ('assets/ae2/ae2guide/'+target) in native.namelist()
                    if not exists:warnings.append([version,'missing guide target',rel,url]);continue
                    if anchor and target in files and anchor not in anchors(files[target]):warnings.append([version,'unresolved guide anchor',rel,url])
        result[version]={'quest_files':len(qs),'quests':totalq,'tasks':totalt,'rewards':totalr,'guide_pages':len(files),'scripts_syntax_checked':len(scripts),'status_lines_translated':20,'resource_pack_keys':len(pack),'script_behavior':behavior,'companion_keys':len(refs),'language_coverage':coverage,'all_mod_chinese_keys_checked':len(langs['zh_cn']),'namespace_order_verified':True,'remaining_language_gaps':len(missing_global),'installed_scripts_checked_for_chinese':len(installed_scripts),'bundled_english_additions_guide_pages':english_additions_pages}
    assert not warnings, warnings
    print(json.dumps({'result':'PASS','versions':result,'guide_findings':warnings},indent=2))

if __name__=='__main__':main()
