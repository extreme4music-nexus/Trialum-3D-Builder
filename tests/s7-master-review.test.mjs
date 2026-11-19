import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
const file=path=>fs.readFileSync(path,"utf8");
const json=path=>JSON.parse(file(path));
const source=file("src/main.js");
const p=json("projects/trialum-s7-master-garden-review.json");
const catalog=json("assets/catalog.json");

test("G01 true original GLB contains 4 morph-animated water surfaces and 6-second loop",()=>{
 const raw=fs.readFileSync("assets/models/g01-water-surfaces-animated.glb");
 assert.equal(raw.subarray(0,4).toString(),"glTF");
 assert.equal(raw.readUInt32LE(8),raw.length);
 const chunkLength=raw.readUInt32LE(12);
 const doc=JSON.parse(raw.subarray(20,20+chunkLength).toString("utf8"));
 assert.equal(doc.nodes.length,4);
 assert.ok(doc.nodes.every(n=>n.name.includes("animated-water-surface")));
 assert.equal(doc.meshes.length,4);
 assert.ok(doc.meshes.every(m=>m.primitives[0].targets.length===2));
 assert.deepEqual(doc.animations.map(x=>x.name),["G01_WATER_RIPPLES_LOOP_6S"]);
 assert.equal(doc.animations[0].channels.length,4);
 assert.match(source,/floorMesh\.visible=!isGreenhouseGardenProject\(\)/);
 assert.match(source,/function styleOriginalG01Water\(root\)/);
 assert.match(source,/water\.depthWrite=false/);
 assert.match(source,/G01_WATER_RIPPLES_LOOP_6S/);
});

test("master keeps greenhouse physics independent, rooted supports and all true model assets",()=>{
 assert.equal(p.schemaVersion,1);
 assert.match(p.projectId,/^trialum-s7-master-garden/);
 assert.equal(p.meta.gameplayWrites,0);
 assert.equal(p.meta.officialScene,false);
 assert.equal(p.meta.ownerVisualPass,false);
 assert.ok(p.instances.length>=280 && p.instances.length<=450,p.instances.length);
 const all=new Set(catalog.assets.map(x=>x.id));
 assert.equal(new Set(p.instances.map(x=>x.id)).size,p.instances.length);
 for(const x of p.instances){
  assert.ok(all.has(x.assetId),x.assetId);
  assert.ok(x.position.every(Number.isFinite),x.id);
  assert.ok(x.scale.every(v=>v>0 && v<20),x.id);
 }
 assert.equal(p.instances.filter(x=>x.id==="shell-original").length,1);
 assert.equal(p.instances.filter(x=>x.assetId==="g01-water-surfaces-animated").length,1);
 assert.ok(!p.instances.some(x=>x.id.startsWith("floor-")),"Old 773 jagged overlay tiles must be REMOVED from MASTER");
 assert.match(source,/function alignGardenObjectToSupport\(obj,rec\)/);
 assert.match(source,/new THREE\.Box3\(\)\.setFromObject\(obj\)/);
 assert.match(source,/function centerGardenFloorPivot\(obj,rec\)/);
 assert.match(source,/obj\.position\.x-=mid\.x/);
 assert.match(source,/obj\.position\.z-=mid\.z/);
 assert.match(source,/if\(rec\.layer!=="props"&&!floorFixture\)return/);
 assert.match(source,/obj\.position\.y\+=delta/);
});

test("four beds are planted near original dome ends, with proper soil and five distinct canonical slots",()=>{
 const specs=[[-73,38],[-38,55],[-2,63],[37,56]];
 for(let i=1;i<=4;i++){
  const [angle,end]=specs[i-1];
  const bed=p.instances.find(x=>x.id===`bed-${i}-real-bed`);
  assert.ok(bed);
  const r=Math.hypot(bed.position[0],bed.position[2]);
  assert.ok(r>end-9 && r<end-4,`${i}: bed at radius ${r} vs shell end ${end}`);
  assert.ok(bed.scale[0]>=3.3 && bed.scale[2]>=3.3);
  assert.ok(p.instances.some(x=>x.id===`master-G-0${i+1}-soil-base`));
  for(let j=1;j<=5;j++){
   const plant=p.instances.find(x=>x.id===`bed-${i}-plant-preview-${j}`);
   assert.ok(plant,`${i}/${j}`);
   assert.ok(Math.hypot(plant.position[0]-bed.position[0],plant.position[2]-bed.position[2])<=1.85);
   assert.ok(plant.scale[0]>=1.3);
   assert.match(plant.assetId,/^(lumemoss|glowfern|mineralreed)-/);
  }
 }
 assert.equal(p.instances.filter(x=>/-soil-island-/.test(x.id)).length,44);
 assert.equal(p.instances.filter(x=>/-foliage-/.test(x.id)).length,44);
 assert.equal(p.instances.filter(x=>x.id.startsWith("master-finger-")&&x.id.includes("-path-")).length,102);
});

