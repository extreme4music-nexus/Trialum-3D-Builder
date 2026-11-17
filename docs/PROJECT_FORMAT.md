# Trialum Builder — JSON scene format v1

All positions are in metres, with Y UP. The builder does NOT recenter GLB
geometry: original pivot and each F01-A/B/C/D origin are respected.

## Example scene

{
  "schemaVersion": 1,
  "projectId": "my-greenhouse-room-01",
  "name": "Моја лабораторија",
  "description": "Owner authored design only, no gameplay state",
  "room": {
    "width": 12, "depth": 12, "height": 4,
    "gridSize": 0.5,
    "showWalls": false,
    "floorColor": "#526b60",
    "wallColor": "#34494c"
  },
  "instances": [
    {
      "id": "floor01",
      "assetId": "f01-a",
      "label": "Мермер пред врата",
      "position": [0, 0, 0],
      "rotationY": 0,
      "scale": [1, 1, 1],
      "layer": "floor",
      "locked": false,
      "visible": true,
      "binding": "",
      "note": ""
    }
  ],
  "assets": [],
  "bindings": {},
  "meta": {
    "editorVersion": "0.1.0",
    "gameplayWrites": 0,
    "officialScene": false
  }
}

The builder writes scene project files into projects/ and references GLBs by
assetId as defined in assets/catalog.json. A local imported .glb must be
saved to the chosen repo root using the Save UI, so assets/models/ and the
catalogue change can be committed in GitHub Desktop.

### Material and grid rules

- F01-A: 1x1x.06m genuine full tile, bottom-left pivot.
- F01-B1: 1x.5m phase 0; B2: matching .5..1 phase. B2 goes z+0.5.
- F01-C1..C4: true half-meter quarters with global U/V phases.
- F01-D: 1m exposed 6cm nose, only OUTSIDE the floor tile boundary, not
  on top of the base tile; corner joins are reserved for F01-E.
- Snap sizes .05/.1/.25/.5/1 metre, angular rotation in inspector measured
  in degrees and saved as radians in rotationY.
- Wall snapping uses the room's selected wall intersection. Imported models
  may use different origins/forward axes; visually verify orientation.
- Built-in overlap indicator is an axis-aligned floor warning, not physics.

### Game integration handoff

The binding field is merely a **text hint** for a future game engineer, for
example lab.seedling.rack-01; it is NOT executable JS, an engine write or
user permission. To integrate a saved scene in the genuine Trialum engine,
check IDs and bindings against a whitelist in the game-side code and use
only authorized authoritative stocks / item state.

### Backward compatibility

schemaVersion=1 required, maximum 6000 instances and 500 imported asset
definitions. Imported strings/coords/scales are sanitized. Future schema
upgrades must include explicit migration tests and keep owner-created JSON
files working. No silent overwrite or automatic game world merge.
