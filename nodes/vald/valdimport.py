#!/usr/bin/env python
"""
VALD Data Import System

Standalone script that can be used directly or imported as Django management commands.

Usage as standalone:
    python valdimport.py import-states --file=vald.dat
    python valdimport.py import-transitions --file=vald.dat

Usage via Django:
    python manage.py import_states --file=vald.dat
    python manage.py import_transitions --file=vald.dat
"""

import sys
import gzip
from dataclasses import dataclass
from typing import Callable, Optional, Iterator, TextIO
from io import StringIO
import csv

# =============================================================================
# VALD FORMAT DEFINITIONS
# =============================================================================

@dataclass
class FieldDef:
    """Definition of a fixed-width field in VALD format"""
    name: str
    start: int
    end: int
    converter: Callable[[str], any] = str.strip
    null_values: tuple = ('', 'X')
    description: str = ''

    def parse(self, line: str):
        """Extract and convert field from line"""
        value = line[self.start:self.end].strip()
        if value in self.null_values:
            return None
        try:
            return self.converter(value)
        except (ValueError, IndexError) as e:
            raise ValueError(
                f"Failed to parse {self.name} at {self.start}:{self.end}: {e}"
            )


def parse_wave(line: str) -> float:
    """Get measured wavelength if available, otherwise RITZ"""
    measured = line[15:30].strip()
    ritz = line[0:15].strip()
    return float(measured if measured != ritz else ritz)


VALD_FIELDS = [
    # Format (from presformat5.f): 2F15.5,I6,F8.3,2(F14.4,F6.1),3F7.2,2F7.3,F8.3,A2,A86,A2,A86,1X,A1,A7,1X,A16,9I4
    # Positions based on FORTRAN fixed format

    # === Wavelengths ===
    FieldDef('wave_ritz', 0, 15, float,
             description="Vacuum wavelength from Ritz (Å)"),
    FieldDef('wave_measured', 15, 30, float,
             description="Measured vacuum wavelength (Å)"),
    FieldDef('wave', 0, 30, parse_wave,
             description="Best wavelength (measured or RITZ)"),

    # === Identifiers ===
    FieldDef('species_id', 30, 36, int),

    # === Transition Properties ===
    FieldDef('loggf', 36, 44, float),

    # === Lower State ===
    # F14.4 = positions 44-58, F6.1 = positions 58-64
    FieldDef('lower_energy', 44, 58, float, description="Energy (cm-1)"),
    FieldDef('lower_j', 58, 64, float, null_values=('', 'X')),

    # === Upper State ===
    # F14.4 = positions 64-78, F6.1 = positions 78-84
    FieldDef('upper_energy', 64, 78, float, description="Energy (cm-1)"),
    FieldDef('upper_j', 78, 84, float, null_values=('', 'X')),

    # === Lande factors ===
    # 3F7.2 = lower_lande (84-91), upper_lande (91-98), mean_lande (98-105)
    FieldDef('lower_lande', 84, 91, float, null_values=('', '99.00', 'X')),
    FieldDef('upper_lande', 91, 98, float, null_values=('', '99.00', 'X')),
    FieldDef('mean_lande', 98, 105, float, null_values=('', '99.00', 'X')),

    # === Broadening ===
    # 2F7.3 = gammarad (105-112), gammastark (112-119)
    FieldDef('gammarad', 105, 112, float, null_values=('0.0', '', 'X')),
    FieldDef('gammastark', 112, 119, float, null_values=('0.000', '', 'X')),
    FieldDef('gammawaals', 119, 127, float, null_values=('0.0', '', 'X')),

    # === Term descriptions ===
    # A2,A86,A2,A86 = tflg_L, term_L, tflg_U, term_U
    FieldDef('lower_term_flag', 127, 129, str.strip),
    FieldDef('lower_term', 129, 215, str.strip),
    FieldDef('upper_term_flag', 215, 217, str.strip),
    FieldDef('upper_term', 217, 303, str.strip),

    # === Accuracy ===
    # 1X,A1,A7 = skip, accurflag, accuracy
    FieldDef('accurflag', 304, 305, str.strip),
    FieldDef('accuracy', 305, 312, str.strip),

    # === References and metadata ===
    # A16,9I4 = comment, then 9 reference indices
    FieldDef('comment', 312, 328, str.strip),
]


