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
  self.assertEqual(len(models),42)
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
   if asset["id"].startswith("f01-"):
    self.assertTrue(gltf.get("images"),str(p))
    self.assertLess(len(d),160_000)
   else:
    self.assertLess(len(d),5_000_000)
   self.assertTrue(gltf.get("materials"),str(p))
 def test_known_rooms_and_annexes_are_real_glbs(self):
  expected=("atrium.glb","warehouse-shell.glb","food-cold-annex-shell.glb",
            "food-packing-annex-shell.glb","greenhouse-shell.glb",
            "g01-main-basin.glb","g01-water-surfaces-animated.glb",
            "aquaglow-mature.glb","pilot-room.glb")
  for f in expected:self.assertTrue((MODEL_DIR/f).is_file(),f)
 def test_original_legacy_glb_hash_manifest_and_real_water_animation(self):
  manifest=json.loads((ROOT/"assets/TRIALUM_LEGACY_GLB_MANIFEST.json").read_text(encoding="utf-8"))
  self.assertEqual(manifest["newModels"],26)
  self.assertEqual(len(manifest["assets"]),26)
  for row in manifest["assets"]:
   p=ROOT/row["src"]
   self.assertEqual(len(p.read_bytes()),row["size"])
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row["sha256"])
  water=(MODEL_DIR/"g01-water-surfaces-animated.glb").read_bytes()
  size=struct.unpack_from("<I",water,12)[0]
  info=json.loads(water[20:20+size])
  self.assertEqual(info["animations"][0]["name"],"G01_WATER_RIPPLES_LOOP_6S")
 def test_owner_render_approved_real_F01_F_glb(self):
  p=MODEL_DIR/"f01-marble-cream-radial-wedge.glb"
  d=p.read_bytes()
  jl=struct.unpack_from("<I",d,12)[0]
  j=json.loads(d[20:20+jl])
  extras=j["nodes"][0]["extras"]
  self.assertEqual(extras["module"],"F01-F")
  self.assertTrue(extras["ownerRenderApproval"])
  self.assertFalse(extras["ownerModelApproval"])
  self.assertEqual(extras["radialBoundsM"],[9.15,10.15])
  self.assertEqual(extras["subdivisions"],32)
  self.assertAlmostEqual(extras["tileThicknessM"],.06)
  self.assertAlmostEqual(extras["bevelM"],.004)
  pbr=j["materials"][0]["pbrMetallicRoughness"]
  self.assertEqual(pbr["metallicFactor"],0)
  self.assertAlmostEqual(pbr["roughnessFactor"],.275)
  self.assertFalse(extras["inGame"])
  self.assertTrue(extras["noGameStateWrites"])
  self.assertGreater(j["accessors"][0]["count"],300)
 def test_frozen_owner_approved_F01_A_SHA(self):
  p=MODEL_DIR/"f01-marble-cream-full.glb"
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),ORIGINAL_F01_A)
 def test_no_game_runtime_or_play_store_assets_inside_builder(self):
  self.assertFalse((ROOT/"android").exists())
  # Design-only declarative snapshots are allowed; playable engine/runtime is NOT.
  self.assertFalse((ROOT/"prototypes/lw-d/scenes/agro-food-warehouse/warehouse-runtime.mjs").exists())
  self.assertFalse((ROOT/"prototypes/lw-d/scenes/agro-greenhouse/greenhouse-app.mjs").exists())
  self.assertFalse((ROOT/"js/engine.js").exists())
if __name__=="__main__":unittest.main(verbosity=2)