test("G-01 aquatic plants remain in FOUR slots of central basin at correct subgrade water level",()=>{
 const slots=p.instances.filter(x=>x.id.startsWith("aquatic-slot-"));
 assert.equal(slots.length,4);
 for(const plant of slots){
  assert.equal(plant.position[1],-.225);
  assert.ok(Math.hypot(plant.position[0],plant.position[2])<6);
  assert.match(plant.assetId,/^aquaglow-/);
 }
});

test("G-00L desk accessories rest on measured real .918m surface and R01 is near dock",()=>{
 const map=new Map(p.instances.map(x=>[x.id,x]));
 const desk=map.get("g00l-equipment-1"),monitor=map.get("g00l-equipment-3");
 const keyboard=map.get("g00l-equipment-5"),mouse=map.get("g00l-equipment-6");
 assert.equal(desk.position[1],0);
 assert.ok(monitor.position[1]>.918 && monitor.position[1]<.95);
 assert.ok(keyboard.position[1]>.918 && keyboard.position[1]<.96);
 assert.ok(mouse.position[1]>.918 && mouse.position[1]<.96);
 assert.ok(Math.hypot(desk.position[0]-monitor.position[0],desk.position[2]-monitor.position[2])<.5);
 const robot=map.get("g00l-equipment-12"),dock=map.get("g00l-equipment-11");
 assert.ok(Math.hypot(robot.position[0]-dock.position[0],robot.position[2]-dock.position[2])<1.5);
 assert.equal(p.instances.filter(x=>x.id.startsWith("g00l-rs-")).length,2);
 assert.equal(p.instances.filter(x=>x.id.startsWith("g00l-rm-")).length,4);
});

test("g00l floor supports racks and tool; no legacy 773-square overlay",()=>{
 const terrace=p.instances.filter(x=>x.id.startsWith("master-g00l-floor-"));
 assert.equal(terrace.length,45);
 assert.ok(terrace.some(x=>x.position[2]===6));
 assert.ok(terrace.some(x=>x.position[2]===22));
 assert.equal(new Set(terrace.map(x=>x.position[0]+","+x.position[2])).size,45);
 const tool=p.instances.find(x=>x.id==="g00l-equipment-13");
 const tray=p.instances.find(x=>x.id==="g00l-equipment-10");
 assert.equal(tool.position[1],.94);
 assert.ok(tray.position[1]>=.7 && tray.position[1]<1);
});

test("G00L open glass canopy covers real service area without altering original central greenhouse",()=>{
 const annex=p.instances.filter(x=>x.id==="master-g00l-glass-annex");
 assert.equal(annex.length,1);
 assert.equal(annex[0].assetId,"s7-master-g00l-glass-service-wing");
 assert.equal(annex[0].layer,"structure");
 const connectors=p.instances.filter(x=>x.id.startsWith("master-g00l-entrance-connector-"));
 assert.equal(connectors.length,8);
 assert.equal(new Set(connectors.map(x=>x.position[0]+","+x.position[2])).size,8);
 const manifest=json("assets/s7-master-g00l-annex-manifest.json");
 assert.equal(manifest.gameplayWrites,0);
 assert.equal(manifest.originalShellUnmodified,true);
 assert.equal(manifest.openServiceZone,true);
 const b=fs.readFileSync("assets/models/s7-master-g00l-glass-service-wing.glb");
 assert.equal(b.subarray(0,4).toString(),"glTF");
 assert.equal(b.readUInt32LE(8),b.length);
 const len=b.readUInt32LE(12);
 const doc=JSON.parse(b.subarray(20,20+len).toString("utf8"));
 assert.equal(doc.asset.version,"2.0");
 assert.equal(doc.asset.extras.isFifthFinger,false);
 assert.equal(doc.asset.extras.originalGreenhouseUnmodified,true);
 assert.equal(doc.materials[0].alphaMode,"BLEND");
 assert.equal(doc.meshes[0].primitives.length,3);
 assert.ok([362,363].includes(catalog.genuineGlbCount),"G00L genuine annex must remain plus optional PASS2 2.3m glass door");
});