def parse_vald_line(line: str) -> dict:
    """Parse a VALD line using field definitions"""
    return {
        field.name: field.parse(line)
        for field in VALD_FIELDS
    }


# =============================================================================
# STREAMING PARSER
# =============================================================================

def parse_vald_stream(input_stream: TextIO,
                      skip_header_lines: int = 2) -> Iterator[dict]:
    """
    Generator that yields parsed VALD records.
    Works with files, stdin, gzipped files, or shell pipes.
    VALD format has 2 lines per record: data line + reference line.
    """

    # Skip header lines
    for _ in range(skip_header_lines):
        next(input_stream, None)

    for line_num, line in enumerate(input_stream, start=1):
        line = line.rstrip('\n')

        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue

        # Skip reference lines (start with lowercase, e.g., "wl:", "gf:", etc.)
        if line and line[0].islower():
            continue

        # Skip error lines
        if 'Unknown' in line:
            continue

        try:
            yield parse_vald_line(line)
        except Exception as e:
            print(f"Warning: Failed to parse line {line_num}: {e}",
                  file=sys.stderr)
            continue


def batch_iterator(iterable: Iterator, batch_size: int = 10000) -> Iterator[list]:
    """Yield batches of items from iterator"""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def open_input(filename: Optional[str] = None) -> TextIO:
    """
    Open input file or stdin.
    Handles gzipped files automatically.
    """
    if filename is None:
        return sys.stdin

    if filename.endswith('.gz'):
        return gzip.open(filename, 'rt')

    return open(filename, 'r')


# =============================================================================
# DATABASE OPERATIONS
# =============================================================================

def bulk_insert_optimized(model, batch: list, batch_size: int = 10000, ignore_conflicts: bool = False):
    """
    Use fastest bulk insert method for each database.

    Performance:
    - PostgreSQL: COPY FROM STDIN (~50k rows/sec)
    - SQLite: executemany (~30k rows/sec)
    - MySQL: bulk_create (~20k rows/sec)
    """
    from django.db import connection

    if connection.vendor == 'postgresql':
        # PostgreSQL: Use COPY for maximum speed
        buffer = StringIO()
        writer = csv.writer(buffer, delimiter='\t')

        field_names = [f.name for f in model._meta.fields if not f.primary_key]

        for obj in batch:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

        buffer.seek(0)

        with connection.cursor() as cursor:
            cursor.copy_from(
                buffer,
                model._meta.db_table,
                columns=field_names,
                sep='\t',
                null=''
            )

    elif connection.vendor == 'sqlite':
        # SQLite: Use raw executemany for speed
        field_names = [f.column for f in model._meta.fields if not f.primary_key]
        placeholders = ','.join(['?'] * len(field_names))

        insert_cmd = "INSERT OR IGNORE" if ignore_conflicts else "INSERT"
        sql = f"{insert_cmd} INTO {model._meta.db_table} ({','.join(field_names)}) VALUES ({placeholders})"

        rows = []
        for obj in batch:
            row = []
            for field in model._meta.fields:
                if field.primary_key:
                    continue
                value = getattr(obj, field.attname)
                row.append(value)
            rows.append(row)

        with connection.cursor() as cursor:
            cursor.executemany(sql, rows)

    else:
        # MySQL: Use Django's bulk_create
        model.objects.bulk_create(
            batch,
            batch_size=batch_size,
            ignore_conflicts=ignore_conflicts
        )


# =============================================================================
# STATE CACHE FOR TRANSITION LOOKUPS
# =============================================================================

