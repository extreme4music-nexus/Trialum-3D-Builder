/* Builder -> Living Spaces room layout bridge. Data only, NO direct gameplay writes. */
import {sanitizeProject} from "./project.js";
export function exportLivingSpace(raw,ownerId="owner-local",roomId="home-main"){
 const p=sanitizeProject(raw),width=p.room.width,depth=p.room.depth;
 if(!ownerId||!roomId)throw Error("Owner and room required");
 const ids=new Set();const items=[];
 const catalogue=new Map((p.assets||[]).map(a=>[a.id,a]));
 for(const object of p.instances){
  if(ids.has(object.id))throw Error("Duplicate instance");
  ids.add(object.id);
  const asset=catalogue.get(object.assetId);
  // For built-in models the authoritative dimensions are in assets/catalog.json.
  // Unknown GLBs are NOT exported as arbitrary 1-meter cubes.
  if(!asset)continue;
  const [w,h,d]=asset.dimensions;
  const [x,y,z]=object.position;
  const pos=[+(x+width/2).toFixed(4),y,+(z+depth/2).toFixed(4)];
  if(![...pos,w,h,d].every(Number.isFinite)||pos[0]<0||pos[2]<0||
     pos[0]+w>width||pos[2]+d>depth||pos[1]<0||pos[1]+h>p.room.height)continue;
  const surface=object.layer==="floor"?"floor":object.layer==="wall"?"wall":"props";
  const isFurniture=object.layer==="props"||object.layer==="decor";
  items.push({id:object.id,assetId:object.assetId,position:pos,rotationY:object.rotationY,
    size:[w,h,d],editable:isFurniture&&!object.locked,petEditable:false,
    surface,label:object.label||asset.name});
 }
 return {schemaVersion:1,ownerId:String(ownerId).slice(0,80),roomId:String(roomId).slice(0,80),
  revision:0,items,history:[],undone:[],createdAt:0,
  source:{builderProjectId:p.projectId,sourceRevision:0,renderer:"glb-world",mode:"DESIGN_IMPORT_REQUIRES_GAME_APPROVAL"},
  bounds:{width,depth,height:p.room.height}};
}
