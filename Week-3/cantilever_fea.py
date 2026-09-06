import bpy
import math
import os
from mathutils import Vector

# Educational FEA visualization / analytical benchmark.
# Blender is used for geometry, heat-map visualization and deformation animation;
# validate engineering results with a dedicated FEA solver before design decisions.

L, B, H = 300.0, 40.0, 20.0
LOAD_N = 1000.0
E = 200e9
I = (B / 1000.0) * (H / 1000.0) ** 3 / 12.0
SIGMA_MAX_MPA = 6 * LOAD_N * (L / 1000.0) / ((B / 1000.0) * (H / 1000.0) ** 2) / 1e6
TIP_DEF_MM = LOAD_N * (L / 1000.0) ** 3 / (3 * E * I) * 1000


def clear():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


def mat(name, color, metallic=0.0, rough=0.4):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (*color, 1)
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = rough
    return m


def box(name, dims, loc, material):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    return o


def cylinder(name, radius, depth, loc, material):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o


def text(body, loc, size=7):
    bpy.ops.object.text_add(location=loc, rotation=(math.pi / 2, 0, 0))
    t = bpy.context.object
    t.data.body = body
    t.data.size = size
    t.data.extrude = 0.05
    return t


clear()
bpy.context.scene.unit_settings.system = 'METRIC'
bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

steel = mat('BeamSteel', (0.24, 0.27, 0.31), 0.65, 0.25)
support_mat = mat('FixedSupport', (0.08, 0.09, 0.11), 0.2, 0.35)
load_mat = mat('LoadMarker', (0.7, 0.12, 0.05), 0.1, 0.3)
heat = []
# blue -> cyan -> green -> yellow -> red style heat map materials
for name, c in [('S0', (0.05,0.15,0.8)), ('S1',(0.0,0.65,0.85)), ('S2',(0.1,0.75,0.25)), ('S3',(0.95,0.8,0.05)), ('S4',(0.85,0.08,0.03))]:
    heat.append(mat(name, c, 0.15, 0.3))

# Beam centered along X; fixed at x=0.
beam = box('Cantilever_Beam', (L, B, H), (L/2, 0, 0), steel)
beam['material'] = 'Structural steel reference'
beam['youngs_modulus_GPa'] = 200
beam['poisson_ratio'] = 0.30
beam['load_N'] = LOAD_N
beam['fixed_end'] = True

# Split the beam visually into 30 segments for a stress heat map.
for i in range(30):
    x0 = i * L / 30
    x1 = (i + 1) * L / 30
    seg = box(f'FEA_Segment_{i+1:02d}', (L/30 + 0.2, B + 0.2, H + 0.2), ((x0+x1)/2, 0, 0), heat[int(i/29*4)])
    seg['stress_MPa_reference'] = SIGMA_MAX_MPA * (1 - i/29)
    seg['x_mm'] = (x0+x1)/2

# Fixed support representation.
support = box('Fixed_Support', (20, 70, 60), (-10, 0, -10), support_mat)
support['constraint'] = 'FIXED'
support['constrained_face'] = 'x=0'

# Load arrow and label.
arrow = cylinder('Load_Arrow', 3, 35, (L+12, 0, -28), load_mat)
arrow.rotation_euler.y = math.pi/2
bpy.ops.object.cone_add(vertices=32, radius1=8, depth=18, location=(L+12, 0, -48), rotation=(0, math.pi/2, 0))
head = bpy.context.object
head.name = 'Load_Arrowhead'
head.data.materials.append(load_mat)
text(f'LOAD = {LOAD_N:.0f} N', (L+28, 0, -55), 6)
text(f'σmax ≈ {SIGMA_MAX_MPA:.1f} MPa', (L/2, 0, 24), 5)
text(f'Tip δ ≈ {TIP_DEF_MM:.3f} mm', (L/2, 0, 31), 5)

# Deformation visualization: exaggerated 30x for readability.
scale = 30.0
for frame in (1, 60, 120):
    factor = (frame-1)/119
    for i in range(30):
        x = (i + 0.5) * L/30
        delta_m = LOAD_N * (x/1000)**2 * (3*(L/1000) - x/1000) / (6*E*I)
        z = -delta_m*1000*scale*factor
        o = bpy.data.objects.get(f'FEA_Segment_{i+1:02d}')
        o.location.z = z
        o.keyframe_insert(data_path='location', index=2, frame=frame)

# Camera and lighting.
bpy.ops.object.camera_add(location=(430, -500, 330))
cam = bpy.context.object
bpy.context.scene.camera = cam

def aim(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()

aim(cam, (L/2, 0, -8)); cam.data.lens = 55
for loc, energy, size in [((120,-250,300),1200,180), ((-80,180,160),800,130), ((380,100,120),900,120)]:
    bpy.ops.object.light_add(type='AREA', location=loc)
    light = bpy.context.object
    light.data.energy = energy
    light.data.shape = 'DISK'
    light.data.size = size
    aim(light, (L/2,0,0))

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1400
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'

root = os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else os.getcwd()
out = os.path.join(root, 'Week-3', 'renders')
os.makedirs(out, exist_ok=True)
scene.render.filepath = os.path.join(out, 'cantilever_fea.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root, 'Week-3', 'cantilever_fea.blend'))
bpy.ops.render.render(write_still=True)
scene.render.filepath = os.path.join(out, 'cantilever_deformation.png')
bpy.context.scene.frame_set(120)
bpy.ops.render.render(write_still=True)
print('Week 3 setup complete')
print(f'Reference max stress: {SIGMA_MAX_MPA:.3f} MPa')
print(f'Reference tip deflection: {TIP_DEF_MM:.4f} mm')