class StateCache:
    """
    Batch-prefetching cache for state lookups.
    Prefetches states in bulk to minimize database queries.
    """

    def __init__(self, max_size: int = 100000):
        self.cache = {}  # (species, energy, j, term) -> state_id
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def prefetch_states(self, state_keys):
        """
        Prefetch states in batch for given keys using temp table.
        Keys should be tuples of (species_id, energy, j, term_desc).
        """
        from django.db import connection

        uncached = [key for key in state_keys if key not in self.cache]
        if not uncached:
            return

        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TEMP TABLE IF NOT EXISTS temp_state_lookup (
                    species_id INTEGER,
                    energy REAL,
                    j REAL,
                    term_desc TEXT
                )
            """)

            cursor.execute("DELETE FROM temp_state_lookup")

            cursor.executemany(
                "INSERT INTO temp_state_lookup VALUES (?, ?, ?, ?)",
                uncached
            )

            cursor.execute("""
                SELECT s.id, s.species_id, s.energy, s.j, s.term_desc
                FROM states s
                INNER JOIN temp_state_lookup t
                ON s.species_id = t.species_id
                   AND s.energy = t.energy
                   AND (s.j = t.j OR (s.j IS NULL AND t.j IS NULL))
                   AND s.term_desc = t.term_desc
            """)

            for row in cursor.fetchall():
                state_id, species_id, energy, j, term_desc = row
                key = (
                    species_id,
                    float(energy) if energy is not None else None,
                    float(j) if j is not None else None,
                    term_desc
                )
                self.cache[key] = state_id

        if len(self.cache) > self.max_size:
            self.cache.clear()

    def get_state_id(self, species_id, energy, j, term):
        """Get state ID from cache (assumes prefetch_states was called)"""
        key = (species_id, energy, j, term)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        raise ValueError(
            f"State not found in cache: species={species_id}, "
            f"energy={energy}, j={j}, term={term}"
        )

    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0


# =============================================================================
# IMPORT FUNCTIONS
# =============================================================================

def import_states(input_file=None, batch_size=10000, skip_header=2, verbose=True):
    """
    Import states from VALD format (Pass 1)

    Returns: (total_processed, total_inserted)
    """
    try:
        from tqdm import tqdm
        progress_bar = tqdm
    except ImportError:
        # Fallback if tqdm not available
        class DummyBar:
            def __init__(self, *args, **kwargs): pass
            def update(self, n): pass
            def set_postfix(self, d): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass
        progress_bar = DummyBar

    # Import Django models (will fail if not in Django context)
    from node_atom.models import State
    from django.db import transaction, connection

    # Temporarily disable foreign key constraints for import
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")

    input_stream = open_input(input_file)
    records = parse_vald_stream(input_stream, skip_header)

    total_processed = 0
    total_inserted = 0

    with progress_bar(desc="Extracting states", unit=" lines", disable=not verbose) as pbar:
        for batch in batch_iterator(records, batch_size):
            states = []

            for row in batch:
                # Extract lower state
                states.append(State(
                    species_id=row.get('species_id'),
                    energy=row['lower_energy'],
                    j=row['lower_j'],
                    lande=row['lower_lande'],
                    term_desc=row['lower_term'],
                    # TODO: Add remaining state fields
                ))

                # Extract upper state
                states.append(State(
                    species_id=row.get('species_id'),
                    energy=row['upper_energy'],
                    j=row['upper_j'],
                    lande=row['upper_lande'],
                    term_desc=row['upper_term'],
                    # TODO: Add remaining state fields
                ))

            # Bulk insert with deduplication
            with transaction.atomic():
                initial_count = State.objects.count()
                bulk_insert_optimized(State, states, batch_size, ignore_conflicts=True)
                final_count = State.objects.count()
                inserted = final_count - initial_count

            total_processed += len(batch)
            total_inserted += inserted
            pbar.update(len(batch))
            pbar.set_postfix({
                'unique_states': total_inserted,
                'dedup_rate': f'{(1 - total_inserted/(total_processed*2))*100:.1f}%'
            })

    return total_processed, total_inserted


def import_transitions(input_file=None, batch_size=10000, skip_header=2,
                      skip_calc=False, verbose=True):
    """
    Import transitions from VALD format (Pass 2)

    Returns: total_processed
    """
    try:
        from tqdm import tqdm
        progress_bar = tqdm
    except ImportError:
        class DummyBar:
            def __init__(self, *args, **kwargs): pass
            def update(self, n): pass
            def set_postfix(self, d): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass
        progress_bar = DummyBar

    from node_atom.models import State, Transition
    from django.db import transaction, connection

    # Temporarily disable foreign key constraints for import
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")

    input_stream = open_input(input_file)
    state_cache = StateCache()
    records = parse_vald_stream(input_stream, skip_header)

    total_processed = 0

    with progress_bar(desc="Importing transitions", unit=" lines", disable=not verbose) as pbar:
        for batch in batch_iterator(records, batch_size):
            state_keys = set()
            for row in batch:
                state_keys.add((row['species_id'], row['lower_energy'], row['lower_j'], row['lower_term']))
                state_keys.add((row['species_id'], row['upper_energy'], row['upper_j'], row['upper_term']))

            state_cache.prefetch_states(state_keys)

            transitions = []
            for row in batch:
                try:
                    transitions.append(Transition(
                        upstate_id=state_cache.get_state_id(
                            row['species_id'],
                            row['upper_energy'],
                            row['upper_j'],
                            row['upper_term']
                        ),
                        lostate_id=state_cache.get_state_id(
                            row['species_id'],
                            row['lower_energy'],
                            row['lower_j'],
                            row['lower_term']
                        ),
                        species_id=row.get('species_id'),
                        wave=row['wave'],
                        waveritz=row['wave_ritz'],
                        loggf=row['loggf'],
                        gammarad=row.get('gammarad'),
                        gammastark=row.get('gammastark'),
                        gammawaals=row.get('gammawaals'),
                        accurflag=row.get('accurflag'),
                        # wave_linelist_id omitted for now (will handle in separate pass)
                        # TODO: Add remaining transition fields
                    ))
                except ValueError as e:
                    print(f"Warning: Skipping row: {e}", file=sys.stderr)
                    continue

            # Bulk insert
            with transaction.atomic():
                bulk_insert_optimized(Transition, transitions, batch_size)

            total_processed += len(batch)
            pbar.update(len(batch))
            pbar.set_postfix({
                'cache_hit_rate': f'{state_cache.hit_rate:.1f}%'
            })

    if verbose:
        print(f'Done! Imported {total_processed} transitions.')
        print(f'Cache stats: {state_cache.hits} hits, {state_cache.misses} misses')

    # Calculate derived fields
    if not skip_calc:
        if verbose:
            print('Calculating Einstein A coefficients...')

        if connection.vendor == 'sqlite':
            # SQLite: simpler SQL syntax
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE transitions
                    SET einsteina = (0.667025 * POWER(10, 16) * POWER(10, loggf))
                                  / ((2.0 * (SELECT j FROM states WHERE states.id = upstate) + 1.0)
                                     * POWER(wave, 2))
                    WHERE einsteina IS NULL AND loggf IS NOT NULL
                """)
        else:
            # PostgreSQL/MySQL: JOIN syntax
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE transitions t
                    SET einsteina = (0.667025 * POWER(10, 16) * POWER(10, t.loggf))
                                  / ((2.0 * s.j + 1.0) * POWER(t.wave, 2))
                    FROM states s
                    WHERE t.upstate = s.id AND t.einsteina IS NULL
                """)

        if verbose:
            print('Einstein A calculated')

    return total_processed


# =============================================================================
# SPECIES IMPORT
# =============================================================================

def import_species(input_file, batch_size=10000, verbose=True):
    """
    Import species from CSV file (VALD List of Species format)

    Format: comma-separated with header
    Use,Index,Name,Charge,InChI,InChIkey,Mass,Ion. en.,Fract.,Num. comp.,N1,N2,N3,N4,Dummy

    Returns: (total_processed, total_inserted)
    """
    try:
        from tqdm import tqdm
        progress_bar = tqdm
    except ImportError:
        class DummyBar:
            def __init__(self, *args, **kwargs): pass
            def update(self, n): pass
            def set_postfix(self, d): pass
            def __enter__(self): return self
            def __exit__(self, *args): pass
        progress_bar = DummyBar

    from node_common.models import Species
    from django.db import transaction
    import csv

    with open(input_file, 'r') as f:
        # Skip comment line
        first_line = f.readline()
        if first_line.startswith('#VER'):
            pass
        else:
            f.seek(0)

        reader = csv.DictReader(f)
        species_list = []
        total_processed = 0

        with progress_bar(desc="Importing species", unit=" lines", disable=not verbose) as pbar:
            for row in reader:
                try:
                    use = row.get('Use', '1').strip()
                    if use != '1':
                        continue

                    species = Species(
                        id=int(row['Index']),
                        name=row['Name'].strip(),
                        ion=int(row['Charge']) if row['Charge'].strip() else None,
                        inchi=row['InChI'].strip() if row['InChI'].strip() else None,
                        inchikey=row['InChIkey'].strip() if row['InChIkey'].strip() else None,
                        mass=float(row['Mass']) if row['Mass'].strip() else None,
                        massno=int(float(row['Mass'])) if row['Mass'].strip() else None,
                        ionen=float(row['Ion. en.']) if row['Ion. en.'].strip() else None,
                        solariso=float(row['Fract.']) if row['Fract.'].strip() else None,
                        ncomp=int(row['Num. comp.']) if row['Num. comp.'].strip() else None,
                    )
                    species_list.append(species)
                    total_processed += 1

                    if len(species_list) >= batch_size:
                        with transaction.atomic():
                            Species.objects.bulk_create(
                                species_list,
                                batch_size=batch_size,
                                ignore_conflicts=True
                            )
                        pbar.update(len(species_list))
                        species_list = []

                except (ValueError, KeyError) as e:
                    if verbose and total_processed < 5:
                        print(f"Warning: Skipping row: {e}", file=sys.stderr)
                    continue

            if species_list:
                with transaction.atomic():
                    Species.objects.bulk_create(
                        species_list,
                        batch_size=batch_size,
                        ignore_conflicts=True
                    )
                pbar.update(len(species_list))

    inserted_count = Species.objects.count()

    return total_processed, inserted_count


# =============================================================================
# STANDALONE CLI
# =============================================================================

def main():
    """Standalone command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description='VALD Data Import')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # States import command
    states_parser = subparsers.add_parser('import-states',
                                         help='Import states (Pass 1)')
    states_parser.add_argument('--file', type=str, help='Input file (or use stdin)')
    states_parser.add_argument('--batch-size', type=int, default=10000)
    states_parser.add_argument('--skip-header', type=int, default=2)

    # Transitions import command
    trans_parser = subparsers.add_parser('import-transitions',
                                        help='Import transitions (Pass 2)')
    trans_parser.add_argument('--file', type=str, help='Input file (or use stdin)')
    trans_parser.add_argument('--batch-size', type=int, default=10000)
    trans_parser.add_argument('--skip-header', type=int, default=2)
    trans_parser.add_argument('--skip-calc', action='store_true',
                            help='Skip Einstein A calculation')

    # Species import command
    species_parser = subparsers.add_parser('import-species',
                                          help='Import species from CSV')
    species_parser.add_argument('--file', type=str, required=True,
                              help='Species CSV file')
    species_parser.add_argument('--batch-size', type=int, default=10000)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Setup Django environment
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_dev')
    import django
    django.setup()

    # Run appropriate command
    if args.command == 'import-states':
        processed, inserted = import_states(
            input_file=args.file,
            batch_size=args.batch_size,
            skip_header=args.skip_header
        )
        print(f'Done! Processed {processed} lines, inserted {inserted} unique states')

    elif args.command == 'import-transitions':
        processed = import_transitions(
            input_file=args.file,
            batch_size=args.batch_size,
            skip_header=args.skip_header,
            skip_calc=args.skip_calc
        )
        print(f'Done! Imported {processed} transitions')

    elif args.command == 'import-species':
        processed, inserted = import_species(
            input_file=args.file,
            batch_size=args.batch_size
        )
        print(f'Done! Processed {processed} lines, inserted {inserted} total species')


if __name__ == '__main__':
    main()
