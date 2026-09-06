# Modular Desk Organizer — Design Portfolio

## 1. Design brief

Create a compact desktop product that combines stationery storage, phone support, cable management, and modular organization while remaining practical for FDM additive manufacturing.

## 2. Concept

The concept uses a rigid open tray as the structural base and removable inserts for personalization. A dedicated phone stand gives the product a useful everyday interaction while the pen cup and divider create configurable storage zones.

## 3. CAD strategy

Primary dimensions are centralized in `cad/desk_organizer_parametric.py`. This makes the model reproducible and allows future variants to change overall tray size, wall thickness, phone-slot dimensions, and divider thickness from one parameter block.

## 4. Assembly

The product is decomposed into printable modules instead of one monolithic part. The animation demonstrates an exploded sequence and return to the assembled state.

## 5. Simulation results

The phone-support feature is checked with a screening cantilever calculation. At a representative 150 N design load, the script computes bending stress and tip deflection and compares stress with a placeholder polymer yield-strength value. These numbers are for workflow demonstration and must be replaced by material-specific validated data before engineering use.

A separate thermal resistance model estimates steady-state surface temperature for an 8 W representative heat source. The model exposes contact, spreading, and convection assumptions so they can be replaced by measured or solver-derived values.

## 6. Manufacturing

The design targets FDM printing in PLA or PETG. Large planar surfaces, modular inserts, and modest wall thickness reduce print complexity. Final STL geometry must be checked for manifoldness and actual printer clearances.

## 7. Technical documentation

`drawings/technical_drawing.svg` contains top/front/profile fabrication references with primary dimensions, tolerances, wall thickness, units, and print process notes.

## 8. Visualization

The Blender script creates a studio camera, three-point lighting, product materials, an assembly animation, and render settings suitable for a portfolio hero image.

## 9. Limitations

This repository is a reproducible internship portfolio project. It does not claim certified structural FEA, CFD, production tooling validation, or printer-specific dimensional qualification. For production release, use a validated solver, mesh convergence study, measured material properties, fit tests, thermal measurements, and a formal design review.

## 10. Portfolio talking points

- Parametric product modeling
- Modular CAD architecture
- Assembly and exploded-view communication
- Simulation-aware design
- Design for additive manufacturing
- Technical drawing practice
- Photorealistic visualization workflow
- Animation and presentation storytelling
