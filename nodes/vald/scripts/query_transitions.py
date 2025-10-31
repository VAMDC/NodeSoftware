#!/usr/bin/env python3
import sys
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote

if len(sys.argv) != 4:
    print("Usage: query_transitions.py <inchikey> <wavelength_min> <wavelength_max>", file=sys.stderr)
    sys.exit(1)

inchikey = sys.argv[1]
wl_min = sys.argv[2]
wl_max = sys.argv[3]

query = f"select * where Inchikey = '{inchikey}' and radtranswavelength < {wl_max} and radtranswavelength > {wl_min}"
url = f"https://vald.astro.uu.se/vamdc-atoms/tap/sync?QUERY={quote(query)}"

print(f"Querying: {query}", file=sys.stderr)
print(f"URL: {url}", file=sys.stderr)

try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching data: {e}", file=sys.stderr)
    sys.exit(1)

print(f"Response size: {len(response.content)} bytes", file=sys.stderr)

try:
    root = ET.fromstring(response.content)
except ET.ParseError as e:
    print(f"Error parsing XML: {e}", file=sys.stderr)
    sys.exit(1)

ns = {
    'xsams': 'http://vamdc.org/xml/xsams/1.0',
}

def find_namespace(root):
    for prefix, uri in root.nsmap.items() if hasattr(root, 'nsmap') else {}:
        if 'xsams' in uri.lower():
            return uri
    tag = root.tag
    if '}' in tag:
        return tag.split('}')[0].strip('{')
    return None

if root.tag.startswith('{'):
    xsams_ns = root.tag.split('}')[0].strip('{')
    ns['xsams'] = xsams_ns
    print(f"Detected namespace: {xsams_ns}", file=sys.stderr)

radiative_transitions = []

for trans in root.findall('.//xsams:RadiativeTransition', ns):
    trans_id = trans.get('{' + xsams_ns + '}' + 'id') if xsams_ns else trans.get('id')

    wavelength_elem = trans.find('.//xsams:Wavelength/xsams:Value', ns)
    wavelength = wavelength_elem.text if wavelength_elem is not None else None
    wavelength_unit = wavelength_elem.get('units') if wavelength_elem is not None else None

    upper_state_ref = trans.find('.//xsams:UpperStateRef', ns)
    lower_state_ref = trans.find('.//xsams:LowerStateRef', ns)

    upper_id = upper_state_ref.text if upper_state_ref is not None else None
    lower_id = lower_state_ref.text if lower_state_ref is not None else None

    probability_elem = trans.find('.//xsams:TransitionProbabilityA/xsams:Value', ns)
    log_gf_elem = trans.find('.//xsams:OscillatorStrength/xsams:Value', ns)

    probability = probability_elem.text if probability_elem is not None else None
    log_gf = log_gf_elem.text if log_gf_elem is not None else None

    radiative_transitions.append({
        'id': trans_id,
        'wavelength': wavelength,
        'wavelength_unit': wavelength_unit,
        'upper_state': upper_id,
        'lower_state': lower_id,
        'probability_a': probability,
        'log_gf': log_gf,
    })

print(f"\nFound {len(radiative_transitions)} radiative transitions", file=sys.stderr)

print("\nParsed transitions:")
print(f"{'ID':<15} {'Wavelength':>12} {'Unit':<6} {'Upper':<15} {'Lower':<15} {'A':>12} {'log(gf)':>12}")
print("-" * 110)

for trans in radiative_transitions[:20]:
    wl_str = trans['wavelength'][:10] if trans['wavelength'] else 'N/A'
    unit_str = trans['wavelength_unit'][:6] if trans['wavelength_unit'] else ''
    upper_str = (trans['upper_state'][:15] if trans['upper_state'] else 'N/A')
    lower_str = (trans['lower_state'][:15] if trans['lower_state'] else 'N/A')
    prob_str = (trans['probability_a'][:12] if trans['probability_a'] else 'N/A')
    gf_str = (trans['log_gf'][:12] if trans['log_gf'] else 'N/A')

    trans_id = (trans['id'][:15] if trans['id'] else 'N/A')

    print(f"{trans_id:<15} {wl_str:>12} {unit_str:<6} {upper_str:<15} {lower_str:<15} {prob_str:>12} {gf_str:>12}")

if len(radiative_transitions) > 20:
    print(f"... and {len(radiative_transitions) - 20} more")

print("\n" + "=" * 110)
print("\n# PLACEHOLDER: Compare with ground truth")
print("# TODO: Load ground truth data and compare")
print("# Expected format: dict with transition IDs or (upper, lower) tuples as keys")
print("# Comparison metrics: wavelength difference, log(gf) difference, missing transitions")

print(f"\nTotal transitions retrieved: {len(radiative_transitions)}")
