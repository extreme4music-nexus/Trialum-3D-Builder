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
test("catalogue contains all 41 historical and derived Trialum room GLBs",()=>{
 const c=JSON.parse(file("assets/catalog.json"));
 const glbs=c.assets.filter(x=>x.src?.endsWith(".glb"));
 assert.equal(glbs.length,41);
 assert.equal(new Set(glbs.map(x=>x.id)).size,41);
 assert.ok(glbs.every(x=>/^assets\/models\/[a-z0-9_.-]+\.glb$/.test(x.src)));
 assert.ok(c.assets.some(x=>x.id==="f01-d-north"));
 assert.ok(c.assets.some(x=>x.id==="f01-e-north-west"));
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
