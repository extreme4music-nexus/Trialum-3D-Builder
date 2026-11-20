#!/usr/bin/env python3
"""Local-only Trialum Builder server: static files + explicit GitHub Desktop-like actions.
Only repository-specific Git commands, never shell, tokens, arbitrary paths or user-supplied refs.
Requires local Git credential helper (GitHub Desktop/Git Credential Manager/SSH).
"""
import base64,hashlib,json,os,re,secrets,subprocess,tempfile,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit,unquote
from handoff_git import publish_handoff
ROOT=Path(__file__).resolve().parents[1]
HOST="127.0.0.1"
BUILDER_BRANCH="feature/remote-builder-3d-20261120"
PUBLIC_ORIGIN=os.environ.get("TRIALUM_BUILDER_PUBLIC_ORIGIN","http://127.0.0.1:8765").rstrip("/")
PUBLIC_HOST=urlsplit(PUBLIC_ORIGIN).netloc
TOKEN=secrets.token_urlsafe(32)
LOCK=threading.Lock()
def importmap_hash():
 """Only the exact locally shipped importmap is allowed as an inline script."""
 page=(ROOT/'index.html').read_text(encoding='utf-8')
 start_tag='<script type="importmap">'
 start=page.find(start_tag)
 end=page.find('</script>',start+len(start_tag)) if start>=0 else -1
 if end<0:raise RuntimeError('Builder importmap missing')
 inline_map=page[start+len(start_tag):end]
 digest=base64.b64encode(hashlib.sha256(inline_map.encode('utf-8')).digest()).decode('ascii')
 return "'sha256-"+digest+"'"
ALLOWED_RE=re.compile(r"^(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)extreme4music-nexus/Trialum-3D-Builder(?:\.git)?/?$")
VALID_BRANCH=BUILDER_BRANCH
DESIGN_PATHS=("projects","assets/models","assets/catalog.json")

class GitFault(RuntimeError):
 def __init__(self,code,detail,hint):
  super().__init__(detail)
  self.code,self.hint=code,hint

def failure(e):
 if isinstance(e,GitFault):
  return {"ok":False,"code":e.code,"error":str(e),"hint":e.hint}
 if isinstance(e,subprocess.TimeoutExpired):
  return {"ok":False,"code":"GIT_TIMEOUT","error":"Git operation timed out","hint":"Close simultaneous GitHub Desktop operations, inspect internet and retry once."}
 return {"ok":False,"code":"GIT_UNEXPECTED","error":str(e)[-650:],
         "hint":"Use CONNECT-GITHUB-WINDOWS.bat to diagnose the local clone before retrying."}

def git(*args,timeout=90):
 try:
  p=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,text=True,timeout=timeout,stdin=subprocess.DEVNULL)
 except FileNotFoundError as e:
  raise GitFault("GIT_NOT_FOUND","Git for Windows is not on PATH",
    "Install Git for Windows and reopen the Builder terminal; GitHub Desktop may use bundled Git.") from e
 if p.returncode:
  message=(p.stderr or p.stdout or "Git operation failed")[-1200:].strip()
  if re.search(r"(index|ORIG_HEAD|HEAD|packed-refs|refs[/\\].+)\.lock.*No such file or directory",message,re.I|re.S):
   raise GitFault("GIT_METADATA_DISAPPEARED",message,
    "Windows cannot create .git locks in this cloned folder. Stop GitHub Desktop operations, check the repository path and .git directory, then run CONNECT-GITHUB-WINDOWS.bat. Do not delete .git or run git init.")
  if re.search(r"Unable to create .*\.lock.*(Permission denied|Access is denied)",message,re.I|re.S):
   raise GitFault("GIT_METADATA_UNWRITABLE",message,
    "Windows denied writing .git lock files. Check read-only/security software/folder permissions and close other Git operations. Do not delete locks automatically.")
  if re.search(r"(index\.lock|ORIG_HEAD\.lock|Another git process|File exists)",message,re.I):
   raise GitFault("GIT_BUSY",message,
    "GitHub Desktop or another Git command may be active. Close overlapping Git operations. Never remove lock files automatically.")
  if "non-fast-forward" in message or "fetch first" in message:
   raise GitFault("GIT_REMOTE_AHEAD",message,
    "GitHub has newer commits. Use GitHub Desktop to review and Pull without discarding local commits.")
  raise GitFault("GIT_COMMAND_FAILED",message,
    "Check GitHub Desktop's repository status and CONNECT-GITHUB-WINDOWS.bat. The source files have not been deleted.")
 return p.stdout.strip()

