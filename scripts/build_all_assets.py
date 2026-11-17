#!/usr/bin/env python3
"""Rebuild ALL original Trialum 3D asset families from mirrored immutable sources.
Output is real GLB 2.0 in Builder assets/models; never writes game data.
The source generators remain byte-identical to Trialum's 2026-11-17 LW-D branch.
"""
from __future__ import annotations
import hashlib,json,shutil,struct,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/"tools/b1"
DEST=ROOT/"assets/models"
SOURCE_COMMIT="b801808a5b219284d52c52a8ae8e643700c84478"
SOURCES={
 "atrium.glb":"prototypes/lw-d/scenes/agro-lobby/atrium.glb",
 "warehouse-shell.glb":"prototypes/lw-d/scenes/agro-food-warehouse/warehouse-shell.glb",
 "smart-storage-rack.glb":"prototypes/lw-d/scenes/agro-food-warehouse/smart-storage-rack.glb",
 "cold-locker.glb":"prototypes/lw-d/scenes/agro-food-warehouse/cold-locker.glb",
 "cargo-crates.glb":"prototypes/lw-d/scenes/agro-food-warehouse/cargo-crates.glb",
 "conveyor-sorter.glb":"prototypes/lw-d/scenes/agro-food-warehouse/conveyor-sorter.glb",
 "holo-inventory-kiosk.glb":"prototypes/lw-d/scenes/agro-food-warehouse/holo-inventory-kiosk.glb",
 "mini-transporter.glb":"prototypes/lw-d/scenes/agro-food-warehouse/mini-transporter.glb",
 "greenhouse-shell.glb":"prototypes/lw-d/scenes/agro-greenhouse/greenhouse-shell.glb",
 "greenhouse-floor-shell.glb":"prototypes/lw-d/scenes/agro-greenhouse/greenhouse-floor-shell.glb",
 "greenhouse-glass-roof-shell.glb":"prototypes/lw-d/scenes/agro-greenhouse/greenhouse-glass-roof-shell.glb",
 "g01-main-basin.glb":"build/g01-watercore/g01-main-basin.glb",
 "g01-satellite-basins.glb":"build/g01-watercore/g01-satellite-basins.glb",
 "g01-walkway-and-railings.glb":"build/g01-watercore/g01-walkway-and-railings.glb",
 "g01-crossing-bridge.glb":"build/g01-watercore/g01-crossing-bridge.glb",
 "g01-visual-service-pumps.glb":"build/g01-watercore/g01-visual-service-pumps.glb",
 "g01-water-surfaces-animated.glb":"build/g01-aquatic-review/g01-water-surfaces-animated.glb",
 **{f"aquaglow-{stage}.glb":f"build/g01-aquatic-review/aquaglow-{stage}.glb"
    for stage in ("sprout","young","growing","mature","weakened","dead")},
 "pilot-room.glb":"prototypes/lw-d/b1/pilot-room.glb",
}
assert len(SOURCES)==24,len(SOURCES)

def run(command):
 print("[GLB] RUN", " ".join(map(str,command)),flush=True)
 subprocess.run(list(map(str,command)),cwd=ROOT,check=True,timeout=240)

def check(raw,name):
 if len(raw)<28 or raw[:4]!=b"glTF" or struct.unpack_from("<II",raw,4)!=(2,len(raw)):
  raise RuntimeError(f"Invalid glTF2 binary: {name}")
 jlen,jtype=struct.unpack_from("<I4s",raw,12)
 if jtype!=b"JSON" or jlen<20 or 20+jlen>len(raw):
  raise RuntimeError(f"Invalid GLB JSON chunk: {name}")
 info=json.loads(raw[20:20+jlen])
 if info.get("asset",{}).get("version")!="2.0" or not info.get("meshes"):
  raise RuntimeError(f"Missing real geometry: {name}")
 if len(raw)>5_000_000:raise RuntimeError(f"GLB unexpectedly large: {name}")
 return {"meshes":len(info["meshes"]),"nodes":len(info.get("nodes",[])),
         "animations":len(info.get("animations",[]))}

def main():
 # Original Trialum generators, not replacements/reconstructions.
 for script in ("build-agro-greenhouse.py","build-agro-g01-watercore.py","build-agro-g01-aquatic.py"):
  run([sys.executable,TOOLS/script])
 for script in ("build-agro-lobby.mjs","build-food-warehouse.mjs","generate-glb.mjs"):
  run(["node",TOOLS/script])
 DEST.mkdir(parents=True,exist_ok=True)
 evidence=[]
 for name,rel in SOURCES.items():
  src=ROOT/rel
  if not src.is_file():raise RuntimeError(f"Missing model source output {rel}")
  raw=src.read_bytes()
  details=check(raw,name)
  target=DEST/name
  if not target.exists() or target.read_bytes()!=raw:
   shutil.copyfile(src,target)
  if target.read_bytes()!=raw:raise RuntimeError(f"Copy verification failure {name}")
  evidence.append({"file":name,"src":"assets/models/"+name,"sourceOutput":rel,
                   "size":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),**details})
 evidence.sort(key=lambda item:item["file"])
 manifest={"schemaVersion":1,"date":"2026-11-17","sourceRepository":"extreme4music-nexus/Trialum",
  "sourceCommit":SOURCE_COMMIT,
  "renderStatus":"BINARY_CI_VERIFIED_OWNER_VISUAL_PENDING",
  "visualOnly":True,"gameplayWrites":False,"newModels":len(evidence),
  "assets":evidence}
 (ROOT/"assets/TRIALUM_LEGACY_GLB_MANIFEST.json").write_text(
  json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(f"[GLB] PASS: all {len(evidence)} original historical GLBs mirrored and hashed",flush=True)

if __name__=="__main__":main()
