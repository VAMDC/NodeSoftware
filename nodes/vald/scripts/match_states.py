#!/usr/bin/env python3
import sqlite3

def match_states():
    conn_ab = sqlite3.connect('AB.db')
    conn_vald = sqlite3.connect('vald_dev.sqlite')

    cursor_ab = conn_ab.cursor()
    cursor_vald = conn_vald.cursor()

    cursor_ab.execute("SELECT SPEID, J, E FROM AB")
    ab_rows = cursor_ab.fetchall()

    total_rows = len(ab_rows)
    single_match = 0
    no_match = 0
    multiple_match = 0
    multiple_match_whitespace_only = 0

    no_match_by_species = {}

    energy_tolerance = 1.0

    def normalize_term(term):
        if term is None:
            return None
        return ' '.join(term.split())

    print(f"Processing {total_rows} rows from AB.db...\n")

    for ab_row in ab_rows:
        species_id, j_value, energy = ab_row

        query = """
            SELECT * FROM states
            WHERE species_id = ?
            AND J = ?
            AND ABS(energy - ?) <= ?
        """
        cursor_vald.execute(query, (species_id, j_value, energy, energy_tolerance))
        matches = cursor_vald.fetchall()

        match_count = len(matches)
        if match_count == 0:
            no_match += 1
            if species_id not in no_match_by_species:
                no_match_by_species[species_id] = 0
            no_match_by_species[species_id] += 1
        elif match_count == 1:
            single_match += 1
        else:
            col_names = [desc[0] for desc in cursor_vald.description]
            match_dicts = [dict(zip(col_names, match)) for match in matches]

            differing_fields = {}
            for col in col_names:
                if col in ['L', 'S', 'P']:
                    continue
                if col == 'term_desc':
                    normalized_values = [normalize_term(m[col]) for m in match_dicts]
                    if len(set(str(v) for v in normalized_values)) > 1:
                        differing_fields[col] = [m[col] for m in match_dicts]
                else:
                    values = [m[col] for m in match_dicts]
                    if len(set(str(v) for v in values)) > 1:
                        differing_fields[col] = values

            significant_diffs = {k for k in differing_fields.keys()
                                if k not in ['id', 'energy', 'energy_scaled']}

            if not significant_diffs:
                multiple_match_whitespace_only += 1
            else:
                multiple_match += 1
                print(f"\nMultiple matches for AB.db row: SPEID={species_id}, J={j_value}, E={energy}")

                for i, match_dict in enumerate(match_dicts):
                    diff_only = {k: match_dict[k] for k in differing_fields.keys()}
                    print(f"  Match {i+1}: {diff_only}")

    conn_ab.close()
    conn_vald.close()

    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"{'='*60}")
    print(f"Total rows: {total_rows}")
    print(f"Single match: {single_match} ({100*single_match/total_rows:.1f}%)")
    print(f"No match: {no_match} ({100*no_match/total_rows:.1f}%)")
    print(f"Multiple matches (insignificant - id/energy/term-whitespace/L/S/P only): {multiple_match_whitespace_only} ({100*multiple_match_whitespace_only/total_rows:.1f}%)")
    print(f"Multiple matches (significant differences): {multiple_match} ({100*multiple_match/total_rows:.1f}%)")

    if no_match_by_species:
        print(f"\n{'='*60}")
        print(f"No matches breakdown by species ID:")
        print(f"{'='*60}")
        sorted_species = sorted(no_match_by_species.items(), key=lambda x: x[1], reverse=True)
        for species_id, count in sorted_species:
            print(f"SPEID {species_id:5d}: {count:4d} rows ({100*count/no_match:.1f}% of no-matches)")
        print(f"\nTotal species with no matches: {len(no_match_by_species)}")

if __name__ == "__main__":
    match_states()
