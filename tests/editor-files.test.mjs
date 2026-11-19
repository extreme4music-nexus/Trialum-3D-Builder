import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
const ROOT=process.cwd();
const file=p=>fs.readFileSync(path.join(ROOT,p),"utf8");
test("HTML includes all interactive controls used by real editor",()=>{
 const html=file("index.html"),js=file("src/main.js");
 for(const id of [...js.matchAll(/\$\("([A-Za-z0-9_-]+)"\)/g)].map(m=>m[1])){
  assert.ok(html.includes('id="'+id+'"'),"Missing HTML control "+id);
 }
 assert.match(html,/type="importmap"/);assert.match(html,/src="\.\/src\/main\.js"/);
});
test("editor uses original Three.js GLTFLoader and TransformControls, no gameplay writes",()=>{
 const source=file("src/main.js"),html=file("index.html");
 assert.match(source,/GLTFLoader/);assert.match(source,/TransformControls/);
 assert.match(source,/showDirectoryPicker/);assert.match(source,/indexedDB/);
 assert.match(source,/createWritable/);assert.match(source,/undo\(/);
 assert.match(source,/makeZip\(/);
 assert.doesNotMatch(source,/fetch\([^)]*\/api\/(?:player|social|inventory)/i);
 assert.doesNotMatch(html,/three\.js.*cdn|http:\/\/[a-z]/i);
});
test("catalogue maintains all real F01 F02 F03 and soil GLB models",()=>{
 const c=JSON.parse(file("assets/catalog.json"));
 const glbs=c.assets.filter(x=>x.src?.endsWith(".glb"));
 assert.equal(glbs.length,c.genuineGlbCount);
 assert.ok(glbs.length>=130);
 assert.equal(new Set(glbs.map(x=>x.id)).size,c.genuineGlbCount);
 assert.ok(glbs.every(x=>/^assets\/models\/[a-z0-9_.-]+\.glb$/.test(x.src)));
 assert.ok(c.assets.some(x=>x.id==="f01-d-north"));
 assert.ok(c.assets.some(x=>x.id==="f01-e-north-west"));
 assert.ok(c.assets.some(x=>x.id==="f01-f-radial-wedge"&&x.approval.includes("PREVIOUS OVERSIZED WEDGE REJECTED")&&x.approval.includes("POOLSIDE REVIEW PENDING")));
 for(const id of ["agro-atrium","food-warehouse-shell","food-cold-annex-shell","food-packing-annex-shell","greenhouse-shell","g01-main-basin","aquaglow-mature","b1-pilot-room"]){
  assert.ok(c.assets.some(x=>x.id===id),"Missing original or derived GLB: "+id);
 }
});
test("starter is localhost only and repo contains standalone handoff docs",()=>{
 const py=file("scripts/server.py"),node=file("scripts/server.mjs");
 assert.match(py,/127\.0\.0\.1/);
 assert.match(node,/127\.0\.0\.1/);
 assert.match(file("START-BUILDER-WINDOWS.bat"),/START|server\.py|server\.mjs/);
 assert.ok(fs.existsSync("docs/HANDOFF.md"));
});

test("official S7 builder project contains original GLB modules, not demo primitives",()=>{
 const p=JSON.parse(file("projects/trialum-s7-f01-production.json"));
 const c=JSON.parse(file("assets/catalog.json"));
 const ids=new Set(c.assets.map(a=>a.id));
 assert.equal(p.schemaVersion,1);
 assert.equal(p.projectId,"trialum-s7-f01-greenhouse-production-20261117");
 assert.equal(p.instances.length,70);
 assert.ok(p.instances.every(i=>ids.has(i.assetId)));
 assert.ok(p.instances.every(i=>i.assetId.startsWith("f01-")));
 assert.equal(p.meta.gameplayWrites,0);
 assert.equal(p.meta.officialScene,false);
 assert.match(file("src/main.js"),/"f01":"trialum-s7-f01-production.json"/);
});

test("existing source rooms and two warehouse annexes have editable non-demo JSON",()=>{
 const c=JSON.parse(file("assets/catalog.json"));
 const known=new Set(c.assets.map(a=>a.id));
 for(const path of ["projects/trialum-agro-atrium.json","projects/trialum-food-warehouse.json","projects/trialum-cold-storage.json",
  "projects/trialum-packing-room.json","projects/trialum-agro-greenhouse.json","projects/trialum-g01-water-core.json"]){
  const p=JSON.parse(file(path));
  assert.equal(p.schemaVersion,1);
  assert.ok(p.instances.length>0,path);
  assert.ok(p.instances.every(x=>known.has(x.assetId)),path);
  assert.ok(p.instances.every(x=>!["block","soil","wall-panel"].includes(x.assetId)),path);
  assert.equal(p.meta.gameplayWrites,0);
  assert.equal(p.meta.officialScene,false);
 }
});

test("room selector has all six true GLB projects, with safely whitelisted file names",()=>{
 const html=file("index.html"),editor=file("src/main.js");
 assert.match(html,/id="scenePreset"/);
 for(const id of ["atrium","warehouse","cold","packing","greenhouse","g01"]){
  assert.ok(html.includes('value="'+id+'"'),id);
  assert.ok(editor.includes(id+':"trialum-')||editor.includes(id+':"trialum-'),id);
 }
 assert.match(editor,/function frameCurrentRoom/);
 assert.match(editor,/function openRoomPreset/);
 assert.match(editor,/const mixer=new THREE.AnimationMixer/);
 assert.match(editor,/" GLB · "/);
});

test("owner-render-approved F01-F has isolated Builder 3D review preset, never installed in game",()=>{
 const p=JSON.parse(file("projects/trialum-f01-f-radial-wedge-review.json"));
 const ids=p.instances.map(x=>x.assetId);
 assert.equal(p.schemaVersion,1);
 assert.equal(p.meta.gameplayWrites,0);
 assert.equal(p.meta.officialScene,false);
 assert.equal(p.meta.ownerCorrectedPhysicalModelPass,false);
 assert.equal(ids.filter(x=>x==="f01-f-radial-wedge").length,7);
 assert.ok(ids.includes("g01-main-basin"));
 assert.ok(ids.includes("g01-walkway-and-railings"));
 assert.ok(ids.includes("g01-water-surfaces-animated"));
 const tiles=p.instances.filter(x=>x.assetId==="f01-f-radial-wedge");
 assert.equal(tiles.length,7);
 for(let i=0;i<tiles.length;i++){
   const idx=i+3,angle=idx*Math.PI*2/48;
   assert.equal(tiles[i].id,"f01-f-pool-"+String(idx).padStart(2,"0"));
   assert.ok(Math.abs(tiles[i].position[0]-7.2*Math.cos(angle))<1e-7);
   assert.ok(Math.abs(tiles[i].position[2]-7.2*Math.sin(angle))<1e-7);
   assert.ok(Math.abs(tiles[i].rotationY+angle)<1e-9);
   assert.equal(tiles[i].position[1],.192);
 }
 assert.match(file("index.html"),/value="f01-f"/);
 assert.match(file("src/main.js"),/"f01-f":"trialum-f01-f-radial-wedge-review.json"/);
});

test("F01-G includes real G01 assembled 7-curb preview plus continuous long showcase",()=>{
 const c=JSON.parse(file("assets/catalog.json")); const known=new Set(c.assets.map(a=>a.id));
 const ids=["f01-g-pool-trim-1m","f01-g-pool-trim-half","f01-g-pool-trim-3m-showcase"];
 assert.ok(ids.every(id=>known.has(id)));
 const p=JSON.parse(file("projects/trialum-f01-g-pool-curb-g01-preview.json"));
 assert.equal(p.meta.gameplayWrites,0);
 assert.equal(p.meta.officialScene,false);
 assert.equal(p.instances.filter(x=>x.assetId==="f01-g-pool-trim-1m").length,7);
 assert.equal(p.instances.filter(x=>x.assetId==="f01-f-radial-wedge").length,7);
 assert.ok(p.instances.some(x=>x.assetId==="g01-main-basin"));
 assert.ok(p.instances.some(x=>x.assetId==="g01-walkway-and-railings"));
 for(let idx=3;idx<=9;idx++){
  const item=p.instances.find(x=>x.id==="f01-g-poolside-curb-"+String(idx).padStart(2,"0"));
  assert.ok(item);
  const rad=idx*Math.PI/24;
  assert.ok(Math.abs(item.position[0]-8.2*Math.cos(rad))<1e-7);
  assert.ok(Math.abs(item.position[2]-8.2*Math.sin(rad))<1e-7);
  assert.ok(Math.abs(item.rotationY+rad)<1e-9);
 }
 const showcase=JSON.parse(file("projects/trialum-f01-g-curved-trim-showcase.json"));
 assert.ok(showcase.instances.some(x=>x.assetId==="f01-g-pool-trim-3m-showcase"));
 assert.equal(showcase.meta.officialScene,false);
 assert.match(file("index.html"),/value="f01-g"/);
 assert.match(file("index.html"),/value="f01-g-showcase"/);
});

test("last F01 white-cream marble family has real distinct H and I GLBs and owner preview",()=>{
 const c=JSON.parse(file("assets/catalog.json"));const byId=new Map(c.assets.map(a=>[a.id,a]));
 assert.ok(c.genuineGlbCount>=130);
 const a=byId.get("f01-a");
 const h=byId.get("f01-h-honed-service"),i=byId.get("f01-i-wet-fine-texture");
 assert.ok(a&&h&&i);
 assert.notEqual(h.src,i.src);
 assert.equal(h.roughness,.70);
 assert.equal(i.roughness,.86);
 assert.equal(h.dimensions[0],1);
 assert.equal(i.dimensions[0],1);
 assert.ok(c.assets.filter(a=>a.id.startsWith("f01-g-pool-trim-")).every(a=>a.approval.includes("OWNER MODEL VISUAL PASS")));
 const p=JSON.parse(file("projects/trialum-f01-h-i-cream-marble-finishes-review.json"));
 assert.equal(p.instances.filter(x=>x.assetId===h.id).length,2);
 assert.equal(p.instances.filter(x=>x.assetId===i.id).length,2);
 assert.equal(p.instances.filter(x=>x.assetId==="f01-a").length,1);
 assert.equal(p.meta.gameplayWrites,0);
 assert.equal(p.meta.officialScene,false);
 assert.equal(p.meta.actualCertifiedSlipResistance,false);
 assert.match(file("index.html"),/value="f01-hi"/);
 assert.match(file("src/main.js"),/"f01-hi":"trialum-f01-h-i-cream-marble-finishes-review.json"/);
});

test("all 29 black marble real assets and three editable owner preview scenes are present",()=>{
 const c=JSON.parse(file("assets/catalog.json"));
 const ids=new Set(c.assets.map(a=>a.id));
 const black=c.assets.filter(a=>a.id.startsWith("f02-black-marble-"));
 assert.equal(black.length,29);
 assert.ok(black.every(a=>a.src.endsWith(".glb")));
 assert.ok(black.every(a=>a.approval.includes("OWNER IN-BUILDER MODEL REVIEW PENDING")));
 const map=[
  ["projects/trialum-f02-black-marble-gallery.json",29],
  ["projects/trialum-f02-black-marble-g01-pool-preview.json",19],
  ["projects/trialum-f02-black-marble-finishes-review.json",3]
 ];
 for(const [path,count] of map){
  const p=JSON.parse(file(path));
  assert.equal(p.instances.length,count,path);
  assert.ok(p.instances.every(x=>ids.has(x.assetId)),path);
  assert.equal(p.meta.gameplayWrites,0,path);
  assert.equal(p.meta.officialScene,false,path);
 }
 const gallery=JSON.parse(file(map[0][0]));
 assert.ok(gallery.instances.some(x=>x.assetId==="f02-black-marble-l-corner-showcase-north-west"));
 assert.ok(gallery.instances.some(x=>x.assetId==="f02-black-marble-raised-border-showcase-east"));
 const pool=JSON.parse(file(map[1][0]));
 assert.equal(pool.instances.filter(x=>x.assetId==="f02-black-marble-radial-wedge").length,7);
 assert.equal(pool.instances.filter(x=>x.assetId==="f02-black-marble-pool-trim-1m").length,7);
 assert.ok(pool.instances.some(x=>x.assetId==="g01-main-basin"));
 assert.ok(pool.instances.some(x=>x.assetId==="g01-walkway-and-railings"));
 const html=file("index.html"),editor=file("src/main.js");
 for(const key of ["f02-gallery","f02-g01","f02-finishes"]){
  assert.ok(html.includes('value="'+key+'"'));
  assert.ok(editor.includes('"'+key+'":"trialum-f02-'));
 }
});

test("both owner-render-approved F03 stone finishes have all 54 genuine GLBs and 6 selectable 3D scenes",()=>{
 const c=JSON.parse(file("assets/catalog.json")),idSet=new Set(c.assets.map(a=>a.id));
 const stones=c.assets.filter(a=>a.id.startsWith("f03-")&&a.src?.endsWith(".glb"));
 assert.equal(stones.length,54);
 assert.equal(stones.filter(a=>a.finish==="SMOOTH_HONED").length,27);
 assert.equal(stones.filter(a=>a.finish==="SUBTLE_MICRO_TEXTURE").length,27);
 assert.ok(stones.every(a=>a.ownerRenderPass===true&&a.ownerModelPass===false&&a.gameplayWrites===0));
 const scenes=[
 ["projects/trialum-f03-all-54-stone-gallery.json",54],
 ["projects/trialum-f03-s-stone-gallery.json",27],
 ["projects/trialum-f03-t-stone-gallery.json",27],
 ["projects/trialum-f03-smooth-vs-textured-compare.json",10],
 ["projects/trialum-f03-s-g01-pool-preview.json",19],
 ["projects/trialum-f03-t-g01-pool-preview.json",19],
 ];
 for(const [path,count] of scenes){
  const p=JSON.parse(file(path));
  assert.equal(p.instances.length,count,path);
  assert.ok(p.instances.every(x=>idSet.has(x.assetId)),path);
  assert.equal(p.meta.gameplayWrites,0,path);
  assert.equal(p.meta.officialScene,false,path);
  assert.equal(p.meta.ownerGlbModelPass,false,path);
 }
 const html=file("index.html"),editor=file("src/main.js");
 for(const key of ["f03-all","f03-s","f03-t","f03-compare","f03-s-g01","f03-t-g01"]){
  assert.ok(html.includes('value="'+key+'"'),key);
  assert.ok(editor.includes('"'+key+'":"trialum-f03-'),key);
 }
 const m=JSON.parse(file("assets/materials/f03-glb-sha-manifest.json"));
 assert.equal(m.models.length,54);
 assert.equal(m.ownerGlbPass,false);
});

test("S02 5x5 interactive soil matrix has 25 stable coordinates and no game-state expansion",()=>{
 const catalogue=JSON.parse(file("assets/catalog.json"));
 const ids=new Set(catalogue.assets.map(a=>a.id));
 for(const id of ["s02-25-planting-grid","s01-dug-turnover","s02-fill-plug","s02-slot-ring","s02-demo-seedling"])
  assert.ok(ids.has(id),"Missing soil GLB in catalogue: "+id);
 assert.ok(catalogue.genuineGlbCount>=150);
 const grid=JSON.parse(file("assets/soil-slot-matrix.json"));
 assert.equal(grid.slotCount,25);
 assert.equal(grid.canonicalPlantSlotsPerBed,5);
 assert.equal(grid.slots.length,25);
 assert.equal(new Set(grid.slots.map(s=>s.slotId)).size,25);
 assert.ok(grid.slots.every(s=>s.status==="OPEN"&&s.plantId===null));
 for(const path of ["projects/trialum-s02-25-empty-holes.json",
   "projects/trialum-s02-mixed-planting-demo.json",
   "projects/trialum-s03-dug-soil.json","projects/trialum-s02-s03-soil-comparison.json"]){
  const p=JSON.parse(file(path));
  assert.ok(p.instances.length>0,path);
  assert.ok(p.instances.every(x=>ids.has(x.assetId)),path);
  assert.equal(p.meta.canonicalSlotsPerBed,5);
  assert.equal(p.meta.officialScene,false);
  assert.equal(p.meta.gameplayWrites,0);
 }
 const mixed=JSON.parse(file("projects/trialum-s02-mixed-planting-demo.json"));
 assert.equal(mixed.instances.filter(x=>x.assetId==="s02-fill-plug").length,3);
 assert.equal(mixed.instances.filter(x=>x.assetId==="s02-demo-seedling").length,2);
 const html=file("index.html"),js=file("src/main.js");
 for(const id of ["soilMatrixTool","soilMatrixPanel","soilMatrixClose","soilMatrixTarget",
                  "soilMatrixCells","soilMatrixStatus"]){
   assert.ok(html.includes('id="'+id+'"'),id);
 }
 for(const preset of ["soil-empty","soil-mixed","soil-dug","soil-compare"]){
   assert.ok(html.includes('value="'+preset+'"'));
   assert.ok(js.includes('"'+preset+'":"trialum-'));
 }
 assert.match(js,/function soilSlotPosition/);
 assert.match(js,/function existingSoilPlug/);
 assert.match(js,/function toggleSoilPreviewSlot/);
 assert.match(js,/if\(total>=5\)/);
 assert.match(js,/plantId must come from canonical game engine/);
});

test("one-click 24-light gallery remains visible after pulling Builder main",()=>{
 const html=file("index.html"),js=file("src/main.js"),launcher=file("START-BUILDER-WINDOWS.bat");
 const c=JSON.parse(file("assets/catalog.json"));
 const lighting=c.assets.filter(a=>/^s7-l(?:f[1-3]|w[1-2]|c[1-3])-/.test(a.id)&&a.src?.endsWith(".glb"));
 assert.equal(lighting.length,24,"Real lighting assets must be present in Builder");
 assert.match(html,/id="packagePreset"/);
 assert.match(html,/id="builderLibraryVersion"/);
 assert.match(js,/"lights-all":"trialum-s7-lights-all-24-glbs.json"/);
 assert.match(js,/LED "\+lightCount\+"\/24 · S7-F /);
 for(const item of ["lights-all","lights-floor","lights-wall","lights-ceiling","lights-g01"]){
  assert.ok(html.includes('value="'+item+'"'),item+" not in room selector");
  assert.ok(js.includes('"'+item+'":"trialum-s7-lights-'),item+" route missing");
 }
 const gallery=JSON.parse(file("projects/trialum-s7-lights-all-24-glbs.json"));
 assert.equal(gallery.instances.length,24);
 assert.ok(gallery.instances.every(x=>lighting.some(a=>a.id===x.assetId)));
 assert.match(launcher,/s7-lf1-perimeter-straight-1m\.glb/);
 assert.match(launcher,/s7-lc1-g01-1plus4-ring-chandelier\.glb/);
 assert.match(launcher,/goto portbusy/);
});

test("G00L twenty-eight real GLBs appear in Builder one-click scene",()=>{
 const c=JSON.parse(file("assets/catalog.json"));
 const items=c.assets.filter(a=>a.id.startsWith("s7-e0e1-")&&a.src.endsWith(".glb"));
 assert.equal(items.length,28);assert.ok(c.genuineGlbCount>=320);
 const h=file("index.html"),j=file("src/main.js");
 assert.match(h,/id="packagePreset"/);assert.match(j,/"g00l-e0e1-all":"trialum-g00l-e0e1-all-review.json"/);
 for(const name of ["all","rs","rm","st","desk","accessories","layout"]){
  assert.ok(h.includes('value="g00l-e0e1-'+name+'"'));
  assert.ok(j.includes('"g00l-e0e1-'+name+'"'));
 }
 const gallery=JSON.parse(file("projects/trialum-g00l-e0e1-all-review.json"));assert.equal(gallery.instances.length,28);
});

test("S7-F robotics eighteen real GLBs and eight Builder galleries",()=>{
 const c=JSON.parse(file("assets/catalog.json")); const a=c.assets.filter(x=>x.id.startsWith("s7-f-")&&x.src?.endsWith(".glb"));
 assert.equal(a.length,18);assert.ok(c.genuineGlbCount>=338);
 const h=file("index.html"),j=file("src/main.js");
 assert.match(h,/id="packagePreset"/);assert.match(j,/"s7f-all":"trialum-s7-f-all.json"/);
 for(const v of ["all","heroes","machines","transports","robot","tools","g00l-preview","rig-demo"]){assert.ok(h.includes('value="s7f-'+v+'"'));assert.ok(j.includes('"s7f-'+v+'"'));}
 assert.equal(JSON.parse(file("projects/trialum-s7-f-all.json")).instances.length,18);
});

test("single-clip S7-F robot animation preview prevents concurrent actions",()=>{
 const h=file("index.html"),j=file("src/main.js");
 for(const name of ["animationControls","animationClip","animationPlay","animationStop"]){
  assert.ok(h.includes('id="'+name+'"'),"Missing robot animation control "+name);
 }
 assert.match(j,/mixer\.stopAllAction\(\)/);
 assert.match(j,/mixer\.clipAction\(defaultClip\)\.reset\(\)\.play\(\)/);
 assert.doesNotMatch(j,/for\(const clip of clips\)mixer\.clipAction\(clip\)\.play\(\)/);
 assert.match(j,/function playSelectedAnimation\(/);
});


test("S7-F and R01 models are directly discoverable and all original binaries exportable",()=>{
 const h=file("index.html"),src=file("src/main.js"),catalog=JSON.parse(file("assets/catalog.json"));
 const parts=catalog.assets.filter(a=>a.id.startsWith("s7-f-")&&a.src?.endsWith(".glb"));
 const robots=parts.filter(a=>a.id.startsWith("s7-f-r01-"));
 assert.equal(parts.length,18);
 assert.equal(robots.length,3);
 assert.equal(new Set(parts.map(a=>a.id)).size,18);
 for(const id of ["packagePreset","handoffBranch","exportHandoff"]){
   assert.ok(h.includes('id="'+id+'"'),id);
   assert.ok(src.includes('"'+id+'"'),id);
 }
 assert.match(src,/const S7_F_ALL=/);
 assert.match(src,/async function exportDesignHandoff/);
 assert.match(src,/downloadBlob\(makeZip\(files\),/);
 assert.match(src,/const files=\[/);
 assert.ok(h.includes('value="s7f-robot"'));
 assert.ok(h.includes('value="s7f-all"'));
 const all=JSON.parse(file("projects/trialum-s7-f-all.json"));
 assert.equal(all.instances.length,18);
 assert.ok(all.instances.every(x=>parts.some(a=>a.id===x.assetId)));
});
