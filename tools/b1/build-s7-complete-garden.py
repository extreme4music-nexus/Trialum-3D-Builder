#!/usr/bin/env python3
"""S7.8-G real visual-only plants + four editable FULL greenhouse review layouts.
Pure-stdlib deterministic GLB2 authoring. NEVER touches the game or production data.
Canonical engine species: lumemoss/glowfern/mineralreed/aquaglow.
"""
from __future__ import annotations
import json, math, struct, hashlib, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[2]
MODEL_DIR=ROOT/"assets/models"
PROJECT_DIR=ROOT/"projects"
MODEL_DIR.mkdir(parents=True,exist_ok=True)
PROJECT_DIR.mkdir(parents=True,exist_ok=True)
TAU=2*math.pi

SPECIES={
 "lumemoss":("Лумемос","terrestrial"),
 "glowfern":("Светлопапрат","terrestrial"),
 "mineralreed":("Минерална трска","terrestrial"),
 "aquaglow":("Аквалум","aquatic")}
STAGES=("seedling","young","growing","mature","ready-for-transplant","weakened","dead")
STAGE_MK={"seedling":"расад","young":"младо","growing":"расте",
          "mature":"зрело","ready-for-transplant":"подготвено за пресадување",
          "weakened":"ослабено","dead":"увенато"}
SCALE={"seedling":.26,"young":.48,"growing":.75,"mature":1.0,
       "ready-for-transplant":1.08,"weakened":.75,"dead":.56}

def norm(a,b,c):
 u=[b[i]-a[i] for i in range(3)]
 v=[c[i]-a[i] for i in range(3)]
 n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
 d=math.sqrt(sum(x*x for x in n)) or 1
 return [round(x/d,7) for x in n]

