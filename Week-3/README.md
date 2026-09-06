# Week 3 — Cantilever Beam FEA Stress Analysis

## Objective
Simulate and visualize a real-world structural scenario: a cantilever beam fixed at one end and loaded at the free end. The project includes a parametric Blender model, an FEA-style analytical reference calculation, stress heat-map visualization, deformation animation, and presentation-ready report assets.

## Model
- Beam: 300 × 40 × 20 mm
- Material: structural steel reference
- Young's modulus: 200 GPa
- Poisson ratio: 0.30
- Density: 7850 kg/m³
- End load: 1000 N downward
- Fixed support: left end face

## Analytical reference
For a rectangular cantilever with an end load:
- Second moment: `I = b h³ / 12`
- Maximum bending stress: `σmax = 6 F L / (b h²)`
- Tip deflection: `δ = F L³ / (3 E I)`

For the project dimensions and load, the reference values are approximately:
- `σmax = 112.5 MPa`
- `δ = 1.6875 mm`

These values provide a sanity check for the numerical/FEA visualization. They are not a substitute for a solver run.

## Deliverables
- `cantilever_fea.py` — Blender procedural model, support/load markers, analytical stress field, heat-map materials, deformation animation, cameras, lights and render setup.
- `fea_reference.py` — Python calculation of bending stress and tip deflection plus CSV report generation.
- `report/fea_report.md` — presentation-ready result summary and interpretation.
- `report/stress_distribution.svg` — stress heat-map/reference plot and beam diagram.
- `renders/README.md` — instructions for generating presentation renders.

## Running
1. Run `fea_reference.py` with Python to generate `fea_results.csv`.
2. Open Blender and run `cantilever_fea.py` from the Scripting workspace.
3. The Blender script creates the beam, fixed support, load indicator, stress visualization, deformed animation, cameras and render setup.
4. For engineering validation, replace the analytical reference visualization with a solver result from a validated FEA package and compare the peak stress/deflection.

> Important: this repository provides an educational FEA visualization and analytical benchmark. Blender alone is not being represented as a certified structural FEA solver.

## Checklist
- [x] Real-world structural scenario
- [x] Beam model
- [x] Load and fixed constraint representation
- [x] Analytical FEA benchmark
- [x] Stress heat-map visualization
- [x] Deformation animation
- [x] Presentation/report assets
- [x] Render setup
- [x] Engineering validation note
