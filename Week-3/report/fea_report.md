# Week 3 FEA Report — Cantilever Beam

## Executive summary
A 300 × 40 × 20 mm rectangular cantilever beam is fixed at one end and subjected to a 1000 N downward tip load. The analytical benchmark predicts a maximum bending stress of **112.5 MPa** at the fixed end and a tip deflection of **1.6875 mm**.

## Boundary conditions
- Fixed support at x = 0 mm.
- Vertical downward load of 1000 N at x = 300 mm.
- Structural-steel reference: E = 200 GPa, ν = 0.30.

## Results
| Quantity | Reference result |
|---|---:|
| Maximum bending stress | 112.5 MPa |
| Tip deflection | 1.6875 mm |
| Second moment of area | 2.6667e-8 m⁴ |

## Stress distribution
For the surface-fiber bending benchmark, stress decreases linearly from the fixed end toward the free end. The Blender scene visualizes this distribution as a heat map, with the highest-stress region near the fixed support.

## Deformation animation
The Blender scene animates the beam from unloaded to loaded configuration. Deformation is intentionally exaggerated for visual clarity; the report value of 1.6875 mm is the analytical physical deflection.

## Engineering interpretation
The fixed end is the critical region because the bending moment is largest there. A real FEA workflow should use a converged mesh, appropriate contact/material models, and a validated solver. Compare solver stress and displacement against the analytical benchmark before drawing engineering conclusions.

## Deliverables
- Parametric Blender model and visualization script
- Analytical benchmark script and CSV generation
- Stress heat-map reference
- Deformation animation setup
- Presentation-ready report

> Educational project: numerical values are analytical reference results, not certification or a substitute for professional engineering analysis.
