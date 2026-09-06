"""Week 4 — Parametric modular desk organizer generator.

Run inside Blender's Python environment. The script creates a small product
assembly, an exploded configuration, animation, materials, cameras, lights,
and render settings. It intentionally keeps dimensions in one parameter block.
"""
import bpy
import math
from mathutils import Vector

# ------------------------- Parameters (mm) -------------------------
TRAY_L = 220.0
TRAY_W = 110.0
TRAY_H = 32.0
WALL = 3.0
PEN_L = 70.0
PEN_W = 70.0
PEN_H = 90.0
PHONE_SLOT_W = 88.0
PHONE_SLOT_D = 14.0
DIVIDER_T = 3.0

# ------------------------- Helpers -------------------------
def mat(name, color, metallic=0.0, roughness=0.4):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
    return m


def cube(name, dims, loc, material=None, bevel=1.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = o.modifiers.new("Edge_Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    if material:
        o.data.materials.append(material)
    return o


def cylinder(name, radius, depth, loc, material=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    if material:
        o.data.materials.append(material)
    return o


def keyframe_location(o, frame, loc):
    o.location = loc
    o.keyframe_insert(data_path="location", frame=frame)

# ------------------------- Scene -------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

body_mat = mat("Body_Matte", (0.055, 0.065, 0.08), metallic=0.05, roughness=0.3)
accent_mat = mat("Accent", (0.10, 0.28, 0.65), metallic=0.15, roughness=0.28)
insert_mat = mat("Insert", (0.16, 0.17, 0.19), metallic=0.0, roughness=0.38)
rubber_mat = mat("Rubber", (0.015, 0.015, 0.018), roughness=0.7)
metal_mat = mat("Metal", (0.32, 0.34, 0.38), metallic=0.8, roughness=0.22)

# Tray: floor + four walls, open top.
parts = []
floor = cube("Tray_Floor", (TRAY_L, TRAY_W, WALL), (0, 0, WALL/2), body_mat, 1.2)
parts.append(floor)
for name, dims, loc in [
    ("Tray_Front", (TRAY_L, WALL, TRAY_H), (0, -TRAY_W/2 + WALL/2, TRAY_H/2)),
    ("Tray_Back", (TRAY_L, WALL, TRAY_H), (0, TRAY_W/2 - WALL/2, TRAY_H/2)),
    ("Tray_Left", (WALL, TRAY_W-2*WALL, TRAY_H), (-TRAY_L/2 + WALL/2, 0, TRAY_H/2)),
    ("Tray_Right", (WALL, TRAY_W-2*WALL, TRAY_H), (TRAY_L/2 - WALL/2, 0, TRAY_H/2)),
]:
    parts.append(cube(name, dims, loc, body_mat, 1.0))

# Phone stand: two feet/rails and a back support with cable opening represented by two rails.
phone_x = -42.0
rail_y = -TRAY_W/2 + 25.0
phone_base = cube("Phone_Base", (PHONE_SLOT_W, 18, 8), (phone_x, rail_y, 6), accent_mat, 1.5)
phone_back = cube("Phone_Back", (PHONE_SLOT_W, 6, 48), (phone_x, rail_y+8, 29), accent_mat, 1.5)
phone_lip = cube("Phone_Lip", (PHONE_SLOT_W, 14, 8), (phone_x, rail_y-2, 17), accent_mat, 1.2)
parts += [phone_base, phone_back, phone_lip]

# Pen cup as an open-top shell assembled from four walls + floor.
pen_x, pen_y = 62.0, 0.0
pen_parts = [
    cube("PenCup_Floor", (PEN_L, PEN_W, WALL), (pen_x, pen_y, WALL/2), insert_mat, 1.0),
    cube("PenCup_Front", (PEN_L, WALL, PEN_H), (pen_x, pen_y-PEN_W/2+WALL/2, PEN_H/2), insert_mat, 1.0),
    cube("PenCup_Back", (PEN_L, WALL, PEN_H), (pen_x, pen_y+PEN_W/2-WALL/2, PEN_H/2), insert_mat, 1.0),
    cube("PenCup_Left", (WALL, PEN_W-2*WALL, PEN_H), (pen_x-PEN_L/2+WALL/2, pen_y, PEN_H/2), insert_mat, 1.0),
    cube("PenCup_Right", (WALL, PEN_W-2*WALL, PEN_H), (pen_x+PEN_L/2-WALL/2, pen_y, PEN_H/2), insert_mat, 1.0),
]
parts += pen_parts

# Divider: removable vertical plate with finger tab.
divider = cube("SnapFit_Divider", (DIVIDER_T, 75, 24), (-42, 30, 13), accent_mat, 0.8)
tab = cube("Divider_Tab", (12, 16, 4), (-42, 30, 27), accent_mat, 1.0)
parts += [divider, tab]

# Cable-management insert: base plus rounded visual grommet.
cable = cube("Cable_Insert", (34, 24, 6), (18, -31, 5), insert_mat, 2.0)
grommet = cylinder("Cable_Grommet", 6, 5, (18, -31, 9), rubber_mat)
parts += [cable, grommet]

# Rubber feet under tray.
for i, (x, y) in enumerate([(-TRAY_L/2+14, -TRAY_W/2+14), (-TRAY_L/2+14, TRAY_W/2-14),
                            (TRAY_L/2-14, -TRAY_W/2+14), (TRAY_L/2-14, TRAY_W/2-14)]):
    parts.append(cylinder(f"RubberFoot_{i+1}", 6, 3, (x, y, -1.5), rubber_mat))

# Add a small parametric data panel as custom properties.
root = bpy.data.objects.new("DeskOrganizer_Product", None)
bpy.context.collection.objects.link(root)
root["parametric_overall_mm"] = f"{TRAY_L} x {TRAY_W} x {TRAY_H}"
root["wall_thickness_mm"] = WALL
root["phone_slot_width_mm"] = PHONE_SLOT_W
root["phone_slot_depth_mm"] = PHONE_SLOT_D
root["divider_thickness_mm"] = DIVIDER_T
root["design_intent"] = "Modular desktop organizer for FDM printing"

# Assembly collection.
assembly = bpy.data.collections.new("ASSEMBLY")
bpy.context.scene.collection.children.link(assembly)
for o in parts:
    # Objects remain in their original collection for simplicity; tag them for downstream export.
    o["assembly_role"] = "product_part"

# ------------------------- Exploded animation -------------------------
# Store original positions, then animate selected inserts away from the tray.
for o in parts:
    o["original_location"] = tuple(o.location)

exploded = {
    "PenCup_Floor": (0, 0, 65),
    "PenCup_Front": (0, 0, 110),
    "PenCup_Back": (0, 0, 150),
    "PenCup_Left": (-65, 0, 105),
    "PenCup_Right": (65, 0, 105),
    "SnapFit_Divider": (-42, 60, 50),
    "Divider_Tab": (-42, 60, 80),
    "Cable_Insert": (18, -70, 45),
    "Cable_Grommet": (18, -70, 58),
    "Phone_Back": (-42, -70, 80),
    "Phone_Lip": (-42, -70, 60),
}
for o in parts:
    base = Vector(o.location)
    keyframe_location(o, 1, base)
    keyframe_location(o, 45, base)
    if o.name in exploded:
        keyframe_location(o, 90, Vector(exploded[o.name]))
    else:
        keyframe_location(o, 90, base)
    keyframe_location(o, 130, base)

# Linear-to-ease interpolation for polished assembly motion.
if bpy.context.scene.animation_data:
    pass
for action in bpy.data.actions:
    for fc in action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'

# ------------------------- Presentation -------------------------
# Ground plane.
ground_mat = mat("Ground", (0.025, 0.028, 0.035), roughness=0.5)
ground = cube("Ground", (520, 420, 4), (0, 0, -8), ground_mat, 0)

# Camera.
bpy.ops.object.camera_add(location=(330, -300, 250))
cam = bpy.context.object
cam.name = "Portfolio_Camera"
bpy.context.scene.camera = cam

def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()
point_at(cam, (0, 0, 25))
cam.data.lens = 52

# Three-point studio lighting.
for name, loc, energy, size in [
    ("Key", (180, -180, 280), 1100, 120),
    ("Fill", (-180, -100, 160), 700, 100),
    ("Rim", (120, 180, 220), 900, 90),
]:
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.object
    l.name = name
    l.data.energy = energy
    l.data.shape = 'DISK'
    l.data.size = size
    point_at(l, (0, 0, 20))

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 1600
scene.render.resolution_y = 1000
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "Week-4/renders/desk_organizer.png"
scene.frame_start = 1
scene.frame_end = 130

# Metadata for portfolio/reproducibility.
scene["project"] = "Week 4 — Parametric Modular Desk Organizer"
scene["units"] = "millimeters"
scene["simulation_status"] = "Reference analytical checks; not certification-grade FEA"
scene["print_process"] = "FDM / PLA or PETG"

# Save blend and render a hero frame.
bpy.ops.wm.save_as_mainfile(filepath="Week-4/desk_organizer.blend")
scene.frame_set(45)
bpy.ops.render.render(write_still=True)
print("Week 4 desk organizer generated.")
