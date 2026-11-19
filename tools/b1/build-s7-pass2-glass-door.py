#!/usr/bin/env python3
"""S7 PASS 2: independently editable REAL GLB2 glass partition + hinged door.

Left G-00L glass room, x=-3.12, z=15.5..24.5. Hinge at z=19.0,
2.30m clear entrance from main walkway, opens INWARDS into G-00L.
Uses immutable original greenhouse-shell.glb. No game/physics writes.
"""
from pathlib import Path
import json,math,hashlib,struct

ROOT=Path(__file__).resolve().parents[2]
ID="s7-pass2-g00l-glass-partition-door"
DEST=ROOT/"assets/models"/(ID+".glb")
BUFFER=bytearray();VIEWS=[];ACCESSORS=[]
MATERIALS=[
 {"name":"etched-glass-sage","doubleSided":True,"alphaMode":"BLEND",
  "pbrMetallicRoughness":{"baseColorFactor":[.50,.81,.76,.25],"roughnessFactor":.09,"metallicFactor":.04}},
 {"name":"anodized-chrome-hinge-and-frame","doubleSided":True,
  "pbrMetallicRoughness":{"baseColorFactor":[.67,.77,.72,1],"roughnessFactor":.33,"metallicFactor":.68}},
 {"name":"matte-emerald-g00l-door-handle","doubleSided":True,
  "pbrMetallicRoughness":{"baseColorFactor":[.18,.47,.40,1],"roughnessFactor":.32,"metallicFactor":.32}}
]
def rec(x0,y0,z0,x1,y1,z1):
 x0,x1=sorted((x0,x1));y0,y1=sorted((y0,y1));z0,z1=sorted((z0,z1))
 A=lambda x,y,z:(x,y,z)
 return [
 (A(x0,y0,z0),A(x1,y0,z0),A(x1,y0,z1),A(x0,y0,z1)),
 (A(x0,y1,z0),A(x0,y1,z1),A(x1,y1,z1),A(x1,y1,z0)),
 (A(x0,y0,z0),A(x0,y1,z0),A(x1,y1,z0),A(x1,y0,z0)),
 (A(x0,y0,z1),A(x1,y0,z1),A(x1,y1,z1),A(x0,y1,z1)),
 (A(x0,y0,z0),A(x0,y0,z1),A(x0,y1,z1),A(x0,y1,z0)),
 (A(x1,y0,z0),A(x1,y1,z0),A(x1,y1,z1),A(x1,y0,z1))]
