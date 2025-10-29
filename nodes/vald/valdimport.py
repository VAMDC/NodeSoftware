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
import threading
import queue
from dataclasses import dataclass
from typing import Callable, Optional, Iterator, TextIO
from io import StringIO
import csv
import re

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
    # 1X,A1,A7,1X,A16,9I4 = skip, accurflag, accuracy, skip, comment, 9 reference indices
    # FORTRAN 1X means skip 1 position
    FieldDef('accurflag', 304, 305, str.strip),
    FieldDef('accuracy', 305, 312, str.strip),
    # Position 312-313 is 1X (skip)
    FieldDef('comment', 313, 329, str.strip),

    # === Reference indices (9I4) ===
    # Each I4 is 4 characters, right-justified
    FieldDef('r1', 329, 333, int, null_values=('', '0', '   0')),
    FieldDef('r2', 333, 337, int, null_values=('', '0', '   0')),
    FieldDef('r3', 337, 341, int, null_values=('', '0', '   0')),
    FieldDef('r4', 341, 345, int, null_values=('', '0', '   0')),
    FieldDef('r5', 345, 349, int, null_values=('', '0', '   0')),
    FieldDef('r6', 349, 353, int, null_values=('', '0', '   0')),
    FieldDef('r7', 353, 357, int, null_values=('', '0', '   0')),
    FieldDef('r8', 357, 361, int, null_values=('', '0', '   0')),
    FieldDef('r9', 361, 365, int, null_values=('', '0', '   0')),
]


def parse_vald_line(line: str) -> dict:
    """
    Parse a VALD line using field definitions.
    Catches parsing errors per-field and sets to None instead of failing entire line.
    """
    result = {}
    for field in VALD_FIELDS:
        try:
            result[field.name] = field.parse(line)
        except (ValueError, IndexError):
            # Field parsing failed, set to None and continue
            # This allows states import to succeed even if reference indices are malformed
            result[field.name] = None
    return result


ENERGY_SCALE_FACTOR = 10000


def scale_energy(value: Optional[float]) -> Optional[int]:
    """Convert energy value to scaled integer (energy * 1e4)"""
    if value is None:
        return None
    return int(round(value * ENERGY_SCALE_FACTOR))


def parse_fraction(s: str) -> Optional[float]:
    """
    Parse string that may contain fraction like '3/2' or decimal like '1.5'.
    Returns float value, dividing by 2 if fraction is present.
    Returns None if string cannot be parsed as number.
    """
    if not s or s.strip() == '':
        return None
    s = s.strip()

    # Remove trailing non-numeric characters (like +, -, ?, etc.)
    while s and not s[-1].isdigit():
        s = s[:-1]

    if not s:
        return None

    try:
        if '/' in s:
            return float(s.split('/')[0]) / 2.0
        return float(s)
    except (ValueError, IndexError):
        return None


def detect_coupling(term_desc: str) -> str:
    """
    Detect coupling scheme from term description structure.
    Returns 'LS', 'JJ', 'JK', 'LK', or 'Unknown'.
    """
    if not term_desc or not term_desc.strip():
        return 'Unknown'

    term = term_desc.strip()

    # JJ coupling: (J1,J2) format
    if re.search(r'\([^)]*,', term):
        return 'JJ'

    # JK/LK coupling: [K] format
    if '[' in term:
        # LK has \ in electronic config, but we can't always distinguish
        # Default to JK for bracket notation
        return 'JK'

    # LS coupling: has letter S,P,D,F,G,H,I,K,L,M,N with multiplicity
    # Remove trailing *, ?, X, a, b, c, +, digits, A, B
    term_clean = term.rstrip('*?Xabc+0123456789AB')
    if term_clean and term_clean[-1] in 'SPDFGHIKLMN':
        return 'LS'

    return 'Unknown'


