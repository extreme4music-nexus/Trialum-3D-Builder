// Trialum World Builder project schema. Data-only, never trusted as game state.
export const SCHEMA_VERSION=1;
const clamp=(n,min,max,def)=>Number.isFinite(Number(n))?Math.max(min,Math.min(max,Number(n))):def;
const name=(s,fallback,max=100)=>String(s??fallback).trim().slice(0,max)||fallback;
const vector=(v,def,min=-1000,max=1000)=>Array.isArray(v)&&v.length===3?v.map((n,i)=>clamp(n,min,max,def[i])):[...def];
export function createProject(title="Моја прва просторија"){
 return {schemaVersion:SCHEMA_VERSION,projectId:"builder-"+Date.now().toString(36),name:title,
  description:"",room:{width:12,depth:12,height:4,gridSize:.5,showWalls:false,
   floorColor:"#526b60",wallColor:"#34494c"},
  instances:[],assets:[],bindings:{},meta:{editorVersion:"0.1.0",gameplayWrites:0,officialScene:false}};
}
export function sanitizeProject(raw){
 if(!raw||typeof raw!=="object"||raw.schemaVersion!==1||!Array.isArray(raw.instances))
  throw new Error("Неподдржан JSON проект. Потребна е шема schemaVersion=1 со instances.");
 if(raw.instances.length>6000)throw new Error("Сцената има премногу предмети (максимум 6000).");
 const src=raw.room||{};
 const p=createProject(name(raw.name,"Нов проект"));
 p.projectId=name(raw.projectId,p.projectId,80);
 p.description=name(raw.description,"",240);
 p.room={
  width:clamp(src.width,2,120,12),depth:clamp(src.depth,2,120,12),
  height:clamp(src.height,2,30,4),
  gridSize:[.05,.1,.25,.5,1].includes(Number(src.gridSize))?Number(src.gridSize):.5,
  showWalls:!!src.showWalls,
  floorColor:/^#[0-9a-f]{6}$/i.test(src.floorColor||"")?src.floorColor:"#526b60",
  wallColor:/^#[0-9a-f]{6}$/i.test(src.wallColor||"")?src.wallColor:"#34494c"
 };
 const ids=new Set();
 p.instances=raw.instances.map((it,i)=>{
  if(!it||typeof it!=="object")return null;
  let id=name(it.id,"obj"+i,80);
  if(ids.has(id))id+="-"+i;
  ids.add(id);
  const layer=["floor","wall","props","decor","structure"].includes(it.layer)?it.layer:"props";
  return {
   id,assetId:name(it.assetId,"block",120),
   label:name(it.label,"",100),
   position:vector(it.position,[0,0,0],-300,300),
   rotationY:clamp(it.rotationY,-20*Math.PI,20*Math.PI,0),
   scale:vector(it.scale,[1,1,1],.05,20),
   layer,locked:!!it.locked,visible:it.visible!==false,
   binding:name(it.binding,"",120),note:name(it.note,"",500),
  };
 }).filter(Boolean);
 p.assets=Array.isArray(raw.assets)?raw.assets.filter(a=>a&&typeof a==="object"&&typeof a.id==="string"&&
      (a.src||a.kind)).slice(0,500).map(a=>({
    id:name(a.id,"asset",120),name:name(a.name,"Модел",100),
    category:name(a.category,"Увезени",80),src:name(a.src||"","",240),
    kind:a.kind==="primitive"?"primitive":"glb",primitive:name(a.primitive||"box","box",40),
    dimensions:vector(a.dimensions,[1,1,1],.01,100),
    placement:["floor","wall","free"].includes(a.placement)?a.placement:"floor"
   })):[];
 return p;
}
export function downloadJson(value,filename){
 const blob=new Blob([JSON.stringify(value,null,2)+"\n"],{type:"application/json;charset=utf-8"});
 downloadBlob(blob,filename);
}
export function downloadBlob(blob,filename){
 const url=URL.createObjectURL(blob),link=document.createElement("a");
 link.href=url;link.download=filename;document.body.append(link);link.click();link.remove();
 setTimeout(()=>URL.revokeObjectURL(url),5000);
}
const mkLatin=Object.freeze({а:"a",б:"b",в:"v",г:"g",д:"d",ѓ:"gj",е:"e",ж:"zh",з:"z",ѕ:"dz",и:"i",ј:"j",к:"k",л:"l",љ:"lj",м:"m",н:"n",њ:"nj",о:"o",п:"p",р:"r",с:"s",т:"t",ќ:"kj",у:"u",ф:"f",х:"h",ц:"c",ч:"ch",џ:"dzh",ш:"sh"});
export function slug(s){
 const transliterated=[...name(s,"scene",80).normalize("NFKD").toLowerCase()].map(c=>mkLatin[c]??c).join("");
 return transliterated.replace(/[^a-z0-9_-]+/g,"-").replace(/-+/g,"-").replace(/^-|-$/g,"")||"scene";
}
export const clone=value=>JSON.parse(JSON.stringify(value));
export const snap=(value,step)=>Math.round(value/step)*step;
export function rectanglesOverlap(a,b,epsilon=0.0001){
 return a.minX<b.maxX-epsilon&&a.maxX>b.minX+epsilon&&a.minZ<b.maxZ-epsilon&&a.maxZ>b.minZ+epsilon;
}
export function validateProject(p){
 const errors=[];
 if(!p||p.schemaVersion!==1)errors.push("Невалидна верзија на шемата.");
 if(!p?.instances||!Array.isArray(p.instances))errors.push("Недостасуваат предмети.");
 for(const it of p?.instances||[]){
  if(!it.assetId||!it.id||it.position?.some(n=>!Number.isFinite(n)))errors.push("Неправилен предмет.");
 }
 return errors;
}
