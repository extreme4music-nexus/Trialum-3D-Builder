import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import {createHash} from "node:crypto";
import {spawn} from "node:child_process";
import net from "node:net";

const html=fs.readFileSync("index.html","utf8");
const opening='<script type="importmap">';
const from=html.indexOf(opening);
const to=html.indexOf("</script>",from+opening.length);
const embedded=html.slice(from+opening.length,to);
const expected="'sha256-"+createHash("sha256").update(embedded,"utf8").digest("base64")+"'";
const map=JSON.parse(embedded);

test("importmap maps Three.js and all three addons to local vendored files",()=>{
 assert.ok(from>=0&&to>from,"importmap must precede app module");
 assert.equal(map.imports.three,"./vendor/three.module.js");
 assert.equal(map.imports["three/addons/"],"./vendor/addons/");
 assert.ok(html.indexOf(opening)<html.indexOf('src="./src/main.js"'));
 assert.ok(fs.existsSync("vendor/three.module.js"));
 assert.ok(fs.existsSync("vendor/addons/loaders/GLTFLoader.js"));
 assert.ok(fs.existsSync("vendor/addons/controls/TransformControls.js"));
});

const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function freePort(){
 const server=net.createServer();
 await new Promise((resolve,reject)=>server.once("error",reject).listen(0,"127.0.0.1",resolve));
 const port=server.address().port;
 await new Promise(resolve=>server.close(resolve));
 return port;
}
async function verifyServer(bin,args){
 const port=await freePort();
 const proc=spawn(bin,args,{env:{...process.env,PORT:String(port)},stdio:"ignore"});
 try{
  let response;
  for(let n=0;n<60;n++){
   if(proc.exitCode!==null)throw Error("Server exited prematurely");
   try{response=await fetch("http://127.0.0.1:"+port+"/");if(response.ok)break;}catch{}
   await sleep(100);
  }
  assert.ok(response?.ok,"Builder localhost server did not start");
  const csp=response.headers.get("content-security-policy")||"";
  assert.ok(csp.includes("script-src 'self' "+expected+";"),"CSP must permit only the exact inline importmap hash: "+csp);
  assert.doesNotMatch(csp,/script-src[^;]*unsafe-inline/);
  assert.match(await response.text(),/Trialum 3D World Builder/);
  const js=await fetch("http://127.0.0.1:"+port+"/vendor/three.module.js");
  assert.equal(js.status,200);
  assert.match(js.headers.get("content-type")||"",/javascript/);
 }finally{proc.kill();}
}
test("Node localhost HTTP CSP authorizes importmap, preserving strict JS policy",async()=>verifyServer("node",["scripts/server.mjs"]));
test("Python localhost HTTP CSP authorizes importmap with identical hash",{skip:process.platform==="win32"},async()=>verifyServer("python3",["scripts/server.py"]));
