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
test("catalogue contains all 42 historical and derived Trialum room GLBs",()=>{
 const c=JSON.parse(file("assets/catalog.json"));
 const glbs=c.assets.filter(x=>x.src?.endsWith(".glb"));
 assert.equal(glbs.length,42);
 assert.equal(new Set(glbs.map(x=>x.id)).size,42);
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
 assert.match(file("src/main.js"),/openS7Project/);
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
