#!/usr/bin/env python3
"""S7 G-00L glass service wing: open floor-to-portal annex for original S7 dome.
Visual-only procedural glTF2. Roof outside original dome circle; no glass floor,
no new room slots, no changes to original greenhouse-shell.glb or game state.
"""
from __future__ import annotations
import hashlib, json, math, pathlib, struct

ROOT=pathlib.Path(__file__).resolve().parents[2]
ID="s7-master-g00l-glass-service-wing"
OUTPUT=ROOT/"assets/models"/(ID+".glb")
BIN=bytearray();VIEWS=[];ACCESSORS=[];PRIMS=[]
MATS=[
 {"name":"G00L light glazing","doubleSided":True,"alphaMode":"BLEND",
  "pbrMetallicRoughness":{"baseColorFactor":[.62,.92,.88,.20],"roughnessFactor":.07,"metallicFactor":0.02}},
 {"name":"G00L brushed structural chrome","doubleSided":True,
  "pbrMetallicRoughness":{"baseColorFactor":[.68,.76,.72,1],"roughnessFactor":.32,"metallicFactor":.68}},
 {"name":"G00L warm sage fascia","doubleSided":True,
  "pbrMetallicRoughness":{"baseColorFactor":[.31,.49,.42,1],"roughnessFactor":.56,"metallicFactor":.31}},
]
def add_faces(faces,mat):
 positions=[];normals=[]
 for a,b,c,d in faces:
  for points in ((a,b,c),(a,c,d)):
   ax,ay,az=points[0];bx,by,bz=points[1];cx,cy,cz=points[2]
   u=(bx-ax,by-ay,bz-az);v=(cx-ax,cy-ay,cz-az)
   n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
   norm=math.sqrt(sum(x*x for x in n)) or 1
   for p in points:
    positions.extend(p);normals.extend(x/norm for x in n)
 def attr(data):
  while len(BIN)%4:BIN.append(0)
  offset=len(BIN)
  raw=struct.pack("<"+len(data)*"f",*data);BIN.extend(raw)
  VIEWS.append({"buffer":0,"byteOffset":offset,"byteLength":len(raw),"target":34962})
  ACCESSORS.append({"bufferView":len(VIEWS)-1,"componentType":5126,
    "count":len(data)//3,"type":"VEC3",
    "min":[min(data[i::3]) for i in range(3)],"max":[max(data[i::3]) for i in range(3)]})
  return len(ACCESSORS)-1
 PRIMS.append({"material":mat,"mode":4,
     "attributes":{"POSITION":attr(positions),"NORMAL":attr(normals)}})
def rectangle(xa,ya,za,xb,yb,zb):
 # Keep coordinate ranges ordered; front/top/bottom for a real solid beam.
 x0,x1=sorted((xa,xb));y0,y1=sorted((ya,yb));z0,z1=sorted((za,zb))
 p=lambda x,y,z:[x,y,z]
 return [
  (p(x0,y0,z0),p(x1,y0,z0),p(x1,y0,z1),p(x0,y0,z1)),
  (p(x0,y1,z0),p(x0,y1,z1),p(x1,y1,z1),p(x1,y1,z0)),
  (p(x0,y0,z0),p(x0,y1,z0),p(x1,y1,z0),p(x1,y0,z0)),
  (p(x0,y0,z1),p(x1,y0,z1),p(x1,y1,z1),p(x0,y1,z1)),
  (p(x0,y0,z0),p(x0,y0,z1),p(x0,y1,z1),p(x0,y1,z0)),
  (p(x1,y0,z0),p(x1,y1,z0),p(x1,y1,z1),p(x1,y0,z1))
 ]
