#!/usr/bin/env python3
"""Builder-only GLB conversion of two EXISTING Trialum S5 warehouse annex structures.
Geometry dimensions / part positions copied from Trialum warehouse-rooms.mjs.
No stock, food, animations, live game writes or simulated props.
"""
import json,runpy,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
Model=runpy.run_path(str(ROOT/"tools/b1/build-agro-greenhouse.py"))["Model"]
OUT=ROOT/"build/warehouse-annex-prefabs";OUT.mkdir(parents=True,exist_ok=True)
MODEL_STATUS="NEW_BUILDER_GLB_CONVERSION_FROM_EXISTING_RUNTIME_GEOMETRY_OWNER_VISUAL_PENDING"
def make(room):
 m=Model()
 m.nodes[0]["name"]="trialum.warehouse."+room+".structural-annex"
 m.nodes[0]["extras"]={"sceneId":"trialum.ground.agro.warehouse","area":room,"gameAuthority":False,
 "source":"prototypes/lw-d/scenes/agro-food-warehouse/warehouse-rooms.mjs","status":MODEL_STATUS}
 colors=[("wall",[.725,.831,.784],.69,.04),("floor",[.482,.682,.643],.42,.13),
         ("frame",[.098,.31,.353],.33,.45),("rim",[.843,.718,.463],.28,.62),
         ("mint",[.333,.804,.722],.3,.10),("cold",[.514,.847,.882],.32,.08),
         ("panel",[.149,.333,.392],.22,.27)]
 mats={}
 for label,rgb,rough,metal in colors:
  mats[label]=len(m.materials)
  mat={"name":"annex."+label,"pbrMetallicRoughness":{
   "baseColorFactor":[*rgb,1.],"roughnessFactor":rough,"metallicFactor":metal},"doubleSided":True}
  if label in ("mint","cold"):mat["emissiveFactor"]=[.02,.16,.14] if label=="mint" else [.01,.1,.13]
  m.materials.append(mat)
 def box(name,material,pos,size):m.box(room+"."+name,pos,size,mats[material])
 w,d,h=4.4,6.7,4.3
 box("floor","floor",[0,-.085,0],[w,.18,d])
 box("solid-roof","wall",[0,h,0],[w,.20,d])
 box("rear-wall","wall",[0,h/2,-d/2],[w,h,.21])
 for side in (-1,1):
  box(f"side-wall-{side}","wall",[side*w/2,h/2,0],[.18,h,d])
  box(f"side-light-{side}","mint",[side*(w/2-.17),h-.22,0],[.065,.05,d-.3])
 box("door-top","rim",[0,3.38,3.38],[2.52,.17,.3])
 for side in (-1,1):box(f"door-post-{side}","rim",[side*1.2,1.69,3.38],[.12,3.38,.3])
 box("terminal","panel",[0,h*.52,-d/2+.2],[2.3,1,.09])
 box("terminal-led-top","mint",[0,h*.82,-d/2+.27],[1.83,.045,.06])
 box("terminal-led-bottom","mint",[0,h*.4,-d/2+.27],[1.44,.045,.06])
 if room=="cold":
  for side in (-1,1):
   box(f"cooling-{side}","cold",[side*1.88,2.4,-1.72],[.12,.82,1.32])
   box(f"thermal-monitor-{side}","panel",[side*1.86,1.9,-1.7],[.15,.31,.45])
  for i in range(4):box(f"sealed-unit-{i}","cold",[-1.25+i*.82,.27,2],[.55,.49,.57])
 else:
  box("dispatch-slot","rim",[0,.85,-1.9],[1.58,.16,.73])
  for i in range(3):box(f"packaging-box-{i}","panel",[(i-1)*.52,1.08,-1.9],[.40,.42,.37])
 m.node("ground.agro.warehouse.subroom-"+("cold" if room=="cold" else "pack"),
        extras={"kind":"portal","noGameAuthority":True,"area":room},xyz=[0,1.6,3.38])
 return m
evidence={}
for kind in ("cold","packing"):
 raw=make(kind).glb()
 name="food-"+kind+"-annex-shell.glb"
 assert raw[:4]==b"glTF" and len(raw)<2_000_000
 (OUT/name).write_bytes(raw)
 evidence[name]={"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"status":MODEL_STATUS}
(OUT/"ANNEX-GLB-EVIDENCE.json").write_text(json.dumps(evidence,indent=2)+"\n")
print("Generated",list(evidence))
