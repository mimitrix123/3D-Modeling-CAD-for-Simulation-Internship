import bpy
import math
import os
from mathutils import Vector

# Week 2: Functional 3-gear train. Run inside Blender.
MODULE = 2.0
GEAR_THICKNESS = 12.0
BORE_DIAMETER = 12.0
SHAFT_DIAMETER = 12.0
BASE_DIMS = (220.0, 100.0, 10.0)
GEARS = [("Gear_1_Input", 20), ("Gear_2_Idler", 30), ("Gear_3_Output", 40)]
CENTER_X = {"Gear_1_Input": -50.0, "Gear_2_Idler": 0.0, "Gear_3_Output": 70.0}

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def material(name, color, metallic=0.0, roughness=0.35):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0); m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
    return m

def add_box(name, dims, loc, mat, bevel=1.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod=o.modifiers.new('Edge_Rounds','BEVEL'); mod.width=bevel; mod.segments=3
    o.data.materials.append(mat); return o

def add_cylinder(name, radius, depth, loc, mat, vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(mat); return o

def create_gear(name, teeth, module, thickness, bore_d, loc, mat):
    root_r=module*(teeth/2.0-1.25); outer_r=module*(teeth/2.0+1.0); inner_r=bore_d/2.0
    steps=teeth*4; outer=[]; inner=[]
    for i in range(steps):
        a=2*math.pi*i/steps; phase=i%4; r=outer_r if phase in (1,2) else root_r
        outer.extend([(r*math.cos(a),r*math.sin(a),-thickness/2),(r*math.cos(a),r*math.sin(a),thickness/2)])
        inner.extend([(inner_r*math.cos(a),inner_r*math.sin(a),-thickness/2),(inner_r*math.cos(a),inner_r*math.sin(a),thickness/2)])
    verts=outer+inner; n=len(outer); faces=[]
    for i in range(0,n,2):
        j=(i+2)%n
        faces += [(i,j,j+1,i+1),(n+i+1,n+j+1,n+j,n+i),(i+1,j+1,n+j+1,n+i+1),(i,n+i,n+j,j)]
    mesh=bpy.data.meshes.new(name+'_Mesh'); mesh.from_pydata(verts,[],faces); mesh.update()
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o); o.location=loc; o.data.materials.append(mat)
    return o

def add_joint_marker(name, loc, parent):
    bpy.ops.object.empty_add(type='AXIS', location=loc)
    e=bpy.context.object; e.name=name; e.empty_display_size=8; e.parent=parent
    e['joint_type']='REVOLUTE'; e['axis']='Z'; e['fixed_to']='Base_Plate'; return e

def driver_ratio(target, source, numerator, denominator):
    f=target.driver_add('rotation_euler',2); d=f.driver; d.type='SCRIPTED'
    v=d.variables.new(); v.name='input_rot'; v.type='SINGLE_PROP'; v.targets[0].id=source; v.targets[0].data_path='rotation_euler[2]'
    d.expression=f'-input_rot*{numerator}/{denominator}'

def point_camera(camera,target):
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()

clear_scene(); bpy.context.scene.unit_settings.system='METRIC'; bpy.context.scene.unit_settings.length_unit='MILLIMETERS'
steel=material('Steel',(0.18,0.20,0.23),0.75,0.22); gear_mat=material('GearSteel',(0.34,0.38,0.44),0.8,0.2); base_mat=material('Base',(0.07,0.09,0.12),0.55,0.28)
base=add_box('Base_Plate',BASE_DIMS,(10,0,0),base_mat,2); base['fixed']=True; base['dimensions_mm']='220 x 100 x 10'
positions=[(CENTER_X['Gear_1_Input'],0,11),(CENTER_X['Gear_2_Idler'],0,11),(CENTER_X['Gear_3_Output'],0,11)]
shafts=[]; gears=[]
for idx,((name,teeth),pos) in enumerate(zip(GEARS,positions),1):
    shaft=add_cylinder(f'Shaft_{idx}_D12',SHAFT_DIAMETER/2,34,pos,steel); shaft.parent=base; shaft['diameter_mm']=12; shafts.append(shaft)
    gear=create_gear(name,teeth,MODULE,GEAR_THICKNESS,BORE_DIAMETER,pos,gear_mat)
    gear['teeth']=teeth; gear['module_mm']=MODULE; gear['pitch_diameter_mm']=MODULE*teeth; gear['thickness_mm']=GEAR_THICKNESS; gear['bore_mm']=BORE_DIAMETER; gear['joint']='REVOLUTE_Z'; gears.append(gear)
    add_joint_marker(f'Joint_Gear{idx}_Revolute',pos,base)
for idx,pos in enumerate(positions,1): add_cylinder(f'Collar_{idx}',8,4,(pos[0],0,22),steel)
driver_ratio(gears[1],gears[0],20,30); driver_ratio(gears[2],gears[1],30,40)
gears[0].rotation_euler.z=0; gears[0].keyframe_insert(data_path='rotation_euler',index=2,frame=1); gears[0].rotation_euler.z=2*math.pi; gears[0].keyframe_insert(data_path='rotation_euler',index=2,frame=120)
exploded=bpy.data.collections.new('EXPLODED_VIEW'); bpy.context.scene.collection.children.link(exploded)
for i,gear in enumerate(gears):
    dup=gear.copy(); dup.data=gear.data.copy(); exploded.objects.link(dup); dup.name=gear.name+'_Exploded'; dup.location.z+=30+i*18
for i,shaft in enumerate(shafts):
    dup=shaft.copy(); dup.data=shaft.data.copy(); exploded.objects.link(dup); dup.name=shaft.name+'_Exploded'; dup.location.z+=30+i*18
bpy.ops.mesh.primitive_plane_add(size=500,location=(10,0,-6)); bpy.context.object.name='Ground'; bpy.context.object.data.materials.append(material('GroundMat',(0.025,0.025,0.03),0,0.5))
bpy.ops.object.camera_add(location=(135,-185,150)); cam=bpy.context.object; cam.name='Camera_Assembly'; bpy.context.scene.camera=cam; point_camera(cam,(10,0,8)); cam.data.lens=52
for typ,loc,energy,size in [('AREA',(20,-80,150),1000,100),('AREA',(-120,50,80),700,80),('AREA',(130,80,70),900,70)]:
    bpy.ops.object.light_add(type=typ,location=loc); l=bpy.context.object; l.data.energy=energy; l.data.size=size; point_camera(l,(10,0,5))
scene=bpy.context.scene; scene.render.engine='BLENDER_EEVEE_NEXT'; scene.render.resolution_x=1200; scene.render.resolution_y=800; scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'
root=os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else os.getcwd(); out=os.path.join(root,'Week-2','renders'); os.makedirs(out,exist_ok=True); blend_path=os.path.join(root,'Week-2','gear_train_assembly.blend'); os.makedirs(os.path.dirname(blend_path),exist_ok=True)
scene.render.filepath=os.path.join(out,'gear_train_assembly.png'); bpy.ops.wm.save_as_mainfile(filepath=blend_path); bpy.ops.render.render(write_still=True)
scene.render.filepath=os.path.join(out,'gear_train_exploded.png'); point_camera(cam,(10,0,35)); bpy.ops.render.render(write_still=True); point_camera(cam,(10,0,8)); bpy.ops.wm.save_as_mainfile(filepath=blend_path)
print('Week 2 gear train created:',blend_path)
