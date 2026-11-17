import test from "node:test";
import assert from "node:assert/strict";
import {createProject,sanitizeProject,snap,rectanglesOverlap,validateProject,slug} from "../src/project.js";
test("new project creates safe classic-independent design schema",()=>{
 const p=createProject("Test");assert.equal(p.schemaVersion,1);
 assert.deepEqual(p.instances,[]);
 assert.equal(p.meta.gameplayWrites,0);assert.equal(p.meta.officialScene,false);
 assert.deepEqual(validateProject(p),[]);
});
test("malformed imported scene cannot inject unbounded coords or prototype code",()=>{
 const raw={schemaVersion:1,name:"QA",instances:[
   {id:"1",assetId:"f01-a",position:[Infinity,99999,-99999],rotationY:99999,scale:[500,-8,1],layer:"invalid",binding:"engine.food",locked:false},
   {id:"1",assetId:"f01-a",position:[0,0,0]}
 ]};
 const p=sanitizeProject(raw);
 assert.equal(p.instances.length,2);
 assert.notEqual(p.instances[0].id,p.instances[1].id);
 assert.deepEqual(p.instances[0].position,[0,300,-300]);
 assert.deepEqual(p.instances[0].scale,[20,.05,1]);
 assert.equal(p.instances[0].layer,"props");
 assert.equal(p.instances[0].binding,"engine.food");
 assert.ok(!Object.hasOwn(p,"command"));
});
test("editing import and output preserves schema and strict bad input gate",()=>{
 assert.throws(()=>sanitizeProject({schemaVersion:99,instances:[]}),/schemaVersion/);
 assert.throws(()=>sanitizeProject({schemaVersion:1,instances:new Array(6001).fill({})}),/6000/);
 const p=createProject("Room");p.instances.push({id:"a",assetId:"block",position:[1,0,2]});
 const clean=sanitizeProject(p);assert.equal(clean.instances[0].position[2],2);
});
test("grid snapping and non-overlapping adjacent floor tiles",()=>{
 assert.equal(snap(.63,.5),.5);assert.equal(snap(1.11,.25),1);
 const a={minX:0,maxX:1,minZ:0,maxZ:1},b={minX:1,maxX:2,minZ:0,maxZ:1};
 const c={minX:.9,maxX:1.9,minZ:0,maxZ:1};
 assert.equal(rectanglesOverlap(a,b),false);
 assert.equal(rectanglesOverlap(a,c),true);
});
test("non-Latin scene title produces safe Git-tracked filename",()=>{
 assert.equal(slug("Floor room 01"),"floor-room-01");
 assert.equal(slug("Мој проект"),"scene");
});
