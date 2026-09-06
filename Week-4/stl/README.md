# STL / 3D-print preparation

The Blender generator tags each product component with `assembly_role=product_part`, making it straightforward to export individual parts.

## Recommended print setup

- Process: FDM
- Material: PLA for prototypes; PETG for tougher functional parts
- Layer height: 0.20 mm
- Nozzle: 0.4 mm
- Wall count: 3–4
- Infill: 15–25%
- Brim: optional for tall pen-cup walls
- Print orientation: keep large flat tray surfaces on the build plate; orient tall walls to minimize unsupported overhangs.

## Export

Inside Blender, select each tagged component and use **File → Export → STL**, with selection-only enabled. Suggested filenames:

```text
tray_floor.stl
tray_front.stl
tray_back.stl
tray_left.stl
tray_right.stl
phone_base.stl
phone_back.stl
phone_lip.stl
pen_cup_floor.stl
pen_cup_front.stl
pen_cup_back.stl
pen_cup_left.stl
pen_cup_right.stl
snapfit_divider.stl
divider_tab.stl
cable_insert.stl
cable_grommet.stl
rubber_foot_1.stl ... rubber_foot_4.stl
```

Before printing, run manifold/non-manifold and wall-thickness checks in the slicer/CAD package. The repository documents the export workflow rather than claiming binary STL files were generated in the current environment.