def write_accessor(values,typ,arity,target=None):
 while len(BUFFER)%4:BUFFER.append(0)
 off=len(BUFFER)
 code="f" if typ==5126 else "H"
 packed=struct.pack("<"+str(len(values))+code,*values)
 BUFFER.extend(packed)
 v={"buffer":0,"byteOffset":off,"byteLength":len(packed)}
 if target:v["target"]=target
 VIEWS.append(v)
 a={"bufferView":len(VIEWS)-1,"componentType":typ,
    "type":{1:"SCALAR",3:"VEC3",4:"VEC4"}[arity],"count":len(values)//arity}
 if typ==5126 and arity==3:
  a["min"]=[min(values[i::3]) for i in range(3)]
  a["max"]=[max(values[i::3]) for i in range(3)]
 ACCESSORS.append(a)
 return len(ACCESSORS)-1
def primitive(quads,material):
 positions=[];normals=[]
 for a,b,c,d in quads:
  for tri in ((a,b,c),(a,c,d)):
   u=[tri[1][i]-tri[0][i] for i in range(3)]
   v=[tri[2][i]-tri[0][i] for i in range(3)]
   n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
   mag=math.sqrt(sum(t*t for t in n)) or 1
   for pt in tri:positions.extend(pt);normals.extend(t/mag for t in n)
 return {"attributes":{"POSITION":write_accessor(positions,5126,3,34962),
                        "NORMAL":write_accessor(normals,5126,3,34962)},
         "material":material,"mode":4}
def main():
 glass=[];frames=[];door_glass=[];door_frame=[];hardware=[]
 X=-3.12
 # Partition on service-room boundary: short western segment and rear segment.
 # True 2.30m gap is between z19.0 and z21.30, from y0..2.60.
 for za,zb in ((15.5,18.98),(21.32,24.5)):
  glass.extend(rec(X-.025,.18,za,X+.025,4.63,zb))
  for z in (za,zb):frames.extend(rec(X-.07,0,z-.052,X+.07,4.82,z+.052))
  frames.extend(rec(X-.062,4.58,za,X+.062,4.75,zb))
 # Glass transom HIGH above doorway and a header over the walking gap.
 glass.extend(rec(X-.025,2.70,18.98,X+.025,4.60,21.32))
 frames.extend(rec(X-.072,2.58,18.97,X+.072,2.76,21.33))
 frames.extend(rec(X-.070,4.58,18.98,X+.070,4.75,21.32))
 # Hinged DOOR dimensions 2.22m wide, 2.48m tall; pivot is z19.03.
 # Door leaf coordinates are LOCAL to the hinge, not world.
 door_glass.extend(rec(-.018,.18,.10,.018,2.35,2.16))
 door_frame.extend(rec(-.055,0,.05,.055,2.51,.15))
 door_frame.extend(rec(-.055,0,2.13,.055,2.51,2.23))
 door_frame.extend(rec(-.055,2.39,.05,.055,2.51,2.23))
 door_frame.extend(rec(-.055,.01,.05,.055,.13,2.23))
 hardware.extend(rec(-.11,.96,1.95,.11,1.09,2.11))
 hardware.extend(rec(-.13,.98,1.88,.13,1.04,1.98))
 meshes=[
 {"name":"G00L.fixed-glass-partition-and-door-frame",
  "primitives":[primitive(glass,0),primitive(frames,1)]},
 {"name":"G00L.hinged-glass-door-2p3m",
  "primitives":[primitive(door_glass,0),primitive(door_frame,1),primitive(hardware,2)]}
 ]
 nodes=[
 {"name":"G00L.fixed-glass-room-wall","mesh":0},
 {"name":"G00L.door-hinge-Y","translation":[X,0,19.0],"children":[2],
  "extras":{"door":True,"ownerVisualPreview":True,"swingDegrees":-72,
            "entryWidthMeters":2.3,"engineCollisionBinding":"PENDING"}},
 {"name":"G00L.door-leaf-and-handle","mesh":1}]
 # One 10-second visual cycle, open, wait, close, dwell; can be paused in editor.
 times=[0,1.0,2.25,5.35,6.5,10]
 inp=write_accessor(times,5126,1,34962)
 angles=[0,0,-math.radians(72),-math.radians(72),0,0]
 quats=[]
 for a in angles:quats.extend([0,math.sin(a/2),0,math.cos(a/2)])
 out=write_accessor(quats,5126,4,34962)
 animations=[{"name":"door-open-hold-close-10s",
  "samplers":[{"input":inp,"output":out,"interpolation":"LINEAR"}],
  "channels":[{"sampler":0,"target":{"node":1,"path":"rotation"}}]}]
 BUFFER.extend(b"\x00"*(-len(BUFFER)%4))
 doc={"asset":{"version":"2.0","generator":"Trialum S7 PASS2 genuine hinged glass door",
      "extras":{"visualOnly":True,"gameplayWrites":0,"collisionRuntime":"NOT_CONNECTED",
                "doors":1,"doorGapMeters":2.30}},
      "scene":0,"scenes":[{"nodes":[0,1]}],"nodes":nodes,"meshes":meshes,
      "materials":MATERIALS,"animations":animations,
      "buffers":[{"byteLength":len(BUFFER)}],"bufferViews":VIEWS,"accessors":ACCESSORS}
 data=json.dumps(doc,separators=(",",":"),ensure_ascii=False).encode("utf8")
 data+=b" "*(-len(data)%4)
 raw=struct.pack("<III",0x46546c67,2,12+8+len(data)+8+len(BUFFER))
 raw+=struct.pack("<II",len(data),0x4e4f534a)+data
 raw+=struct.pack("<II",len(BUFFER),0x004e4942)+bytes(BUFFER)
 assert raw[:4]==b"glTF" and struct.unpack_from("<I",raw,8)[0]==len(raw)
 DEST.write_bytes(raw)
 catalogpath=ROOT/"assets/catalog.json"
 c=json.loads(catalogpath.read_text(encoding="utf8"))
 entry={"id":ID,"name":"G-00L · стаклена просторија со вистинска анимирана врата",
    "category":"Градина S7 · Завршни елементи",
    "src":"assets/models/"+ID+".glb","dimensions":[.14,4.82,9.0],
    "placement":"floor","visualOnly":True,"gameplayWrites":0,
    "ownerVisualPass":False,"doorAnimation":"door-open-hold-close-10s",
    "source":"tools/b1/build-s7-pass2-glass-door.py"}
 if ID not in {x["id"] for x in c["assets"]}:c["assets"].append(entry)
 c["genuineGlbCount"]=sum(str(x.get("src") or "").endswith(".glb") for x in c["assets"])
 assert c["genuineGlbCount"]==363,c["genuineGlbCount"]
 c["assetLibraryVersion"]="2026-11-19-S7-MASTER-PASS2-door-stone-hoses-363"
 catalogpath.write_text(json.dumps(c,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 manifest={"id":ID,"binary":str(DEST.relative_to(ROOT)),"sha256":hashlib.sha256(raw).hexdigest(),
    "bytes":len(raw),"staticMeshCount":2,"animations":1,"durationSeconds":10,
    "visualOnly":True,"collisionRuntime":"PENDING","source":str(Path(__file__).relative_to(ROOT))}
 (ROOT/"assets/s7-pass2-g00l-door-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf8")
 print(json.dumps(manifest,indent=2))
if __name__=="__main__":main()
