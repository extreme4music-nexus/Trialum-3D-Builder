#!/usr/bin/env python3
"""Original S7 G01 anti-jagged 3D edge trim; preserves four water cutouts.
Generate a single physically real glTF2 GLB and register it ONLY in Builder
S7 MASTER review branch. This is visual decoration, never gameplay geometry.
"""
import hashlib, json, math, struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MODEL_ID="s7-master-g01-edge-finish"
PATH=ROOT/"assets/models"/(MODEL_ID+".glb")
N=192
BIN=bytearray()
VIEWS=[];ACCESSORS=[];PRIMS=[]
MATERIALS=[
 {"name":"S7 G01 honed cream edge","doubleSided":True,
  "pbrMetallicRoughness":{"baseColorFactor":[.78,.78,.71,1],"metallicFactor":0.02,"roughnessFactor":.64}},
 {"name":"S7 G01 sage dark lip","doubleSided":True,
  "pbrMetallicRoughness":{"baseColorFactor":[.32,.48,.44,1],"metallicFactor":.43,"roughnessFactor":.44}},
 {"name":"S7 G01 soft cyan inlay","doubleSided":True,
  "emissiveFactor":[.005,.09,.09],
  "pbrMetallicRoughness":{"baseColorFactor":[.22,.74,.7,1],"metallicFactor":.07,"roughnessFactor":.35}}
]

def triangles(material,quad_iter):
 points=[];normals=[]
 for a,b,c,d in quad_iter:
  for q in ((a,b,c),(a,c,d)):
   u=[q[1][k]-q[0][k] for k in range(3)]
   v=[q[2][k]-q[0][k] for k in range(3)]
   n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
   norm=math.sqrt(sum(k*k for k in n)) or 1
   for p in q:points.extend(p);normals.extend(x/norm for x in n)
 def attr(vals):
  while len(BIN)%4:BIN.append(0)
  start=len(BIN)
  raw=struct.pack("<"+"f"*len(vals),*vals)
  BIN.extend(raw)
  VIEWS.append({"buffer":0,"byteOffset":start,"byteLength":len(raw),"target":34962})
  ACCESSORS.append({"bufferView":len(VIEWS)-1,"componentType":5126,
     "count":len(vals)//3,"type":"VEC3",
     "min":[min(vals[k::3]) for k in range(3)],
     "max":[max(vals[k::3]) for k in range(3)]})
  return len(ACCESSORS)-1
 p=attr(points);n=attr(normals)
 PRIMS.append({"attributes":{"POSITION":p,"NORMAL":n},"material":material,"mode":4})

def ring(r1,r2,y):
 for i in range(N):
  a=math.tau*i/N;b=math.tau*(i+1)/N
  yield ([r2*math.cos(a),y,r2*math.sin(a)],
   [r1*math.cos(a),y,r1*math.sin(a)],
   [r1*math.cos(b),y,r1*math.sin(b)],
   [r2*math.cos(b),y,r2*math.sin(b)])
def outer_wall(r,y_top,y_low):
 for i in range(N):
  a=math.tau*i/N;b=math.tau*(i+1)/N
  yield ([r*math.cos(a),y_top,r*math.sin(a)],
   [r*math.cos(a),y_low,r*math.sin(a)],
   [r*math.cos(b),y_low,r*math.sin(b)],
   [r*math.cos(b),y_top,r*math.sin(b)])

def main():
 # The old original G01 padded-circle has visible 0.46m square steps at radius
 # 16.95. This edge trim extends to r=17.43, hiding every terminal square;
 # the nearest aquatic satellite is inside r=13.38, so water stays open.
 triangles(0,ring(16.05,17.38,.065))
 triangles(1,ring(17.35,17.43,.075))
 triangles(1,outer_wall(17.43,.075,-.13))
 triangles(2,ring(16.10,16.17,.081))
 BIN.extend(b"\0"*(-len(BIN)%4))
 doc={"asset":{"version":"2.0","generator":"Trialum S7 MASTER original circular G01 edge 192 segments",
       "extras":{"visualOnly":True,"gameplayWrites":0,"preservesFourWaterHoles":True}},
  "scene":0,"scenes":[{"nodes":[0]}],
  "nodes":[{"name":"G01.finish.smooth-circular-pad-edge","mesh":0,
   "extras":{"visualOnly":True,"renderOnly":True,"noNewAquaticSlots":True}}],
  "meshes":[{"name":"G01.cream-metal-cyan.trim","primitives":PRIMS}],
  "materials":MATERIALS,"buffers":[{"byteLength":len(BIN)}],
  "bufferViews":VIEWS,"accessors":ACCESSORS}
 data=json.dumps(doc,separators=(",",":"),ensure_ascii=False).encode("utf8")
 data+=b" "*(-len(data)%4)
 raw=(struct.pack("<III",0x46546c67,2,12+8+len(data)+8+len(BIN))+
      struct.pack("<II",len(data),0x4e4f534a)+data+
      struct.pack("<II",len(BIN),0x004e4942)+bytes(BIN))
 assert raw[:4]==b"glTF"
 assert struct.unpack_from("<I",raw,8)[0]==len(raw)
 PATH.write_bytes(raw)
 catalogpath=ROOT/"assets/catalog.json"
 catalog=json.loads(catalogpath.read_text(encoding="utf8"))
 row={"id":MODEL_ID,"name":"G-01 · мазен кружен раб (192 сегменти)",
  "category":"Градина S7 · Завршни елементи","src":"assets/models/"+MODEL_ID+".glb",
  "dimensions":[34.86,.211,34.86],"placement":"floor",
  "visualOnly":True,"gameplayWrites":0,"ownerVisualPass":False,
  "source":"tools/b1/build-s7-master-g01-finish.py"}
 ids={a["id"] for a in catalog["assets"]}
 if MODEL_ID not in ids:catalog["assets"].append(row)
 catalog["genuineGlbCount"]=sum(str(a.get("src") or "").endswith(".glb") for a in catalog["assets"])
 assert catalog["genuineGlbCount"]==361,catalog["genuineGlbCount"]
 catalog["assetLibraryVersion"]="2026-11-19-s7-master-review-smoothed-g01-361"
 catalogpath.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 projectpath=ROOT/"projects/trialum-s7-master-garden-review.json"
 proj=json.loads(projectpath.read_text(encoding="utf8"))
 if not any(x["id"]=="master-g01-edge-finish" for x in proj["instances"]):
  proj["instances"].append({
   "id":"master-g01-edge-finish","assetId":MODEL_ID,
   "label":"G-01 · професионален непрекинат кружен завршеток",
   "position":[0,0,0],"rotationY":0,"scale":[1,1,1],"layer":"structure",
   "locked":False,"visible":True,"binding":"",
   "note":"192-segment circular anti-jagged finish, explicitly outside all 4 water apertures, no gameplay write."})
 projectpath.write_text(json.dumps(proj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 report={"glb":str(PATH.relative_to(ROOT)),"sha256":hashlib.sha256(raw).hexdigest(),
         "bytes":len(raw),"outerRadius":17.43,"segments":N,
         "waterBasinCount":4,"gameplayWrites":0,"ownerVisualPass":False}
 (ROOT/"assets/s7-master-g01-edge-manifest.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
 print("PASS S7 G01 real 192-section finish GLB",report)
if __name__=="__main__":main()
