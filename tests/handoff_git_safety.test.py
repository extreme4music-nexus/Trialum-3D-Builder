#!/usr/bin/env python3
"""S7 design handoff must never write Trialum Game, change Builder main, checkout
worktree, force push, or change unrelated files. Pure local temporary Git test.
"""
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from handoff_git import validate_handoff,publish_handoff

class Fault(RuntimeError):
 def __init__(self,code,detail,hint):
  super().__init__(detail)
  self.code,self.hint=code,hint

def sample(branch="design/s7-garden-v1"):
 project={
  "schemaVersion":1,"projectId":"trialum-s7-complete-garden-v1-test",
  "name":"Review owner garden","instances":[
   {"id":"plant-1","assetId":"lumemoss-mature",
    "position":[0.0,0.0,2.0],"rotationY":0,"scale":[1,1,1]}],
  "assets":[],"meta":{"officialScene":False,"gameplayWrites":0}}
 manifest={"targetBranch":branch,"gameMainWrites":False,
           "referencedAssets":[{"assetId":"lumemoss-mature","src":"assets/models/lumemoss-mature.glb"}]}
 return {"branch":branch,"project":project,"manifest":manifest}

class HandoffTests(unittest.TestCase):
 def test_malformed_or_game_state_payload_is_rejected(self):
  p=sample()
  for candidate in ["../main","main","feature/lw-d-game","design/s7-garden-v0","design/s7-garden-v5"]:
   with self.subTest(candidate=candidate):
    p=sample(candidate)
    with self.assertRaises(Fault):
     validate_handoff(p,Fault)
  assert validate_handoff(sample("design/s7-master-pass2"),Fault)[0]=="design/s7-master-pass2"
  p=sample();p["project"]["meta"]["gameplayWrites"]=1
  with self.assertRaises(Fault):validate_handoff(p,Fault)
  p=sample();p["project"]["meta"]["officialScene"]=True
  with self.assertRaises(Fault):validate_handoff(p,Fault)
  p=sample();p["project"]["instances"][0]["position"]=[1,9e99,0]
  with self.assertRaises(Fault):validate_handoff(p,Fault)
  p=sample();p["project"]["instances"][0]["id"]="../config"
  # IDs are opaque strings but never used as filenames.
  assert validate_handoff(p,Fault)[0]=="design/s7-garden-v1"

 def test_branch_contains_only_handoff_diff_main_untouched(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);bare=root/"remote.git";work=root/"work"
   def run(cwd,*args,input=None):
    r=subprocess.run(["git",*args],cwd=cwd,input=input,text=True,capture_output=True,timeout=60)
    if r.returncode:raise RuntimeError("git failed "+repr(args)+": "+r.stderr)
    return r.stdout.strip()
   run(root,"init","--bare",str(bare))
   run(root,"clone",str(bare),str(work))
   run(work,"config","user.name","Trialum Safety QA")
   run(work,"config","user.email","builder-qa@users.noreply.github.com")
   run(work,"checkout","-b","main")
   (work/"README.md").write_text("main original\n")
   run(work,"add","README.md")
   run(work,"commit","-m","initial")
   run(work,"push","-u","origin","main")
   original=run(work,"rev-parse","HEAD")
   def git(*args,timeout=90):
    return run(work,*args)
   def guard():
    assert run(work,"branch","--show-current")=="main"
    assert not list((work/".git").glob("*.lock"))
    return work/".git"
   response=publish_handoff(sample(),work,guard,git,Fault)
   self.assertEqual(response["branch"],"design/s7-garden-v1")
   self.assertEqual(run(work,"branch","--show-current"),"main")
   self.assertEqual(run(work,"rev-parse","HEAD"),original)
   self.assertEqual(run(work,"status","--porcelain"),"")
   remote=run(work,"ls-remote","origin","refs/heads/main")
   self.assertTrue(remote.startswith(original))
   diff=run(work,"diff","--name-only",original,response["commit"]).splitlines()
   self.assertEqual(diff,["handoff/approved-scene.json","handoff/manifest.json"])
   published=run(work,"ls-remote","origin","refs/heads/design/s7-garden-v1")
   self.assertTrue(published.startswith(response["commit"]))
   # Repeat same branch, new review: still only data files and safe fast-forward.
   p=sample();p["project"]["instances"][0]["position"][0]=2
   response2=publish_handoff(p,work,guard,git,Fault)
   self.assertNotEqual(response2["commit"],response["commit"])
   self.assertEqual(run(work,"branch","--show-current"),"main")
   self.assertEqual(run(work,"rev-parse","HEAD"),original)
   self.assertEqual(run(work,"status","--porcelain"),"")
   self.assertEqual(run(work,"diff","--name-only",response["commit"],response2["commit"]),
                    "handoff/approved-scene.json")

if __name__=="__main__":
 unittest.main(verbosity=2)
