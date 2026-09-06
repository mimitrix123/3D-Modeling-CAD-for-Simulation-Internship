import bpy
import math
from mathutils import Vector

# Week 1 Mini Project: Complete Desk Setup
# Blender 3.x/4.x compatible procedural scene.
# Builds desk, monitor, keyboard, mouse, lamp and mug, applies materials,
# creates a 3-point lighting setup, and renders at 1920x1080.

# -------------------------
# Scene cleanup
# -------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    # Keep datablocks managed by Blender; unused ones are harmless.
    pass

# -------------------------
# Helpers
# -------------------------
def mat(name, color, metallic=0.0, roughness=0.45):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    return m

def cube(name, loc, scale, material, bevel=0.06):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new('Soft edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
    o.data.materials.append(material)
    return o

def cyl(name, loc, radius, depth, material, vertices=64, bevel=0.04):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    if bevel:
        mod = o.modifiers.new('Soft edges', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
    o.data.materials.append(material)
    return o

def uv_sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o

def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# -------------------------
# Materials
# -------------------------
wood = mat('Walnut Wood', (0.20, 0.075, 0.025), roughness=0.32)
black = mat('Matte Black', (0.012, 0.016, 0.02), roughness=0.28)
dark = mat('Dark Plastic', (0.035, 0.045, 0.055), roughness=0.38)
white = mat('Ceramic White', (0.82, 0.84, 0.86), roughness=0.22)
metal = mat('Brushed Metal', (0.22, 0.25, 0.28), metallic=0.85, roughness=0.24)
blue = mat('Accent Blue', (0.025, 0.18, 0.55), metallic=0.1, roughness=0.28)
coffee = mat('Coffee', (0.035, 0.012, 0.006), roughness=0.2)
wall = mat('Wall', (0.12, 0.14, 0.17), roughness=0.72)

# -------------------------
# Floor / background
# -------------------------
cube('Floor', (0, 0, -0.12), (5.8, 4.5, 0.12), wall, 0.02)
cube('Back Wall', (0, 4.35, 3.2), (5.8, 0.10, 3.4), wall, 0.02)

# -------------------------
# Desk
# -------------------------
cube('Desktop', (0, 0, 1.55), (3.9, 1.65, 0.12), wood, 0.08)
for x in (-3.45, 3.45):
    for y in (-1.28, 1.28):
        cube('Desk Leg', (x, y, 0.72), (0.18, 0.18, 0.72), black, 0.04)
cube('Cable Tray', (0, 1.25, 1.28), (2.7, 0.16, 0.08), black, 0.03)

# -------------------------
# Monitor
# -------------------------
cube('Monitor Stand Base', (0, 0.35, 1.83), (0.78, 0.42, 0.07), metal, 0.05)
cube('Monitor Stand', (0, 0.35, 2.28), (0.09, 0.09, 0.40), metal, 0.03)
cube('Monitor Body', (0, 0.35, 3.12), (2.25, 0.12, 0.76), black, 0.08)
cube('Monitor Screen', (0, 0.205, 3.12), (2.03, 0.025, 0.56), blue, 0.025)
# simple screen highlight / status bar
cube('Screen Bar', (0, 0.165, 2.70), (0.85, 0.015, 0.035), white, 0.01)

# -------------------------
# Keyboard
# -------------------------
cube('Keyboard Body', (-0.55, -0.62, 1.72), (1.65, 0.48, 0.08), dark, 0.07)
for r in range(4):
    count = 12 if r < 3 else 10
    for c in range(count):
        x = -1.72 + c * 0.22 + (0.11 if r == 3 else 0)
        y = -0.95 + r * 0.22
        cube('Key', (x, y, 1.82), (0.075, 0.065, 0.035), white, 0.018)
cube('Spacebar', (-0.55, -0.30, 1.82), (0.58, 0.065, 0.035), white, 0.018)

# -------------------------
# Mouse + pad
# -------------------------
cube('Mouse Pad', (2.15, -0.70, 1.69), (0.90, 0.68, 0.025), black, 0.08)
uv_sphere('Mouse', (2.15, -0.72, 1.82), (0.38, 0.52, 0.16), dark)
cube('Mouse Center Strip', (2.15, -0.35, 1.93), (0.025, 0.18, 0.018), blue, 0.01)

# -------------------------
# Lamp
# -------------------------
cyl('Lamp Base', (-2.95, 0.85, 1.76), 0.42, 0.10, metal)
cyl('Lamp Pole', (-2.95, 0.85, 2.35), 0.055, 1.15, metal)
bpy.ops.mesh.primitive_cone_add(vertices=64, radius1=0.46, radius2=0.23, depth=0.48, location=(-2.95, 0.85, 2.98))
shade = bpy.context.object
shade.name = 'Lamp Shade'
shade.rotation_euler[1] = math.radians(-18)
shade.data.materials.append(black)
bpy.ops.object.shade_smooth()
# lamp bulb
uv_sphere('Lamp Bulb', (-2.95, 0.72, 2.88), (0.12, 0.12, 0.12), white)

# -------------------------
# Coffee mug
# -------------------------
cyl('Coffee Mug', (2.95, 0.45, 1.91), 0.34, 0.55, white, bevel=0.035)
# coffee surface
cyl('Coffee', (2.95, 0.45, 2.195), 0.275, 0.025, coffee, bevel=0.01)
# torus handle
bpy.ops.mesh.primitive_torus_add(major_radius=0.28, minor_radius=0.065, major_segments=48, minor_segments=16, location=(3.27, 0.45, 1.96), rotation=(math.radians(90), 0, 0))
handle = bpy.context.object
handle.name = 'Mug Handle'
handle.scale.y = 0.78
handle.data.materials.append(white)

# -------------------------
# 3-point lighting
# -------------------------
def area(name, loc, energy, size, target, color=(1.0, 1.0, 1.0)):
    data = bpy.data.lights.new(name, type='AREA')
    data.energy = energy
    data.shape = 'DISK'
    data.size = size
    data.color = color
    o = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o

area('Key Light', (-4.5, -4.0, 6.0), 1050, 4.0, (0, 0, 1.8), (1.0, 0.90, 0.78))
area('Fill Light', (4.5, -2.0, 4.0), 650, 4.5, (0, 0, 2.0), (0.78, 0.88, 1.0))
area('Rim Light', (0, 3.5, 5.5), 900, 3.0, (0, 0, 2.4), (1.0, 1.0, 1.0))

# Warm practical lamp light
lamp_data = bpy.data.lights.new('Lamp Glow', type='POINT')
lamp_data.energy = 90
lamp_data.color = (1.0, 0.55, 0.20)
lamp_obj = bpy.data.objects.new('Lamp Glow', lamp_data)
bpy.context.collection.objects.link(lamp_obj)
lamp_obj.location = (-2.95, 0.60, 2.95)

# -------------------------
# Camera
# -------------------------
cam_data = bpy.data.cameras.new('Camera')
cam = bpy.data.objects.new('Camera', cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
cam.location = (7.6, -8.6, 5.7)
cam_data.lens = 48
look_at(cam, (0, 0.15, 2.0))

# -------------------------
# Render settings
# -------------------------
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '//render/week1_desk_setup.png'
scene.render.film_transparent = False
scene.world.color = (0.025, 0.03, 0.045)

# Color management
scene.view_settings.look = 'AgX - Medium High Contrast'

# Ground contact polish
scene.render.image_settings.color_mode = 'RGBA'

# Save and render
bpy.ops.wm.save_as_mainfile(filepath='//week1_desk_setup.blend')
bpy.ops.render.render(write_still=True)
print('Week 1 desk setup created and rendered to render/week1_desk_setup.png')
