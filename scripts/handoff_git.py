"""Safe, isolated Git plumbing for explicit owner design handoff branches.
Never checks out a branch, resets working files, force pushes, or changes Trialum game.
The branch diff adds/replaces only handoff/approved-scene.json and handoff/manifest.json.
"""
import json, math, os, re, subprocess, tempfile
from pathlib import Path

ALLOWED_BRANCH=re.compile(r"^design/(?:s7-garden-v[1-4]|s7-master-pass2)$")

def validate_handoff(payload, GitFault):
 if not isinstance(payload,dict) or set(payload)!={"branch","project","manifest"}:
  raise GitFault("HANDOFF_PAYLOAD","Expected branch, project and manifest only","Use the Builder handoff button.")
 branch=payload["branch"]
 if not isinstance(branch,str) or not ALLOWED_BRANCH.fullmatch(branch):
  raise GitFault("HANDOFF_BRANCH","Only design/s7-garden-v1..v4 or design/s7-master-pass2 can receive a handoff","Choose one of four safe garden branches.")
 scene=payload["project"];manifest=payload["manifest"]
 if not isinstance(scene,dict) or scene.get("schemaVersion")!=1 or not isinstance(scene.get("instances"),list):
  raise GitFault("HANDOFF_SCENE","Expected an editable Builder schemaVersion=1 scene","Open a Builder garden first.")
 if len(scene["instances"])>6000:
  raise GitFault("HANDOFF_SCENE_SIZE","More than 6000 scene instances","Reduce scene complexity.")
 if scene.get("meta",{}).get("gameplayWrites",0)!=0 or scene.get("meta",{}).get("officialScene",False):
  raise GitFault("HANDOFF_RUNTIME","Scene must be design-only and not official gameplay","Only visual review designs can be handed off.")
 ids=set()
 for x in scene["instances"]:
  if not isinstance(x,dict) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,120}",str(x.get("assetId",""))):
   raise GitFault("HANDOFF_ASSET","Invalid asset ID","Save the scene with valid catalog models.")
  id=x.get("id")
  if not isinstance(id,str) or len(id)>80 or id in ids:
   raise GitFault("HANDOFF_INSTANCES","Scene object ID is missing or duplicated","Fix duplicate objects and retry.")
  ids.add(id)
  xyz=x.get("position")
  if not isinstance(xyz,list) or len(xyz)!=3 or any(not isinstance(v,(int,float)) or not math.isfinite(v) or abs(v)>300 for v in xyz):
   raise GitFault("HANDOFF_POSITION","Object coordinates are invalid","Use finite coordinates inside ±300m.")
 if not isinstance(manifest,dict) or manifest.get("targetBranch")!=branch or manifest.get("gameMainWrites") is not False:
  raise GitFault("HANDOFF_MANIFEST","Handoff manifest is inconsistent","Regenerate via Builder's handoff tool.")
 if not isinstance(manifest.get("referencedAssets"),list) or len(manifest["referencedAssets"])>500:
  raise GitFault("HANDOFF_REFERENCES","Invalid GLB reference manifest","Builder scene may refer to no more than 500 distinct assets.")
 if any(not isinstance(a,dict) or a.get("assetId") not in {v.get("assetId") for v in scene["instances"]} for a in manifest["referencedAssets"]):
  raise GitFault("HANDOFF_REFERENCES","Handoff assets do not match scene objects","Re-export the current scene.")
 return branch,scene,manifest

def publish_handoff(payload, ROOT, guard, git, GitFault):
 branch,scene,manifest=validate_handoff(payload,GitFault)
 gitdir=guard()  # localhost-only clone/branch/remote/git-lock safety
 git("fetch","origin","main",timeout=120)
 remote=git("ls-remote","--heads","origin","refs/heads/"+branch,timeout=90).splitlines()
 if remote:
  git("fetch","origin","refs/heads/"+branch+":refs/remotes/origin/"+branch,timeout=90)
  parent=git("rev-parse","refs/remotes/origin/"+branch)
 else:
  parent=git("rev-parse","refs/remotes/origin/main")
 with tempfile.TemporaryDirectory(prefix="trialum_handoff_",dir=str(gitdir)) as tmp:
  env={**os.environ,"GIT_INDEX_FILE":os.path.join(tmp,"index")}
  def isolated(*args,stdin=None):
   data=stdin.encode("utf8") if isinstance(stdin,str) else stdin
   p=subprocess.run(["git",*args],cwd=ROOT,env=env,input=data,capture_output=True,timeout=90)
   if p.returncode:
    raise GitFault("HANDOFF_GIT",p.stderr.decode("utf8","replace")[-1000:],
      "Git operation failed; local projects and current branch are untouched.")
   return p.stdout.decode("utf8","replace").strip()
  isolated("read-tree",parent)
  scene_json=json.dumps(scene,ensure_ascii=False,indent=2,allow_nan=False)+"\n"
  meta_json=json.dumps(manifest,ensure_ascii=False,indent=2,allow_nan=False)+"\n"
  for path,body in (("handoff/approved-scene.json",scene_json),("handoff/manifest.json",meta_json)):
   blob=isolated("hash-object","-w","--stdin",stdin=body)
   isolated("update-index","--add","--cacheinfo","100644",blob,path)
  tree=isolated("write-tree")
  commit=isolated("-c","user.name=Trialum Builder Owner Design",
      "-c","user.email=trialum-builder@users.noreply.github.com",
      "commit-tree",tree,"-p",parent,"-m","design(handoff): owner S7 garden JSON for "+branch)
 # No -f/force; remote may reject if branch advanced since we checked it.
 result=git("push","origin",commit+":refs/heads/"+branch,timeout=120)
 return {"branch":branch,"commit":commit,"message":result[-650:]}