class Plant:
 def __init__(self,sp,stage):
  self.sp=sp;self.stage=stage;self.mats=[];self.tris={}
  weak=stage in ("weakened","dead")
  palettes={
   "lumemoss":[(.16,.32,.23),(.11,.65,.46),(.48,.95,.72),(.82,.96,.35)],
   "glowfern":[(.13,.30,.22),(.12,.53,.35),(.45,.86,.64),(.64,.93,.92)],
   "mineralreed":[(.28,.34,.30),(.32,.63,.57),(.57,.85,.73),(.59,.78,.96)],
   "aquaglow":[(.18,.38,.30),(.09,.74,.68),(.41,.97,.82),(.84,.40,.96)]}
  root,green,vein,bloom=palettes[sp]
  self.root=self.addmat("rhizome-stem",root,.85)
  self.green=self.addmat("living-leaves",(.37,.40,.29) if weak else green,.54,(0,0,0) if weak else tuple(x*.11 for x in green))
  self.vein=self.addmat("luminous-veins",(.50,.52,.33) if weak else vein,.5)
  self.bloom=self.addmat("pollen-crystals",(.43,.38,.32) if weak else bloom,.34,(0,0,0) if weak else tuple(x*.24 for x in bloom))
  self.soil=self.addmat("root-base",(.19,.18,.14),.92)
 def addmat(self,name,color,rough,glow=None):
  a={"name":name,"doubleSided":True,
     "pbrMetallicRoughness":{"baseColorFactor":[*color,1],"metallicFactor":.06,"roughnessFactor":rough}}
  if glow:a["emissiveFactor"]=list(glow)
  self.mats.append(a);return len(self.mats)-1
 def tri(self,a,b,c,mat):
  self.tris.setdefault(mat,[]).append((tuple(a),tuple(b),tuple(c)))
 def quad(self,a,b,c,d,mat):
  self.tri(a,b,c,mat);self.tri(a,c,d,mat)
 def beam(self,a,b,r,mat,sides=7):
  axis=[b[i]-a[i] for i in range(3)]
  ln=math.sqrt(sum(x*x for x in axis)) or 1
  v=[x/ln for x in axis]
  aux=[1,0,0] if abs(v[1])>.85 else [0,1,0]
  n=[v[1]*aux[2]-v[2]*aux[1],v[2]*aux[0]-v[0]*aux[2],v[0]*aux[1]-v[1]*aux[0]]
  d=math.sqrt(sum(x*x for x in n)) or 1;n=[x/d for x in n]
  w=[v[1]*n[2]-v[2]*n[1],v[2]*n[0]-v[0]*n[2],v[0]*n[1]-v[1]*n[0]]
  rings=[]
  for c in (a,b):
   rings.append([tuple(c[j]+r*(n[j]*math.cos(TAU*i/sides)+w[j]*math.sin(TAU*i/sides)) for j in range(3)) for i in range(sides)])
  for i in range(sides):
   q=(i+1)%sides
   self.quad(rings[0][i],rings[0][q],rings[1][q],rings[1][i],mat)
  for i in range(1,sides-1):
   self.tri(rings[0][0],rings[0][i+1],rings[0][i],mat)
   self.tri(rings[1][0],rings[1][i],rings[1][i+1],mat)
 def ellipsoid(self,c,rx,ry,rz,mat,seg=9,lat=6):
  rings=[]
  for j in range(lat+1):
   phi=math.pi*j/lat
   rings.append([[c[0]+rx*math.sin(phi)*math.cos(TAU*i/seg),
                  c[1]+ry*math.cos(phi),
                  c[2]+rz*math.sin(phi)*math.sin(TAU*i/seg)] for i in range(seg)])
  for j in range(lat):
   for i in range(seg):
    k=(i+1)%seg
    self.quad(rings[j][i],rings[j][k],rings[j+1][k],rings[j+1][i],mat)
 def leaf(self,origin,angle,height,length,width,mat,dead=False):
  # Continuous bowed, tapering, two-sided 3D fan, not a flat square placeholder.
  u=(math.cos(angle),math.sin(angle))
  pts=[]
  for j in range(8):
   t=j/7;d=length*t
   zed=origin[1]+height*(math.sin(t*math.pi*.64)-(.68*t*t if dead else .04*t*t))
   thick=width*(math.sin(math.pi*t)**.72) if 0<t<1 else .005
   center=[origin[0]+u[0]*d,zed,origin[2]+u[1]*d]
   v=(-u[1],u[0])
   pts.append(([center[0]+v[0]*thick,zed+.012*t,center[2]+v[1]*thick],
               [center[0]-v[0]*thick,zed-.012*t,center[2]-v[1]*thick],center))
  for i in range(7):
   a,b,c=pts[i];d,e,f=pts[i+1]
   self.quad(a,d,e,b,mat)
   self.beam(c,f,.006,self.vein,5)
 def build(self):
  k=SCALE[self.stage];dead=self.stage=="dead";weak=self.stage=="weakened"
  self.ellipsoid((0,.08*k,0),.16*k,.09*k,.16*k,self.root)
  # Explicit origin is floor y=0, Y-up; root below ground is a decorative reference.
  if self.sp=="lumemoss":
   for i in range(8 if k>.6 else 5):
    a=TAU*i/(8 if k>.6 else 5);radius=.16*k+(i%3)*.06*k
    x=radius*math.cos(a);z=radius*math.sin(a)
    top=(.3+(i%4)*.07)*k*(.46 if dead else 1)
    self.beam((x,.03*k,z),(x*.86,top,z*.86),.032*k,self.root)
    self.ellipsoid((x*.86,top,z*.86),.10*k,.16*k,.09*k,self.green)
    if k>.45 and not dead and i%2==0:self.ellipsoid((x*.88,top+.08*k,z*.88),.033*k,.048*k,.033*k,self.bloom)
  elif self.sp=="glowfern":
   n=5 if k<.5 else 7
   for i in range(n):
    a=TAU*i/n
    h=(.45+.22*(i%3))*k;length=(.45+.09*(i%3))*k
    self.beam((0,.06*k,0),(.14*k*math.cos(a),h*.5,.14*k*math.sin(a)),.026*k,self.root)
    self.leaf((.06*k*math.cos(a),.14*k,.06*k*math.sin(a)),a,h,length,.14*k,self.green,dead)
    if k>.6 and not dead:
     for j in range(3):
      pos=.22+.19*j
      x=length*pos*math.cos(a);z=length*pos*math.sin(a)
      self.ellipsoid((x,.25*k+h*(1-pos*.5),z),.022*k,.022*k,.022*k,self.bloom,7,4)
  elif self.sp=="mineralreed":
   n=4 if k<.5 else 6
   for i in range(n):
    a=TAU*i/n;d=.13*k if k>.5 else .08*k
    p=(d*math.cos(a),.06*k,d*math.sin(a));top=(d*math.cos(a),(.75+.19*(i%3))*k,d*math.sin(a))
    if dead:top=(top[0]+.20*k,.23*k,top[2]+.22*k)
    self.beam(p,top,.035*k,self.root)
    self.leaf(p,a+.33,.24*k,.28*k,.07*k,self.green,dead)
    self.ellipsoid(top,.042*k,.16*k,.042*k,self.bloom if not weak else self.root,8,5)
    if not dead and k>.65:
     for j in range(3):
      x=top[0]+.06*k*math.cos(a+TAU*j/3)
      z=top[2]+.06*k*math.sin(a+TAU*j/3)
      self.beam((top[0],top[1]-.10*k,top[2]),(x,top[1]+.1*k,z),.014*k,self.vein)
  else:
   n=5 if k<.5 else 9
   for i in range(n):
    a=TAU*i/n
    p=(0,.08*k,0)
    q=(.15*k*math.cos(a),(.25+.07*(i%3))*k,.15*k*math.sin(a))
    self.beam(p,q,.026*k,self.root)
    self.leaf(q,a,.32*k,.47*k,.13*k,self.green,dead)
    if i%3==0 and not weak:
     center=(q[0]+.08*k*math.cos(a),q[1]+.14*k,q[2]+.08*k*math.sin(a))
     self.ellipsoid(center,.055*k,.085*k,.055*k,self.bloom)
  if dead:
   for i in range(3):
    a=TAU*i/3;self.beam((0,.04*k,0),(.3*k*math.cos(a),.01,.3*k*math.sin(a)),.016*k,self.root)
 def glb(self):
  self.build()
  binary=bytearray();views=[];accessors=[];meshes=[];nodes=[]
  def accessor(nums,code,arity,target=None):
   while len(binary)%4:binary.append(0)
   offset=len(binary);fmt="f" if code==5126 else "H"
   packed=struct.pack("<"+fmt*len(nums),*nums);binary.extend(packed)
   v={"buffer":0,"byteOffset":offset,"byteLength":len(packed)}
   if target:v["target"]=target
   views.append(v)
   val={"bufferView":len(views)-1,"componentType":code,"count":len(nums)//arity,
        "type":{1:"SCALAR",3:"VEC3",4:"VEC4"}[arity]}
   if arity==3 and code==5126:
    val["min"]=[min(nums[i::3]) for i in range(3)]
    val["max"]=[max(nums[i::3]) for i in range(3)]
   accessors.append(val);return len(accessors)-1
  nodes.append({"name":self.sp+".floor-root","children":[1],
       "extras":{"speciesId":self.sp,"stage":self.stage,"renderOnly":True,"gameplayWrites":0}})
  nodes.append({"name":self.sp+".sway-pivot","children":[],"translation":[0,0,0]})
  for mid,tris in sorted(self.tris.items()):
   pts=[];norms=[];indices=[]
   for tri in tris:
    n=norm(*tri)
    for p in tri:
     indices.append(len(indices));pts.extend(p);norms.extend(n)
   if len(indices)>65535:raise RuntimeError("mesh indices > uint16")
   p=accessor(pts,5126,3,34962)
   n=accessor(norms,5126,3,34962)
   idx=accessor(indices,5123,1,34963)
   meshes.append({"name":self.sp+"."+self.stage+"."+self.mats[mid]["name"],
        "primitives":[{"attributes":{"POSITION":p,"NORMAL":n},"indices":idx,"material":mid,"mode":4}]})
   node=len(nodes);nodes.append({"name":"mesh."+str(mid),"mesh":len(meshes)-1})
   nodes[1]["children"].append(node)
  animations=[]
  clips={"idle-sway":(.035,4),"machine-pass":(.12,1.5),"water-react":(.055,2.2),
         "root-settle":(.018,2.6),"growth-crossfade":(.045,3),
         "droop":(.095,2.6)}
  for name,(angle,duration) in clips.items():
   if self.stage=="dead":angle*=.3
   t=accessor([0,duration/2,duration],5126,1,34962)
   quat=[]
   for a in (0,angle,0):
    # Rotation around Z, with valid normalized quaternion.
    quat.extend([0,0,math.sin(a/2),math.cos(a/2)])
   o=accessor(quat,5126,4,34962)
   animations.append({"name":name,"samplers":[{"input":t,"output":o,"interpolation":"LINEAR"}],
            "channels":[{"sampler":0,"target":{"node":1,"path":"rotation"}}]})
  binary.extend(b"\0"*(-len(binary)%4))
  doc={"asset":{"version":"2.0","generator":"Trialum S7 original four flora species visual kit"},
       "scene":0,"scenes":[{"nodes":[0]}],"nodes":nodes,"meshes":meshes,
       "materials":self.mats,"animations":animations,"buffers":[{"byteLength":len(binary)}],
       "bufferViews":views,"accessors":accessors}
  j=json.dumps(doc,separators=(",",":"),ensure_ascii=False).encode("utf8")
  j+=b" "*(-len(j)%4)
  return (struct.pack("<III",0x46546c67,2,12+8+len(j)+8+len(binary))+
      struct.pack("<II",len(j),0x4e4f534a)+j+struct.pack("<II",len(binary),0x004e4942)+bytes(binary))

