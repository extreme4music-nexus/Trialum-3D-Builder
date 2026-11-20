#!/usr/bin/env python3
"""Package the exact offline S7 MASTER PASS2 Builder as a separate Android QA app.
Original web Builder source and the Trialum game are NEVER edited by this step.
"""
from pathlib import Path
import json
import shutil

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"android-preview/app/src/main/assets/web"
expected=ROOT/"projects/trialum-s7-master-garden-pass2.json"
scene=json.loads(expected.read_text(encoding="utf-8"))
catalog=json.loads((ROOT/"assets/catalog.json").read_text(encoding="utf-8"))
assert scene["meta"]["gameplayWrites"]==0
assert scene["meta"]["officialScene"] is False
assert scene["meta"]["engineIntegration"]=="NOT_STARTED"
assert len(scene["instances"])==703, len(scene["instances"])
assert catalog["genuineGlbCount"]==363, catalog["genuineGlbCount"]
assert sum(x["assetId"].startswith("s7-i05-") for x in scene["instances"])==0
assert sum(x["assetId"]=="s7-pass2-g00l-glass-partition-door" for x in scene["instances"])==1
assert (ROOT/"assets/models/s7-pass2-g00l-glass-partition-door.glb").read_bytes()[:4]==b"glTF"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for name in ("assets","projects","src","vendor"):
    shutil.copytree(ROOT/name,OUT/name)
shutil.copy2(ROOT/"index.html",OUT/"index.html")
(OUT/"preview").mkdir()
shutil.copy2(ROOT/"android-preview/tour.js",OUT/"preview/tour.js")
shutil.copy2(ROOT/"android-preview/tour.css",OUT/"preview/tour.css")

index=OUT/"index.html"
html=index.read_text(encoding="utf-8")
assert '<script type="module" src="./src/main.js"></script>' in html
assert "</head>" in html
html=html.replace("</head>",'<link rel="stylesheet" href="./preview/tour.css">\n</head>')
html=html.replace(
 '<script type="module" src="./src/main.js"></script>',
 '<script type="module" src="./src/main.js"></script>\n'
 '<script defer src="./preview/tour.js"></script>')
html=html.replace('<title>Trialum 3D World Builder</title>',
                  '<title>Trialum 3D · S7 MASTER PASS 2</title>')
index.write_text(html,encoding="utf-8")

script=OUT/"src/main.js"
main=script.read_text(encoding="utf-8")
needle="renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));"
assert needle in main
main=main.replace(needle,"renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.25));",1)
assert "function applyGardenCameraBookmark(view){" in main
main+='\n// Native tour controls are camera-only; never mutate gameplay.\n'
main+='window.trialumPreviewCamera=function(view){applyGardenCameraBookmark(view);return true;};\n'
script.write_text(main,encoding="utf-8")

# Native Android SAF JSON export (user's layout) instead of Blob download which
# is not reliably supported in a WebView.
project=OUT/"src/project.js"
js=project.read_text(encoding="utf-8")
start=js.index("export function downloadJson(value,filename){")
end=js.index("export function downloadBlob(",start)
js=js[:start]+'''export function downloadJson(value,filename){
 const content=JSON.stringify(value,null,2)+"\\\\n";
 if(typeof window!=="undefined"&&window.TrialumPreviewAndroid?.saveJson){
  window.TrialumPreviewAndroid.saveJson(filename,content);
  return;
 }
 downloadBlob(new Blob([content],{type:"application/json;charset=utf-8"}),filename);
}
'''+js[end:]
# Preserve a literal JS newline escape, not an accidental line break.
js=js.replace('JSON.stringify(value,null,2)+"\\\\\\\\n"', 'JSON.stringify(value,null,2)+"\\\\n"')
project.write_text(js,encoding="utf-8")

# Remove only the remote font import in this OFFLINE APK: use system fallback.
css=OUT/"src/style.css"
style=css.read_text(encoding="utf-8")
style=style.replace("@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');","")
css.write_text(style,encoding="utf-8")

assert (OUT/"vendor/three.module.js").is_file()
assert (OUT/"vendor/addons/loaders/GLTFLoader.js").is_file()
assert (OUT/"projects/trialum-s7-master-garden-pass2.json").is_file()
models=list((OUT/"assets/models").glob("*.glb"))
assert len(models)==363,len(models)
assert "<script" in html and "tour.js" in html
print("PASS: fully offline S7 Android preview, 363 real GLBs, 703 objects")
print("WebView bundled bytes:",sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()))
print("Source Trialum game repo: UNTOUCHED; engine: NOT_CONNECTED")
