import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

# ==== Configuration ====
sink_type = "Shell_Point_Wilson_Mesons"
target_gamma = "15"
target_momentum = "0 0 0"
input_file = "hadspec.dat.xml"

# Plateau fit range
t_min = 5
t_max = 12
# =======================

# Load and parse the XML
tree = ET.parse(input_file)
root = tree.getroot()
mesons_path = f".//Wilson_hadron_measurements/elem/{sink_type}"
mesons_elem = root.find(mesons_path)

if mesons_elem is None:
    print(f"Error: Could not find path '{mesons_path}'")
    exit(1)

found = False
data = []

for meson in mesons_elem.findall("elem"):
    gamma_val = meson.find("gamma_value")
    if gamma_val is not None and gamma_val.text.strip() == target_gamma:
        for mom in meson.find("momenta").findall("elem"):
            sink_mom = mom.find("sink_mom")
            if sink_mom is not None and sink_mom.text.strip() == target_momentum:
                print(f"Found correlator for:")
                print(f"  sink_type   = {sink_type}")
                print(f"  gamma_value = {target_gamma}")
                print(f"  sink_mom    = {target_momentum}\n")
                for point in mom.find("mesprop").findall("elem"):
                    re = float(point.find("re").text.strip())
                    im = float(point.find("im").text.strip())
                    data.append((re, im))
                found = True
                break
        if found:
            break

if not found:
    print("No matching correlator found.")
    exit(1)

# Convert to NumPy arrays
data_array = np.array(data)
time = np.arange(len(data_array))
re_part = data_array[:, 0]
mag_part = np.abs(re_part)

# Calculate effective mass: m_eff(t) = log(C(t)/C(t+1))
eff_mass = np.log(np.divide(mag_part[:-1], mag_part[1:],
                            out=np.zeros_like(mag_part[:-1]), where=mag_part[1:] > 0))

# Plateau fit
plateau_region = (time[:-1] >= t_min) & (time[:-1] <= t_max)
plateau_values = eff_mass[plateau_region]
plateau_times = time[:-1][plateau_region]

if len(plateau_values) == 0:
    print("Warning: No data in plateau region.")
    plateau_avg = None
else:
    plateau_avg = np.mean(plateau_values)
    plateau_std = np.std(plateau_values) / np.sqrt(len(plateau_values))

# Plotting
plt.figure(figsize=(10, 4))

# Correlator
plt.subplot(1, 2, 1)
plt.semilogy(time, mag_part, marker='o', label="|Re|")
plt.title("Correlator (log scale)")
plt.xlabel("Time slice")
plt.ylabel("Correlator")
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend()

# Effective mass with plateau
plt.subplot(1, 2, 2)
plt.plot(time[:-1], eff_mass, marker='s', color='darkgreen', label="m_eff(t)")
if plateau_avg is not None:
    plt.hlines(plateau_avg, t_min, t_max, color='red', linestyle='--',
               label=f"Plateau Fit: {plateau_avg:.4f} ± {plateau_std:.4f}")
    plt.axvspan(t_min, t_max, color='red', alpha=0.1)
plt.title("Effective Mass with Plateau Fit")
plt.xlabel("Time slice")
plt.ylabel("m_eff(t)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.tight_layout()
plt.show()
