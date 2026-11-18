import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import {sanitizeProject,LEGACY_SOIL_ASSET_ALIASES} from "../src/project.js";
const file=p=>JSON.parse(fs.readFileSync(p,"utf8"));
test("S01/S02/S03 taxonomy is explicit and non-deceptive",()=>{
 const tax=file("docs/S7_SOIL_CANONICAL_STATES_20261118.json");
 assert.equal(tax.schemaVersion,1);
 assert.equal(tax.canonicalStates.S01.builderAssetId,"s01-dug-turnover");
 assert.equal(tax.canonicalStates.S01.legacyBuilderAssetId,"s03-dug-turnover");
 assert.equal(tax.canonicalStates.S02.physicalHoles,25);
 assert.equal(tax.canonicalStates.S03.realModelVariants,15);
 assert.equal(tax.canonicalStates.S03.existingGlb,"assets/models/s03-untreated-full.glb");
 assert.equal(tax.constraints.canonicalTerrestrialBeds,4);
 assert.equal(tax.constraints.realPlantSlotsPerBed,5);
 assert.equal(tax.constraints.createsNewPlantCapacity,false);
});
test("existing exact soil binary stays byte-identical while canonical S01 asset resolves",()=>{
 const c=file("assets/catalog.json");
 const models=c.assets.filter(x=>x.src?.endsWith(".glb"));
 assert.equal(models.length,210);
 const map=new Map(models.map(x=>[x.id,x]));
 assert.ok(map.has("s01-dug-turnover"));
 assert.ok(!map.has("s03-dug-turnover"));
 assert.equal(map.get("s01-dug-turnover").src,"assets/models/s03-dug-turnover-soil.glb");
 assert.ok(fs.existsSync(map.get("s01-dug-turnover").src));
 assert.ok(!models.some(a=>a.canonicalSoilState==="S03"));
 assert.equal(file("assets/soil-slot-matrix.json").canonicalPlantSlotsPerBed,5);
});
test("both authored scenes use S01, no invented S03 GLB",()=>{
 for(const filename of ["projects/trialum-s03-dug-soil.json","projects/trialum-s02-s03-soil-comparison.json"]){
  const p=file(filename);
  assert.ok(p.instances.some(x=>x.assetId==="s01-dug-turnover"));
  assert.ok(!p.instances.some(x=>x.assetId==="s03-dug-turnover"));
  assert.equal(p.meta.gameplayWrites,0);
  assert.equal(p.meta.officialScene,false);
 }
 const html=fs.readFileSync("index.html","utf8");
 assert.match(html,/soil-dug">🪴 S01/);
 assert.match(html,/soil-compare">🌿 S01\/S02/);
});
test("older Builder JSON keeps working via safe asset-ID alias without touching owner customs",()=>{
 assert.equal(LEGACY_SOIL_ASSET_ALIASES["s03-dug-turnover"],"s01-dug-turnover");
 const base={schemaVersion:1,name:"Legacy",room:{},assets:[],instances:[{
  id:"old-tile",assetId:"s03-dug-turnover",position:[0,0,0],rotationY:0,scale:[1,1,1]
 }]};
 const migrated=sanitizeProject(base);
 assert.equal(migrated.instances[0].assetId,"s01-dug-turnover");
 const custom={...base,assets:[{id:"s03-dug-turnover",name:"My custom model",src:"assets/models/custom.glb",dimensions:[1,1,1]}]};
 assert.equal(sanitizeProject(custom).instances[0].assetId,"s03-dug-turnover");
});