def obj(i,asset,x,y,z,layer="props",rot=0,note="",binding="",locked=False):
 return {"id":i,"assetId":asset,"label":asset,"position":[round(x,4),round(y,4),round(z,4)],
  "rotationY":round(rot,7),"scale":[1,1,1],"layer":layer,"locked":locked,"visible":True,
  "binding":binding,"note":note or "Builder visual scene only; no gameplay writes"}
def add(out,i,asset,x,y,z,layer="props",rot=0,note="",binding="",locked=False):
 out.append(obj(i,asset,x,y,z,layer,rot,note,binding,locked))

BEDS=[("G-02","bed-1",-24.86,-7.6,-73),("G-03","bed-2",-22.164,-28.368,-38),
      ("G-04","bed-3",-1.326,-37.977,-2),("G-05","bed-4",21.665,-28.751,37)]
PALETTE={
 1:("f01-a","f03-s-stone-full","m01-metal-full","f02-black-marble-full"),
 2:("f02-black-marble-full","f01-a","m03-metal-full","f03-s-stone-full"),
 3:("f03-s-stone-full","f03-t-stone-full","f01-a","m02-metal-full"),
 4:("f01-a","f02-black-marble-full","f03-s-stone-full","m01-metal-full")}
STYLE={1:"крем-бел мермер и светол раб",2:"темен мермер со крем контраст",
       3:"сиво-зелен природен камен",4:"мешан модуларен мозаик"}
