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
test("catalogue is auditable; 11 true original F01 GLB model references",()=>{
 const c=JSON.parse(file("assets/catalog.json"));
 const glbs=c.assets.filter(x=>x.src?.endsWith(".glb"));
 assert.equal(glbs.length,11);
 assert.equal(new Set(glbs.map(x=>x.id)).size,11);
 assert.ok(glbs.every(x=>/^assets\/models\/[a-z0-9_.-]+\.glb$/.test(x.src)));
 assert.ok(c.assets.some(x=>x.id==="f01-d-north"));
});
test("starter is localhost only and repo contains standalone handoff docs",()=>{
 const py=file("scripts/server.py"),node=file("scripts/server.mjs");
 assert.match(py,/127\.0\.0\.1/);
 assert.match(node,/127\.0\.0\.1/);
 assert.match(file("START-BUILDER-WINDOWS.bat"),/START|server\.py|server\.mjs/);
 assert.ok(fs.existsSync("docs/HANDOFF.md"));
});
