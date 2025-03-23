import xml.etree.ElementTree as ET

# ==== Configuration ====
sink_type = "Point_Shell_Wilson_Mesons"  # e.g. Shell_Shell_Wilson_Mesons, Point_Shell_Wilson_Mesons
target_gamma = "15"
target_momentum = "1 0 0"
input_file = "hadspec.dat.xml"
# =======================

# Load and parse the XML
tree = ET.parse(input_file)
root = tree.getroot()

# Navigate to the specified sink type
mesons_path = f".//Wilson_hadron_measurements/elem/{sink_type}"
mesons_elem = root.find(mesons_path)

if mesons_elem is None:
    print(f"Error: Could not find path '{mesons_path}'")
    exit(1)

found = False

# Loop through gamma structures
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
                    re = point.find("re").text.strip()
                    im = point.find("im").text.strip()
                    print(f"{re} {im}")
                found = True
                break
        if found:
            break

if not found:
    print("No matching correlator found.")
