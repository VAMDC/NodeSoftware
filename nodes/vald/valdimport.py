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

def bulk_insert_optimized(model, batch: list, batch_size: int = 10000):
    """
    Use fastest bulk insert method for each database.

    Performance:
    - PostgreSQL: COPY FROM STDIN (~50k rows/sec)
    - MySQL: bulk_create (~20k rows/sec)
    - SQLite: bulk_create (~10k rows/sec)
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

    else:
        # MySQL and SQLite: Use Django's bulk_create
        # Note: ignore_conflicts requires Django 4.1+ and PostgreSQL/SQLite 3.24+
        model.objects.bulk_create(
            batch,
            batch_size=batch_size,
            ignore_conflicts=True  # For deduplication in Pass 1
        )


# =============================================================================
# STATE CACHE FOR TRANSITION LOOKUPS
# =============================================================================

class StateCache:
    """
    LRU cache for state lookups.
    First ~10M lookups will be cache misses (DB queries).
    Subsequent 245M will be cache hits (no DB queries).
    """

    def __init__(self, max_size: int = 100000):
        self.cache = {}  # (species, energy, j, term) -> state_id
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def get_state_id(self, species_id, energy, j, term):
        """Get state ID with caching"""
        key = (species_id, energy, j, term)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        # Cache miss - query database
        self.misses += 1
        from node_atom.models import State
        try:
            state_id = State.objects.get(
                species_id=species_id,
                energy=energy,
                j=j,
                term_desc=term
            ).id
        except State.DoesNotExist:
            raise ValueError(
                f"State not found: species={species_id}, "
                f"energy={energy}, j={j}, term={term}"
            )

        # Simple LRU: clear cache if too big
        if len(self.cache) > self.max_size:
            self.cache.clear()

        self.cache[key] = state_id
        return state_id

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
                bulk_insert_optimized(State, states, batch_size)
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


if __name__ == '__main__':
    main()