def main():
 glass=[];metal=[];sage=[]
 # Geometry is to the LEFT (negative X) of the actual entrance x=-3..3,z=14..25.
 # This is an open side service extension, not a fifth crop finger.
 for x in range(-19,-3):
  for z in range(5,25):
   # Do not add a second roof under original central GLASS DOME.
   # The matching dome's 17m footprint and curved surface are kept untouched.
   if math.hypot(x+.5,z+.5)<16.85:continue
   glass.append(([x,5.15,z],[x+1,5.15,z],
                 [x+1,5.15,z+1],[x,5.15,z+1]))
 # Minimal vertical glazing only at exterior boundaries; entry and dome
 # connection are OPEN, so no navigational wall blocks the existing architecture.
 for z in range(5,25):
  if math.hypot(-19,z+.5)<16.9:continue
  glass.append(([-19,.15,z],[-19,.15,z+1],
                [-19,5.15,z+1],[-19,5.15,z]))
 for x in range(-19,-3):
  glass.append(([x,.15,25],[x+1,.15,25],[x+1,5.15,25],[x,5.15,25]))
 # Exterior chrome posts and 1m-spaced lightweight roof stringers.
 for z in (5,9,13,17,21,25):
  metal.extend(rectangle(-19.09,.03,z-.065,-18.91,5.21,z+.065))
  metal.extend(rectangle(-19.1,5.11,z-.055,-3.0,5.22,z+.055))
 for x in (-19,-15,-11,-7,-3):
  metal.extend(rectangle(x-.065,5.10,5.0,x+.065,5.21,25.0))
 for x in (-19,-15,-11,-7,-3):
  metal.extend(rectangle(x-.075,.03,24.93,x+.075,5.21,25.07))
 # Facade belt and open public threshold — no teleport, collision or gameplay.
 sage.extend(rectangle(-19.10,4.93,24.94,-3.0,5.12,25.10))
 sage.extend(rectangle(-19.10,.02,24.93,-3.02,.14,25.06))
 assert len(glass)>150
 add_faces(glass,0);add_faces(metal,1);add_faces(sage,2)
 BIN.extend(b"\0"*(-len(BIN)%4))
 doc={"asset":{"version":"2.0","generator":"Trialum G00L MASTER open service corner original visual-only extension",
    "extras":{"originalGreenhouseUnmodified":True,"gameplayWrites":0,"ownerApproval":"PENDING",
      "serviceZone":"G-00L","isFifthFinger":False}},
   "scene":0,"scenes":[{"nodes":[0]}],
   "nodes":[{"name":"G00L.open-glass-service-annex","mesh":0}],
   "meshes":[{"name":"G00L-original-service-wing","primitives":PRIMS}],
   "materials":MATS,"buffers":[{"byteLength":len(BIN)}],
   "bufferViews":VIEWS,"accessors":ACCESSORS}
 data=json.dumps(doc,separators=(",",":")).encode("utf8");data+=b" "*(-len(data)%4)
 raw=(struct.pack("<III",0x46546c67,2,12+8+len(data)+8+len(BIN))+
   struct.pack("<II",len(data),0x4e4f534a)+data+struct.pack("<II",len(BIN),0x004e4942)+bytes(BIN))
 assert raw[:4]==b"glTF" and struct.unpack_from("<I",raw,8)[0]==len(raw)
 OUTPUT.write_bytes(raw)
 catpath=ROOT/"assets/catalog.json"
 catalog=json.loads(catpath.read_text(encoding="utf8"))
 row={"id":ID,"name":"G-00L · стаклен отворен сервисен анекс",
   "category":"Градина S7 · Завршни елементи","src":"assets/models/"+ID+".glb",
   "dimensions":[16.2,5.23,20.2],"placement":"floor",
   "visualOnly":True,"gameplayWrites":0,"ownerVisualPass":False,
   "source":"tools/b1/build-s7-g00l-annex.py"}
 if not any(x["id"]==ID for x in catalog["assets"]):catalog["assets"].append(row)
 catalog["genuineGlbCount"]=sum(str(a.get("src") or "").endswith(".glb") for a in catalog["assets"])
 assert catalog["genuineGlbCount"]==362,catalog["genuineGlbCount"]
 catalog["assetLibraryVersion"]="2026-11-19-s7-master-g00l-glass-annex-362"
 catpath.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 scene=ROOT/"projects/trialum-s7-master-garden-review.json"
 p=json.loads(scene.read_text(encoding="utf8"))
 if not any(a["id"]=="master-g00l-glass-annex" for a in p["instances"]):
  p["instances"].append({"id":"master-g00l-glass-annex","assetId":ID,
   "label":"G-00L · отворен стаклен сервисен анекс",
   "position":[0,0,0],"rotationY":0,"scale":[1,1,1],
   "layer":"structure","locked":False,"visible":True,"binding":"",
   "note":"S7 owner review: original central glass dome remains untouched; G-00L left of entrance remains open to main greenhouse."})
 # Bridge between the service platform and the actual entrance floor, without
 # inventing another room or going through the central water basins.
 known={a["id"] for a in p["instances"]}
 for z in (17,19,21,23):
  for x in (-6,-4):
   id=f"master-g00l-entrance-connector-x{abs(x)}-z{z}"
   if id in known:continue
   p["instances"].append({"id":id,"assetId":"f01-a",
    "label":"G-00L · поврзувачка подна патека",
    "position":[x,.012,z],"rotationY":0,"scale":[2,1,2],
    "layer":"floor","locked":False,"visible":True,"binding":"",
    "note":"Physical 2m passage from G-00L racks to original greenhouse entrance; fully editable."})
 p["meta"]["ownerVisualPass"]=False;p["meta"]["officialScene"]=False;p["meta"]["gameplayWrites"]=0
 scene.write_text(json.dumps(p,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 manifest={"id":ID,"path":str(OUTPUT.relative_to(ROOT)),
  "bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
  "openServiceZone":True,"roofOnlyOutsideOriginalDome":True,
  "originalShellUnmodified":True,"gameplayWrites":0,"ownerVisualPass":False}
 (ROOT/"assets/s7-master-g00l-annex-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf8")
 print(json.dumps(manifest,ensure_ascii=False))
if __name__=="__main__":main()