def static_components():
 items=[]
 add(items,"shell-original","greenhouse-shell",0,0,0,"structure",locked=True,
     note="Original S7 glass shell. Existing physical glass/floor and pool cutout MUST be owner verified.")
 for asset in ("g01-main-basin","g01-satellite-basins","g01-walkway-and-railings",
               "g01-crossing-bridge","g01-visual-service-pumps","g01-water-surfaces-animated"):
  add(items,"g01-"+asset,asset,0,0,0,"structure",locked=True,
      note="Original G01 water module. Real engine has exactly FOUR aquatic slots; preview only.")
 for n,(x,z) in enumerate(((-2.7,-2),(2.7,-2),(-2.7,2),(2.7,2)),1):
  add(items,"aquatic-slot-"+str(n),"aquaglow-"+("mature","growing","young","ready-for-transplant")[n-1],
      x,0,z,"props",binding="preview:G01:aquatic-slot-"+str(n),
      note="Preview exemplar; NEVER create a real plantId or new aquarium capacity.")
 # G-00L is LEFT of entry from z positive, not a fifth growing finger.
 for n,(x,z) in enumerate(((-13,13),(-13,16)),1):
  add(items,"g00l-rs-"+str(n),"s7-e0e1-rs0"+str(n)+"-nursery-"+("3-tier" if n==1 else "4-tier"),
      x,0,z,note="G-00L seedling rack display; real seedlings inventory comes from engine.")
 for n,(x,z) in enumerate(((-15,6),(-11.5,6),(-15,9),(-11.5,9)),1):
  asset=("s7-e0e1-rm01-mature-single","s7-e0e1-rm02-mature-double",
         "s7-e0e1-rm03-mature-tall","s7-e0e1-rm04-reinforced-mature-carrier")[n-1]
  add(items,"g00l-rm-"+str(n),asset,x,0,z,note="Larger and MORE numerous RM racks: 4 versus 2 RS; no fictional stored plants.")
 for i,(asset,x,z) in enumerate((
   ("s7-e0e1-w01-workstation-desk",-8.7,12.0),
   ("s7-e0e1-w02-ergonomic-chair",-8.8,13.4),
   ("s7-e0e1-w03-hologram-monitor",-8.7,12.0),
   ("s7-e0e1-w04-workstation-tower",-8.0,12.0),
   ("s7-e0e1-w05-backlit-keyboard",-8.8,12.4),
   ("s7-e0e1-w06-ergonomic-mouse",-8.4,12.4),
   ("s7-e0e1-st01-spares-rack",-15,17.5),
   ("s7-e0e1-st02-secure-cabinet",-11.5,17.5),
   ("s7-e0e1-st03-mobile-tool-cart",-9.5,17.4),
   ("s7-e0e1-cn01-seedling-tray-demo",-12.8,14.3),
   ("s7-f-r01-charging-dock",-7.4,17.6),
   ("s7-f-r01-humanoid",-7.4,16.5),
   ("s7-f-r01-repair-tool",-9.5,16.5),
   ("s7-f-t01-planting-carrier",-7.5,7.0),
   ("s7-f-t02-flat-transport",-10.5,4.5),
   ("s7-f-t03-heavy-transport",-7.5,4.5),
   ("s7-f-e01-excavator",-10.5,1.0),
   ("s7-f-e02-tiller",-8.0,1.0)
 ),1):
  add(items,"g00l-equipment-"+str(i),asset,x,0,z,
      note="G-00L physical service/robotics. Animations are visual only, no jobs or gameplay writes.")
 for n,(zone,bed,cx,cz,angle) in enumerate(BEDS,1):
  add(items,bed+"-real-bed","s02-25-planting-grid",cx,0,cz,"floor",
      rot=math.radians(angle),binding="preview:"+bed,
      note="ONE 5x5 HOLE GRID VISUAL per REAL 5-slot bed, NOT 25 gameplay plants.")
  add(items,bed+"-irrigation-controller","s7-c-irr01-bed-control-compact",cx-2.2,0,cz+1.8,
      binding="preview:"+bed,note="Per-bed panel, read-only until engine contract.")
  for j,(asset,dx,dz) in enumerate((
   ("s7-i01-source-tank-compact",-3.7,1.2),
   ("s7-i02-pump-compact",-2.7,1.2),
   ("s7-i03-flex-main-straight-1m",-1.1,1.1),
   ("s7-i04-tee-splitter",-.5,1.1),
   ("s7-i05-drip-emitter",.1,.7),
   ("s7-i06-flow-sensor",.8,.7)),1):
   # Add only known IDs (generator will validate), selecting canonical IDs below if variants differ.
   add(items,bed+"-irrig-"+str(j),asset,cx+dx,0,cz+dz,
       note="I01–I06 representative hardware, preview only; no water transfer.")
  for i,(dx,dz) in enumerate(((-.28,-.28),(.28,-.28),(0,0),(-.28,.28),(.28,.28)),1):
   sp=("lumemoss","glowfern","mineralreed")[(i+n)%3]
   stage=("seedling","young","growing","mature","ready-for-transplant")[i-1]
   add(items,bed+"-plant-preview-"+str(i),sp+"-"+stage,cx+dx,.12,cz+dz,
       binding="preview:"+bed+":slot-"+str(i),
       note="5 preview exemplars = exactly 5 canonical slots. No real plantId, no growth/treatment actions.")
  add(items,bed+"-ceiling-ring","s7-lc3-corridor-ceiling-ring-medium",cx,5.3,cz,
      "decor",note="Real ceiling fixture mesh; lighting engine not enabled.")
  add(items,bed+"-led-floor","s7-lf1-perimeter-straight-1m",cx+2,0,cz-1.4,"decor")
 add(items,"g01-five-rings","s7-lc1-g01-1plus4-ring-chandelier",0,7.8,0,"decor",
     note="Chandelier physical mesh; no automatic day-night lighting.")
 for i,(x,z) in enumerate(((-8,-8),(8,-8),(-8,8),(8,8)),1):
  add(items,"g01-perimeter-led-"+str(i),"s7-lf1-perimeter-g01-curve",x,0,z,"decor")
 return items

