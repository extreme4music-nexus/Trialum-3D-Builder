/* Trialum World Builder v0.1 — local-only modular level editor.
 * Geometry and scene layouts are design-only. No Trialum user/player state.
 * Three.js MIT, pinned and vendored locally under vendor/ by setup/CI.
 */
import * as THREE from "three";
import {OrbitControls} from "three/addons/controls/OrbitControls.js";
import {TransformControls} from "three/addons/controls/TransformControls.js";
import {GLTFLoader} from "three/addons/loaders/GLTFLoader.js";
import {createProject,sanitizeProject,downloadJson,downloadBlob,slug,clone,snap,rectanglesOverlap} from "./project.js";
import {exportLivingSpace} from "./living-spaces-adapter.js";

const $=id=>document.getElementById(id);
const ids=["projectName","saveIndicator","assetSearch","categoryFilter","catalog",
 "assetCounter","objectCounter","objectList","sceneCanvas","viewport","statusText",
 "noSelection","inspector","selectedAssetTitle","objLabel","posX","posY","posZ",
 "rotY","scaleVal","layerSelect","binding","objLocked","objVisible","roomWidth",
 "roomDepth","roomHeight","showWalls","surfaceMode","gridStep","snapEnabled",
 "toggleGrid","glbFileInput","projectFileInput"];
const ui=Object.fromEntries(ids.map(id=>[id,$(id)]));
const LOCAL_AUTOSAVE="trialum-3d-builder:scene-v1";
const CATALOG_URL="./assets/catalog.json";
const GLB_MAX_BYTES=32*1024*1024;
const loader=new GLTFLoader();
const math=THREE.MathUtils;
const state={
 project:createProject(),catalog:[],registry:new Map(),selectedId:null,selectedAssetId:null,
 tool:"select",roomMeshes:[],instanceMeshes:new Map(),history:[],historyIndex:-1,
 saveHandle:null,repoHandle:null,dirty:false,modelCache:new Map(),localUrls:new Map(),
 localFiles:new Map(),gridOn:true,dragging:false,dragChanged:false,
 busy:0,warningCount:0,modelAnimations:new Map(),animationMixers:new Map(),
};

const scene=new THREE.Scene();
scene.background=new THREE.Color("#172a2c");
scene.fog=new THREE.Fog("#172a2c",55,150);
const canvas=ui.sceneCanvas;
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false,powerPreference:"high-performance"});
renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));
renderer.outputColorSpace=THREE.SRGBColorSpace;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.45;
const camera=new THREE.PerspectiveCamera(54,1,.05,800);
camera.position.set(10,10,11);
const controls=new OrbitControls(camera,canvas);
controls.enableDamping=true;
controls.dampingFactor=.09;
controls.minDistance=.5;
controls.maxDistance=220;
controls.maxPolarAngle=Math.PI*.49;
controls.mouseButtons={LEFT:THREE.MOUSE.PAN,MIDDLE:THREE.MOUSE.DOLLY,RIGHT:THREE.MOUSE.ROTATE};
controls.target.set(0,0,0);
scene.add(new THREE.HemisphereLight(0xe4f4ec,0x61706b,2.4));
const sunlight=new THREE.DirectionalLight(0xffffff,3.2);
sunlight.position.set(-5,14,9);scene.add(sunlight);
const fill=new THREE.DirectionalLight(0x88b7b9,1.0);
fill.position.set(6,5,-7);scene.add(fill);
const contentRoot=new THREE.Group();contentRoot.name="Trialum_Design_Objects";scene.add(contentRoot);
const helpers=new THREE.Group();helpers.name="BuilderHelpers";scene.add(helpers);
const gizmo=new TransformControls(camera,canvas);
gizmo.setSpace("world");
const gizmoHelper=gizmo.getHelper();
scene.add(gizmoHelper);
gizmo.addEventListener("dragging-changed",event=>{
 state.dragging=!!event.value;
 controls.enabled=!event.value;
 if(!event.value&&state.dragChanged){
  const rec=getSelected(),mesh=rec&&state.instanceMeshes.get(rec.id);
  if(rec&&mesh){
   rec.position=mesh.position.toArray().map(n=>+n.toFixed(4));
   rec.rotationY=+mesh.rotation.y.toFixed(6);
   if(ui.snapEnabled.checked){
    rec.position=rec.position.map((n,i)=>i===1&&rec.layer==="floor"?0:snap(n,gridStep()));
    mesh.position.fromArray(rec.position);
   }
   markChanged();refreshInspector();warnIfCollision(rec);
  }
  state.dragChanged=false;
 }
});
gizmo.addEventListener("objectChange",()=>{state.dragChanged=true;refreshInspectorFromMesh();});
const raycaster=new THREE.Raycaster();
const pointer=new THREE.Vector2();
const floorPlane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
let floorMesh,grid,wallMeshes=[],lastPointerDown=null;
function say(message,warning=false){
 ui.statusText.textContent=message;
 ui.statusText.style.color=warning?"#f2be8b":"#b0dcc8";
 if(warning)console.warn("[Trialum Builder]",message);
}
function gridStep(){return Number(ui.gridStep.value)||.5;}
function id(){return "obj-"+Date.now().toString(36)+"-"+Math.random().toString(36).slice(2,7);}
function getSelected(){return state.project.instances.find(x=>x.id===state.selectedId);}
function assetById(assetId){return state.registry.get(assetId);}
function textureColor(asset){
 if(asset?.color)return asset.color;
 if(asset?.category?.includes("Растенија"))return "#6da77d";
 if(asset?.category?.includes("Земја"))return "#8f7659";
 return "#9cbdb1";
}