def validate_clone():
 # This is deliberately checked BEFORE any Git write; a moved or deleted
 # repository is never silently reinitialized, recloned or repaired.
 if not ROOT.is_dir():
  raise GitFault("REPO_PATH_MISSING","The Builder project directory no longer exists",
     "Verify the exact local path in GitHub Desktop and launch START-BUILDER-WINDOWS.bat from that same folder.")
 dot=ROOT/".git"
 if not dot.is_dir():
  raise GitFault("GIT_DIRECTORY_MISSING","The Builder folder has no usable .git directory: "+str(dot),
     "Check the repository's local path in GitHub Desktop. Preserve projects/ and GLBs. Do not git init, force clone or delete .git.")
 try:
  gitdir=(dot).resolve(strict=True)
  if not gitdir.is_dir():
   raise FileNotFoundError()
 except (OSError,FileNotFoundError) as e:
  raise GitFault("GIT_DIRECTORY_MISSING","Git metadata directory cannot be accessed",
     "Check folder moves, Windows access permissions and security software. No automatic repair was attempted.") from e
 toplevel=git("rev-parse","--show-toplevel")
 if os.path.normcase(os.path.realpath(toplevel))!=os.path.normcase(os.path.realpath(str(ROOT))):
  raise GitFault("GIT_WRONG_WORKTREE","Git points at a different working copy: "+toplevel,
     "Open the correct clone through GitHub Desktop. Do not push edits from a mismatched folder.")
 if git("branch","--show-current")!=VALID_BRANCH:
  raise GitFault("GIT_WRONG_BRANCH","Only the dedicated Builder service branch is supported for direct sync",
     "Switch to feature/remote-builder-3d-20261120 in GitHub Desktop; this Builder control never changes branches for you.")
 if not ALLOWED_RE.fullmatch(git("remote","get-url","origin")):
  raise GitFault("GIT_WRONG_REMOTE","Origin is not the expected Trialum-3D-Builder repo",
     "Check GitHub Desktop repository identity. This control will not push to another remote.")
 return gitdir

def ensure_writable_gitdir(gitdir):
 if not gitdir.is_dir():
  raise GitFault("GIT_DIRECTORY_MISSING","Git metadata vanished during this session: "+str(gitdir),
     "Stop sync and check the cloned folder. Restart Builder from the correct folder after resolving Windows access.")
 for lock in ("index.lock","ORIG_HEAD.lock","HEAD.lock","packed-refs.lock"):
  if (gitdir/lock).exists():
   raise GitFault("GIT_BUSY","A Git lock is already present: "+lock,
     "Finish or close the GitHub Desktop operation first. Do not delete lock files while Git might be running.")
 try:
  # Harmless unique temporary probe proves .git currently permits file creation.
  # NEVER touch index.lock / ORIG_HEAD.lock; Git manages them itself.
  with tempfile.TemporaryFile(dir=str(gitdir)) as probe:
   probe.write(b"trialum local git write probe")
   probe.flush()
 except (OSError,PermissionError) as e:
  raise GitFault("GIT_METADATA_UNWRITABLE","Cannot create a temporary file inside the local .git directory: "+str(e),
     "Check Windows folder availability/permissions and antivirus. Do not reinstall or reclone before preserving design files.") from e

def guard():
 gitdir=validate_clone()
 ensure_writable_gitdir(gitdir)
 return gitdir

def is_clean():
 return not git("status","--porcelain")

def staged_paths():
 return [x.replace("\\","/") for x in git("diff","--cached","--name-only").splitlines() if x]

def publish_designs():
 guard()
 staged=staged_paths()
 if staged:
  raise GitFault("GIT_STAGED_CHANGES","Existing staged changes must be reviewed in GitHub Desktop: "+", ".join(staged[:8]),
    "The browser refuses to include unrelated staged files in a design commit. Review/commit/unstage them in GitHub Desktop; no automatic reset.")
 # New local commits from a prior failed push MUST be pushed, not recommitted.
 ahead=int(git("rev-list","--count",f"origin/{VALID_BRANCH}..HEAD") or "0")
 if ahead:
  if not is_clean():
   raise GitFault("GIT_LOCAL_COMMITS_WITH_CHANGES","Local commits await push but the worktree also has uncommitted changes",
     "Review pending work and publish existing commits in GitHub Desktop before making another design commit.")
  return git("push","origin",f"HEAD:{VALID_BRANCH}",timeout=120)
 git("add","--",*DESIGN_PATHS)
 staged=staged_paths()
 if not staged:
  raise GitFault("NO_DESIGN_CHANGES","No saved design changes found to publish",
   "Save your Builder project into this exact cloned repository first. Then use GitHub ↑.")
 for p in staged:
  if not (p.startswith("projects/") or p.startswith("assets/models/") or p=="assets/catalog.json"):
   raise GitFault("GIT_UNSAFE_STAGING","An unrelated file is staged: "+p,
     "Review staged changes in GitHub Desktop. The editor cannot commit arbitrary source files.")
 git("commit","-m","design(builder): owner layout update",timeout=60)
 return git("push","origin",f"HEAD:{VALID_BRANCH}",timeout=120)

