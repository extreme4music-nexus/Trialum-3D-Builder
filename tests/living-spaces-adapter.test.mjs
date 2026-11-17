import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import {exportLivingSpace} from "../src/living-spaces-adapter.js";
const read=p=>JSON.parse(fs.readFileSync(p,"utf8"));
test("production design exports canonical 70 GLB instances without game writes",()=>{
 const p=read("projects/trialum-s7-f01-production.json");
 const catalog=read("assets/catalog.json");
 const x=exportLivingSpace(p,catalog.assets,"owner-test","room-one");
 assert.equal(x.schemaVersion,1);
 assert.equal(x.ownerId,"owner-test");
 assert.equal(x.items.length,70);
 assert.equal(new Set(x.items.map(i=>i.id)).size,70);
 assert.ok(x.items.every(i=>i.position[0]>=0&&i.position[2]>=0));
 assert.ok(x.items.every(i=>i.editable===false&&i.petEditable===false));
 assert.equal(x.source.mode,"DESIGN_IMPORT_REQUIRES_GAME_APPROVAL");
 assert.ok(!Object.hasOwn(x,"foodStock"));
});
test("unresolved models cannot silently become arbitrary cubes",()=>{
 const p=read("projects/trialum-s7-f01-production.json");
 const x=exportLivingSpace(p,[],"owner","room");
 assert.equal(x.items.length,0);
});