function roomHelpers(){
 state.roomMeshes.forEach(x=>helpers.remove(x));
 state.roomMeshes.length=0;wallMeshes=[];
 const {width,depth,height,showWalls,floorColor,wallColor}=state.project.room;
 const mat=new THREE.MeshStandardMaterial({color:floorColor,roughness:.96,metalness:0});
 floorMesh=new THREE.Mesh(new THREE.PlaneGeometry(width,depth),mat);
 floorMesh.rotation.x=-Math.PI/2;
 floorMesh.position.y=-.018;
 floorMesh.name="ReferenceFloor_NoGameplay";
 helpers.add(floorMesh);state.roomMeshes.push(floorMesh);
 grid=new THREE.GridHelper(Math.max(width,depth),Math.round(Math.max(width,depth)/gridStep()),0x63a68f,0x415a58);
 grid.position.y=.003;
 grid.material.transparent=true;grid.material.opacity=.68;grid.visible=state.gridOn;
 helpers.add(grid);state.roomMeshes.push(grid);
 const wallMat=new THREE.MeshStandardMaterial({color:wallColor,roughness:.85,transparent:true,opacity:showWalls?.22:.055,depthWrite:false,side:THREE.DoubleSide});
 const wallSpecs=[
  [width,height,0.01,0,height/2,-depth/2,0,"north"],
  [width,height,0.01,0,height/2,depth/2,0,"south"],
  [depth,height,0.01,-width/2,height/2,0,Math.PI/2,"west"],
  [depth,height,0.01,width/2,height/2,0,Math.PI/2,"east"]
 ];
 for(const [w,h,d,x,y,z,ry,side]of wallSpecs){
  const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),wallMat);
  mesh.position.set(x,y,z);mesh.rotation.y=ry;mesh.userData.wallSide=side;
  mesh.visible=showWalls;wallMeshes.push(mesh);helpers.add(mesh);state.roomMeshes.push(mesh);
 }
 ui.roomWidth.value=width;ui.roomDepth.value=depth;ui.roomHeight.value=height;
 ui.showWalls.checked=showWalls;
}
function syncGrid(){if(grid){grid.visible=state.gridOn;grid.geometry.dispose();const size=Math.max(state.project.room.width,state.project.room.depth);const fresh=new THREE.GridHelper(size,Math.round(size/gridStep()),0x63a68f,0x415a58);grid.geometry=fresh.geometry;grid.material=fresh.material;grid.position.y=.003;}}

function placeholder(asset,failed=false){
 const d=asset?.dimensions||[1,1,1];
 const group=new THREE.Group();
 const color=failed?"#9d615e":textureColor(asset);
 const shape=new THREE.Mesh(
  new THREE.BoxGeometry(d[0],d[1],d[2]),
  new THREE.MeshStandardMaterial({color,roughness:.61,metalness:.07,transparent:true,opacity:failed?.65:.86})
 );
 shape.position.set(d[0]/2,d[1]/2,d[2]/2);
 shape.castShadow=false;group.add(shape);
 const edge=new THREE.LineSegments(new THREE.EdgesGeometry(shape.geometry),new THREE.LineBasicMaterial({color:0xd0f1e0,transparent:true,opacity:.25}));
 edge.position.copy(shape.position);group.add(edge);
 return group;
}