def parse_quantum_numbers(species_id: int, j: Optional[float],
                         coupling: str, term_desc: str,
                         level_desc: str = None) -> dict:
    """
    Parse VALD term description to extract quantum numbers.

    Based on parse_vald_term.c logic from VALD.

    Args:
        species_id: Species identifier (for H/He special case)
        j: Total angular momentum J
        coupling: Coupling scheme flag ('LS', 'JJ', 'JK', 'LK', or other)
        term_desc: Term name/description (e.g., '2F*', '(6,7/2)*', '2[11/2]')
                   Can be full level (config + term) - will be split automatically
        level_desc: Full level description including electronic config (needed for JK/LK Jc extraction)

    Returns:
        dict with keys: l, s, p, j1, j2, k, s2, jc, sn, n
        Only non-None values are included.
    """
    if not term_desc or not term_desc.strip():
        return {}

    full_level = term_desc.strip()

    # Split electronic configuration from term name (C code: find first space after backslash-spaces)
    # In VALD format, config and term are separated by space(s)
    # But backslash-space (\ ) is an escaped space within config
    # For simplicity: split on last space to get term name
    if ' ' in full_level and not full_level.startswith('('):
        # Split on last space group to separate config from term
        parts = full_level.rsplit(maxsplit=1)
        if len(parts) > 1:
            config, term = parts
        else:
            term = full_level
            config = ''
    else:
        term = full_level
        config = ''

    result = {}

    # Auto-detect coupling if not provided or empty
    if not coupling or coupling.strip() == '':
        coupling = detect_coupling(term)

    # Check for H/He special case: n=X pattern
    if species_id <= 3:
        n_match = re.search(r'n=(\d+)', term_desc)
        if n_match:
            result['n'] = int(n_match.group(1))
            # Also parse parity
            if term.endswith('*'):
                result['p'] = 1
            else:
                result['p'] = 2
            return result

    # Parse parity (odd parity marked with *)
    parity = 2
    if term.endswith('*'):
        parity = 1
        term = term[:-1].strip()

    # LS COUPLING
    if coupling == 'LS':
        # Find the last occurrence of multiplicity+letter pattern
        # Pattern: optional lowercase/parens + digit(s) + capital letter
        # e.g., "Q(5D)5G518" -> need to find "5G"

        term_clean = term

        # Skip trailing '?', 'X', 'a', 'b', 'c', '+'
        while term_clean and term_clean[-1] in '?Xabc+':
            term_clean = term_clean[:-1]

        # Check for second parity marker
        if term_clean.endswith('*'):
            parity = 1
            term_clean = term_clean[:-1]

        # Parse seniority (trailing digits or A/B)
        seniority = None
        # Strip trailing digits and A/B for seniority
        while term_clean and (term_clean[-1].isdigit() or term_clean[-1] in 'AB'):
            if not seniority:
                # Only capture first character as seniority
                seniority = term_clean[-1]
            term_clean = term_clean[:-1]

        # Now find the last capital letter that could be L quantum number
        # Scan backwards for pattern: digit(s) + letter
        l_idx = -1
        for i in range(len(term_clean) - 1, -1, -1):
            if term_clean[i] in 'SPDFGHIKLMN':
                # Found a potential L letter, check if preceded by digit
                if i > 0 and term_clean[i-1].isdigit():
                    l_idx = i
                    break

        if l_idx >= 0:
            l_char = term_clean[l_idx]
            l_map = {'S': 0, 'P': 1, 'D': 2, 'F': 3, 'G': 4,
                    'H': 5, 'I': 6, 'K': 7, 'L': 8, 'M': 9, 'N': 10}

            if l_char in l_map:
                result['l'] = l_map[l_char]

                # Parse multiplicity (digits before L letter)
                mult_start = l_idx - 1
                while mult_start > 0 and term_clean[mult_start-1].isdigit():
                    mult_start -= 1

                multiplicity_str = term_clean[mult_start:l_idx]
                if multiplicity_str and multiplicity_str.isdigit():
                    multiplicity = int(multiplicity_str)
                    result['s'] = (multiplicity - 1) / 2.0

        if seniority:
            result['sn'] = ord(seniority) if seniority in 'AB' else int(seniority)

        result['p'] = parity
        return result

    # JJ COUPLING
    elif coupling == 'JJ':
        # Format: (J1,J2) or (J1,J2)*
        # Extract values between parentheses
        match = re.search(r'\(([^,]+),([^)]+)\)', term)
        if match:
            j1_str = match.group(1).strip()
            j2_str = match.group(2).strip()
            result['j1'] = parse_fraction(j1_str)
            result['j2'] = parse_fraction(j2_str)
            result['p'] = parity
        return result

    # JK COUPLING
    elif coupling == 'JK':
        # Format: multiplicity[K] or (S2)[K]
        # K is in square brackets, S2 is either in parentheses or derived from multiplicity

        # Parse K from [K]
        k_match = re.search(r'\[([^\]]+)\]', term)
        if k_match:
            k_str = k_match.group(1)
            result['k'] = parse_fraction(k_str)

        # Parse S2 from (S2) or from multiplicity
        s2_match = re.search(r'\(([^\)]+)\)', term)
        if s2_match:
            s2_str = s2_match.group(1)
            result['s2'] = parse_fraction(s2_str)
        else:
            # Parse multiplicity at start
            mult_match = re.match(r'^(\d+)', term)
            if mult_match:
                multiplicity = int(mult_match.group(1))
                result['s2'] = (multiplicity - 1) / 2.0

        # Parse Jc from <Jc> in level description (use full_level if level_desc not provided)
        search_str = level_desc if level_desc else full_level
        if search_str:
            jc_match = re.search(r'<([^>]+)>', search_str)
            if jc_match:
                jc_str = jc_match.group(1)
                result['jc'] = parse_fraction(jc_str)

        result['p'] = parity
        return result

    # LK COUPLING
    elif coupling == 'LK':
        # Similar to JK but L is parsed from electronic config after '\ '

        # Parse K from [K]
        k_match = re.search(r'\[([^\]]+)\]', term)
        if k_match:
            k_str = k_match.group(1)
            result['k'] = parse_fraction(k_str)

        # Parse S2 from (S2) or from multiplicity
        s2_match = re.search(r'\(([^\)]+)\)', term)
        if s2_match:
            s2_str = s2_match.group(1)
            result['s2'] = parse_fraction(s2_str)
        else:
            # Parse multiplicity at start
            mult_match = re.match(r'^(\d+)', term)
            if mult_match:
                multiplicity = int(mult_match.group(1))
                result['s2'] = (multiplicity - 1) / 2.0

        # Parse L from level description after '\ ' (use full_level if level_desc not provided)
        search_str = level_desc if level_desc else full_level
        if search_str:
            backslash_match = re.search(r'\\ ([A-Z])', search_str)
            if backslash_match:
                l_char = backslash_match.group(1)
                l_map = {'S': 0, 'P': 1, 'D': 2, 'F': 3, 'G': 4,
                        'H': 5, 'I': 6, 'K': 7, 'L': 8, 'M': 9, 'N': 10}
                if l_char in l_map:
                    result['l'] = l_map[l_char]

        result['p'] = parity
        return result

    # Unknown coupling - just return parity if we found it
    if parity == 1:
        result['p'] = parity

    return result


