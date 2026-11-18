from pathlib import Path
import hashlib,struct,json
import trimesh
ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/'assets/materials/s03-untreated-15-glb-manifest.json').read_text())
assert M['modelCount']==15 and len(M['models'])==15
for a in M['models']:
 p=ROOT/'assets/models'/a['file'];raw=p.read_bytes()
 assert raw[:4]==b'glTF' and struct.unpack_from('<II',raw,4)==(2,len(raw))
 assert hashlib.sha256(raw).hexdigest()==a['sha256']
 n=struct.unpack_from('<I',raw,12)[0]
 data=json.loads(raw[20:20+n])['asset']['extras']['trialum']
 assert data['canonicalSoilState']=='S03' and data['plantingHoles']==0 and data['gameplayWrites']==0
 scene=trimesh.load(p,force='scene');assert scene.geometry
 assert all(m.is_watertight for m in scene.geometry.values())
 span=scene.bounds[1]-scene.bounds[0]
 assert abs(span[0]-a['widthMeters'])<.001 and abs(span[2]-a['depthMeters'])<.001
print('PASS all 15 standalone S03 untreated GLBs')