async function db(){
 if(!("indexedDB" in window))throw Error("IndexedDB недостапна");
 return new Promise((resolve,reject)=>{
  const request=indexedDB.open("TrialumWorldBuilderAssets",1);
  request.onupgradeneeded=()=>request.result.createObjectStore("glbs");
  request.onsuccess=()=>resolve(request.result);
  request.onerror=()=>reject(request.error);
 });
}
async function cacheAsset(id,buffer){
 const d=await db();
 await new Promise((resolve,reject)=>{
  const tx=d.transaction("glbs","readwrite");
  tx.objectStore("glbs").put(buffer,id);
  tx.oncomplete=resolve;tx.onerror=()=>reject(tx.error);
 });d.close();
}
async function restoreAsset(id){
 const d=await db();
 const result=await new Promise((resolve,reject)=>{
  const tx=d.transaction("glbs","readonly"),r=tx.objectStore("glbs").get(id);
  r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);
 });
 d.close();return result;
}
async function glbUrl(asset){
 if(asset.src?.startsWith("local:")){
  if(state.localUrls.has(asset.id))return state.localUrls.get(asset.id);
  const array=state.localFiles.get(asset.id)||await restoreAsset(asset.id);
  if(!array)throw Error("Локалниот GLB не е достапен. Повтори го увозот: "+asset.name);
  const url=URL.createObjectURL(new Blob([array],{type:"model/gltf-binary"}));
  state.localUrls.set(asset.id,url);return url;
 }
 if(!asset.src)throw Error("Asset has no src");
 const safe=String(asset.src);
 if(!/^assets\/models\/[a-z0-9_.-]+\.glb$/i.test(safe))throw Error("Недозволена GLB патека");
 return "./"+safe;
}
async function modelObject(asset){
 if(!asset.src)return placeholder(asset);
 if(!state.modelCache.has(asset.id)){
  state.modelCache.set(asset.id,(async()=>{
   const url=await glbUrl(asset);
   const gltf=await loader.loadAsync(url);
   if(!gltf?.scene)throw Error("GLB без 3D сцена");
   state.modelAnimations.set(asset.id,gltf.animations||[]);
   return gltf.scene;
  })());
 }
 return (await state.modelCache.get(asset.id)).clone(true);
}
function sceneGroupFor(rec){
 const group=new THREE.Group();
 group.name=rec.label||rec.assetId;
 group.userData.instanceId=rec.id;
 group.position.fromArray(rec.position);
 group.rotation.y=rec.rotationY;
 group.scale.fromArray(rec.scale);
 group.visible=rec.visible;
 return group;
}
async function renderInstance(rec){
 const old=state.instanceMeshes.get(rec.id);
 if(old){if(gizmo.object===old)gizmo.detach();contentRoot.remove(old);state.animationMixers.delete(rec.id);}
 const root=sceneGroupFor(rec);
 state.instanceMeshes.set(rec.id,root);
 contentRoot.add(root);
 const asset=assetById(rec.assetId);
 if(!asset){root.add(placeholder({dimensions:[1,.5,1],color:"#b65e66"},true));return;}
 try{
  const obj=await modelObject(asset);
  if(state.instanceMeshes.get(rec.id)!==root)return;
  root.add(obj);
  const clips=state.modelAnimations.get(asset.id)||[];
  if(clips.length){const mixer=new THREE.AnimationMixer(obj);for(const clip of clips)mixer.clipAction(clip).play();state.animationMixers.set(rec.id,mixer);}
 }catch(e){
  console.error("Model load failed:",asset.id,e);
  if(state.instanceMeshes.get(rec.id)===root)root.add(placeholder(asset,true));
  say("Не можев да го вчитам "+asset.name+" — провери assets/models и setup.",true);
 }
 if(state.selectedId===rec.id&&!rec.locked)gizmo.attach(root);
}
function clearScene(){
 gizmo.detach();state.animationMixers.clear();
 for(const mesh of state.instanceMeshes.values())contentRoot.remove(mesh);
 state.instanceMeshes.clear();
}
async function rebuildScene(){
 clearScene();
 for(const item of state.project.instances)renderInstance(item);
 refreshObjectList();selectObject(state.selectedId,false);
}
function recordSnapshot(){
 const serial=JSON.stringify(state.project);
 if(state.history[state.historyIndex]===serial)return;
 state.history=state.history.slice(0,state.historyIndex+1);
 state.history.push(serial);
 if(state.history.length>60)state.history.shift();
 state.historyIndex=state.history.length-1;
}
function markChanged(){
 state.dirty=true;
 ui.saveIndicator.textContent="● Незачувани измени";
 ui.saveIndicator.style.color="#edb979";
 recordSnapshot();
 try{localStorage.setItem(LOCAL_AUTOSAVE,JSON.stringify(state.project));}catch{}
 updateCounters();
}
function markSaved(){
 state.dirty=false;
 ui.saveIndicator.textContent="● Зачуван проект";
 ui.saveIndicator.style.color="#8adbb4";
}
function undo(direction){
 const next=state.historyIndex+direction;
 if(next<0||next>=state.history.length)return;
 state.historyIndex=next;
 state.project=sanitizeProject(JSON.parse(state.history[next]));
 state.selectedId=null;
 ui.projectName.value=state.project.name;
 roomHelpers();rebuildScene();
 state.dirty=true;
 ui.saveIndicator.textContent="● Незачувани измени";
 try{localStorage.setItem(LOCAL_AUTOSAVE,JSON.stringify(state.project));}catch{}
 say(direction<0?"Вратен претходен чекор.":"Вратен следен чекор.");
}
function updateCounters(){
 $("objectCounter").textContent=state.project.instances.length;
 const all=[...state.registry.values()],real=all.filter(a=>a.src&&(a.src.endsWith(".glb")||a.src.startsWith("local:"))).length;
 $("assetCounter").textContent=real+" GLB · "+(all.length-real)+" макети";
}
function refreshObjectList(){
 ui.objectList.replaceChildren();
 if(!state.project.instances.length){
  const p=document.createElement("p");p.className="helper";
  p.textContent="Празна сцена. Избери модел и кликни на подот.";
  ui.objectList.append(p);return;
 }
 for(const rec of state.project.instances.slice().reverse()){
  const btn=document.createElement("div");
  btn.className="object-entry"+(rec.id===state.selectedId?" selected":"");
  btn.tabIndex=0;btn.setAttribute("role","button");
  const label=document.createElement("span");
  label.textContent=(rec.locked?"🔒 ":"")+(rec.visible?"":"◌ ")+(rec.label||assetById(rec.assetId)?.name||rec.assetId);
  const idEl=document.createElement("span");idEl.className="obj-count";idEl.textContent=rec.layer;
  btn.append(label,idEl);
  btn.onclick=()=>selectObject(rec.id);
  btn.onkeydown=e=>{if(e.key==="Enter")selectObject(rec.id)};
  ui.objectList.append(btn);
 }
}
function refreshInspector(){
 const rec=getSelected();
 ui.noSelection.hidden=!!rec;
 ui.inspector.hidden=!rec;
 if(!rec){refreshObjectList();return;}
 $("selectedAssetTitle").textContent=assetById(rec.assetId)?.name||rec.assetId;
 ui.objLabel.value=rec.label||"";
 ui.posX.value=+rec.position[0].toFixed(3);
 ui.posY.value=+rec.position[1].toFixed(3);
 ui.posZ.value=+rec.position[2].toFixed(3);
 ui.rotY.value=+(math.radToDeg(rec.rotationY).toFixed(2));
 ui.scaleVal.value=rec.scale[0];
 ui.layerSelect.value=rec.layer;
 ui.binding.value=rec.binding||"";
 ui.objLocked.checked=rec.locked;
 ui.objVisible.checked=rec.visible;
 refreshObjectList();
}
function refreshInspectorFromMesh(){
 const rec=getSelected(),root=rec&&state.instanceMeshes.get(rec.id);
 if(!root)return;
 ui.posX.value=+root.position.x.toFixed(3);
 ui.posY.value=+root.position.y.toFixed(3);
 ui.posZ.value=+root.position.z.toFixed(3);
 ui.rotY.value=+math.radToDeg(root.rotation.y).toFixed(2);
}
function selectObject(recId,speak=true){
 state.selectedId=state.project.instances.some(p=>p.id===recId)?recId:null;
 const rec=getSelected(),root=rec&&state.instanceMeshes.get(rec.id);
 gizmo.detach();
 if(root&&!rec.locked)gizmo.attach(root);
 if(speak&&rec)say("Избран: "+(rec.label||assetById(rec.assetId)?.name||rec.assetId));
 refreshInspector();
}
function chooseAsset(assetId){
 state.selectedAssetId=assetId;
 const asset=assetById(assetId);
 if(!asset)return;
 document.querySelectorAll(".asset-card").forEach(b=>b.classList.toggle("selected",b.dataset.assetId===assetId));
 setTool("place");
 ui.surfaceMode.value=asset.placement||"floor";
 say("Избрано: "+asset.name+". Кликни во 3Д сцената за поставување.");
}
function renderCatalogue(){
 const search=ui.assetSearch.value.trim().toLocaleLowerCase("mk");
 const cat=ui.categoryFilter.value;
 ui.catalog.replaceChildren();
 let n=0;
 for(const asset of state.registry.values()){
  if(cat&&asset.category!==cat)continue;
  if(search&&!((asset.name+" "+asset.id+" "+asset.category).toLocaleLowerCase("mk").includes(search)))continue;
  n++;
  const b=document.createElement("button");b.className="asset-card"+(state.selectedAssetId===asset.id?" selected":"");
  b.dataset.assetId=asset.id;b.setAttribute("role","option");b.title=asset.src?"GLB модел":"Развојна коцка/placeholder";
  const icon=document.createElement("span");icon.className="asset-icon";
  icon.textContent=asset.src?"⬡":asset.placement==="wall"?"▤":"▣";
  const div=document.createElement("span");const nm=document.createElement("span");nm.className="asset-name";nm.textContent=asset.name;
  const mt=document.createElement("small");mt.className="asset-meta";mt.textContent=asset.category+" · "+(asset.src?"GLB":"пример");
  div.append(nm,mt);b.append(icon,div);b.onclick=()=>chooseAsset(asset.id);ui.catalog.append(b);
 }
 if(!n){const p=document.createElement("p");p.className="helper";p.textContent="Нема такви модели.";ui.catalog.append(p);}
 updateCounters();
}
function refreshCategories(){
 const val=ui.categoryFilter.value;
 const categories=[...new Set([...state.registry.values()].map(a=>a.category||"Останато"))].sort();
 ui.categoryFilter.replaceChildren();
 for(const [v,label]of [["","Сите категории"],...categories.map(x=>[x,x])]){
  const op=document.createElement("option");op.value=v;op.textContent=label;ui.categoryFilter.append(op);
 }
 ui.categoryFilter.value=categories.includes(val)?val:"";
 renderCatalogue();
}
function setTool(tool){
 state.tool=tool;
 document.querySelectorAll("[data-tool]").forEach(el=>el.classList.toggle("active",el.dataset.tool===tool));
 gizmo.enabled=["select","move","rotate"].includes(tool);
 if(tool==="move")gizmo.setMode("translate");
 if(tool==="rotate")gizmo.setMode("rotate");
 if(tool==="select")gizmo.setMode("translate");
 if(tool==="erase")gizmo.detach();
 else if(getSelected()&&!getSelected().locked){
  const root=state.instanceMeshes.get(getSelected().id);
  if(root)gizmo.attach(root);
 }
 canvas.style.cursor=tool==="place"?"crosshair":tool==="erase"?"not-allowed":"default";
}
function screenRay(clientX,clientY){
 const rect=canvas.getBoundingClientRect();
 pointer.set((clientX-rect.left)/rect.width*2-1,-((clientY-rect.top)/rect.height*2-1));
 raycaster.setFromCamera(pointer,camera);return raycaster;
}
function hitSurface(ray){
 const mode=ui.surfaceMode.value;
 if(mode==="wall"){
  const r=ray.intersectObjects(wallMeshes,true);
  if(r.length){
   const hit=r[0],side=hit.object.userData.wallSide||"north";
   return {point:hit.point.clone(),rotationY:side==="east"?Math.PI/2:side==="west"?-Math.PI/2:side==="south"?Math.PI:0,side};
  }
  return null;
 }
 const hit=new THREE.Vector3();
 if(!ray.ray.intersectPlane(floorPlane,hit))return null;
 if(Math.abs(hit.x)>state.project.room.width/2+.2||Math.abs(hit.z)>state.project.room.depth/2+.2)return null;
 return {point:hit,rotationY:0,side:"floor"};
}
async function placeAsset(clientX,clientY){
 const asset=assetById(state.selectedAssetId);
 if(!asset){say("Прво избери GLB од библиотеката.",true);return;}
 const hit=hitSurface(screenRay(clientX,clientY));
 if(!hit){say("Кликни на подот или на видлив ѕид.",true);return;}
 let p=hit.point.toArray();
 if(ui.snapEnabled.checked)p=p.map((q,i)=>i===1&&ui.surfaceMode.value==="floor"?0:snap(q,gridStep()));
 if(ui.surfaceMode.value==="floor"||ui.surfaceMode.value==="free")p[1]=0;
 if(ui.surfaceMode.value==="wall")p[1]=Math.max(0,p[1]);
 const rec={id:id(),assetId:asset.id,label:"",position:p,rotationY:hit.rotationY,
  scale:[1,1,1],layer:ui.surfaceMode.value==="floor"?"floor":ui.surfaceMode.value==="wall"?"wall":"props",
  locked:false,visible:true,binding:"",note:""};
 state.project.instances.push(rec);
 await renderInstance(rec);
 selectObject(rec.id,false);
 markChanged();refreshObjectList();warnIfCollision(rec);
 say("Поставено: "+asset.name+" · X "+p[0]+", Z "+p[2]);
}
function hitObject(ray){
 const intersections=ray.intersectObjects([...state.instanceMeshes.values()],true);
 for(const hit of intersections){
  let n=hit.object;
  while(n&&n!==contentRoot){
   if(n.userData.instanceId)return n.userData.instanceId;
   n=n.parent;
  }
 }
 return null;
}
function deleteSelected(){
 const rec=getSelected();
 if(!rec||rec.locked){say("Нема предмет за бришење или е заклучен.",true);return;}
 const object=state.instanceMeshes.get(rec.id);
 if(object){gizmo.detach();contentRoot.remove(object);}
 state.instanceMeshes.delete(rec.id);
 state.project.instances=state.project.instances.filter(x=>x.id!==rec.id);
 selectObject(null,false);markChanged();
 say("Предметот е избришан.");
}
async function duplicateSelected(){
 const rec=getSelected();
 if(!rec)return;
 const duplicate=clone(rec);
 duplicate.id=id();duplicate.label=(rec.label||assetById(rec.assetId)?.name||"Модел")+" · копија";
 duplicate.position[0]=+(duplicate.position[0]+gridStep()).toFixed(4);
 state.project.instances.push(duplicate);await renderInstance(duplicate);
 selectObject(duplicate.id,false);markChanged();say("Направена копија.");
}
function warnIfCollision(rec){
 const asset=assetById(rec.assetId);
 if(!asset||rec.layer!=="floor"||asset.id.startsWith("f01-d"))return;
 const w=(asset.dimensions?.[0]||1)*rec.scale[0],d=(asset.dimensions?.[2]||1)*rec.scale[2];
 const box={minX:rec.position[0],maxX:rec.position[0]+w,minZ:rec.position[2],maxZ:rec.position[2]+d};
 const overlaps=state.project.instances.filter(other=>{
  if(other.id===rec.id||other.layer!=="floor"||other.assetId.startsWith("f01-d")||!other.visible)return false;
  const a=assetById(other.assetId);if(!a)return false;
  const ow=(a.dimensions?.[0]||1)*other.scale[0],od=(a.dimensions?.[2]||1)*other.scale[2];
  return rectanglesOverlap(box,{minX:other.position[0],maxX:other.position[0]+ow,minZ:other.position[2],maxZ:other.position[2]+od});
 });
 if(overlaps.length)say("Внимание: предметот се преклопува со "+overlaps.length+" други. Само предупредување.",true);
}
function applyInspector(){
 const rec=getSelected();if(!rec){say("Прво избери предмет.",true);return;}
 if(rec.locked&&ui.objLocked.checked){say("За да го отклучиш, исклучи Заклучен предмет, па Примени.",true);return;}
 const pos=[ui.posX,ui.posY,ui.posZ].map((node,i)=>Number.isFinite(Number(node.value))?math.clamp(Number(node.value),-300,300):rec.position[i]);
 const scale=math.clamp(Number(ui.scaleVal.value)||1,.05,20);
 rec.label=ui.objLabel.value.slice(0,100);
 rec.position=pos;
 rec.rotationY=math.degToRad(math.clamp(Number(ui.rotY.value)||0,-3600,3600));
 rec.scale=[scale,scale,scale];
 rec.layer=ui.layerSelect.value;
 rec.binding=ui.binding.value.slice(0,120);
 rec.visible=ui.objVisible.checked;
 rec.locked=ui.objLocked.checked;
 const mesh=state.instanceMeshes.get(rec.id);
 if(mesh){
  mesh.position.fromArray(rec.position);
  mesh.rotation.y=rec.rotationY;mesh.scale.fromArray(rec.scale);mesh.visible=rec.visible;
 }
 if(rec.locked)gizmo.detach();else if(mesh)gizmo.attach(mesh);
 markChanged();refreshInspector();warnIfCollision(rec);
 say("Промените се зачувани во сцената.");
}
function newProject(){
 if(state.dirty&&!confirm("Има незачувани промени. Да отвориме празна сцена?"))return;
 state.project=createProject();
 state.selectedId=null;state.history=[];state.historyIndex=-1;state.saveHandle=null;
 ui.projectName.value=state.project.name;
 roomHelpers();rebuildScene();recordSnapshot();markSaved();
 say("Нова просторија е подготвена.");
}
function useProject(raw,fromDisk=false){
 const project=sanitizeProject(raw);
 state.project=project;state.selectedId=null;state.history=[];state.historyIndex=-1;
 state.saveHandle=fromDisk?state.saveHandle:null;
 for(const asset of project.assets)state.registry.set(asset.id,asset);
 ui.projectName.value=project.name;
 roomHelpers();syncGrid();refreshCategories();rebuildScene();
 recordSnapshot();
 if(fromDisk)markSaved();else markChanged();
 say("Отворен проект: "+project.name+" · "+project.instances.length+" предмети.");
}
function collectProject(){
 state.project.name=ui.projectName.value.trim().slice(0,100)||"Без име";
 state.project.room.gridSize=gridStep();
 return sanitizeProject(state.project);
}
async function saveText(fileHandle,text){
 const writer=await fileHandle.createWritable();
 try{await writer.write(text);await writer.close();}
 catch(e){await writer.abort().catch(()=>{});throw e;}
}
async function ensureDirectory(root,name){return root.getDirectoryHandle(name,{create:true});}
async function saveProjectToRepo(){
 if(!("showDirectoryPicker" in window)){
  downloadJson(collectProject(),slug(state.project.name)+".json");
  markSaved();say("JSON е преземен. Премести го во projects/ од GitHub Desktop.");return;
 }
 try{
  if(!state.repoHandle){
   const root=await window.showDirectoryPicker({id:"trialum-builder-repository",mode:"readwrite"});
   try{await root.getFileHandle("package.json",{create:false})}
   catch{if(!confirm("Избраната папка можеби не е Trialum-3D-Builder. Сепак да ја користиме?"))return;}
   state.repoHandle=root;
  }
  const dir=await ensureDirectory(state.repoHandle,"projects");
  // Import GLBs into Git-tracked assets/models/ before writing their references.
  let changedCatalogue=false;
  const assetsDir=await ensureDirectory(state.repoHandle,"assets");
  const modelsDir=await ensureDirectory(assetsDir,"models");
  for(const asset of state.project.assets){
   if(!asset.src?.startsWith("local:"))continue;
   const bytes=state.localFiles.get(asset.id)||await restoreAsset(asset.id);
   if(!bytes)throw new Error("Не е достапен увезениот GLB "+asset.name);
   const filename=(asset.fileName||slug(asset.id)+".glb").replace(/[^a-z0-9_.-]/gi,"_");
   const h=await modelsDir.getFileHandle(filename,{create:true});
   const writer=await h.createWritable();await writer.write(bytes);await writer.close();
   asset.src="assets/models/"+filename;
   changedCatalogue=true;
   state.modelCache.delete(asset.id);
  }
  if(changedCatalogue){
   let prev={schemaVersion:1,name:"Trialum World Builder GLB catalogue",assets:[]};
   try{const h=await assetsDir.getFileHandle("catalog.json");prev=JSON.parse(await (await h.getFile()).text())}
   catch{}
   const m=new Map((prev.assets||[]).map(a=>[a.id,a]));
   for(const a of state.project.assets)m.set(a.id,a);
   const file=await assetsDir.getFileHandle("catalog.json",{create:true});
   await saveText(file,JSON.stringify({...prev,assets:[...m.values()]},null,2)+"\n");
  }
  const slugName=slug(state.project.name)+".json";
  const file=await dir.getFileHandle(slugName,{create:true});
  await saveText(file,JSON.stringify(collectProject(),null,2)+"\n");
  markSaved();say("Зачувано во projects/"+slugName+". Во GitHub Desktop направи Commit → Push.");
 }catch(e){if(e.name!=="AbortError")say("Зачувувањето не успеа: "+e.message,true);}
}
async function fileOpen(file){
 if(!file)return;
 if(file.size>3*1024*1024)throw Error("Проектот е преголем");
 const contents=JSON.parse(await file.text());
 useProject(contents,true);
}
async function importGlbs(files){
 for(const file of files){
  if(!file.name.toLowerCase().endsWith(".glb")||file.size>GLB_MAX_BYTES){say("Се прифаќаат .glb до 32 MB.",true);continue;}
  const bytes=await file.arrayBuffer();
  const view=new DataView(bytes);
  if(bytes.byteLength<20||view.getUint32(0,true)!==0x46546c67||view.getUint32(4,true)!==2){
   say("Ова не е исправен GLB 2.0: "+file.name,true);continue;
  }
  const key="custom-"+slug(file.name.replace(/\.glb$/i,""))+"-"+Math.random().toString(36).slice(2,7);
  const name=file.name.replace(/\.glb$/i,"").slice(0,100);
  const asset={id:key,name,category:"Мои модели",kind:"glb",src:"local:"+key,
   fileName:slug(name)+"-"+Math.random().toString(36).slice(2,6)+".glb",
   dimensions:[1,1,1],placement:"floor",origin:"original"};
  state.localFiles.set(key,bytes);
  try{await cacheAsset(key,bytes)}catch(e){say("GLB е вчитан, но не може да се чува во browser cache: "+e.message,true);}
  state.registry.set(key,asset);
  state.project.assets.push(asset);
  try{
   const object=await modelObject(asset);
   const box=new THREE.Box3().setFromObject(object),dims=new THREE.Vector3();
   box.getSize(dims);
   asset.dimensions=dims.toArray().map(n=>Math.max(.01,+n.toFixed(3)));
  }catch(e){say("GLB увезен, но проверката на геометријата не успеа: "+e.message,true);}
  say("Увезен GLB: "+name+". Избери го од Мои модели, па зачувај во GitHub папката.");
 }
 refreshCategories();markChanged();
}
function zipU16(x){return [x&255,(x>>>8)&255]}
function zipU32(x){return [x&255,(x>>>8)&255,(x>>>16)&255,(x>>>24)&255]}
function crc32(bytes){let c=0xffffffff;for(const b of bytes){c^=b;for(let k=0;k<8;k++)c=(c>>>1)^(0xedb88320&-(c&1));}return(c^0xffffffff)>>>0;}
function makeZip(files){
 const enc=new TextEncoder(),local=[],central=[];
 let offset=0;
 for(const [filename,source]of files){
  const name=enc.encode(filename);
  const data=source instanceof Uint8Array?source:enc.encode(String(source));
  const crc=crc32(data),size=data.byteLength;
  const localHead=Uint8Array.from([...zipU32(0x04034b50),...zipU16(20),...zipU16(0x0800),
    ...zipU16(0),...zipU16(0),...zipU16(0),...zipU32(crc),...zipU32(size),
    ...zipU32(size),...zipU16(name.length),...zipU16(0)]);
  local.push(localHead,name,data);
  const cent=Uint8Array.from([...zipU32(0x02014b50),...zipU16(20),...zipU16(20),...zipU16(0x0800),
    ...zipU16(0),...zipU16(0),...zipU16(0),...zipU32(crc),...zipU32(size),
    ...zipU32(size),...zipU16(name.length),...zipU16(0),...zipU16(0),...zipU16(0),
    ...zipU16(0),...zipU32(0),...zipU32(offset)]);
  central.push(cent,name);
  offset+=localHead.length+name.length+size;
 }
 const centralLength=central.reduce((n,b)=>n+b.length,0);
 const end=Uint8Array.from([...zipU32(0x06054b50),...zipU16(0),...zipU16(0),
   ...zipU16(files.length),...zipU16(files.length),...zipU32(centralLength),...zipU32(offset),...zipU16(0)]);
 return new Blob([...local,...central,end],{type:"application/zip"});
}
async function exportBundle(){
 const p=collectProject(),assets=p.assets,files=[];
 files.push(["projects/"+slug(p.name)+".json",JSON.stringify(p,null,2)+"\n"]);
 for(const asset of assets){
  if(!asset.src?.startsWith("local:"))continue;
  const raw=state.localFiles.get(asset.id)||await restoreAsset(asset.id);
  if(!raw){say("Не е достапен GLB за ZIP: "+asset.name,true);return;}
  const filename=asset.fileName||slug(asset.name)+".glb";
  files.push(["assets/models/"+filename,new Uint8Array(raw)]);
 }
 const cat={schemaVersion:1,name:"Trialum World Builder export models",assets:assets.map(x=>({
  ...x,src:x.src.startsWith("local:")?"assets/models/"+(x.fileName||slug(x.name)+".glb"):x.src
 }))};
 // Bundle includes an additive custom-catalogue recipe, not replacement for
 // the existing library. Direct folder save merges with assets/catalog.json.
 files.push(["my-imported-assets.json",JSON.stringify(cat,null,2)+"\n"]);
 files.push(["README-IMPORT.txt","Unzip into your cloned Trialum-3D-Builder repo.\nCopy GLBs to assets/models/ and project JSON to projects/.\nFor imported assets merge my-imported-assets.json assets into assets/catalog.json, or use the in-browser Save button instead.\nOriginal bundled Trialum models must remain in repo; do not delete them.\n"]);
 downloadBlob(makeZip(files),slug(p.name)+"-builder-export.zip");
 say("Извезен ZIP. За автоматско додавање GLB во Git repo користи Зачувај.");
}

