import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

# ==== Configuration ====
target_sink_type = "Shell_Shell_Wilson_Mesons"
target_gamma = "15"
input_file = "hadspec.dat.xml"
plateau_range = (5, 12)

momenta_to_check = [
    "0 0 0",
    "1 0 0",
    "1 1 0",
    "1 1 1",
]

# ==== Helper Functions ====
def parse_correlator_data(mom_elem):
    data = []
    for point in mom_elem.find("mesprop").findall("elem"):
        re = float(point.find("re").text.strip())
        data.append(re)
    return np.array(data)

def compute_effective_mass(corr):
    return np.log(np.divide(corr[:-1], corr[1:], out=np.zeros_like(corr[:-1]), where=corr[1:] > 0))

def fit_plateau(m_eff, t_min, t_max):
    time = np.arange(len(m_eff))
    mask = (time >= t_min) & (time <= t_max)
    values = m_eff[mask]
    return np.mean(values), np.std(values) / np.sqrt(len(values))

def squared_momentum(mom_str):
    px, py, pz = map(int, mom_str.split())
    return px**2 + py**2 + pz**2

# ==== XML Parsing ====
tree = ET.parse(input_file)
root = tree.getroot()
mesons_path = f".//Wilson_hadron_measurements/elem/{target_sink_type}"
mesons_elem = root.find(mesons_path)

energies = []
momentum_sq = []

if mesons_elem is None:
    print(f"Error: Could not find path '{mesons_path}'")
    exit(1)

for meson in mesons_elem.findall("elem"):
    gamma_val = meson.find("gamma_value")
    if gamma_val is None or gamma_val.text.strip() != target_gamma:
        continue

    for mom in meson.find("momenta").findall("elem"):
        sink_mom = mom.find("sink_mom")
        if sink_mom is None:
            continue

        mom_str = sink_mom.text.strip()
        if mom_str not in momenta_to_check:
            continue

        corr = parse_correlator_data(mom)
        eff_mass = compute_effective_mass(np.abs(corr))
        E, E_err = fit_plateau(eff_mass, *plateau_range)

        p2 = squared_momentum(mom_str)
        momentum_sq.append(p2)
        energies.append((E, E_err))

# ==== Plot Dispersion Relation ====
p2_arr = np.array(momentum_sq)
E_arr = np.array([e[0] for e in energies])
E_err = np.array([e[1] for e in energies])

plt.errorbar(p2_arr, E_arr**2, yerr=2*E_arr*E_err, fmt='o', capsize=4, label="Lattice data")
plt.plot(p2_arr, (E_arr[0]**2 + p2_arr), '--', label="Continuum $E^2 = m^2 + p^2$")

plt.xlabel(r"$|\vec{p}|^2$ (lattice units)")
plt.ylabel(r"$E(\vec{p})^2$")
plt.title("Meson Dispersion Relation")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
