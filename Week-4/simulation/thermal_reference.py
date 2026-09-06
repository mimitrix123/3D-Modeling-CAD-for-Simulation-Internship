"""Steady-state thermal screening estimate for a device on the phone stand."""
import csv
from pathlib import Path

P = 8.0             # W representative heat generation
R_contact = 1.2     # K/W contact/interface resistance
R_spread = 1.8      # K/W conduction/spreading resistance
R_conv = 4.0        # K/W convection estimate
T_ambient = 25.0    # deg C
R_total = R_contact + R_spread + R_conv
delta_t = P * R_total
T_surface = T_ambient + delta_t

print(f"Total thermal resistance: {R_total:.2f} K/W")
print(f"Estimated surface temperature: {T_surface:.1f} deg C")

out = Path(__file__).with_name("thermal_results.csv")
with out.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "value", "unit"])
    w.writerow(["heat_load", P, "W"])
    w.writerow(["total_thermal_resistance", R_total, "K/W"])
    w.writerow(["ambient_temperature", T_ambient, "deg C"])
    w.writerow(["estimated_surface_temperature", T_surface, "deg C"])