function isTyping(e){return ["INPUT","TEXTAREA","SELECT"].includes(document.activeElement?.tagName)||document.activeElement?.isContentEditable}
function handleKey(e){
 if(isTyping(e))return;
 const ctrl=e.ctrlKey||e.metaKey;
 if(ctrl&&e.key.toLowerCase()==="s"){e.preventDefault();saveProjectToRepo();return;}
 if(ctrl&&e.key.toLowerCase()==="z"){e.preventDefault();undo(-1);return;}
 if(ctrl&&(e.key.toLowerCase()==="y"||e.shiftKey&&e.key.toLowerCase()==="z")){
  e.preventDefault();undo(1);return;
 }
 if(ctrl&&e.key.toLowerCase()==="d"){e.preventDefault();duplicateSelected();return;}
 if(["Delete","Backspace"].includes(e.key)){e.preventDefault();deleteSelected();return;}
 const key=e.key.toLowerCase(),map={v:"select",p:"place",g:"move",r:"rotate"};
 if(map[key]){e.preventDefault();setTool(map[key]);}
}

// Explicit local GitHub sync. Browser never receives credentials or runs arbitrary commands.
let gitToken="";
async function githubSync(action){
 if(!["pull","publish"].includes(action))return;
 if(state.dirty){say("Прво Зачувај ги измените во клонираната Builder папка.",true);return;}
 const btn=$("git"+(action==="pull"?"Pull":"Publish"));
 btn.disabled=true;
 try{
  const statusResponse=await fetch("./api/git-status",{cache:"no-store"});
  const status=await statusResponse.json();
  if(!status.ok)throw Error(status.error||"Локалниот Git сервис не е достапен");
  gitToken=status.csrf;
  if(!confirm(action==="pull"?
    "GitHub ↓ ќе направи Pull (ff-only) од Builder main. Продолжи?":
    "GitHub ↑ ќе ги објави зачуваните projects/ и GLB дизајни на Builder main. Продолжи?"))return;
  const res=await fetch("./api/git-"+action,{method:"POST",headers:{"Content-Type":"application/json","X-Trialum-CSRF":gitToken},body:"{}"});
  const data=await res.json();
  if(!data.ok)throw Error(data.error||"GitHub sync не успеа");
  say("GitHub "+(action==="pull"?"Pull":"Push")+" успешно: "+data.message);
  if(action==="pull")say("GitHub Pull заврши. Освежи го Builder за новиот каталог.");
 }catch(e){say("GitHub: "+e.message+" · користи Python сервер и поставена GitHub Desktop/Git Credential Manager автентикација.",true)}
 finally{btn.disabled=false;}
}