def parse_reference_line(ref_line: str) -> dict:
    """
    Parse VALD reference line.
    Format: "wl:K07 gf:K07 K07 K07 K07 K07 K07 K07 K07"
    Returns dict with 'wave_ref' and 'refs' (list of 9 reference strings)
    """
    parts = ref_line.strip().split()
    refs = {}

    # First part should be "wl:XXX"
    if parts and ':' in parts[0]:
        wave_ref = parts[0].split(':', 1)[1]
        refs['wave_ref'] = wave_ref
    else:
        refs['wave_ref'] = None

    # Collect all reference codes (there should be 9 total)
    ref_codes = []
    for part in parts:
        if ':' in part:
            ref_codes.append(part.split(':', 1)[1])
        else:
            ref_codes.append(part)

    # Pad to 9 refs if needed
    while len(ref_codes) < 9:
        ref_codes.append(None)

    refs['ref_codes'] = ref_codes[:9]

    return refs


# =============================================================================
# STREAMING PARSER
# =============================================================================

def parse_vald_stream(input_stream: TextIO,
                      skip_header_lines: int = 2) -> Iterator[dict]:
    """
    Generator that yields parsed VALD records.
    Works with files, stdin, gzipped files, or shell pipes.
    VALD format has 2 lines per record: data line + reference line.

    Yields dict with both data fields and reference info.
    """

    # Skip header lines
    for _ in range(skip_header_lines):
        next(input_stream, None)

    # Convert to iterator for manual line reading
    line_iter = iter(input_stream)
    line_num = 0

    while True:
        try:
            # Read data line
            data_line = next(line_iter)
            line_num += 1
            data_line = data_line.rstrip('\n')

            # Skip comments and empty lines
            if not data_line or data_line.startswith('#'):
                continue

            # Skip reference lines that appear out of sequence
            if data_line and data_line[0].islower():
                continue

            # Skip error lines
            if 'Unknown' in data_line:
                continue

            # Parse data line
            try:
                data = parse_vald_line(data_line)
            except Exception as e:
                print(f"Warning: Failed to parse data line {line_num}: {e}",
                      file=sys.stderr)
                continue

            # Read reference line
            ref_line = next(line_iter, '')
            line_num += 1
            ref_line = ref_line.rstrip('\n')

            # Parse reference line if it exists
            if ref_line and ref_line[0].islower():
                try:
                    ref_data = parse_reference_line(ref_line)
                    data.update(ref_data)
                except Exception as e:
                    print(f"Warning: Failed to parse reference line {line_num}: {e}",
                          file=sys.stderr)

            yield data

        except StopIteration:
            break


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

    def __init__(self, max_size: Optional[int] = None):
        self.cache = {}  # (species, energy_scaled, j, term) -> state_id
        self.max_size = max_size
        self.hits = 0
        self.misses = 0

    def prefetch_states(self, state_keys):
        """
        Prefetch states in batch for given keys using temp table.
        Keys should be tuples of (species_id, energy_scaled, j).
        """
        from django.db import connection

        uncached = [
            key for key in state_keys
            if key[1] is not None and key not in self.cache
        ]
        if not uncached:
            return

        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TEMP TABLE IF NOT EXISTS temp_state_lookup (
                    species_id INTEGER,
                    energy_scaled INTEGER,
                    j REAL
                )
            """)

            cursor.execute("DELETE FROM temp_state_lookup")

            cursor.executemany(
                "INSERT INTO temp_state_lookup VALUES (?, ?, ?)",
                uncached
            )

            cursor.execute("""
                SELECT s.id, s.species_id, s.energy_scaled, s.j
                FROM states s
                INNER JOIN temp_state_lookup t
                ON s.species_id = t.species_id
                   AND s.energy_scaled = t.energy_scaled
                   AND (s.j = t.j OR (s.j IS NULL AND t.j IS NULL))
            """)

            for row in cursor.fetchall():
                state_id, species_id, energy_scaled, j = row
                key = (
                    species_id,
                    energy_scaled,
                    float(j) if j is not None else None
                )
                self.cache[key] = state_id

        if self.max_size and len(self.cache) > self.max_size:
            self.cache.clear()

    def get_state_id(self, species_id, energy_scaled, j, term):
        """Get state ID from cache (assumes prefetch_states was called)"""
        key = (species_id, energy_scaled, j)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        self.misses += 1
        raise ValueError(
            f"State not found in cache: species={species_id}, "
            f"energy_scaled={energy_scaled}, j={j}"
        )

    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0


class LineListCache:
    """
    Cache for linelist lookups and creation.
    Creates linelist records on-the-fly as needed.
    """

    def __init__(self):
        self.cache = {}  # (wave_ref, r1...r9) -> linelist_id
        self.hits = 0
        self.misses = 0

    def _make_key(self, wave_ref, r1, r2, r3, r4, r5, r6, r7, r8, r9):
        """Create cache key from reference data"""
        return (wave_ref, r1, r2, r3, r4, r5, r6, r7, r8, r9)

    def get_or_create_linelist(self, wave_ref, r1, r2, r3, r4, r5, r6, r7, r8, r9):
        """
        Get or create linelist record.
        Returns linelist_id.
        """
        from node_common.models import LineList
        from django.db import transaction

        key = self._make_key(wave_ref, r1, r2, r3, r4, r5, r6, r7, r8, r9)

        if key in self.cache:
            self.hits += 1
            return self.cache[key]

        self.misses += 1

        # Create new linelist
        with transaction.atomic():
            linelist = LineList.objects.create(
                srcfile=wave_ref or 'unknown',
                r1=r1,
                r2=r2,
                r3=r3,
                r4=r4,
                r5=r5,
                r6=r6,
                r7=r7,
                r8=r8,
                r9=r9,
            )
            linelist_id = linelist.id

        self.cache[key] = linelist_id
        return linelist_id

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
                lower_energy = row['lower_energy']
                lower_energy_scaled = scale_energy(lower_energy)
                upper_energy = row['upper_energy']
                upper_energy_scaled = scale_energy(upper_energy)

                species_id = row.get('species_id')

                # Parse quantum numbers for lower state
                lower_qn = parse_quantum_numbers(
                    species_id=species_id,
                    j=row['lower_j'],
                    coupling=row['lower_term_flag'],
                    term_desc=row['lower_term'],
                    level_desc=row['lower_term']
                )

                # Parse quantum numbers for upper state
                upper_qn = parse_quantum_numbers(
                    species_id=species_id,
                    j=row['upper_j'],
                    coupling=row['upper_term_flag'],
                    term_desc=row['upper_term'],
                    level_desc=row['upper_term']
                )

                # Extract lower state
                states.append(State(
                    species_id=species_id,
                    energy=lower_energy,
                    energy_scaled=lower_energy_scaled,
                    j=row['lower_j'],
                    lande=row['lower_lande'],
                    term_desc=row['lower_term'] or None,
                    l=lower_qn.get('l'),
                    s=lower_qn.get('s'),
                    p=lower_qn.get('p'),
                    j1=lower_qn.get('j1'),
                    j2=lower_qn.get('j2'),
                    k=lower_qn.get('k'),
                    s2=lower_qn.get('s2'),
                    jc=lower_qn.get('jc'),
                    sn=lower_qn.get('sn'),
                    n=lower_qn.get('n'),
                ))

                # Extract upper state
                states.append(State(
                    species_id=species_id,
                    energy=upper_energy,
                    energy_scaled=upper_energy_scaled,
                    j=row['upper_j'],
                    lande=row['upper_lande'],
                    term_desc=row['upper_term'] or None,
                    l=upper_qn.get('l'),
                    s=upper_qn.get('s'),
                    p=upper_qn.get('p'),
                    j1=upper_qn.get('j1'),
                    j2=upper_qn.get('j2'),
                    k=upper_qn.get('k'),
                    s2=upper_qn.get('s2'),
                    jc=upper_qn.get('jc'),
                    sn=upper_qn.get('sn'),
                    n=upper_qn.get('n'),
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
    linelist_cache = LineListCache()
    records = parse_vald_stream(input_stream, skip_header)

    total_processed = 0

    with progress_bar(desc="Importing transitions", unit=" lines", disable=not verbose) as pbar:
        for batch in batch_iterator(records, batch_size):
            state_keys = set()
            for row in batch:
                lower_energy_scaled = scale_energy(row['lower_energy'])
                upper_energy_scaled = scale_energy(row['upper_energy'])
                row['_lower_energy_scaled'] = lower_energy_scaled
                row['_upper_energy_scaled'] = upper_energy_scaled

                state_keys.add((row['species_id'], lower_energy_scaled, row['lower_j']))
                state_keys.add((row['species_id'], upper_energy_scaled, row['upper_j']))

            state_cache.prefetch_states(state_keys)

            transitions = []
            for row in batch:
                try:
                    # Get or create linelist for this transition
                    linelist_id = linelist_cache.get_or_create_linelist(
                        wave_ref=row.get('wave_ref'),
                        r1=row.get('r1'),
                        r2=row.get('r2'),
                        r3=row.get('r3'),
                        r4=row.get('r4'),
                        r5=row.get('r5'),
                        r6=row.get('r6'),
                        r7=row.get('r7'),
                        r8=row.get('r8'),
                        r9=row.get('r9'),
                    )

                    transitions.append(Transition(
                        upstate_id=state_cache.get_state_id(
                            row['species_id'],
                            row['_upper_energy_scaled'],
                            row['upper_j'],
                            row['upper_term'] or None
                        ),
                        lostate_id=state_cache.get_state_id(
                            row['species_id'],
                            row['_lower_energy_scaled'],
                            row['lower_j'],
                            row['lower_term'] or None
                        ),
                        species_id=row.get('species_id'),
                        wave=row['wave'],
                        waveritz=row['wave_ritz'],
                        loggf=row['loggf'],
                        gammarad=row.get('gammarad'),
                        gammastark=row.get('gammastark'),
                        gammawaals=row.get('gammawaals'),
                        accurflag=row.get('accurflag'),
                        wave_linelist_id=linelist_id,
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
        print(f'State cache stats: {state_cache.hits} hits, {state_cache.misses} misses')
        print(f'Linelist cache stats: {linelist_cache.hits} hits, {linelist_cache.misses} misses')
        print(f'Created {linelist_cache.misses} unique linelists')

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


def import_states_transitions(input_file=None, batch_size=10000, skip_header=2,
                              skip_calc=False, read_ahead=True, verbose=True):
    """
    Combined single-pass import of states and transitions from VALD format.

    For each batch:
    1. Extract and insert states (lower and upper)
    2. Prefetch just-inserted state IDs
    3. Create and insert transitions using those state IDs

    Memory-efficient for large datasets - only one batch in memory at a time.

    Args:
        read_ahead: If True, read and parse in separate thread to keep extraction
                   tool running at full speed. Safe with SQLite (no locking issues).

    Returns: (total_processed, total_states_inserted, total_transitions_inserted)
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
    linelist_cache = LineListCache()

    total_processed = 0
    total_states_inserted = 0
    total_transitions_inserted = 0

    # Setup batch source (either direct or via read-ahead thread)
    if read_ahead:
        batch_queue = queue.Queue(maxsize=3)
        reader_error = []

        def reader_thread():
            try:
                records = parse_vald_stream(input_stream, skip_header)
                for batch in batch_iterator(records, batch_size):
                    batch_queue.put(batch)
            except Exception as e:
                reader_error.append(e)
            finally:
                batch_queue.put(None)

        reader = threading.Thread(target=reader_thread, daemon=True)
        reader.start()

        def batch_source():
            while True:
                if reader_error:
                    raise reader_error[0]
                batch = batch_queue.get()
                if batch is None:
                    break
                yield batch
    else:
        records = parse_vald_stream(input_stream, skip_header)
        batch_source = lambda: batch_iterator(records, batch_size)

    with progress_bar(desc="Importing VALD data", unit=" lines", disable=not verbose) as pbar:
        for batch in batch_source():
            # === STEP 1: Insert states directly (bypass Django ORM) ===
            state_keys = set()
            state_rows = []

            for row in batch:
                species_id = row['species_id']

                # Lower state
                lower_energy, lower_j, lower_lande, lower_term = (
                    row['lower_energy'], row['lower_j'],
                    row['lower_lande'], row['lower_term'] or None
                )
                lower_energy_scaled = scale_energy(lower_energy)
                row['_lower_energy_scaled'] = lower_energy_scaled

                # Parse quantum numbers for lower state
                lower_qn = parse_quantum_numbers(
                    species_id=species_id,
                    j=lower_j,
                    coupling=row['lower_term_flag'],
                    term_desc=lower_term,
                    level_desc=lower_term
                )

                state_keys.add((species_id, lower_energy_scaled, lower_j))
                state_rows.append((
                    species_id, lower_energy, lower_energy_scaled, lower_j, lower_lande, lower_term,
                    lower_qn.get('l'), lower_qn.get('s'), lower_qn.get('p'),
                    lower_qn.get('j1'), lower_qn.get('j2'), lower_qn.get('k'),
                    lower_qn.get('s2'), lower_qn.get('jc'), lower_qn.get('sn'), lower_qn.get('n')
                ))

                # Upper state
                upper_energy, upper_j, upper_lande, upper_term = (
                    row['upper_energy'], row['upper_j'],
                    row['upper_lande'], row['upper_term'] or None
                )
                upper_energy_scaled = scale_energy(upper_energy)
                row['_upper_energy_scaled'] = upper_energy_scaled

                # Parse quantum numbers for upper state
                upper_qn = parse_quantum_numbers(
                    species_id=species_id,
                    j=upper_j,
                    coupling=row['upper_term_flag'],
                    term_desc=upper_term,
                    level_desc=upper_term
                )

                state_keys.add((species_id, upper_energy_scaled, upper_j))
                state_rows.append((
                    species_id, upper_energy, upper_energy_scaled, upper_j, upper_lande, upper_term,
                    upper_qn.get('l'), upper_qn.get('s'), upper_qn.get('p'),
                    upper_qn.get('j1'), upper_qn.get('j2'), upper_qn.get('k'),
                    upper_qn.get('s2'), upper_qn.get('jc'), upper_qn.get('sn'), upper_qn.get('n')
                ))

            # Direct SQL insert (faster than Django ORM)
            with transaction.atomic():
                initial_state_count = State.objects.count()
                with connection.cursor() as cursor:
                    cursor.executemany(
                        "INSERT OR IGNORE INTO states (species_id, energy, energy_scaled, J, lande, term_desc, L, S, P, J1, J2, K, S2, Jc, Sn, n) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        state_rows
                    )
                final_state_count = State.objects.count()
                states_inserted = final_state_count - initial_state_count

            total_states_inserted += states_inserted

            # === STEP 2: Prefetch state IDs for this batch ===
            state_cache.prefetch_states(state_keys)

            # === STEP 3: Insert transitions directly (bypass Django ORM) ===
            transition_rows = []
            for row in batch:
                try:
                    # Cache lookups once
                    species_id = row['species_id']

                    # Get or create linelist for this transition
                    linelist_id = linelist_cache.get_or_create_linelist(
                        row.get('wave_ref'), row.get('r1'), row.get('r2'), row.get('r3'),
                        row.get('r4'), row.get('r5'), row.get('r6'),
                        row.get('r7'), row.get('r8'), row.get('r9')
                    )

                    # Get state IDs
                    upstate_id = state_cache.get_state_id(
                        species_id, row['_upper_energy_scaled'],
                        row['upper_j'], row['upper_term'] or None
                    )
                    lostate_id = state_cache.get_state_id(
                        species_id, row['_lower_energy_scaled'],
                        row['lower_j'], row['lower_term'] or None
                    )

                    transition_rows.append((
                        upstate_id, lostate_id, species_id,
                        row['wave'], row['wave_ritz'], row['loggf'],
                        row.get('gammarad'), row.get('gammastark'), row.get('gammawaals'),
                        row.get('accurflag'), linelist_id
                    ))
                except ValueError as e:
                    print(f"Warning: Skipping transition: {e}", file=sys.stderr)
                    continue

            # Direct SQL insert (faster than Django ORM)
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.executemany(
                        "INSERT INTO transitions (upstate, lostate, species_id, wave, waveritz, loggf, gammarad, gammastark, gammawaals, accurflag, wave_linelist_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        transition_rows
                    )

            total_transitions_inserted += len(transition_rows)
            total_processed += len(batch)

            pbar.update(len(batch))
            pbar.set_postfix({
                'states': total_states_inserted,
                'transitions': total_transitions_inserted,
                'cache_hit': f'{state_cache.hit_rate:.1f}%'
            })

    if verbose:
        print(f'Processed {total_processed} lines')
        print(f'Inserted {total_states_inserted} unique states')
        print(f'Inserted {total_transitions_inserted} transitions')
        print(f'State cache: {state_cache.hits} hits, {state_cache.misses} misses')
        print(f'Linelist cache: {linelist_cache.hits} hits, {linelist_cache.misses} misses')
        print(f'Created {linelist_cache.misses} unique linelists')

    # Calculate derived fields
    if not skip_calc:
        if verbose:
            print('Calculating Einstein A coefficients...')

        if connection.vendor == 'sqlite':
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE transitions
                    SET einsteina = (0.667025 * POWER(10, 16) * POWER(10, loggf))
                                  / ((2.0 * (SELECT j FROM states WHERE states.id = upstate) + 1.0)
                                     * POWER(wave, 2))
                    WHERE einsteina IS NULL AND loggf IS NOT NULL
                """)
        else:
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

    return total_processed, total_states_inserted, total_transitions_inserted


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
# HYPERFINE STRUCTURE CONSTANTS IMPORT
# =============================================================================

def import_hfs(input_file, batch_size=1000, verbose=True, energy_tolerance=1.0):
    """
    Import hyperfine structure constants (A and B) from AB.db SQLite database.

    Matches AB.db records to existing states using the same criteria as Fortran code:
    - SPEID -> species_id (exact match)
    - J -> J (exact match)
    - abs(E - energy) < energy_tolerance (default: 1.0 cm⁻¹)

    When multiple states match, takes the last one (mimics Fortran behavior).

    Updates existing State records with hfs_a, hfs_a_error, hfs_b, hfs_b_error.

    Args:
        input_file: Path to AB.db SQLite database
        batch_size: Number of updates per transaction
        verbose: Print progress messages
        energy_tolerance: Maximum energy difference for matching (cm⁻¹)

    Returns: (total_processed, matched, multiple_matches, no_match)
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

    from node_atom.models import State
    from django.db import transaction, connection
    import sqlite3

    ab_conn = sqlite3.connect(input_file)
    ab_conn.text_factory = lambda b: b.decode(errors='ignore')
    ab_cursor = ab_conn.cursor()

    ab_cursor.execute("SELECT COUNT(*) FROM AB")
    total_records = ab_cursor.fetchone()[0]

    ab_cursor.execute("""
        SELECT ID, SPEID, E, J, TERM, A, dA, B, dB
        FROM AB
        ORDER BY ID
    """)

    stats = {
        'total': 0,
        'matched': 0,
        'multiple_matches': 0,
        'no_match': 0,
        'updated': 0
    }

    update_queue = []

    with progress_bar(desc="Importing HFS constants", unit=" records", total=total_records, disable=not verbose) as pbar:
        for row in ab_cursor:
            ab_id, speid, energy, j, term, a, da, b, db = row
            stats['total'] += 1

            candidates = State.objects.filter(
                species_id=speid,
                j=j
            ).extra(
                where=[f"ABS(energy - {energy}) < {energy_tolerance}"]
            )

            candidate_count = candidates.count()

            if candidate_count == 0:
                stats['no_match'] += 1
            else:
                if candidate_count > 1:
                    stats['multiple_matches'] += 1

                state = candidates.last()
                stats['matched'] += 1
                update_queue.append({
                    'state_id': state.id,
                    'a': a,
                    'da': da,
                    'b': b,
                    'db': db
                })

            if len(update_queue) >= batch_size:
                with transaction.atomic():
                    for update in update_queue:
                        State.objects.filter(id=update['state_id']).update(
                            hfs_a=update['a'],
                            hfs_a_error=update['da'],
                            hfs_b=update['b'],
                            hfs_b_error=update['db']
                        )
                        stats['updated'] += 1
                update_queue = []

            pbar.update(1)
            pbar.set_postfix({
                'matched': stats['matched'],
                'updated': stats['updated']
            })

        if update_queue:
            with transaction.atomic():
                for update in update_queue:
                    State.objects.filter(id=update['state_id']).update(
                        hfs_a=update['a'],
                        hfs_a_error=update['da'],
                        hfs_b=update['b'],
                        hfs_b_error=update['db']
                    )
                    stats['updated'] += 1

    ab_conn.close()

    if verbose:
        print(f"\nHFS Import Summary:")
        print(f"  Total AB records: {stats['total']}")
        print(f"  Matched: {stats['matched']}")
        print(f"  Multiple candidates (took last): {stats['multiple_matches']}")
        print(f"  No match: {stats['no_match']}")
        print(f"  States updated: {stats['updated']}")

    return stats['total'], stats['matched'], stats['multiple_matches'], stats['no_match']


