# Major Project — Week 4: Parametric Desk Organizer

A complete product-design workflow for a modular **desk organizer** intended to demonstrate CAD modeling, parametric thinking, assembly design, simulation-ready setup, technical documentation, 3D-print preparation, rendering, and animation.

## Product concept

The product is a compact modular desktop organizer consisting of:

- Main organizer tray/body
- Removable pen cup
- Phone stand insert
- Cable-management insert
- Snap-fit divider
- Optional rubber-foot locations

The design is intentionally split into parts so the assembly can be edited, printed, and demonstrated as a small portfolio project.

## Deliverables

| Requirement | Deliverable |
|---|---|
| Concept sketch | `concept/concept_sketch.svg` |
| Parametric CAD | `cad/desk_organizer_parametric.py` |
| Assembly | `assembly/assembly_plan.md` + Blender generator |
| Stress simulation | `simulation/stress_reference.py` |
| Thermal simulation | `simulation/thermal_reference.py` |
| Technical drawings | `drawings/technical_drawing.svg` |
| 3D printing STL | `stl/README.md` + STL generation workflow |
| Photorealistic render | `renders/README.md` + Blender render setup |
| Assembly animation | Blender animation setup in CAD generator |
| Portfolio | `portfolio/design_portfolio.md` |

## Parametric dimensions

All primary dimensions are centralized in the CAD generator so the design can be resized without rebuilding the model manually.

- Overall tray: 220 × 110 × 32 mm
- Wall thickness: 3 mm
- Pen cup: 70 × 70 × 90 mm
- Phone slot width: 88 mm
- Phone slot depth: 14 mm
- Cable slot: 12 mm nominal
- Divider thickness: 3 mm

## Simulation approach

The project includes lightweight Python reference calculations for screening-level design validation:

- Static bending/stress check for the organizer's cantilevered phone-support feature.
- Steady-state thermal resistance estimate for a warm device resting in the stand.

These calculations are **engineering reference checks, not certification-grade FEA/CFD**. A production design should be validated in a qualified solver with material characterization, realistic contacts, mesh convergence, and appropriate safety factors.

## Blender workflow

Run the CAD generator inside Blender's Python environment to create:

1. Parametric parts and materials.
2. Assembly placement and exploded-view positions.
3. Camera and studio lighting.
4. Stress/thermal visualization materials.
5. Assembly animation.
6. Render settings.
7. A `.blend` project file.

The current repository contains reproducible scripts and documentation; binary `.blend`, `.stl`, and rendered image outputs should be generated locally in Blender using the included workflow.

## Portfolio structure

The final portfolio documents:

- Design objective and user problem
- Concept evolution
- Parametric modeling strategy
- Part breakdown and assembly
- Simulation assumptions and results
- Manufacturing/3D-print considerations
- Technical drawings and dimensions
- Rendering and animation
- Limitations and next improvements

## Suggested execution

```text
1. Open Blender
2. Run cad/desk_organizer_parametric.py
3. Inspect the assembled and exploded configurations
4. Run simulation/stress_reference.py and simulation/thermal_reference.py with Python
5. Export individual printable components as STL
6. Generate technical-drawing output
7. Render the studio views
8. Play the assembly animation
9. Use portfolio/design_portfolio.md as the presentation narrative
```

## Learning outcomes

This project demonstrates a realistic end-to-end product-design pipeline rather than a single isolated CAD model: **concept → parametric CAD → assembly → simulation → drawing → additive manufacturing → visualization → portfolio**.