const ROOM_PRESETS=Object.freeze({
 atrium:"trialum-agro-atrium.json",
 warehouse:"trialum-food-warehouse.json",
 cold:"trialum-cold-storage.json",
 packing:"trialum-packing-room.json",
 greenhouse:"trialum-agro-greenhouse.json",
 g01:"trialum-g01-water-core.json",
 "f01-f":"trialum-f01-f-radial-wedge-review.json",
 f01:"trialum-s7-f01-production.json"
});
function frameCurrentRoom(){
 const {width,depth,height}=state.project.room;
 const size=Math.max(width,depth);
 const distance=Math.max(12,size*1.08);
 camera.position.set(distance*.55,Math.max(7,height*.9,distance*.52),distance*.82);
 controls.target.set(0,Math.min(height*.3,3),0);
 controls.maxDistance=Math.max(220,size*3);
 camera.far=Math.max(800,size*12);
 camera.updateProjectionMatrix();controls.update();
}
async function openRoomPreset(key){
 const file=ROOM_PRESETS[key];if(!file)return;
 if(state.dirty&&!confirm("Има незачувани измени. Да ја отвориме другата просторија?"))return;
 try{
  const response=await fetch("./projects/"+file,{cache:"no-store"});
  if(!response.ok)throw Error("HTTP "+response.status);
  const data=await response.json();
  // Never keep the save handle for the previously opened room.
  state.saveHandle=null;
  useProject(data,true);
  frameCurrentRoom();
  if(key==="f01-f"){
    // Focus on the TRUE G01 north-east poolside arc (22.5–75 degrees).
    // The seven small separate tiles must be visible, not one lonely slab.
    camera.position.set(18,13,16);
    controls.target.set(4.9,.16,4.9);
    controls.maxDistance=120;
    controls.update();
  }
  try{localStorage.setItem(LOCAL_AUTOSAVE,JSON.stringify(state.project));}catch{}
  say("Вчитана вистинска GLB просторија: "+data.name+" · "+data.instances.length+" елементи.");
 }catch(e){say("Не можам да ја отворам просторијата: "+e.message,true)}
 finally{$("scenePreset").value="";}
}

