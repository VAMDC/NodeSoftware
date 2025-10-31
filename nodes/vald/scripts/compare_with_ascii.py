#!/usr/bin/env python3
import sys
import csv
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote

if len(sys.argv) != 5:
    print("Usage: compare_with_ascii.py <inchikey> <wavelength_min> <wavelength_max> <ascii_file>", file=sys.stderr)
    sys.exit(1)

inchikey = sys.argv[1]
wl_min = float(sys.argv[2])
wl_max = float(sys.argv[3])
ascii_file = sys.argv[4]

species_lookup = {}
with open('VALD_list_of_species.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip version
    next(reader)  # skip header
    for row in reader:
        species_id = int(row[1])
        species_inchikey = row[5]
        species_name = row[2]
        species_charge = row[3]
        species_lookup[species_id] = {
            'inchikey': species_inchikey,
            'name': species_name,
            'charge': species_charge
        }

target_species_id = None
for sid, data in species_lookup.items():
    if data['inchikey'] == inchikey:
        target_species_id = sid
        break

if target_species_id is None:
    print(f"Error: InChIKey {inchikey} not found in species list", file=sys.stderr)
    sys.exit(1)

print(f"Found species ID {target_species_id} for InChIKey {inchikey}", file=sys.stderr)
print(f"Species: {species_lookup[target_species_id]['name']} {species_lookup[target_species_id]['charge']}", file=sys.stderr)

ascii_transitions = []

with open(ascii_file, 'r') as f:
    lines = f.readlines()

skip_lines = 2
line_idx = skip_lines

while line_idx < len(lines):
    data_line = lines[line_idx]

    if len(data_line) < 100:
        line_idx += 1
        continue

    try:
        wl_center = float(data_line[0:15].strip())
        wl_out = float(data_line[15:30].strip())
        species_code = int(data_line[30:36].strip())
        log_gf = float(data_line[36:44].strip())
        e_low = float(data_line[44:58].strip())
        j_low = float(data_line[58:64].strip())
        e_up = float(data_line[64:78].strip())
        j_up = float(data_line[78:84].strip())
        lande_low = float(data_line[84:91].strip())
        lande_up = float(data_line[91:98].strip())
        lande_mean = float(data_line[98:105].strip())
        rad_damp = float(data_line[105:112].strip())
        stark_damp = float(data_line[112:119].strip())
        waals_damp = float(data_line[119:127].strip())

        term_low = data_line[127:213].strip() if len(data_line) > 213 else ""
        term_up = data_line[213:299].strip() if len(data_line) > 299 else ""

    except (ValueError, IndexError) as e:
        line_idx += 2
        continue

    if species_code == target_species_id and wl_min < wl_out < wl_max:
        ascii_transitions.append({
            'wl_center': wl_center,
            'wl_out': wl_out,
            'species_code': species_code,
            'log_gf': log_gf,
            'e_low': e_low,
            'j_low': j_low,
            'e_up': e_up,
            'j_up': j_up,
            'lande_low': lande_low,
            'lande_up': lande_up,
            'lande_mean': lande_mean,
            'rad_damp': rad_damp,
            'stark_damp': stark_damp,
            'waals_damp': waals_damp,
            'term_low': term_low,
            'term_up': term_up,
        })

    line_idx += 2

print(f"Found {len(ascii_transitions)} transitions in ASCII file matching species and wavelength range", file=sys.stderr)

query = f"select * where Inchikey = '{inchikey}' and radtranswavelength < {wl_max} and radtranswavelength > {wl_min}"
url = f"https://vald.astro.uu.se/vamdc-atoms/tap/sync?QUERY={quote(query)}"

print(f"Querying API...", file=sys.stderr)

try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching data: {e}", file=sys.stderr)
    sys.exit(1)

print(f"Response size: {len(response.content)} bytes", file=sys.stderr)

try:
    content = response.content.decode('utf-8')
    content_clean = content
    root = ET.fromstring(content_clean.encode('utf-8'))
except ET.ParseError as e:
    print(f"Error parsing XML: {e}", file=sys.stderr)
    print(f"Attempting to recover by using lenient parser...", file=sys.stderr)
    try:
        from xml.etree.ElementTree import XMLParser
        parser = XMLParser(encoding='utf-8')
        parser.entity.update({'#10': '\n'})
        root = ET.fromstring(response.content, parser=parser)
    except Exception as e2:
        print(f"Recovery failed: {e2}", file=sys.stderr)
        print(f"Trying to fix problematic XML content...", file=sys.stderr)
        import re
        content = response.content.decode('utf-8', errors='ignore')
        content = re.sub(r'<BibTeX>.*?</BibTeX>', '<BibTeX>removed</BibTeX>', content, flags=re.DOTALL)
        content = re.sub(r'<Title>.*?</Title>', '<Title>removed</Title>', content, flags=re.DOTALL)
        content = re.sub(r'<--', '&lt;--', content)
        content = re.sub(r'-->', '--&gt;', content)
        try:
            root = ET.fromstring(content.encode('utf-8'))
            print(f"Successfully recovered XML", file=sys.stderr)
        except Exception as e3:
            print(f"All recovery attempts failed: {e3}", file=sys.stderr)
            sys.exit(1)

ns = {'xsams': 'http://vamdc.org/xml/xsams/1.0'}

if root.tag.startswith('{'):
    xsams_ns = root.tag.split('}')[0].strip('{')
    ns['xsams'] = xsams_ns

states = {}
for state in root.findall('.//xsams:AtomicState', ns):
    state_id = state.get('stateID')

    energy_elem = state.find('.//xsams:AtomicNumericalData/xsams:StateEnergy/xsams:Value', ns)
    if energy_elem is None:
        energy_elem = state.find('.//xsams:StateEnergy/xsams:Value', ns)
    energy = float(energy_elem.text) if energy_elem is not None else None

    j_elem = state.find('.//xsams:AtomicQuantumNumbers/xsams:TotalAngularMomentum', ns)
    if j_elem is None:
        j_elem = state.find('.//xsams:TotalAngularMomentum', ns)
    j_val = float(j_elem.text) if j_elem is not None else None

    lande_elem = state.find('.//xsams:LandeFactor/xsams:Value', ns)
    lande = float(lande_elem.text) if lande_elem is not None else None

    states[state_id] = {
        'energy': energy,
        'j': j_val,
        'lande': lande
    }

xml_transitions = []

for trans in root.findall('.//xsams:RadiativeTransition', ns):
    trans_id = trans.get('id')

    wavelengths = trans.findall('.//xsams:Wavelength', ns)
    wl_ritz = None
    wl_measured = None
    for wl_elem in wavelengths:
        comments_elem = wl_elem.find('xsams:Comments', ns)
        value_elem = wl_elem.find('xsams:Value', ns)
        if value_elem is not None:
            val = float(value_elem.text)
            comments_text = comments_elem.text if comments_elem is not None else ''
            if 'RITZ' in comments_text and 'non-RITZ' not in comments_text:
                wl_ritz = val
            elif 'non-RITZ' in comments_text:
                wl_measured = val
            elif wl_ritz is None:
                wl_ritz = val

    wavelength = wl_ritz if wl_ritz else wl_measured

    upper_state_ref = trans.find('.//xsams:UpperStateRef', ns)
    lower_state_ref = trans.find('.//xsams:LowerStateRef', ns)

    upper_id = upper_state_ref.text if upper_state_ref is not None else None
    lower_id = lower_state_ref.text if lower_state_ref is not None else None

    log_gf_elem = trans.find('.//xsams:Log10WeightedOscillatorStrength/xsams:Value', ns)
    if log_gf_elem is None:
        log_gf_elem = trans.find('.//xsams:OscillatorStrength/xsams:Value', ns)
    log_gf = float(log_gf_elem.text) if log_gf_elem is not None else None

    rad_damp = None
    stark_damp = None
    waals_damp = None

    for broadening in trans.findall('.//xsams:Broadening', ns):
        name = broadening.get('name')
        comments_elem = broadening.find('.//xsams:Comments', ns)
        comments = comments_elem.text if comments_elem is not None else ''

        param = broadening.find('.//xsams:LineshapeParameter/xsams:Value', ns)
        if param is not None:
            val = float(param.text)
            if 'natural' in name.lower() or 'Natural' in comments:
                rad_damp = val
            elif 'stark' in name.lower() or 'Stark' in comments:
                stark_damp = val
            elif 'waals' in name.lower() or 'pressure-neutral' in name.lower():
                waals_damp = val

    xml_transitions.append({
        'id': trans_id,
        'wavelength': wavelength,
        'wl_ritz': wl_ritz,
        'wl_measured': wl_measured,
        'upper_state_id': upper_id,
        'lower_state_id': lower_id,
        'log_gf': log_gf,
        'upper_state': states.get(upper_id, {}),
        'lower_state': states.get(lower_id, {}),
        'rad_damp': rad_damp,
        'stark_damp': stark_damp,
        'waals_damp': waals_damp,
    })

print(f"Found {len(xml_transitions)} transitions in XML", file=sys.stderr)
for i, trans in enumerate(xml_transitions[:3]):
    print(f"  XML transition {i}: WL={trans.get('wavelength')}, wl_ritz={trans.get('wl_ritz')}, wl_measured={trans.get('wl_measured')}", file=sys.stderr)

print("\n" + "="*160)
print("COMPARISON RESULTS - All Fields")
print("="*160)

mismatches = []
matched_count = 0
field_mismatches = {
    'wavelength': 0, 'log_gf': 0, 'e_low': 0, 'e_up': 0,
    'j_low': 0, 'j_up': 0, 'lande_low': 0, 'lande_up': 0,
    'rad_damp': 0, 'stark_damp': 0, 'waals_damp': 0
}

for ascii_trans in ascii_transitions:
    best_match = None
    best_diff = float('inf')

    for xml_trans in xml_transitions:
        if xml_trans['wavelength'] is None:
            continue
        wl_diff = abs(xml_trans['wavelength'] - ascii_trans['wl_out'])
        if wl_diff < best_diff:
            best_diff = wl_diff
            best_match = xml_trans

    if best_match and best_diff < 0.01:
        matched_count += 1

        wl_ascii = ascii_trans['wl_out']
        wl_xml = best_match['wavelength']
        wl_diff = wl_xml - wl_ascii if wl_xml else float('nan')

        gf_ascii = ascii_trans['log_gf']
        gf_xml = best_match['log_gf']
        gf_diff = gf_xml - gf_ascii if gf_xml is not None else float('nan')

        e_low_ascii = ascii_trans['e_low']
        e_low_xml = best_match['lower_state'].get('energy')
        e_low_diff = (e_low_xml - e_low_ascii) if e_low_xml is not None else float('nan')

        e_up_ascii = ascii_trans['e_up']
        e_up_xml = best_match['upper_state'].get('energy')
        e_up_diff = (e_up_xml - e_up_ascii) if e_up_xml is not None else float('nan')

        j_low_ascii = ascii_trans['j_low']
        j_low_xml = best_match['lower_state'].get('j')
        j_low_diff = (j_low_xml - j_low_ascii) if j_low_xml is not None else float('nan')

        j_up_ascii = ascii_trans['j_up']
        j_up_xml = best_match['upper_state'].get('j')
        j_up_diff = (j_up_xml - j_up_ascii) if j_up_xml is not None else float('nan')

        lande_low_ascii = ascii_trans['lande_low']
        lande_low_xml = best_match['lower_state'].get('lande')
        lande_low_diff = (lande_low_xml - lande_low_ascii) if lande_low_xml is not None else float('nan')

        lande_up_ascii = ascii_trans['lande_up']
        lande_up_xml = best_match['upper_state'].get('lande')
        lande_up_diff = (lande_up_xml - lande_up_ascii) if lande_up_xml is not None else float('nan')

        rad_ascii = ascii_trans['rad_damp']
        rad_xml = best_match['rad_damp']
        rad_diff = (rad_xml - rad_ascii) if rad_xml is not None else float('nan')

        stark_ascii = ascii_trans['stark_damp']
        stark_xml = best_match['stark_damp']
        stark_diff = (stark_xml - stark_ascii) if stark_xml is not None else float('nan')

        waals_ascii = ascii_trans['waals_damp']
        waals_xml = best_match['waals_damp']
        waals_diff = (waals_xml - waals_ascii) if waals_xml is not None else float('nan')

        has_mismatch = False
        if wl_xml and abs(wl_diff) > 0.001:
            has_mismatch = True
            field_mismatches['wavelength'] += 1
        if gf_xml is not None and abs(gf_diff) > 0.01:
            has_mismatch = True
            field_mismatches['log_gf'] += 1
        if e_low_xml and abs(e_low_diff) > 0.1:
            has_mismatch = True
            field_mismatches['e_low'] += 1
        if e_up_xml and abs(e_up_diff) > 0.1:
            has_mismatch = True
            field_mismatches['e_up'] += 1
        if j_low_xml is not None and abs(j_low_diff) > 0.01:
            has_mismatch = True
            field_mismatches['j_low'] += 1
        if j_up_xml is not None and abs(j_up_diff) > 0.01:
            has_mismatch = True
            field_mismatches['j_up'] += 1
        if lande_low_xml is not None and abs(lande_low_diff) > 0.01:
            has_mismatch = True
            field_mismatches['lande_low'] += 1
        if lande_up_xml is not None and abs(lande_up_diff) > 0.01:
            has_mismatch = True
            field_mismatches['lande_up'] += 1
        if rad_xml is not None and abs(rad_diff) > 0.01:
            has_mismatch = True
            field_mismatches['rad_damp'] += 1
        if stark_xml is not None and abs(stark_diff) > 0.01:
            has_mismatch = True
            field_mismatches['stark_damp'] += 1
        if waals_xml is not None and abs(waals_diff) > 0.01:
            has_mismatch = True
            field_mismatches['waals_damp'] += 1

        if has_mismatch:
            mismatches.append((ascii_trans, best_match))

        status = " *" if has_mismatch else ""

        print(f"Transition WL={wl_ascii:.5f} {status}")
        print(f"  WL:      ASCII={wl_ascii:12.5f}  XML={wl_xml if wl_xml else 'N/A':>12}  Δ={wl_diff if wl_xml else 'N/A':>8}")
        print(f"  log(gf): ASCII={gf_ascii:12.3f}  XML={gf_xml if gf_xml is not None else 'N/A':>12}  Δ={gf_diff if gf_xml is not None else 'N/A':>8}")
        print(f"  E_low:   ASCII={e_low_ascii:12.2f}  XML={e_low_xml if e_low_xml else 'N/A':>12}  Δ={e_low_diff if e_low_xml else 'N/A':>8}")
        print(f"  E_up:    ASCII={e_up_ascii:12.2f}  XML={e_up_xml if e_up_xml else 'N/A':>12}  Δ={e_up_diff if e_up_xml else 'N/A':>8}")
        print(f"  J_low:   ASCII={j_low_ascii:12.1f}  XML={j_low_xml if j_low_xml is not None else 'N/A':>12}  Δ={j_low_diff if j_low_xml is not None else 'N/A':>8}")
        print(f"  J_up:    ASCII={j_up_ascii:12.1f}  XML={j_up_xml if j_up_xml is not None else 'N/A':>12}  Δ={j_up_diff if j_up_xml is not None else 'N/A':>8}")
        print(f"  g_low:   ASCII={lande_low_ascii:12.2f}  XML={lande_low_xml if lande_low_xml is not None else 'N/A':>12}  Δ={lande_low_diff if lande_low_xml is not None else 'N/A':>8}")
        print(f"  g_up:    ASCII={lande_up_ascii:12.2f}  XML={lande_up_xml if lande_up_xml is not None else 'N/A':>12}  Δ={lande_up_diff if lande_up_xml is not None else 'N/A':>8}")
        print(f"  Rad:     ASCII={rad_ascii:12.3f}  XML={rad_xml if rad_xml is not None else 'N/A':>12}  Δ={rad_diff if rad_xml is not None else 'N/A':>8}")
        print(f"  Stark:   ASCII={stark_ascii:12.3f}  XML={stark_xml if stark_xml is not None else 'N/A':>12}  Δ={stark_diff if stark_xml is not None else 'N/A':>8}")
        print(f"  Waals:   ASCII={waals_ascii:12.3f}  XML={waals_xml if waals_xml is not None else 'N/A':>12}  Δ={waals_diff if waals_xml is not None else 'N/A':>8}")
        print()

print("\n" + "="*120)
print(f"Summary:")
print(f"  ASCII transitions: {len(ascii_transitions)}")
print(f"  XML transitions: {len(xml_transitions)}")
print(f"  Matched: {matched_count}")
print(f"  Transitions with any mismatch: {len(mismatches)}")
print(f"  Unmatched: {len(ascii_transitions) - matched_count}")
print(f"\nField-specific mismatches:")
for field, count in field_mismatches.items():
    print(f"  {field:15s}: {count:3d} mismatches")
print("="*120)