def pull_designs():
 guard()
 if not is_clean():
  raise GitFault("GIT_DIRTY_WORKTREE","Local changes exist; Pull would risk overwriting them",
   "Save and commit your changes through GitHub Desktop or Builder GitHub ↑ before pulling.")
 return git("pull","--ff-only","origin",VALID_BRANCH,timeout=120)

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
  return self.headers.get("Origin")==PUBLIC_ORIGIN and self.headers.get("Host")==PUBLIC_HOST
 def do_GET(self):
  route=urlsplit(self.path).path
  if route=="/api/git-status":
   try:
    if self.headers.get("Host")!=PUBLIC_HOST:
     raise GitFault("BAD_HOST","Untrusted Builder Host header","Open the official Builder address.")
    guard()
    self.respond(200,{"ok":True,"csrf":TOKEN,"branch":VALID_BRANCH,
       "changes":git("status","--short").splitlines()[:60],
       "remote":"Trialum-3D-Builder origin"})
   except (GitFault,RuntimeError,subprocess.TimeoutExpired,FileNotFoundError) as e:
    self.respond(409,failure(e))
   return
  super().do_GET()

 def do_POST(self):
  route=urlsplit(self.path).path
  if route=="/api/handoff-publish":
   if not self.allowed_origin() or self.headers.get("X-Trialum-CSRF")!=TOKEN or self.headers.get("Content-Type")!="application/json":
    self.respond(403,{"ok":False,"code":"INVALID_SESSION","error":"Invalid origin or session"});return
   try:
    length=int(self.headers.get("Content-Length","0"))
   except (ValueError,OverflowError):
    length=-1
   if length<32 or length>3000000:
    self.respond(400,{"ok":False,"code":"HANDOFF_TOO_LARGE","error":"Handoff JSON must be 32B..3MB"});return
   try:
    payload=json.loads(self.rfile.read(length))
   except (ValueError,UnicodeError):
    self.respond(400,{"ok":False,"code":"HANDOFF_BAD_JSON","error":"Invalid JSON"});return
   if not LOCK.acquire(blocking=False):
    self.respond(409,{"ok":False,"code":"GIT_BUSY","error":"Another Git operation is running"});return
   try:
    result=publish_handoff(payload,ROOT,guard,git,GitFault)
    self.respond(200,{"ok":True,**result})
   except (GitFault,RuntimeError,subprocess.TimeoutExpired,FileNotFoundError,ValueError,TypeError) as e:
    self.respond(409,failure(e))
   finally:
    LOCK.release()
   return

  if route not in ("/api/git-pull","/api/git-publish"):
   self.respond(404,{"ok":False,"code":"UNKNOWN_ROUTE","error":"Unknown route"});return
  if not self.allowed_origin() or self.headers.get("X-Trialum-CSRF")!=TOKEN or self.headers.get("Content-Type")!="application/json":
   self.respond(403,{"ok":False,"code":"INVALID_SESSION","error":"Invalid origin or session"});return
  if self.headers.get("Content-Length")!="2":
   self.respond(400,{"ok":False,"code":"INVALID_PAYLOAD","error":"Expected empty JSON object"});return
  if self.rfile.read(2)!=b"{}":
   self.respond(400,{"ok":False,"code":"INVALID_PAYLOAD","error":"Invalid request"});return
  if not LOCK.acquire(blocking=False):
   self.respond(409,{"ok":False,"code":"GIT_BUSY","error":"Another Builder Git action is running",
      "hint":"Finish the previous operation; avoid concurrent GitHub Desktop sync."});return
  try:
   output=pull_designs() if route=="/api/git-pull" else publish_designs()
   self.respond(200,{"ok":True,"message":output[-800:] or "Complete"})
  except (GitFault,RuntimeError,subprocess.TimeoutExpired,FileNotFoundError) as e:
   self.respond(409,failure(e))
  finally:
   LOCK.release()

if __name__=="__main__":
 PORT=int(os.environ.get("PORT","8765"))
 print(f"TRIALUM BUILDER READY http://{HOST}:{PORT}/ (Ctrl+C to stop)",flush=True)
 ThreadingHTTPServer((HOST,PORT),Handler).serve_forever()
