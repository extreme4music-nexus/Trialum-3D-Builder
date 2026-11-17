/* Runtime diagnostics so import/WebGL failure cannot masquerade as a working empty editor. */
(function(){
 const show=(msg)=>{
  const node=document.getElementById("statusText");
  if(node){node.textContent="⚠ Builder startup: "+String(msg).slice(0,260);node.style.color="#ffad9c";}
  else {const el=document.createElement("div");el.textContent="⚠ Builder startup: "+String(msg).slice(0,260);
   el.style.cssText="position:fixed;bottom:2px;left:2px;right:2px;padding:12px;background:#6a2830;color:white;z-index:99";
   document.body.append(el);}
 };
 window.addEventListener("error",ev=>show(ev.message||"JavaScript / Three.js module failed"));
 window.addEventListener("unhandledrejection",ev=>show(ev.reason?.message||"Unhandled JavaScript rejection"));
 window.setTimeout(()=>{const node=document.getElementById("statusText");
  if(node&&node.textContent==="Подготвено за дизајнирање.")show("3D editor did not initialize; press F12 → Console and check vendor/ models.");
 },7000);
})();