def add_floor(items,v):
 # ONLY floor palette differs between variants. No changes to machinery, G01, racks or plant placements.
 a,b,c,d=PALETTE[v]
 n=0
 def tile(x,z,kind="main",orientation=0):
  nonlocal n
  palette={"main":a,"contrast":b,"service":c,"accent":d}
  asset=palette[kind];n+=1
  add(items,"floor-"+str(n),asset,x,0,z,"floor",orientation,
       "S7 visual-only modular tile; floor tile may be moved/replaced by owner")
 # G01 dry annulus: reserve actual main basin and three satellite pools.
 for x in range(-15,16):
  for z in range(-15,16):
   r=math.hypot(x,z)
   if r<9 or r>14.8:continue
   if any(math.hypot(x-cx,z-cz)<2.8 for cx,cz in ((-10,0),(10,1),(0,-11))):continue
   kind=("contrast" if ((x+z)%8 in (0,1)) else "accent" if (x*z)%17==0 else "main")
   if v==4:kind=("main","contrast","accent","service")[(x+2*z)%4]
   tile(x,z,kind)
 # Exit-to-lobby corridor, preserve 3 m navigable passage in middle.
 for x in range(-3,4):
  for z in range(14,25):
   kind="service" if abs(x)==3 else "contrast" if z%6==0 else "main"
   if v==4:kind=("main","contrast","accent","service")[(abs(x)+z)%4]
   tile(x,z,kind)
 # Four distinct long fingers, with centered path, a visible open slot for the actual beds.
 for n,(_,bed,cx,cz,ang) in enumerate(BEDS,1):
  # Extend approach from center to a safe distance before each bed, 1m floor tiles.
  length=max(6,int(math.hypot(cx,cz)-17))
  vx,vz=cx/math.hypot(cx,cz),cz/math.hypot(cx,cz)
  px,pz=-vz,vx
  for step in range(length):
   r=17+step
   for lane in (-1,0,1):
    x=round(vx*r+px*lane,3);z=round(vz*r+pz*lane,3)
    kind="accent" if lane else "contrast" if step%6==0 else "main"
    if v==4:kind=("main","contrast","accent","service")[(step+lane+4)%4]
    tile(x,z,kind,math.atan2(-vz,vx))
 # G-00L service floor on the true LEFT of entrance (not the small G02 finger).
 for x in range(-16,-6):
  for z in range(4,20):
   if math.hypot(x,z)>20:continue
   kind="service" if x%5==0 or z%6==0 else "main"
   if v==4:kind=("main","contrast","accent","service")[(x+z)%4]
   tile(x,z,kind)
 return n

