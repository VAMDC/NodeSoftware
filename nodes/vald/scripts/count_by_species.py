#!/usr/bin/env python3
import csv
import requests
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

species_data = {}
with open('VALD_list_of_species.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip version line
    next(reader)  # skip header
    for row in reader:
        species_index = int(row[1])
        atom_name = row[2]
        charge = row[3]
        inchikey = row[5]
        num_components = int(row[9])
        z_number = int(row[10])

        if num_components == 1 and z_number <= 54:
            species_data[species_index] = {
                'atom': atom_name,
                'charge': charge,
                'inchikey': inchikey,
                'z': z_number
            }

transitions_by_species = {}
with open('trans_by_species.dat', 'r') as f:
    for line in f:
        parts = line.strip().split()
        species_index = int(parts[0]) + 1
        num_transitions = int(parts[1])

        if species_index in species_data:
            transitions_by_species[species_index] = num_transitions

def get_vamdc_count_by_inchikey(inchikey):
    url = f"https://vald.astro.uu.se/vamdc-atoms/tap/sync?LANG=VSS2&REQUEST=doQuery&FORMAT=XSAMS&QUERY=select+*+where+((InchiKey+%3D+%27{inchikey}%27))"
    try:
        response = requests.head(url, timeout=30)
        count = response.headers.get('vamdc-count-radiative')
        return int(count) if count else None
    except Exception as e:
        return None

def process_species(species_index):
    data = species_data[species_index]
    my_count = transitions_by_species[species_index]
    vamdc_count = get_vamdc_count_by_inchikey(data['inchikey'])
    return species_index, data, my_count, vamdc_count

print("Querying VAMDC API for each species...", file=sys.stderr)
print(f"{'Species':>7} {'Atom':<6} {'Charge':<7} {'trans.dat':>10} {'VAMDC API':>10} {'Diff':>10}")
print("-" * 65)

mismatches = []
total_species = len(transitions_by_species)
completed = 0
results_buffer = []

BATCH_SIZE = 20

with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
    futures = {executor.submit(process_species, idx): idx for idx in sorted(transitions_by_species.keys())}

    for future in as_completed(futures):
        completed += 1
        species_index, data, my_count, vamdc_count = future.result()

        results_buffer.append((species_index, data, my_count, vamdc_count))

        if completed % 10 == 0:
            print(f"  ... processed {completed}/{total_species} species", file=sys.stderr)

results_buffer.sort(key=lambda x: x[0])

for species_index, data, my_count, vamdc_count in results_buffer:
    if vamdc_count is not None:
        diff = my_count - vamdc_count

        if diff != 0:
            mismatches.append((species_index, data['atom'], data['charge'], my_count, vamdc_count, diff))

        status = "" if diff == 0 else " *"
        print(f"{species_index:>7} {data['atom']:<6} {data['charge']:<7} {my_count:>10} {vamdc_count:>10} {diff:>10}{status}")
    else:
        print(f"{species_index:>7} {data['atom']:<6} {data['charge']:<7} {my_count:>10} {'ERROR':>10} {'':>10}")

print("\n" + "=" * 65)
if mismatches:
    print(f"\n{len(mismatches)} species with differences:")
    for species_index, atom, charge, my_count, vamdc_count, diff in mismatches[:20]:
        print(f"  Species {species_index} ({atom} {charge}): {my_count} vs {vamdc_count} (diff: {diff})")
    if len(mismatches) > 20:
        print(f"  ... and {len(mismatches) - 20} more")
else:
    print("\nAll counts match!")
