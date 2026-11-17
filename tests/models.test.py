#!/usr/bin/env python3
"""Validate shipped model catalogue: GLB integrity and F01-A exact original."""
from pathlib import Path
import hashlib,json,struct,unittest
ROOT=Path(__file__).resolve().parents[1]
MODEL_DIR=ROOT/"assets/models"
CAT=ROOT/"assets/catalog.json"
ORIGINAL_F01_A="787965608e2e4005a0ee84c857d7f0379a8093149b39da6bacb2d012feafc147"
class GLBModels(unittest.TestCase):
 def test_every_real_catalog_file_exists_and_loads_as_valid_glb2(self):
  assets=json.loads(CAT.read_text(encoding="utf-8"))["assets"]
  models=[x for x in assets if isinstance(x.get("src"),str) and x["src"].endswith(".glb")]
  self.assertEqual(len(models),15)
  for asset in models:
   p=ROOT/asset["src"]
   self.assertTrue(p.is_file(),str(p))
   d=p.read_bytes()
   self.assertEqual(d[:4],b"glTF")
   self.assertEqual(struct.unpack_from("<II",d,4),(2,len(d)))
   jl,kind=struct.unpack_from("<I4s",d,12)
   self.assertEqual(kind,b"JSON")
   gltf=json.loads(d[20:20+jl])
   self.assertTrue(gltf["meshes"],str(p))
   self.assertEqual(gltf["asset"]["version"],"2.0")
   self.assertTrue(gltf["images"],str(p))
   self.assertLess(len(d),160_000)
 def test_frozen_owner_approved_F01_A_SHA(self):
  p=MODEL_DIR/"f01-marble-cream-full.glb"
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),ORIGINAL_F01_A)
 def test_no_game_scenes_or_play_store_assets_inside_builder(self):
  self.assertFalse((ROOT/"android").exists())
  self.assertFalse((ROOT/"prototypes/lw-d/scenes").exists())
  self.assertFalse((ROOT/"js/engine.js").exists())
if __name__=="__main__":unittest.main(verbosity=2)