def garden(v,catalog):
 items=static_components()
 # Validate all optional irrigation assets by canonical subfamily prefix, fallback to first genuine available.
 known={a["id"] for a in catalog["assets"]}
 for it in items:
  if it["assetId"] in known:continue
  if "-irrig-" in it["id"]:
   sub=it["assetId"].split("-")[1] if False else it["assetId"].split("-")[1]
   prefix="-".join(it["assetId"].split("-")[:2])+"-"
   matches=sorted(x for x in known if x.startswith(prefix) and x.endswith(("compact","1m","standard","straight","body","sensor","emitter","kit","tee")))
   if not matches:matches=sorted(x for x in known if x.startswith(prefix))
   if not matches:raise RuntimeError("No authentic hardware in "+prefix)
   it["assetId"]=matches[0];it["label"]=matches[0]
  else:raise RuntimeError("Missing authentic GLB asset "+it["assetId"])
 tiles=[]
 count=add_floor(tiles,v)
 # For every variant exact same non-floor sequence; ONLY chosen floor palette and tile IDs vary.
 items=tiles+items
 ids={x["id"] for x in items}
 assert len(ids)==len(items)
 assert len([x for x in items if x["id"].endswith("real-bed")])==4
 assert len([x for x in items if "-plant-preview-" in x["id"]])==20
 assert len([x for x in items if x["id"].startswith("aquatic-slot-")])==4
 assert len([x for x in items if x["id"].startswith("g00l-rm-")])==4
 assert len([x for x in items if x["id"].startswith("g00l-rs-")])==2
 assert all(x["assetId"] in known for x in items)
 return {
  "schemaVersion":1,"projectId":"trialum-s7-complete-garden-v"+str(v)+"-20261119",
  "name":"S7 · Целосна градина V"+str(v)+" · "+STYLE[v],
  "description":"Four editable owner-review designs. Every structural/functional asset identical; only floor tile material pattern differs. No game implementation or inventories.",
  "room":{"width":82,"depth":104,"height":12.5,"gridSize":.5,
          "showWalls":False,"floorColor":"#273d3b","wallColor":"#56736c"},
  "instances":items,"assets":[],"bindings":{},
  "meta":{"editorVersion":"0.1.0","gameplayWrites":0,"officialScene":False,
          "ownerVisualPass":False,"reviewOnly":True,"physicalCutoutQARequired":True,
          "zones":{"G-00L":"service left of entrance","G-01":"water 4 slots",
             "G-02":"bed-1","G-03":"bed-2","G-04":"bed-3","G-05":"bed-4"},
          "capacity":{"beds":4,"slotsPerBed":5,"aquaticSlots":4},
          "floorTileCount":count,"floorPalette":STYLE[v]}}
