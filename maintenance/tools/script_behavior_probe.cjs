const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const acorn=require('internal/deps/acorn/acorn/dist/acorn');
const [pkg,instance,languageFile]=process.argv.slice(2);
const english=JSON.parse(fs.readFileSync(languageFile,'utf8'));
const read=(root,rel)=>fs.readFileSync(path.join(root,rel),'utf8').replace(/^\ufeff/,'');
function normalize(value){
  if(Array.isArray(value))return value.map(normalize);
  if(!value||typeof value!=='object')return value;
  if(value.type==='CallExpression'&&value.callee.type==='MemberExpression'&&['displayName','tooltip'].includes(value.callee.property.name))return normalize(value.callee.object);
  const result={};
  for(const [key,v]of Object.entries(value))if(!['start','end','raw'].includes(key))result[key]=normalize(v);
  return result;
}
const originalItem=read(instance,'kubejs/startup_scripts/item.js');
const translatedItem=read(pkg,'kubejs/startup_scripts/item.js');
assert.deepStrictEqual(normalize(acorn.parse(translatedItem,{ecmaVersion:'latest'})),normalize(acorn.parse(originalItem,{ecmaVersion:'latest'})),'Item registration mechanics differ');

let missing=[];
function components(language,strict=true){
  function component(text){return {value:text,append(other){this.value+=other.value;return this;},toString(){return this.value;}};}
  return {
    literal(value){assert.strictEqual(typeof value,'string','Literal input is not a JavaScript string');return component(value);},
    translatable(key,...args){
      if(strict && !(key in language))missing.push(key);
      let ordinal=0;
      const text=(language[key]??key).replace(/%(?:(\d+)\$)?[sdf]/g,(_,index)=>String(args[index?Number(index)-1:ordinal++]));
      const value=component(text);
      // Simulate a wrapped Java String: length is a method, not a JS number.
      value.string={toString:()=>text,valueOf:()=>text,length:()=>text.length};
      return value;
    }
  };
}
function registration(source,language,strict=true){
  const registrations=new Map();
  function builder(id){return new Proxy({}, {get:(_,method)=>(...args)=>{
    const entry=registrations.get(id);
    if(method==='tooltip')entry.tooltips.push(String(args[0]));
    if(method==='displayName')entry.displayName=String(args[0]);
    return builder(id);
  }});}
  const context={Component:components(language,strict),StartupEvents:{registry(type,fn){fn({create(id){assert(!registrations.has(id),'Duplicate item registration '+id);registrations.set(id,{tooltips:[],displayName:null});return builder(id);}});}},
    ItemEvents:{armorTierRegistry(fn){fn({add(id,configure){configure({});}});},modification(fn){fn({modify(id,configure){configure({setBurnTime(){}});}});}}};
  vm.runInNewContext(source,context,{timeout:2000});return registrations;
}
// Chinese source literals resolve without a dictionary; display-only calls
// added by the translation must resolve against the actual packaged entries.
const oldItems=registration(originalItem,english,false),newItems=registration(translatedItem,english);
assert.deepStrictEqual([...oldItems.keys()],[...newItems.keys()]);

function forgeTooltips(source,id,language,strict=true){
  let handler;const lines=[];
  const component=components(language,strict);
  const util=new Proxy({}, {get:(_,name)=>(text)=>{assert.strictEqual(typeof text,'string','Gradient received a wrapped Java String');assert(text.length>0,'Blank gradient');return `[${name}]${text}`;}});
  vm.runInNewContext(source,{Component:component,TextUtil:util,LDLib:{isClient:()=>true},ForgeEvents:{onEvent(type,fn){assert.strictEqual(type,'net.minecraftforge.event.entity.player.ItemTooltipEvent');handler=fn;}}},{timeout:2000});
  handler({getItemStack:()=>({getId:()=>id}),getToolTip:()=>({add(value){lines.push(String(value));},size:()=>lines.length,get:index=>lines[index],set(index,value){lines[index]=value;}})});
  return lines;
}
function clientTooltips(source,language,strict=true){
  const result=new Map();
  vm.runInNewContext(source,{Component:components(language,strict),ItemEvents:{tooltip(fn){fn({add(id,values){if(!Array.isArray(values))values=[values];assert(!result.has(id),'Repeated client tooltip registration '+id);result.set(id,values.map(String));}});}}},{timeout:2000});
  return result;
}
const startupRel='kubejs/startup_scripts/tips.js',clientRel='kubejs/client_scripts/tips.js';
const oldStartup=read(instance,startupRel),newStartup=read(pkg,startupRel);
const oldClient=clientTooltips(read(instance,clientRel),english,false),newClient=clientTooltips(read(pkg,clientRel),english);
const targets=new Set([...oldItems.keys()].map(id=>'kubejs:'+id));
for(const script of[oldStartup,newStartup,read(instance,clientRel),read(pkg,clientRel)]){
  for(const match of script.matchAll(/["']((?:kubejs|gtceu|minecraft|ad_astra):[^"'\s]+)["']/g))targets.add(match[1]);
}
let forgeLines=0;
for(const id of targets){
  const oldLines=forgeTooltips(oldStartup,id,english,false),newLines=forgeTooltips(newStartup,id,english);
  assert.strictEqual(newLines.length,oldLines.length,'Tooltip line count changed for '+id);
  for(const line of newLines){assert(line.length>0);assert(!/[\u3400-\u9fff]|gtl1450\./.test(line),'Untranslated or raw-key tooltip for '+id+': '+line);}
  forgeLines+=newLines.length;
}
for(const[id,values]of oldClient){assert(newClient.has(id),'Dropped tooltip target '+id);assert.strictEqual(newClient.get(id).length,values.length,'Client tooltip line count changed '+id);}
const tiers=['ulv','lv','mv','hv','ev','iv','luv','zpm','uv','uhv','uev','uiv','uxv','opv','max'];
for(const tier of tiers){
  const id='kubejs:'+tier+'_universal_circuit';assert(newClient.has(id));
  assert.strictEqual(newClient.get(id).length,oldItems.get(tier+'_universal_circuit').tooltips.length+(oldClient.get(id)?.length||0));
  assert(english['item.kubejs.'+tier+'_universal_circuit'],'Missing item name for '+id);
}
assert.strictEqual(newClient.size-oldClient.size,tiers.filter(tier=>!oldClient.has('kubejs:'+tier+'_universal_circuit')).length);
for(const [tier,label]of [['luv','LuV'],['opv','OpV']]) {
  const lines=forgeTooltips(newStartup,'kubejs:suprachronal_'+tier,english);
  assert(lines.some(line=>line.includes(label+' Circuit')),'Noncanonical tier spelling '+tier);
}
for(const[id,values]of newClient)for(const value of values)assert(value&&!/[\u3400-\u9fff]|gtl1450\./.test(value),'Bad client tooltip '+id);
assert.deepStrictEqual(missing,[],'Unknown dynamic translation keys');
console.log(JSON.stringify({result:'PASS',registered_items:newItems.size,item_mechanics_ast_identical:true,tooltip_targets_exercised:targets.size,forge_tooltip_lines:forgeLines,client_tooltip_targets:newClient.size,universal_circuit_tiers:tiers.length,missing_dynamic_keys:missing}));
