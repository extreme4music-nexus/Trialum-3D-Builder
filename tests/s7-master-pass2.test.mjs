import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import {sanitizeProject} from "../src/project.js";
const read=f=>JSON.parse(fs.readFileSync(f,"utf8"));
const before=read("projects/trialum-s7-master-garden-review.json");
const after=read("projects/trialum-s7-master-garden-pass2.json");
const catalog=read("assets/catalog.json");
const objs=after.instances;const lookup=new Map(objs.map(x=>[x.id,x]));
test("PASS2 upgrades existing MASTER without deleting objects or touching game",()=>{
 assert.equal(before.instances.length,372);
 assert.equal(catalog.genuineGlbCount,363);
 assert.equal(after.schemaVersion,1);
 assert.equal(after.meta.gameplayWrites,0);
 assert.equal(after.meta.officialScene,false);
 assert.equal(after.meta.ownerVisualPass,false);
 assert.equal(new Set(objs.map(x=>x.id)).size,objs.length);
 const known=new Set(catalog.assets.map(a=>a.id));
 for(const old of before.instances)assert.ok(lookup.has(old.id),"Missing old id "+old.id);
 for(const x of objs)assert.ok(known.has(x.assetId),"Unknown GLB "+x.assetId);
 assert.equal(objs.filter(x=>x.id.startsWith("aquatic-slot-")).length,4);
 assert.equal(objs.filter(x=>/^bed-[1-4]-plant-preview-/.test(x.id)).length,20);
});
test("real 2.3m G00L glass door GLB has moving hinged animation",()=>{
 const b=fs.readFileSync("assets/models/s7-pass2-g00l-glass-partition-door.glb");
 assert.equal(b.subarray(0,4).toString(),"glTF");
 assert.equal(b.readUInt32LE(8),b.length);
 const j=JSON.parse(b.subarray(20,20+b.readUInt32LE(12)).toString("utf8"));
 assert.equal(j.asset.version,"2.0");
 assert.equal(j.asset.extras.doorGapMeters,2.3);
 assert.equal(j.asset.extras.gameplayWrites,0);
 assert.equal(j.meshes.length,2);
 assert.equal(j.animations[0].name,"door-open-hold-close-10s");
 assert.equal(j.animations[0].channels[0].target.node,1);
 assert.equal(j.animations[0].channels[0].target.path,"rotation");
 assert.ok(lookup.has("pass2-g00l-animated-glass-door"));
 for(const id of ["g00l-equipment-1","g00l-equipment-3","g00l-equipment-5"])
  assert.ok(lookup.get(id).position[2]>=22,"Desk misplaced "+id);
 assert.equal(lookup.get("g00l-equipment-3").position[1],.93);
});
test("four 5-slot crop rows are STRAIGHT and .59m apart",()=>{
 const angles=[-73,-38,-2,37],ends=[38,55,63,56];
 for(let i=1;i<=4;i++){
  const a=angles[i-1]*Math.PI/180;
  const ps=Array.from({length:5},(_,k)=>lookup.get("bed-"+i+"-plant-preview-"+(k+1)));
  assert.ok(ps.every(Boolean),"Missing bed row "+i);
  const radial=ps.map(x=>x.position[0]*Math.sin(a)-x.position[2]*Math.cos(a));
  const lateral=ps.map(x=>x.position[0]*Math.cos(a)+x.position[2]*Math.sin(a));
  assert.ok(Math.max(...radial)-Math.min(...radial)<.001);
  for(let k=1;k<5;k++)assert.ok(Math.abs(lateral[k]-lateral[k-1]-.59)<.002);
  for(const plant of ps)assert.equal(plant.rotationY,0);
  assert.ok(Math.abs(radial[0]-(ends[i-1]-6.3))<.002);
 }
});
test("bed irrigation consists of reservoir, pump and hoses, NEVER dripline",()=>{
 assert.equal(objs.filter(x=>x.assetId.startsWith("s7-i05-")).length,0);
 for(let i=1;i<=4;i++){
  assert.equal(lookup.get("bed-"+i+"-irrig-5").assetId,"s7-i03-hose-straight-2p0m");
  assert.equal(lookup.get("bed-"+i+"-irrig-1").assetId,"s7-i01-reservoir-buffer");
  assert.equal(objs.filter(x=>x.id.startsWith("pass2-bed"+i+"-supply-hose-")).length,4);
 }
 for(const id of ["tank","pump","filter","distribution","hose","riser","valve"])
  assert.ok(lookup.has("pass2-g00l-pump-"+id));
});
test("black and white genuine marble does NOT seal any G01 water opening",()=>{
 const tiles=objs.filter(x=>x.id.startsWith("pass2-g01-marble-"));
 assert.equal(tiles.filter(x=>x.assetId==="f02-black-marble-full").length,67);
 assert.equal(tiles.filter(x=>x.assetId==="f01-a").length,61);
 const pools=[[0,0,6.96],[-10,0,2.32],[10,1,2.32],[0,-11,2.22]];
 for(const x of tiles){
  const [xx,yy,zz]=x.position;
  assert.equal(yy,.022);
  const half=x.scale[0]*Math.SQRT2/2;
  assert.ok(Math.hypot(xx,zz)+half<16.1,x.id);
  for(const [hx,hz,r] of pools)
   assert.ok(Math.hypot(xx-hx,zz-hz)>r+half+.05,"Marble across water: "+x.id);
 }
 assert.equal(objs.filter(x=>/pass2-bed\d+-round-stone-/.test(x.id)).length,32);
 assert.equal(objs.filter(x=>/pass2-bed\d+-seedling-/.test(x.id)).length,88);
 assert.equal(objs.filter(x=>/pass2-bed\d+-stone-border-/.test(x.id)).length,88);
});
test("Builder JSON roundtrip retains safe engine PASS2 instructions",()=>{
 const p=sanitizeProject(after);
 assert.equal(p.instances.length,objs.length);
 assert.equal(p.meta.version,"MASTER_PASS_2");
 assert.equal(p.meta.gameplayWrites,0);
 assert.equal(p.meta.officialScene,false);
 assert.equal(p.meta.ownerVisualPass,false);
 assert.equal(p.meta.capacity.beds,4);
 assert.equal(p.meta.capacity.aquaticSlots,4);
 assert.equal(p.meta.irrigation.dripIrrigation,false);
 assert.equal(p.meta.s7Door.collisionRuntime,"NOT_CONNECTED");
 assert.equal(p.meta.nextEngineHandoff.authority,"DESIGN_ONLY");
 assert.equal(p.meta.nextEngineHandoff.inventoryWrites,false);
});