def main():
 catalogPath=ROOT/"assets/catalog.json"
 catalog=json.loads(catalogPath.read_text(encoding="utf8"))
 byid={a["id"]:a for a in catalog["assets"]}
 generated=[]
 for sp,(name,medium) in SPECIES.items():
  for stage in STAGES:
   if sp=="aquaglow" and stage!="ready-for-transplant":continue # preserve existing 6 aquatic GLBs
   asset_id=sp+"-"+stage
   path=MODEL_DIR/(asset_id+".glb")
   binary=Plant(sp,stage).glb()
   assert binary[:4]==b"glTF" and struct.unpack_from("<I",binary,8)[0]==len(binary)
   assert len(binary)<400000,asset_id
   path.write_bytes(binary)
   row={"id":asset_id,"name":name+" · "+STAGE_MK[stage],
        "category":"Растенија S7 · "+name,
        "src":"assets/models/"+asset_id+".glb",
        "dimensions":[1.15,1.5,1.15] if sp=="mineralreed" else [.85,1.1,.85],
        "placement":"floor","speciesId":sp,"medium":medium,"visualStage":stage,
        "animationClips":["idle-sway","machine-pass","water-react","root-settle","growth-crossfade","droop"],
        "ownerVisualPass":False,"runtimeIntegration":False,"gameplayWrites":0,
        "source":"tools/b1/build-s7-complete-garden.py"}
   if asset_id in byid:
    assert byid[asset_id]["src"]==row["src"]
   else:catalog["assets"].append(row);byid[asset_id]=row
   generated.append({"id":asset_id,"bytes":len(binary),"sha256":hashlib.sha256(binary).hexdigest()})
 assert len(generated)==22,len(generated)
 catalog["genuineGlbCount"]=sum(a.get("src","").endswith(".glb") for a in catalog["assets"])
 assert catalog["genuineGlbCount"]==360,catalog["genuineGlbCount"]
 catalog["assetLibraryVersion"]="2026-11-19-s7-complete-flora-and-four-gardens-360"
 catalog["name"]="Trialum 3D World Builder — 360 genuine GLBs, 4 canonical plants, 4 S7 full gardens"
 catalogPath.write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 scenes=[]
 stable_non_floor=None
 for v in (1,2,3,4):
  p=garden(v,catalog)
  canonical=[x for x in p["instances"] if not x["id"].startswith("floor-")]
  if stable_non_floor is None:stable_non_floor=canonical
  else:assert canonical==stable_non_floor,"Variants must differ ONLY in floor tiles"
  path=PROJECT_DIR/("trialum-s7-complete-garden-v"+str(v)+".json")
  path.write_text(json.dumps(p,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
  scenes.append({"path":str(path.relative_to(ROOT)),"instances":len(p["instances"]),
                 "floorTiles":p["meta"]["floorTileCount"]})
 out={"generator":"S7.8-G","models":generated,"scenes":scenes,
      "canonicalPlantSpecies":list(SPECIES),"newGlbCount":22,"totalGlbCount":360,
      "gameplayWrites":0,"ownerVisualPass":False}
 (ROOT/"assets/s7-flora-22-manifest.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
 print(json.dumps({"newGLB":22,"totalGLB":360,"scenes":scenes},ensure_ascii=False))
if __name__=="__main__":main()
