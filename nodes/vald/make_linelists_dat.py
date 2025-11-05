#!/usr/bin/env python3
"""
Create linelists.dat from default.cfg and VALD3linelists.txt
"""
import os
import re

METHOD_TYPE_MAP = {
    'exp': 0,   # experiment
    'obs': 1,   # observed
    'emp': 2,   # empirical
    'pred': 3,  # theory (predicted)
    'calc': 4,  # semiempirical (calculated)
    'mix': 5,   # compilation
    'comp': 5   # compilation (alternative name)
}

def parse_vald3linelists(filename):
    """Parse VALD3linelists.txt and return dict of filename -> type"""
    linelist_types = {}

    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip()
            # Look for table rows (wiki format with ||)
            if line.startswith('||') and not line.startswith('||\'\'\''):
                # Split by || but preserve empty columns
                parts = line.split('||')[1:]  # Skip first empty element before first ||
                if len(parts) >= 3:
                    # First column is filename, third is type
                    filename_col = parts[0].strip()
                    # Remove wiki formatting characters (! prevents auto-linking)
                    filename_col = filename_col.lstrip('!')
                    type_col = parts[2].strip()
                    # Only store if filename is not empty
                    if filename_col:
                        linelist_types[filename_col] = type_col

    return linelist_types

def parse_default_cfg(filename, linelist_types):
    """Parse default.cfg and generate output rows"""
    rows = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Skip first 3 header lines
    for line in lines[3:]:
        line = line.strip()
        if not line:
            continue

        # Remove all leading semicolons (there can be ;; for extra commenting)
        line = line.lstrip(';').strip()

        # Skip if nothing left after stripping semicolons
        if not line:
            continue

        # Parse the line - columns are separated by commas
        # First column is the path in quotes
        match = re.match(r"'([^']+)'\s*,\s*(\d+)", line)
        if match:
            path = match.group(1)
            col2 = match.group(2)

            # Get basename
            basename = os.path.basename(path)

            # Look up type in linelist_types
            type_str = linelist_types.get(basename, '')

            # Map to integer
            type_int = METHOD_TYPE_MAP.get(type_str, -1)

            rows.append((basename, col2, type_str, type_int))

    return rows

def main():
    # Parse VALD3linelists.txt
    linelist_types = parse_vald3linelists('VALD3linelists.txt')

    # Parse default.cfg
    rows = parse_default_cfg('default.cfg', linelist_types)

    # Write output
    with open('linelists.dat', 'w') as f:
        for basename, col2, type_str, type_int in rows:
            f.write(f"{basename}\t{col2}\t{type_str}\t{type_int}\n")

    print(f"Generated linelists.dat with {len(rows)} rows")

if __name__ == '__main__':
    main()
