#!/usr/bin/env python3
import csv
import requests
import time
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

species_to_atom = {}
species_to_z = {}
with open('VALD_list_of_species.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip version line
    next(reader)  # skip header
    for row in reader:
        species_index = int(row[1])  # Index column
        atom_name = row[2]  # Name column
        num_components = int(row[9])  # Num. comp. column
        z_number = int(row[10])  # N1 column (atomic number)
        species_to_atom[species_index] = atom_name
        if num_components == 1:  # only count atomic species
            species_to_z[species_index] = z_number

transitions_by_atom = defaultdict(int)
transitions_by_z = defaultdict(int)

with open('trans_by_species.dat', 'r') as f:
    for line in f:
        parts = line.strip().split()
        species_index = int(parts[0]) + 1
        num_transitions = int(parts[1])

        if species_index in species_to_z:
            z = species_to_z[species_index]
            if z <= 54:  # only up to Xenon
                atom = species_to_atom[species_index]
                transitions_by_atom[atom] += num_transitions
                transitions_by_z[z] += num_transitions

z_to_symbol = {}
for species_index, z in species_to_z.items():
    if z <= 54:
        symbol = species_to_atom[species_index]
        if z not in z_to_symbol:
            z_to_symbol[z] = symbol

def get_vamdc_count(symbol):
    url = f"https://vald.astro.uu.se/vamdc-atoms/tap/sync?LANG=VSS2&REQUEST=doQuery&FORMAT=XSAMS&QUERY=select+*+where+((AtomSymbol+%3D+%27{symbol}%27))"
    try:
        response = requests.head(url, timeout=30)
        count = response.headers.get('vamdc-count-radiative')
        return int(count) if count else None
    except Exception as e:
        print(f"Error fetching {symbol}: {e}", file=sys.stderr)
        return None

def process_element(z):
    symbol = z_to_symbol.get(z)
    if not symbol:
        return None
    my_count = transitions_by_z.get(z, 0)
    vamdc_count = get_vamdc_count(symbol)
    return z, symbol, my_count, vamdc_count

print("Querying VAMDC API for each element...", file=sys.stderr)
print(f"{'Z':>3} {'Symbol':<6} {'trans_by_species':>16} {'VAMDC API':>16} {'Difference':>12}")
print("-" * 65)

vamdc_counts = {}
mismatches = []
results_buffer = []

BATCH_SIZE = 20

with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
    futures = {executor.submit(process_element, z): z for z in sorted(transitions_by_z.keys())}

    for future in as_completed(futures):
        result = future.result()
        if result:
            results_buffer.append(result)

results_buffer.sort(key=lambda x: x[0])

for z, symbol, my_count, vamdc_count in results_buffer:
    if vamdc_count is not None:
        vamdc_counts[z] = vamdc_count
        diff = my_count - vamdc_count

        if diff != 0:
            mismatches.append((z, symbol, my_count, vamdc_count, diff))

        print(f"{z:>3} {symbol:<6} {my_count:>16} {vamdc_count:>16} {diff:>12}")
    else:
        print(f"{z:>3} {symbol:<6} {my_count:>16} {'ERROR':>16} {'':>12}")

if mismatches:
    print(f"\n{len(mismatches)} elements with differences:")
    for z, symbol, my_count, vamdc_count, diff in mismatches[:10]:
        print(f"  {symbol}: {my_count} vs {vamdc_count} (diff: {diff})")
else:
    print("\nAll counts match!")
