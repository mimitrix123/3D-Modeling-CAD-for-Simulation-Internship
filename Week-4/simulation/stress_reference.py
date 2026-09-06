"""Screening stress check for the phone-support feature.

This is a compact mechanics benchmark, not a full 3-D FEA solver.
"""
import csv
from pathlib import Path

F = 150.0
L = 0.088
B = 0.014
H = 0.006
E = 2.1e9
I = B * H**3 / 12
sigma_pa = 6 * F * L / (B * H**2)
delta_m = F * L**3 / (3 * E * I)
YIELD_MPA = 45.0
SF = (YIELD_MPA * 1e6) / sigma_pa

print(f"Bending stress: {sigma_pa/1e6:.2f} MPa")
print(f"Tip deflection: {delta_m*1000:.2f} mm")
print(f"Screening factor of safety: {SF:.2f}")

out = Path(__file__).with_name("stress_results.csv")
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "value", "unit"])
    w.writerow(["load", F, "N"])
    w.writerow(["bending_stress", sigma_pa/1e6, "MPa"])
    w.writerow(["tip_deflection", delta_m*1000, "mm"])
    w.writerow(["screening_yield_strength", YIELD_MPA, "MPa"])
    w.writerow(["factor_of_safety", SF, "-"])
print(f"Wrote {out}")
