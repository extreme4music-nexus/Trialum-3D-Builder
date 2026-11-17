#!/usr/bin/env python3
"""Local-only Trialum Builder server: static files + explicit GitHub Desktop-like actions.
Only repository-specific Git commands, never shell, tokens, arbitrary paths or user-supplied refs.
Requires local Git credential helper (GitHub Desktop/Git Credential Manager/SSH).
"""
import base64,hashlib,json,os,re,secrets,subprocess,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
HOST="127.0.0.1"
TOKEN=secrets.token_urlsafe(32)
LOCK=threading.Lock()
def importmap_hash():
 """Only the exact locally shipped importmap is allowed as an inline script."""
 page=(ROOT/'index.html').read_text(encoding='utf-8')
 match=re.search(r'<script\\s+type=[\"\\\']importmap[\"\\\']\\s*>(.*?)</script>',page,re.S|re.I)
 if not match:raise RuntimeError('Builder importmap missing')
 digest=base64.b64encode(hashlib.sha256(match.group(1).encode('utf-8')).digest()).decode('ascii')
 return "'sha256-"+digest+"'"
ALLOWED_RE=re.compile(r"^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)extreme4music-nexus/Trialum-3D-Builder(?:\.git)?/?$")
def git(*args,timeout=90):
 p=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,text=True,timeout=timeout,stdin=subprocess.DEVNULL)
 if p.returncode:raise RuntimeError((p.stderr or p.stdout or "Git operation failed")[-650:])
 return p.stdout.strip()
def guard():
 if not (ROOT/".git").exists():raise RuntimeError("Repository not cloned with Git")
 if git("branch","--show-current")!="main":raise RuntimeError("Only Builder main is supported")
 if not ALLOWED_RE.fullmatch(git("remote","get-url","origin")):raise RuntimeError("Unexpected origin; refused")
def is_clean():
 return not git("status","--porcelain")
class Handler(SimpleHTTPRequestHandler):
 extensions_map={**SimpleHTTPRequestHandler.extensions_map,".js":"text/javascript",".mjs":"text/javascript",
 ".glb":"model/gltf-binary",".json":"application/json",".css":"text/css",".md":"text/markdown"}
 def translate_path(self,path):
  rel=unquote(urlsplit(path).path).lstrip("/")
  if not rel:rel="index.html"
  target=(ROOT/rel).resolve()
  if not target.is_relative_to(ROOT):return str(ROOT/"__blocked__")
  if any(p.startswith(".") for p in target.relative_to(ROOT).parts):return str(ROOT/"__blocked__")
  return str(target)
 def end_headers(self):
  self.send_header("Cache-Control","no-store")
  self.send_header("X-Content-Type-Options","nosniff")
  self.send_header("Referrer-Policy","no-referrer")
  self.send_header("Cross-Origin-Resource-Policy","same-origin")
  self.send_header("Content-Security-Policy","default-src 'self' blob: data:; script-src 'self' "+importmap_hash()+"; style-src 'self' 'unsafe-inline'; connect-src 'self' blob:; img-src 'self' blob: data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
  super().end_headers()
 def respond(self,status,data):
  raw=json.dumps(data,ensure_ascii=False).encode("utf-8")
  self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Content-Length",str(len(raw)));self.end_headers();self.wfile.write(raw)
 def allowed_origin(self):
  return self.headers.get("Origin")==f"http://{HOST}:{PORT}" and self.headers.get("Host")==f"{HOST}:{PORT}"
 def do_GET(self):
  route=urlsplit(self.path).path
  if route=="/api/git-status":
   try:
    if self.headers.get("Host")!=f"{HOST}:{PORT}":raise RuntimeError("Untrusted host")
    guard()
    self.respond(200,{"ok":True,"csrf":TOKEN,"branch":"main","changes":git("status","--short").splitlines()[:60],"remote":"GitHub Builder origin"})
   except (RuntimeError,subprocess.TimeoutExpired,FileNotFoundError) as e:self.respond(409,{"ok":False,"error":str(e)})
   return
  super().do_GET()
 def do_POST(self):
  route=urlsplit(self.path).path
  if route not in ("/api/git-pull","/api/git-publish"):self.respond(404,{"ok":False,"error":"Unknown route"});return
  if not self.allowed_origin() or self.headers.get("X-Trialum-CSRF")!=TOKEN or self.headers.get("Content-Type")!="application/json":
   self.respond(403,{"ok":False,"error":"Invalid origin or session"});return
  if self.headers.get("Content-Length")!="2":
   self.respond(400,{"ok":False,"error":"Expected empty JSON object"});return
  if self.rfile.read(2)!=b"{}":
   self.respond(400,{"ok":False,"error":"Invalid request"});return
  if not LOCK.acquire(blocking=False):self.respond(409,{"ok":False,"error":"Another Git action is running"});return
  try:
   guard()
   if route=="/api/git-pull":
    if not is_clean():raise RuntimeError("Uncommitted changes; save/publish before pull")
    output=git("pull","--ff-only","origin","main",timeout=120)
   else:
    # Commit only explicitly allowed design outputs, NOT scripts/server credentials.
    git("add","--","projects","assets/models","assets/catalog.json")
    if not git("diff","--cached","--name-only"):raise RuntimeError("No saved design changes to publish")
    git("commit","-m","design(builder): owner layout update",timeout=60)
    output=git("push","origin","HEAD:main",timeout=120)
   self.respond(200,{"ok":True,"message":output[-800:] or "Complete"})
  except (RuntimeError,subprocess.TimeoutExpired,FileNotFoundError) as e:self.respond(409,{"ok":False,"error":str(e)})
  finally:LOCK.release()
if __name__=="__main__":
 PORT=int(os.environ.get("PORT","8765"))
 print(f"TRIALUM BUILDER READY http://{HOST}:{PORT}/ (Ctrl+C to stop)",flush=True)
 ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