# =============================================================================
# BIBTEX IMPORT
# =============================================================================

def import_bibtex(input_file, batch_size=1000, verbose=True):
    """
    Import references from BibTeX file.

    For each BibTeX entry:
    - Uses the BibTeX key as the Reference.id
    - Stores the raw BibTeX text in Reference.bibtex
    - Converts to XML using BibTeX2XML() and stores in Reference.xml

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

    from node_common.models import Reference
    from vamdctap.bibtextools import BibTeX2XML
    from django.db import transaction

    bibtex_pattern = re.compile(r'^@\w+\{([^,]+),', re.MULTILINE)

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    references = []
    total_processed = 0

    entry_start = None
    current_entry = []
    brace_count = 0
    lines = content.split('\n')

    with progress_bar(desc="Importing references", unit=" refs", disable=not verbose) as pbar:
        for i, line in enumerate(lines):
            if line.strip().startswith('@'):
                if current_entry:
                    bibtex_text = '\n'.join(current_entry)
                    match = bibtex_pattern.search(bibtex_text)
                    if match:
                        bibtex_key = match.group(1).strip()
                        try:
                            xml_text = BibTeX2XML(bibtex_text, key=bibtex_key)
                            ref = Reference(
                                id=bibtex_key,
                                bibtex=bibtex_text,
                                xml=xml_text
                            )
                            references.append(ref)
                            total_processed += 1

                            if len(references) >= batch_size:
                                with transaction.atomic():
                                    Reference.objects.bulk_create(
                                        references,
                                        batch_size=batch_size,
                                        ignore_conflicts=True
                                    )
                                pbar.update(len(references))
                                references = []
                        except Exception as e:
                            if verbose:
                                print(f"Warning: Failed to process entry {bibtex_key}: {e}", file=sys.stderr)

                current_entry = [line]
                brace_count = line.count('{') - line.count('}')
            elif current_entry:
                current_entry.append(line)
                brace_count += line.count('{') - line.count('}')

                if brace_count == 0 and line.strip().endswith('}'):
                    bibtex_text = '\n'.join(current_entry)
                    match = bibtex_pattern.search(bibtex_text)
                    if match:
                        bibtex_key = match.group(1).strip()
                        try:
                            xml_text = BibTeX2XML(bibtex_text, key=bibtex_key)
                            ref = Reference(
                                id=bibtex_key,
                                bibtex=bibtex_text,
                                xml=xml_text
                            )
                            references.append(ref)
                            total_processed += 1

                            if len(references) >= batch_size:
                                with transaction.atomic():
                                    Reference.objects.bulk_create(
                                        references,
                                        batch_size=batch_size,
                                        ignore_conflicts=True
                                    )
                                pbar.update(len(references))
                                references = []
                        except Exception as e:
                            if verbose:
                                print(f"Warning: Failed to process entry {bibtex_key}: {e}", file=sys.stderr)

                    current_entry = []
                    brace_count = 0

        if current_entry and brace_count == 0:
            bibtex_text = '\n'.join(current_entry)
            match = bibtex_pattern.search(bibtex_text)
            if match:
                bibtex_key = match.group(1).strip()
                try:
                    xml_text = BibTeX2XML(bibtex_text, key=bibtex_key)
                    ref = Reference(
                        id=bibtex_key,
                        bibtex=bibtex_text,
                        xml=xml_text
                    )
                    references.append(ref)
                    total_processed += 1
                except Exception as e:
                    if verbose:
                        print(f"Warning: Failed to process entry {bibtex_key}: {e}", file=sys.stderr)

        if references:
            with transaction.atomic():
                Reference.objects.bulk_create(
                    references,
                    batch_size=batch_size,
                    ignore_conflicts=True
                )
            pbar.update(len(references))

    inserted_count = Reference.objects.count()

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

    # Combined import command
    combined_parser = subparsers.add_parser('import-states-transitions',
                                           help='Combined single-pass import (states + transitions)')
    combined_parser.add_argument('--file', type=str, help='Input file (or use stdin)')
    combined_parser.add_argument('--batch-size', type=int, default=10000)
    combined_parser.add_argument('--skip-header', type=int, default=2)
    combined_parser.add_argument('--skip-calc', action='store_true',
                               help='Skip Einstein A calculation')
    combined_parser.add_argument('--no-read-ahead', action='store_true',
                               help='Disable read-ahead thread (enabled by default)')

    # Species import command
    species_parser = subparsers.add_parser('import-species',
                                          help='Import species from CSV')
    species_parser.add_argument('--file', type=str, required=True,
                              help='Species CSV file')
    species_parser.add_argument('--batch-size', type=int, default=10000)

    # BibTeX import command
    bibtex_parser = subparsers.add_parser('import-bibtex',
                                         help='Import references from BibTeX file')
    bibtex_parser.add_argument('--file', type=str, required=True,
                              help='BibTeX file')
    bibtex_parser.add_argument('--batch-size', type=int, default=1000)

    # HFS import command
    hfs_parser = subparsers.add_parser('import-hfs',
                                       help='Import hyperfine structure constants from AB.db')
    hfs_parser.add_argument('--file', type=str, required=True,
                           help='AB.db SQLite database file')
    hfs_parser.add_argument('--batch-size', type=int, default=1000)
    hfs_parser.add_argument('--energy-tolerance', type=float, default=1.0,
                           help='Energy matching tolerance in cm-1 (default: 1.0)')

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

    elif args.command == 'import-states-transitions':
        processed, states_inserted, trans_inserted = import_states_transitions(
            input_file=args.file,
            batch_size=args.batch_size,
            skip_header=args.skip_header,
            skip_calc=args.skip_calc,
            read_ahead=not args.no_read_ahead
        )
        print(f'Done! Processed {processed} lines')
        print(f'Inserted {states_inserted} unique states')
        print(f'Inserted {trans_inserted} transitions')

    elif args.command == 'import-species':
        processed, inserted = import_species(
            input_file=args.file,
            batch_size=args.batch_size
        )
        print(f'Done! Processed {processed} lines, inserted {inserted} total species')

    elif args.command == 'import-bibtex':
        processed, inserted = import_bibtex(
            input_file=args.file,
            batch_size=args.batch_size
        )
        print(f'Done! Processed {processed} BibTeX entries, inserted {inserted} total references')

    elif args.command == 'import-hfs':
        total, matched, multiple, no_match = import_hfs(
            input_file=args.file,
            batch_size=args.batch_size,
            energy_tolerance=args.energy_tolerance
        )
        print(f'Done! Processed {total} HFS records')
        print(f'Matched: {matched}, Multiple candidates: {multiple}, No match: {no_match}')


if __name__ == '__main__':
    main()