function addListeners(){
 document.querySelectorAll("[data-tool]").forEach(b=>b.addEventListener("click",()=>setTool(b.dataset.tool)));
 ui.assetSearch.addEventListener("input",renderCatalogue);
 ui.categoryFilter.addEventListener("change",renderCatalogue);
 ui.projectName.addEventListener("change",()=>{state.project.name=ui.projectName.value;markChanged();});
 $("newProject").onclick=newProject;
 $("openProject").onclick=()=>ui.projectFileInput.click();
 $("openS7Project").onclick=()=>openRoomPreset("f01");
 $("scenePreset").onchange=e=>openRoomPreset(e.target.value);
 ui.projectFileInput.onchange=async e=>{
  try{await fileOpen(e.target.files?.[0])}catch(err){say("Неправилен проект: "+err.message,true)}
  e.target.value="";
 };
 $("saveProject").onclick=saveProjectToRepo;
 $("gitPull").onclick=()=>githubSync("pull");
 $("gitPublish").onclick=()=>githubSync("publish");
 $("exportProject").onclick=()=>{downloadJson(collectProject(),slug(state.project.name)+".json");say("JSON проектот е преземен. Зачувај го во projects/.")};
 $("exportLivingSpace").onclick=()=>{try{const data=exportLivingSpace(collectProject(),[...state.registry.values()]);downloadJson(data,slug(state.project.name)+"-living-space.json");say("Извезен Living Spaces JSON: "+data.items.length+" предмети. Не ја менува играта.");}catch(e){say("Living Spaces export: "+e.message,true)}};
 $("exportBundle").onclick=exportBundle;
 $("importGlb").onclick=()=>ui.glbFileInput.click();
 ui.glbFileInput.onchange=async e=>{await importGlbs([...e.target.files]);e.target.value=""};
 $("applyInspector").onclick=applyInspector;
 $("duplicateObject").onclick=duplicateSelected;
 $("deleteObject").onclick=deleteSelected;
 $("applyRoom").onclick=()=>{
  state.project.room.width=math.clamp(Number(ui.roomWidth.value)||12,2,120);
  state.project.room.depth=math.clamp(Number(ui.roomDepth.value)||12,2,120);
  state.project.room.height=math.clamp(Number(ui.roomHeight.value)||4,2,30);
  state.project.room.showWalls=ui.showWalls.checked;
  roomHelpers();markChanged();say("Просторијата е обновена.");};
 $("resetCamera").onclick=()=>{
  frameCurrentRoom();say("Камерата е прилагодена на големината на просторијата.");};
 ui.gridStep.addEventListener("change",()=>{state.project.room.gridSize=gridStep();syncGrid();markChanged()});
 $("toggleGrid").onclick=()=>{
  state.gridOn=!state.gridOn;
  if(grid)grid.visible=state.gridOn;
  $("toggleGrid").classList.toggle("active",state.gridOn);
 };
 ui.surfaceMode.addEventListener("change",()=>{
  if(ui.surfaceMode.value==="wall"){state.project.room.showWalls=true;roomHelpers();}
 });
 canvas.addEventListener("pointerdown",e=>{if(e.button===0)lastPointerDown={x:e.clientX,y:e.clientY,time:Date.now()};});
 canvas.addEventListener("pointerup",e=>{
  if(e.button!==0||!lastPointerDown||state.dragging)return;
  if(Math.hypot(e.clientX-lastPointerDown.x,e.clientY-lastPointerDown.y)>5)return;
  lastPointerDown=null;
  const ray=screenRay(e.clientX,e.clientY);
  if(state.tool==="place"){placeAsset(e.clientX,e.clientY);return;}
  const objectId=hitObject(ray);
  if(state.tool==="erase"){selectObject(objectId);deleteSelected();return;}
  if(objectId)selectObject(objectId);else selectObject(null);
 });
 const viewport=$("viewport");
 viewport.addEventListener("dragover",e=>{e.preventDefault();$("dropOverlay").classList.add("visible");});
 viewport.addEventListener("dragleave",e=>{if(!viewport.contains(e.relatedTarget))$("dropOverlay").classList.remove("visible");});
 viewport.addEventListener("drop",async e=>{
  e.preventDefault();$("dropOverlay").classList.remove("visible");
  await importGlbs([...e.dataTransfer.files]);
 });
 window.addEventListener("keydown",handleKey);
 window.addEventListener("beforeunload",e=>{if(state.dirty){e.preventDefault();e.returnValue="";}});
 const observer=new ResizeObserver(()=>{
  const rect=ui.viewport.getBoundingClientRect();if(rect.width<1||rect.height<1)return;
  camera.aspect=rect.width/rect.height;camera.updateProjectionMatrix();
  renderer.setSize(rect.width,rect.height,false);
 });
 observer.observe(ui.viewport);
}
const animationClock=new THREE.Clock();
function tick(){
 requestAnimationFrame(tick);
 const dt=Math.min(animationClock.getDelta(),0.08);
 for(const mixer of state.animationMixers.values())mixer.update(dt);
 controls.update();
 renderer.render(scene,camera);
}
async function startup(){
 try{
  const response=await fetch(CATALOG_URL,{cache:"no-store"});
  if(!response.ok)throw Error("HTTP "+response.status);
  const library=await response.json();
  state.catalog=library.assets||[];
  for(const item of state.catalog)state.registry.set(item.id,item);
 }catch(err){say("Каталогот не е достапен: "+err.message,true);}
 // Built-in placeholders are harmless editor-only components.
 for(const item of [
  {id:"block",name:"Коцка · градежен модул",category:"Градежни блокови",
   dimensions:[.5,.5,.5],placement:"floor",color:"#8db59d"},
  {id:"soil",name:"Земја · тест површина",category:"Градежни блокови",
   dimensions:[.5,.15,.5],placement:"floor",color:"#84634a"},
  {id:"wall-panel",name:"Ѕиден панел · тест",category:"Градежни блокови",
   dimensions:[1,1,.10],placement:"wall",color:"#668e87"}
 ])if(!state.registry.has(item.id))state.registry.set(item.id,item);
 let data;let recoveredLocalDraft=false;
 try{const saved=localStorage.getItem(LOCAL_AUTOSAVE);if(saved){data=JSON.parse(saved);recoveredLocalDraft=true;}}catch{}
 if(!data)try{const r=await fetch("./projects/trialum-s7-f01-production.json");if(r.ok)data=await r.json()}catch{}
 try{state.project=data?sanitizeProject(data):createProject()}catch{state.project=createProject()}
 for(const asset of state.project.assets)state.registry.set(asset.id,asset);
 ui.projectName.value=state.project.name;
 ui.gridStep.value=String(state.project.room.gridSize||.5);
 refreshCategories();roomHelpers();addListeners();await rebuildScene();recordSnapshot();
 if(recoveredLocalDraft){state.dirty=true;ui.saveIndicator.textContent="● Локална копија · треба Git зачувување";ui.saveIndicator.style.color="#edb979";}
 else markSaved();
 updateCounters();
 $("viewportHint").textContent="Лев клик: избор или лепење · Десен клик: орбита · Среден: зум · Ctrl+S: зачувај";
 tick();
 say((recoveredLocalDraft?"Вратена локална копија (Зачувај во GitHub папка). ":"")+
 "Trialum Builder е подготвен · "+state.catalog.length+" оригинални модели во каталогот.");
 if(!state.catalog.length)say("Нема GLB каталог. Стартувај scripts/build_assets.py или провери GitHub Actions.",true);
}
startup().catch(e=>{console.error(e);say("Грешка при стартување: "+e.message,true);});
