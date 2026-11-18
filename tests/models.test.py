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
  self.assertEqual(len(models),130)
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
    self.assertLess(len(d),500_000)
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
  self.assertTrue(extras["ownerApprovedConceptRender"])
  self.assertFalse(extras["ownerCorrectedModelApproval"])
  self.assertEqual(extras["moduleRadialBoundsM"],[7.2,8.2])
  self.assertEqual(extras["subdivisions"],24)
  self.assertTrue(extras["poolsideNotOutboard"])
  self.assertTrue(extras["previousOversizedStandaloneRejected"])
  self.assertAlmostEqual(extras["tileThicknessM"],.06)
  self.assertAlmostEqual(extras["bevelM"],.004)
  pbr=j["materials"][0]["pbrMetallicRoughness"]
  self.assertEqual(pbr["metallicFactor"],0)
  self.assertAlmostEqual(pbr["roughnessFactor"],.275)
  self.assertFalse(extras["inGame"])
  self.assertTrue(extras["noGameStateWrites"])
  self.assertGreater(j["accessors"][0]["count"],300)
 def test_f01_g_actual_cream_bevelled_curved_trim_variants(self):
  files=("f01-g-cream-marble-pool-trim-1m.glb","f01-g-cream-marble-pool-trim-half.glb",
         "f01-g-cream-marble-pool-trim-3m-showcase.glb")
  for file in files:
   raw=(MODEL_DIR/file).read_bytes()
   assert raw[:4]==b"glTF"
   jl=struct.unpack_from("<I",raw,12)[0]
   j=json.loads(raw[20:20+jl])
   meta=j["nodes"][0]["extras"]
   self.assertEqual(meta["module"],"F01-G")
   self.assertAlmostEqual(meta["heightM"],.135)
   self.assertAlmostEqual(meta["topBevelM"],.008)
   self.assertEqual(meta["realG01RadiusInnerM"],8.2)
   self.assertEqual(meta["realG01RadiusOuterM"],8.39)
   self.assertFalse(meta["inGame"])
   self.assertEqual(meta["gameplayWrites"],0)
   self.assertEqual(meta["textureSha256"],"81c434a57b770148ced6e9c40dccabade929a844a27b143f2dc13a4da0ff8c98")
   self.assertTrue(j["images"])
   self.assertGreater(j["accessors"][0]["count"],100)
  one=json.loads((MODEL_DIR/files[0]).read_bytes()[20:20+struct.unpack_from("<I",(MODEL_DIR/files[0]).read_bytes(),12)[0]])
  self.assertAlmostEqual(one["nodes"][0]["extras"]["arcRadians"],3.141592653589793/24)
 def test_real_F01_H_and_I_matte_and_wet_visual_microtextures(self):
  names={"H":"f01-h-cream-marble-matte-service.glb","I":"f01-i-cream-marble-fine-textured-wet.glb"}
  for mode,file in names.items():
   raw=(MODEL_DIR/file).read_bytes()
   n=struct.unpack_from("<I",raw,12)[0]
   model=json.loads(raw[20:20+n])
   meta=model["nodes"][0]["extras"]
   self.assertEqual(meta["module"],"F01-"+mode)
   self.assertEqual(meta["dimensionsM"],[1,.06,1])
   self.assertAlmostEqual(meta["bevelM"],.004)
   self.assertEqual(meta["realTopSurfaceDisplacement"],mode=="I")
   self.assertEqual(meta["normalMapEmbedded"],True)
   self.assertTrue(meta["ownerModelVisualReviewPending"])
   self.assertFalse(meta["actualTestedSlipResistance"])
   self.assertFalse(meta["inGame"])
   self.assertEqual(len(model["images"]),2)
   mat=model["materials"][0]
   self.assertEqual(mat["pbrMetallicRoughness"]["metallicFactor"],0)
   self.assertEqual(mat["pbrMetallicRoughness"]["roughnessFactor"],.70 if mode=="H" else .86)
   self.assertEqual(meta["frozenOriginalF01ATextureSha256"],"81c434a57b770148ced6e9c40dccabade929a844a27b143f2dc13a4da0ff8c98")

 def test_approved_render_F02_29_real_veined_black_marble(self):
  manifest=json.loads((ROOT/"assets/materials/f02-glb-sha-manifest.json").read_text(encoding="utf8"))
  self.assertEqual(len(manifest["models"]),29)
  self.assertEqual(manifest["atlasSha256"],"397184703cbb45563a953dbf178243060e499ae8815e95c3170753db1fe0599e")
  expected=("full","half-first","half-second","quarter-c1","quarter-c4","edge-north","edge-west",
            "corner-north-east","l-corner-showcase-north-east","raised-border-showcase-north",
            "radial-wedge","pool-trim-1m","pool-trim-half","pool-trim-3m-showcase",
            "matte-service","fine-textured-wet")
  for name in expected:self.assertTrue((MODEL_DIR/("f02-black-marble-"+name+".glb")).is_file(),name)
  for item in manifest["models"]:
   raw=(MODEL_DIR/item["file"]).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),item["sha256"])
   length=struct.unpack_from("<I",raw,12)[0]
   g=json.loads(raw[20:20+length])
   self.assertEqual(g["asset"]["version"],"2.0")
   self.assertTrue(g["meshes"][0]["primitives"][0]["attributes"]["NORMAL"]>=0)
   self.assertTrue(g.get("images"))
   self.assertTrue(g["nodes"][0]["extras"]["ownerRenderApproval"])
   self.assertFalse(g["nodes"][0]["extras"]["ownerGlbModelPass"])
   self.assertFalse(g["nodes"][0]["extras"]["inGame"])
   self.assertEqual(g["nodes"][0]["extras"]["gameplayWrites"],0)
   self.assertEqual(g["materials"][0]["pbrMetallicRoughness"]["metallicFactor"],0)
  self.assertGreater(next(x for x in manifest["models"] if x["module"]=="F02-I")["triangles"],1000)
 def test_F03_54_actual_gltf_stone_models_from_approved_render_references(self):
  m=json.loads((ROOT/"assets/materials/f03-glb-sha-manifest.json").read_text(encoding="utf-8"))
  self.assertEqual(len(m["models"]),54)
  self.assertTrue(m["ownerRenderPass"])
  self.assertFalse(m["ownerGlbPass"])
  self.assertEqual(m["gameplayWrites"],0)
  self.assertEqual(sum(x["finish"]=="s" for x in m["models"]),27)
  self.assertEqual(sum(x["finish"]=="t" for x in m["models"]),27)
  for finish in ("s","t"):
   ref=(ROOT/f"assets/materials/f03-{finish}-reference-derived-atlas.png").read_bytes()
   self.assertEqual(hashlib.sha256(ref).hexdigest(),m["embeddedAtlasSha256"][finish])
  for row in m["models"]:
   raw=(MODEL_DIR/row["file"]).read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),row["sha256"])
   self.assertEqual(len(raw),row["size"])
   length=struct.unpack_from("<I",raw,12)[0]
   gltf=json.loads(raw[20:20+length])
   self.assertEqual(gltf["asset"]["version"],"2.0")
   self.assertEqual(len(gltf["images"]),2)
   self.assertEqual(gltf["nodes"][0]["extras"]["family"],"F03")
   self.assertTrue(gltf["nodes"][0]["extras"]["ownerRenderPass"])
   self.assertFalse(gltf["nodes"][0]["extras"]["ownerGlbVisualPass"])
   self.assertFalse(gltf["nodes"][0]["extras"]["inGame"])
   self.assertEqual(gltf["materials"][0]["pbrMetallicRoughness"]["roughnessFactor"],.61 if row["finish"]=="s" else .79)
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
