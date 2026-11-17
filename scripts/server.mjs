import http from "node:http";
import {createHash} from "node:crypto";
import {readFile,stat,realpath} from "node:fs/promises";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const port=Number(process.env.PORT||8765),host="127.0.0.1";
const mime={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",".mjs":"text/javascript; charset=utf-8",
".json":"application/json; charset=utf-8",".css":"text/css; charset=utf-8",".glb":"model/gltf-binary",".png":"image/png",
".jpg":"image/jpeg",".jpeg":"image/jpeg",".svg":"image/svg+xml",".txt":"text/plain; charset=utf-8",".md":"text/markdown; charset=utf-8"};
const importmapHash=async()=>{
 const page=await readFile(path.join(root,"index.html"),"utf8");
 const match=page.match(/<script\\s+type=["\u0027]importmap["\u0027]\\s*>([\\s\\S]*?)<\\/script>/i);
 if(!match)throw Error("Builder importmap missing");
 return "\u0027sha256-"+createHash("sha256").update(match[1],"utf8").digest("base64")+"\u0027";
};
const server=http.createServer(async(req,res)=>{
 try{
  if(!["GET","HEAD"].includes(req.method)){res.writeHead(405);res.end("Method not allowed");return;}
  const pathname=new URL(req.url||"/","http://"+host+":"+port).pathname;
  const decoded=decodeURIComponent(pathname);
  if(decoded.includes("\0")||decoded.includes("\\"))throw Error("bad path");
  let target=path.resolve(root,"."+decoded);
  if(target!==root&&!target.startsWith(root+path.sep))throw Error("outside root");
  if(path.relative(root,target).split(path.sep).some(seg=>seg.startsWith(".")))throw Error("hidden path");
  if(target===root)target=path.join(root,"index.html");
  const resolved=await realpath(target);
  if(resolved!==root&&!resolved.startsWith(root+path.sep))throw Error("link outside root");
  const info=await stat(resolved),ext=path.extname(resolved).toLowerCase();
  if(!info.isFile()||!mime[ext])throw Error("unsupported");
  const bytes=await readFile(resolved);
  res.writeHead(200,{"Content-Type":mime[ext],"Content-Length":bytes.length,
   "Cache-Control":"no-cache","X-Content-Type-Options":"nosniff",
   "Referrer-Policy":"no-referrer","Cross-Origin-Resource-Policy":"same-origin",
   `Content-Security-Policy`:`default-src 'self' blob: data:; script-src 'self' ${await importmapHash()}; style-src 'self' 'unsafe-inline'; connect-src 'self' blob:; img-src 'self' blob: data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`});
  res.end(req.method==="HEAD"?undefined:bytes);
 }catch{res.writeHead(404,{"Content-Type":"text/plain"});res.end("Not found");}
});
server.listen(port,host,()=>console.log("TRIALUM BUILDER READY http://"+host+":"+port+"/ (Ctrl+C to stop)"));
