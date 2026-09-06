"""Week 3 analytical benchmark for a rectangular cantilever beam."""
import csv

L = 0.300
b = 0.040
h = 0.020
F = 1000.0
E = 200e9

I = b * h**3 / 12.0
sigma_max = 6.0 * F * L / (b * h**2)
delta_tip = F * L**3 / (3.0 * E * I)

print(f"Second moment I = {I:.6e} m^4")
print(f"Maximum bending stress = {sigma_max/1e6:.3f} MPa")
print(f"Tip deflection = {delta_tip*1000:.4f} mm")

rows = []
for i in range(31):
    x = L * i / 30.0
    sigma = 6.0 * F * (L - x) / (b * h**2)
    delta = F * x**2 * (3.0 * L - x) / (6.0 * E * I)
    rows.append((x * 1000.0, sigma / 1e6, delta * 1000.0))

with open("fea_results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["x_mm", "bending_stress_MPa", "deflection_mm"])
    w.writerows(rows)

print("Wrote fea_results.csv")
