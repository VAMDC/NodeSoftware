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
    # F8.3 at 119-127: gammawaals OR encoded alpha+sigma
    # Auto-detected: if value < 0 -> gammawaals
    #                if value > 0 -> integer part = sigma, fractional part = alpha
    FieldDef('gammawaals_raw', 119, 127, float, null_values=('0.0', '', 'X')),

    # === Term descriptions ===
    # A2,A86,A2,A86 = tflg_L, term_L, tflg_U, term_U
    FieldDef('lower_term_flag', 127, 129, str.strip),
    FieldDef('lower_term', 129, 215, str.strip),
    FieldDef('upper_term_flag', 215, 217, str.strip),
    FieldDef('upper_term', 217, 303, str.strip),

    # === Accuracy and transition flags ===
    # 1X,A1,A7,1X,A16,9I4 = skip, accurflag, accuracy, skip, comment, 9 reference indices
    # FORTRAN 1X means skip 1 position
    FieldDef('accurflag', 304, 305, str.strip),
    FieldDef('accuracy', 305, 312, str.strip),
    # Positions 312-313 contain transition flags (not actually skipped in data)
    FieldDef('transition_flag', 311, 312, str.strip,
             description="Transition type: ' '=E1, A=autoion, B=E2, C=M1, D=M2, E=E3, F=M3"),
    FieldDef('broadening_flag', 312, 313, str.strip,
             description="Broadening flag: 0-7 for different broadening types"),
    FieldDef('comment', 313, 329, str.strip),

    # === Linelist IDs (9I4) ===
    # Each I4 is 4 characters, right-justified
    FieldDef('ll1', 329, 333, int, null_values=('', '0', '   0')),
    FieldDef('ll2', 333, 337, int, null_values=('', '0', '   0')),
    FieldDef('ll3', 337, 341, int, null_values=('', '0', '   0')),
    FieldDef('ll4', 341, 345, int, null_values=('', '0', '   0')),
    FieldDef('ll5', 345, 349, int, null_values=('', '0', '   0')),
    FieldDef('ll6', 349, 353, int, null_values=('', '0', '   0')),
    FieldDef('ll7', 353, 357, int, null_values=('', '0', '   0')),
    FieldDef('ll8', 357, 361, int, null_values=('', '0', '   0')),
    FieldDef('ll9', 361, 365, int, null_values=('', '0', '   0')),
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


def parse_waals_broadening(gammawaals_raw: Optional[float]) -> tuple:
    """
    Parse van der Waals broadening value and auto-detect format.

    Args:
        gammawaals_raw: Raw value from field at positions 119-127

    Returns:
        tuple: (gammawaals, alphawaals, sigmawaals)
            If value < 0: (gammawaals, None, None)
            If value > 0: (None, alpha, sigma) where:
                - sigma = integer part
                - alpha = fractional part (parsed as string to avoid precision errors)
            If value is None or 0: (None, None, None)
    """
    if gammawaals_raw is None or gammawaals_raw == 0.0:
        return None, None, None

    if gammawaals_raw < 0:
        # Standard format: negative gammawaals value
        return gammawaals_raw, None, None

    # Extended format: positive value encodes sigma.alpha
    # Parse as string to avoid floating point precision errors
    value_str = str(gammawaals_raw)

    if '.' in value_str:
        int_part, frac_part = value_str.split('.', 1)
        sigma = int(int_part)
        # Parse fractional part as "0.xxx" to get clean decimal
        alpha = float('0.' + frac_part)
    else:
        # No fractional part (e.g., "2.0" or "2")
        sigma = int(gammawaals_raw)
        alpha = 0.0

    return None, alpha, sigma


def accuracy_to_loggf_error(accurflag: Optional[str], accuracy: Optional[str]) -> Optional[float]:
    """
    Convert VALD accuracy information to numerical log(gf) error in dex.

    Based on https://www.astro.uu.se/valdwiki/VALD3_accuracy

    Args:
        accurflag: Single character flag: 'N' (NIST), 'E' (error in dex), 'C' (cancellation), 'P' (predicted), or '_'/'None' (blank)
        accuracy: 7-character accuracy value (NIST code, numeric error, or other)

    Returns:
        Error in dex, or None if cannot be determined

    NIST Quality Classes (flag='N'):
        AAA: ≤0.3%  -> 0.0013 dex
        AA:  ≤1%    -> 0.0043 dex
        A+:  ≤2%    -> 0.0087 dex
        A:   ≤3%    -> 0.013 dex
        B+:  ≤7%    -> 0.030 dex
        B:   ≤10%   -> 0.043 dex
        C+:  ≤18%   -> 0.079 dex
        C:   ≤25%   -> 0.11 dex
        D+:  ≤40%   -> 0.18 dex
        D:   ≤50%   -> 0.22 dex
        E:   >50%   -> 0.5 dex (estimated)

    Error flag (flag='E'):
        Direct numerical error in dex

    Cancellation flag (flag='C'):
        Cancellation factor - not directly an error estimate
        Return None (could be very uncertain)

    Predicted flag (flag='P'):
        Predicted line - assume large uncertainty
        Return None or large value
    """
    if not accurflag or not accuracy:
        return None

    accurflag = accurflag.strip()
    accuracy = accuracy.strip()

    if not accurflag or not accuracy:
        return None

    # NIST quality classes
    if accurflag == 'N':
        # Map NIST codes to percentage error, then convert to dex
        # error_dex ≈ log10(1 + error_fraction) ≈ error_fraction / ln(10) ≈ 0.434 * error_fraction
        nist_errors = {
            'AAA': 0.0013,  # 0.3% -> 0.003/ln(10)
            'AA':  0.0043,  # 1%
            'A+':  0.0087,  # 2%
            'A':   0.013,   # 3%
            'B+':  0.030,   # 7%
            'B':   0.043,   # 10%
            'C+':  0.079,   # 18%
            'C':   0.11,    # 25%
            'D+':  0.18,    # 40%
            'D':   0.22,    # 50%
            'E':   0.5,     # >50%, estimated
        }

        # Handle variants with trailing characters (like "D-", "A ")
        for code, error in nist_errors.items():
            if accuracy.startswith(code):
                return error

        return None

    # Direct error in dex
    elif accurflag == 'E':
        try:
            return abs(float(accuracy))
        except (ValueError, TypeError):
            return None

    # Cancellation factor - not an error estimate
    elif accurflag == 'C':
        return None

    # Predicted line - no error estimate
    elif accurflag == 'P':
        return None

    # Blank or underscore - sometimes has quality indicators like "A"
    elif accurflag in ('_', ' ', ''):
        # Try to interpret as NIST code
        nist_errors = {
            'AAA': 0.0013,
            'AA':  0.0043,
            'A+':  0.0087,
            'A':   0.013,
            'B+':  0.030,
            'B':   0.043,
            'C+':  0.079,
            'C':   0.11,
            'D+':  0.18,
            'D':   0.22,
            'E':   0.5,
        }

        for code, error in nist_errors.items():
            if accuracy.startswith(code):
                return error

        return None

    return None


def parse_transition_properties(transition_flag: Optional[str],
                                 lower_energy: Optional[float],
                                 upper_energy: Optional[float]) -> tuple:
    """
    Determine transition_type and autoionized from VALD transition flag.

    Based on logic from SOURCE/TOOLS/test_parse.c lines 46-99.

    Args:
        transition_flag: Single character flag from position 312 (FORTRAN)
        lower_energy: Lower state energy in cm^-1
        upper_energy: Upper state energy in cm^-1

    Returns:
        tuple: (transition_type, autoionized)
            transition_type: 'E1', 'E2', 'M1', 'M2', 'E3', 'M3', or None
            autoionized: True if autoionization transition, False otherwise

    Transition type mapping:
        ' ' (space) -> 'E1' (electric dipole, allowed)
        'A' -> autoionization (if lower_energy > upper_energy)
        'B' -> 'E2' (electric quadrupole, forbidden)
        'C' -> 'M1' (magnetic dipole, forbidden)
        'D' -> 'M2' (magnetic quadrupole, forbidden)
        'E' -> 'E3' (electric octupole, forbidden)
        'F' -> 'M3' (magnetic octupole, forbidden)
    """
    if not transition_flag:
        return None, False

    TRANSITION_MAP = {
        ' ': 'E1',  # Electric dipole (allowed)
        'B': 'E2',  # Electric quadrupole
        'C': 'M1',  # Magnetic dipole
        'D': 'M2',  # Magnetic quadrupole
        'E': 'E3',  # Electric octupole
        'F': 'M3',  # Magnetic octupole
    }

    autoionized = False

    # Check for autoionization
    if transition_flag == 'A':
        # Validate: autoionization occurs when lower energy > upper energy
        if lower_energy is not None and upper_energy is not None:
            if lower_energy > upper_energy:
                autoionized = True
                return None, autoionized  # No transition_type for autoionization
        # If validation fails, treat as normal transition (reset flag)
        transition_flag = ' '

    transition_type = TRANSITION_MAP.get(transition_flag)
    return transition_type, autoionized


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


def parse_molecular_quantum_numbers(species_id: int, j: Optional[float],
                                   term_desc: str, coupling: str = None) -> dict:
    """
    Parse VALD molecular term description to extract molecular quantum numbers.

    CSV format: label,multiplicity,|Lambda|,parity,|Omega| or N,v
    Example: X,2,0,+,0.5,0 (case a) or a,1,2,0,113,0 (case b)
    - label: electronic state label (X, A, B, a, b, etc.)
    - multiplicity: 2S+1
    - |Lambda|: projection of orbital angular momentum (0=Sigma, 1=Pi, 2=Delta, etc.)
    - parity: +, -, 0, e, f (or sometimes empty)
    - |Omega| (case a) or N (case b): quantum number
    - v: vibrational quantum number

    Args:
        coupling: Hund's case indicator (e.g., 'Ha', 'Hb')

    Returns:
        dict with keys: elecstate, v, Lambda, Omega, s, p, j, rotN, config, term, coupling_case
    """
    if not term_desc or not term_desc.strip():
        return {}

    result = {}
    term = term_desc.strip()

    if ',' in term:
        fields = [f.strip() for f in term.split(',')]
        if len(fields) >= 6:
            # Field 0: electronic state label
            if fields[0] and fields[0] not in ('none', ''):
                result['elecstate'] = fields[0]

            # Field 1: multiplicity (2S+1)
            if fields[1] and fields[1].isdigit():
                multiplicity = int(fields[1])
                result['s'] = (multiplicity - 1) / 2.0

            # Field 2: |Lambda|
            if fields[2] and fields[2].isdigit():
                result['Lambda'] = int(fields[2])

            # Field 3: parity (+, -, 0, e, f)
            if fields[3] and fields[3] not in ('', 'none'):
                parity_val = fields[3]
                if parity_val in ('e', 'f'):
                    # Kronig parity (e/f parity)
                    result['kronig_parity'] = parity_val
                else:
                    # Total parity (+, -, 0)
                    result['p'] = parity_val

            # Field 4: |Omega| (case a) or N (case b)
            if fields[4] and fields[4] not in ('', 'none'):
                try:
                    value = parse_fraction(fields[4])
                    if coupling == 'Hb':
                        # Hund's case (b): field 4 is N (rotational QN)
                        if value % 1 == 0:
                            result['rotN'] = int(value)
                    else:
                        # Hund's case (a) or unknown: field 4 is Omega
                        result['Omega'] = value
                except:
                    pass

            # Field 5: vibrational quantum number v
            if fields[5] and fields[5].isdigit():
                result['v'] = int(fields[5])

            # Field 6 (optional): electronic inversion parity (g/u) or asSym (a/s)
            if len(fields) >= 7 and fields[6] and fields[6] not in ('', 'none'):
                inv_val = fields[6]
                if inv_val in ('g', 'u'):
                    result['elec_inversion'] = inv_val
                elif inv_val in ('a', 's'):
                    result['asSym'] = inv_val

    if j is not None:
        result['j'] = j

    if coupling and coupling.strip() in ('Ha', 'Hb'):
        result['coupling_case'] = coupling.strip()

    result['term'] = term_desc.strip()

    return result


class SpeciesTypeCache:
    """Cache for species types to avoid repeated database lookups"""
    def __init__(self):
        self._cache = {}

    def is_molecule(self, species_id: int) -> bool:
        """Check if species is a molecule (ncomp > 1)"""
        if species_id not in self._cache:
            from node.models import Species
            try:
                species = Species.objects.get(id=species_id)
                self._cache[species_id] = species.isMolecule()
            except Species.DoesNotExist:
                # If species doesn't exist, assume atomic (safer default)
                self._cache[species_id] = False
        return self._cache[species_id]

    def clear(self):
        """Clear the cache"""
        self._cache.clear()


# Global species type cache
_species_cache = SpeciesTypeCache()


def parse_quantum_numbers(species_id: int, j: Optional[float],
                         coupling: str, term_desc: str,
                         level_desc: str = None) -> dict:
    """
    Parse VALD term description to extract quantum numbers.

    Automatically detects molecular vs atomic terms based on species type.

    Based on parse_vald_term.c logic from VALD.

    Args:
        species_id: Species identifier (determines if molecular or atomic)
        j: Total angular momentum J
        coupling: Coupling scheme flag ('LS', 'JJ', 'JK', 'LK', or other for atoms)
        term_desc: Term name/description
                   Atomic: e.g., '2F*', '(6,7/2)*', '2[11/2]'
                   Molecular: e.g., 'X 2Pi v=0 J=1.5', 'A 1Sigma+ v=5'
                   Can be full level (config + term) - will be split automatically
        level_desc: Full level description including electronic config (needed for JK/LK Jc extraction)

    Returns:
        dict with keys: config, term, l, s, p, j1, j2, k, s2, jc, sn, n (atomic)
                    or: elecstate, v, Lambda, Sigma, Omega, s, p, j, rotN (molecular)
        Only non-None values are included.
    """
    if not term_desc or not term_desc.strip():
        return {}

    # Use species type to determine parser
    if _species_cache.is_molecule(species_id):
        return parse_molecular_quantum_numbers(species_id, j, term_desc, coupling)

    full_level = term_desc.strip()

    # Split electronic configuration from term name
    # VALD format: spaces within config are escaped as backslash-space (\ )
    # Config and term are separated by unescaped space
    # Split on first space NOT preceded by backslash
    config = ''
    term = full_level

    if ' ' in full_level and not full_level.startswith('('):
        # Match: (config)(unescaped space)(term)
        match = re.match(r'^(.*?)(?<!\\)\s+(.+)$', full_level)
        if match:
            config = match.group(1).strip()
            term = match.group(2).strip()

    result = {
        'config': config if config else None,
        'term': term if term else None
    }

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
                if multiplicity > 0:
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
                if multiplicity > 0:
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
    Parse VALD reference line (space-separated format).

    First field can be:
    - "wl:key1" -> wave_ref = "key1"
    - "wl:key1,iso:key2" -> wave_ref = "key1,key2"
    - "wl:key1,wl:key2" -> wave_ref = "key1,key2"

    Remaining fields are reference codes for the 9 data columns.

    Returns dict with 'wave_ref' and 'ref_codes' (list of 9 reference strings)
    """
    parts = ref_line.strip().split()
    refs = {}

    # Parse first field which may contain comma-separated type:key pairs
    if parts and ':' in parts[0]:
        # Split by comma to handle "wl:key1,iso:key2" or "wl:key1,wl:key2"
        wl_parts = parts[0].split(',')
        keys = []
        for wl_part in wl_parts:
            if ':' in wl_part:
                key = wl_part.split(':', 1)[1]
                keys.append(key)

        # Store comma-separated keys in wave_ref
        refs['wave_ref'] = ','.join(keys) if keys else None
    else:
        refs['wave_ref'] = None

    # Collect all reference codes (there should be 9 total)
    # The first field may have multiple comma-separated pairs, but we only use the first key for ref_codes[0]
    ref_codes = []
    for i, part in enumerate(parts):
        if i == 0:
            # First field: extract first key only for ref_codes
            if ':' in part:
                first_pair = part.split(',')[0]
                if ':' in first_pair:
                    ref_codes.append(first_pair.split(':', 1)[1])
                else:
                    ref_codes.append(None)
            else:
                ref_codes.append(part)
        else:
            # Remaining fields: extract key if type:key format, otherwise use as-is
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
        self.cache = {}  # (species, energy_scaled, j) -> state_id
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
                    J REAL
                )
            """)

            cursor.execute("DELETE FROM temp_state_lookup")

            cursor.executemany(
                "INSERT INTO temp_state_lookup VALUES (?, ?, ?)",
                uncached
            )

            cursor.execute("""
                SELECT s.id, s.species_id, s.energy_scaled, s.J
                FROM states s
                INNER JOIN temp_state_lookup t
                ON s.species_id = t.species_id
                   AND s.energy_scaled = t.energy_scaled
                   AND (s.J = t.J OR (s.J IS NULL AND t.J IS NULL))
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


# =============================================================================
# IMPORT FUNCTIONS
# =============================================================================

def import_states(input_file=None, batch_size=10000, skip_header=2, verbose=True, node_pkg='node'):
    """
    Import states from VALD format (Pass 1)

    Args:
        node_pkg: Node package name ('node' or 'node_molec')

    Returns: (total_processed, total_inserted)
    """
    # Import Django models (will fail if not in Django context)
    import importlib
    node_models = importlib.import_module(f'{node_pkg}.models')
    State = node_models.State
    from node.models import LineList
    from django.db import transaction, connection

    # Temporarily disable foreign key constraints for import
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")

    # Load linelist method lookup
    linelist_methods = {ll.id: ll.method for ll in LineList.objects.all()}
    if verbose:
        print(f'Loaded {len(linelist_methods)} linelist method mappings')

    input_stream = open_input(input_file)
    records = parse_vald_stream(input_stream, skip_header)

    total_processed = 0
    total_inserted = 0

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

            # Extract lower state (use ll3 for energy method)
            lower_energy_method = linelist_methods.get(row.get('ll3'))

            # Build state kwargs conditionally based on model fields
            lower_state_kwargs = {
                'species_id': species_id,
                'energy': lower_energy,
                'energy_scaled': lower_energy_scaled,
                'energy_method': lower_energy_method,
                'j': row['lower_j'],
                'lande': row['lower_lande'],
                'config': lower_qn.get('config'),
                'term': lower_qn.get('term'),
                's': lower_qn.get('s'),
                'p': lower_qn.get('p'),
                'n': lower_qn.get('n'),
            }

            # Add atomic-specific fields if they exist in the model
            if hasattr(State, 'l'):
                lower_state_kwargs.update({
                    'l': lower_qn.get('l'),
                    'j1': lower_qn.get('j1'),
                    'j2': lower_qn.get('j2'),
                    'k': lower_qn.get('k'),
                    's2': lower_qn.get('s2'),
                    'jc': lower_qn.get('jc'),
                    'sn': lower_qn.get('sn'),
                })

            # Add molecular-specific fields if they exist in the model
            if hasattr(State, 'v'):
                lower_state_kwargs.update({
                    'v': lower_qn.get('v'),
                    'Lambda': lower_qn.get('Lambda'),
                    'Sigma': lower_qn.get('Sigma'),
                    'Omega': lower_qn.get('Omega'),
                    'rotN': lower_qn.get('rotN'),
                    'elecstate': lower_qn.get('elecstate'),
                })

            states.append(State(**lower_state_kwargs))

            # Extract upper state (use ll4 for energy method)
            upper_energy_method = linelist_methods.get(row.get('ll4'))

            # Build state kwargs conditionally based on model fields
            upper_state_kwargs = {
                'species_id': species_id,
                'energy': upper_energy,
                'energy_scaled': upper_energy_scaled,
                'energy_method': upper_energy_method,
                'j': row['upper_j'],
                'lande': row['upper_lande'],
                'config': upper_qn.get('config'),
                'term': upper_qn.get('term'),
                's': upper_qn.get('s'),
                'p': upper_qn.get('p'),
                'n': upper_qn.get('n'),
            }

            # Add atomic-specific fields if they exist in the model
            if hasattr(State, 'l'):
                upper_state_kwargs.update({
                    'l': upper_qn.get('l'),
                    'j1': upper_qn.get('j1'),
                    'j2': upper_qn.get('j2'),
                    'k': upper_qn.get('k'),
                    's2': upper_qn.get('s2'),
                    'jc': upper_qn.get('jc'),
                    'sn': upper_qn.get('sn'),
                })

            # Add molecular-specific fields if they exist in the model
            if hasattr(State, 'v'):
                upper_state_kwargs.update({
                    'v': upper_qn.get('v'),
                    'Lambda': upper_qn.get('Lambda'),
                    'Sigma': upper_qn.get('Sigma'),
                    'Omega': upper_qn.get('Omega'),
                    'rotN': upper_qn.get('rotN'),
                    'elecstate': upper_qn.get('elecstate'),
                })

            states.append(State(**upper_state_kwargs))

        # Bulk insert with deduplication
        with transaction.atomic():
            initial_count = State.objects.count()
            bulk_insert_optimized(State, states, batch_size, ignore_conflicts=True)
            final_count = State.objects.count()
            inserted = final_count - initial_count

        total_processed += len(batch)
        total_inserted += inserted

    return total_processed, total_inserted


def import_transitions(input_file=None, batch_size=10000, skip_header=2,
                      skip_calc=False, verbose=True, node_pkg='node'):
    """
    Import transitions from VALD format (Pass 2)

    Args:
        node_pkg: Node package name ('node' or 'node_molec')

    Van der Waals broadening is auto-detected:
    - If value < 0: stored as gammawaals
    - If value > 0: integer part = sigmawaals, fractional part = alphawaals

    Returns: total_processed
    """
    import importlib
    node_models = importlib.import_module(f'{node_pkg}.models')
    State = node_models.State
    Transition = node_models.Transition
    from node.models import LineList
    from django.db import transaction, connection

    # Temporarily disable foreign key constraints for import
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")

    # Load linelist method lookup
    linelist_methods = {ll.id: ll.method for ll in LineList.objects.all()}
    if verbose:
        print(f'Loaded {len(linelist_methods)} linelist method mappings')

    input_stream = open_input(input_file)
    state_cache = StateCache()
    records = parse_vald_stream(input_stream, skip_header)

    total_processed = 0

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
                loggf_error = accuracy_to_loggf_error(
                    row.get('accurflag'),
                    row.get('accuracy')
                )

                transition_type, autoionized = parse_transition_properties(
                    row.get('transition_flag'),
                    row.get('lower_energy'),
                    row.get('upper_energy')
                )

                wave_method = linelist_methods.get(row.get('ll1'))

                # Auto-detect van der Waals format
                gammawaals_val, alphawaals_val, sigmawaals_val = parse_waals_broadening(
                    row.get('gammawaals_raw')
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
                    wave_method=wave_method,
                    gammarad=row.get('gammarad'),
                    gammastark=row.get('gammastark'),
                    gammawaals=gammawaals_val,
                    alphawaals=alphawaals_val,
                    sigmawaals=sigmawaals_val,
                    accurflag=row.get('accurflag'),
                    accur=row.get('accuracy'),
                    loggf_err=loggf_error,
                    transition_type=transition_type,
                    autoionized=autoionized,
                ))
            except ValueError as e:
                print(f"Warning: Skipping row: {e}", file=sys.stderr)
                continue

        # Bulk insert
        with transaction.atomic():
            bulk_insert_optimized(Transition, transitions, batch_size)

        total_processed += len(batch)

    if verbose:
        print(f'Done! Imported {total_processed} transitions.')
        print(f'State cache stats: {state_cache.hits} hits, {state_cache.misses} misses')

    # Calculate derived fields
    if not skip_calc:
        if verbose:
            print('Calculating Einstein A coefficients...')

        if connection.vendor == 'sqlite':
            # SQLite 3.33+: use UPDATE FROM for better performance
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE transitions
                    SET einsteina = (0.667025 * POWER(10, 16) * POWER(10, loggf))
                                  / ((2.0 * states.J + 1.0) * POWER(wave, 2))
                    FROM states
                    WHERE transitions.upstate = states.id
                      AND transitions.einsteina IS NULL
                      AND transitions.loggf IS NOT NULL
                """)
        else:
            # PostgreSQL/MySQL: JOIN syntax
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE transitions t
                    SET einsteina = (0.667025 * POWER(10, 16) * POWER(10, t.loggf))
                                  / ((2.0 * s.J + 1.0) * POWER(t.wave, 2))
                    FROM states s
                    WHERE t.upstate = s.id AND t.einsteina IS NULL
                """)

        if verbose:
            print('Einstein A calculated')

    return total_processed


def import_states_transitions(input_file=None, batch_size=10000, skip_header=2,
                              skip_calc=False, read_ahead=True, verbose=True, node_pkg='node'):
    """
    Combined single-pass import of states and transitions from VALD format.

    For each batch:
    1. Extract and insert states (lower and upper)
    2. Prefetch just-inserted state IDs
    3. Create and insert transitions using those state IDs

    Memory-efficient for large datasets - only one batch in memory at a time.

    Van der Waals broadening is auto-detected:
    - If value < 0: stored as gammawaals
    - If value > 0: integer part = sigmawaals, fractional part = alphawaals

    Args:
        node_pkg: Node package name ('node' or 'node_molec')
        read_ahead: If True, read and parse in separate thread to keep extraction
                   tool running at full speed. Safe with SQLite (no locking issues).

    Returns: (total_processed, total_states_inserted, total_transitions_inserted)
    """
    import importlib
    node_models = importlib.import_module(f'{node_pkg}.models')
    State = node_models.State
    Transition = node_models.Transition
    from node.models import LineList
    from django.db import transaction, connection

    # Temporarily disable foreign key constraints for import
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA foreign_keys = OFF")

    # Load linelist method lookup
    linelist_methods = {ll.id: ll.method for ll in LineList.objects.all()}
    if verbose:
        print(f'Loaded {len(linelist_methods)} linelist method mappings')

    input_stream = open_input(input_file)
    state_cache = StateCache()

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
            lower_energy_method = linelist_methods.get(row.get('ll3'))

            ref_codes = row.get('ref_codes', [None]*9)
            lower_energy_ref = ref_codes[2]
            lower_lande_ref = ref_codes[4]
            lower_level_ref = ref_codes[8]

            # Build state row conditionally based on model fields
            lower_row = [
                species_id, lower_energy, lower_energy_scaled, lower_energy_method, lower_j, lower_lande,
                lower_qn.get('config'), lower_qn.get('term'),
                lower_qn.get('s'), lower_qn.get('p'), lower_qn.get('n')
            ]

            # Add atomic fields if model has them
            if hasattr(State, 'l'):
                lower_row.extend([
                    lower_qn.get('l'), lower_qn.get('j1'), lower_qn.get('j2'),
                    lower_qn.get('k'), lower_qn.get('s2'), lower_qn.get('jc'), lower_qn.get('sn')
                ])

            # Add molecular fields if model has them
            if hasattr(State, 'v'):
                lower_row.extend([
                    lower_qn.get('v'), lower_qn.get('Lambda'), lower_qn.get('Sigma'),
                    lower_qn.get('Omega'), lower_qn.get('rotN'), lower_qn.get('elecstate'),
                    lower_qn.get('coupling_case'), lower_qn.get('kronig_parity'),
                    lower_qn.get('elec_inversion'), lower_qn.get('asSym')
                ])

            # Add reference fields
            lower_row.extend([lower_energy_ref, lower_lande_ref, lower_level_ref])
            state_rows.append(tuple(lower_row))

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
            upper_energy_method = linelist_methods.get(row.get('ll4'))

            upper_energy_ref = ref_codes[3]
            upper_lande_ref = ref_codes[4]
            upper_level_ref = ref_codes[8]

            # Build state row conditionally based on model fields
            upper_row = [
                species_id, upper_energy, upper_energy_scaled, upper_energy_method, upper_j, upper_lande,
                upper_qn.get('config'), upper_qn.get('term'),
                upper_qn.get('s'), upper_qn.get('p'), upper_qn.get('n')
            ]

            # Add atomic fields if model has them
            if hasattr(State, 'l'):
                upper_row.extend([
                    upper_qn.get('l'), upper_qn.get('j1'), upper_qn.get('j2'),
                    upper_qn.get('k'), upper_qn.get('s2'), upper_qn.get('jc'), upper_qn.get('sn')
                ])

            # Add molecular fields if model has them
            if hasattr(State, 'v'):
                upper_row.extend([
                    upper_qn.get('v'), upper_qn.get('Lambda'), upper_qn.get('Sigma'),
                    upper_qn.get('Omega'), upper_qn.get('rotN'), upper_qn.get('elecstate'),
                    upper_qn.get('coupling_case'), upper_qn.get('kronig_parity'),
                    upper_qn.get('elec_inversion'), upper_qn.get('asSym')
                ])

            # Add reference fields
            upper_row.extend([upper_energy_ref, upper_lande_ref, upper_level_ref])
            state_rows.append(tuple(upper_row))

        # Direct SQL insert (faster than Django ORM)
        # Build SQL dynamically based on which fields exist in the model
        with transaction.atomic():
            initial_state_count = State.objects.count()
            with connection.cursor() as cursor:
                # Build column list based on model fields
                base_cols = 'species_id, energy, energy_scaled, energy_method, J, lande, config, term, S, P, n'
                base_placeholders = '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'

                # Check if atomic fields exist
                if hasattr(State, 'l'):
                    atomic_cols = ', L, J1, J2, K, S2, Jc, Sn'
                    atomic_placeholders = ', ?, ?, ?, ?, ?, ?, ?'
                else:
                    atomic_cols = ''
                    atomic_placeholders = ''

                # Check if molecular fields exist
                if hasattr(State, 'v'):
                    molec_cols = ', v, Lambda, Sigma, Omega, rotN, elecstate, coupling_case, kronig_parity, elec_inversion, asSym'
                    molec_placeholders = ', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?'
                else:
                    molec_cols = ''
                    molec_placeholders = ''

                ref_cols = ', energy_ref_id, lande_ref_id, level_ref_id'
                ref_placeholders = ', ?, ?, ?'

                sql = f"INSERT OR IGNORE INTO states ({base_cols}{atomic_cols}{molec_cols}{ref_cols}) VALUES ({base_placeholders}{atomic_placeholders}{molec_placeholders}{ref_placeholders})"
                cursor.executemany(sql, state_rows)
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

                # Get state IDs
                upstate_id = state_cache.get_state_id(
                    species_id, row['_upper_energy_scaled'],
                    row['upper_j'], row['upper_term'] or None
                )
                lostate_id = state_cache.get_state_id(
                    species_id, row['_lower_energy_scaled'],
                    row['lower_j'], row['lower_term'] or None
                )

                loggf_error = accuracy_to_loggf_error(
                    row.get('accurflag'),
                    row.get('accuracy')
                )

                transition_type, autoionized = parse_transition_properties(
                    row.get('transition_flag'),
                    row.get('lower_energy'),
                    row.get('upper_energy')
                )

                wave_method = linelist_methods.get(row.get('ll1'))

                # Auto-detect van der Waals format
                gammawaals_val, alphawaals_val, sigmawaals_val = parse_waals_broadening(
                    row.get('gammawaals_raw')
                )

                ref_codes = row.get('ref_codes', [None]*9)
                wave_ref = row.get('wave_ref')
                loggf_ref = ref_codes[1]
                gammarad_ref = ref_codes[5]
                gammastark_ref = ref_codes[6]
                waals_ref = ref_codes[7]

                transition_rows.append((
                    upstate_id, lostate_id, species_id,
                    row['wave'], row['wave_ritz'], row['loggf'], wave_method,
                    row.get('gammarad'), row.get('gammastark'), gammawaals_val,
                    alphawaals_val, sigmawaals_val,
                    row.get('accurflag'), row.get('accuracy'), loggf_error,
                    transition_type, autoionized,
                    wave_ref, wave_ref, loggf_ref, gammarad_ref, gammastark_ref, waals_ref
                ))
            except ValueError as e:
                print(f"Warning: Skipping transition: {e}", file=sys.stderr)
                continue

        # Direct SQL insert (faster than Django ORM)
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO transitions (upstate, lostate, species_id, wave, waveritz, loggf, wave_method, gammarad, gammastark, gammawaals, alphawaals, sigmawaals, accurflag, accur, loggf_err, transition_type, autoionized, wave_ref_id, waveritz_ref_id, loggf_ref_id, gammarad_ref_id, gammastark_ref_id, waals_ref_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    transition_rows
                )

        total_transitions_inserted += len(transition_rows)
        total_processed += len(batch)

    if verbose:
        print(f'Processed {total_processed} lines')
        print(f'Inserted {total_states_inserted} unique states')
        print(f'Inserted {total_transitions_inserted} transitions')
        print(f'State cache: {state_cache.hits} hits, {state_cache.misses} misses')

    # Calculate derived fields
    if not skip_calc:
        if verbose:
            print('Calculating Einstein A coefficients...')

        if connection.vendor == 'sqlite':
            # SQLite 3.33+: use UPDATE FROM for better performance
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE transitions
                    SET einsteina = (0.667025 * POWER(10, 16) * POWER(10, loggf))
                                  / ((2.0 * states.J + 1.0) * POWER(wave, 2))
                    FROM states
                    WHERE transitions.upstate = states.id
                      AND transitions.einsteina IS NULL
                      AND transitions.loggf IS NOT NULL
                """)
        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE transitions t
                    SET einsteina = (0.667025 * POWER(10, 16) * POWER(10, t.loggf))
                                  / ((2.0 * s.J + 1.0) * POWER(t.wave, 2))
                    FROM states s
                    WHERE t.upstate = s.id AND t.einsteina IS NULL
                """)

        if verbose:
            print('Einstein A calculated')

    # Update ground_state_id for all species
    if verbose:
        print('Setting ground state references...')

    with connection.cursor() as cursor:
        # For each species, find the state with minimum energy and set it as ground_state_id
        cursor.execute("""
            UPDATE species
            SET ground_state_id = (
                SELECT id FROM states
                WHERE states.species_id = species.id
                ORDER BY states.energy ASC
                LIMIT 1
            )
        """)

    if verbose:
        updated = cursor.rowcount if hasattr(cursor, 'rowcount') else 'N/A'
        print(f'Ground state references set (updated {updated} species)')

    return total_processed, total_states_inserted, total_transitions_inserted


# =============================================================================
# SPECIES IMPORT
# =============================================================================

def import_species(input_file, batch_size=10000, verbose=True):
    """
    Import species from CSV file (VALD List of Species format)

    Format: comma-separated with header
    Use,Index,Name,Charge,InChI,InChIkey,Mass,Ion. en.,Fract.,Num. comp.,N1,N2,N3,N4,Dummy

    For molecules (Num. comp. > 1), also populates the SpeciesComp table
    to establish molecule-atom relationships using N1, N2, N3, N4 columns.

    Returns: (total_processed, total_inserted)
    """
    from node.models import Species, SpeciesComp
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
        component_list = []
        total_processed = 0

        for row in reader:
            try:
                # Ignore Use field - import all species
                # use = row.get('Use', '1').strip()
                # if use != '1':
                #     continue

                species_id = int(row['Index'])
                ncomp = int(row['Num. comp.']) if row['Num. comp.'].strip() else None

                species = Species(
                    id=species_id,
                    name=row['Name'].strip(),
                    ion=int(row['Charge']) if row['Charge'].strip() else None,
                    inchi=row['InChI'].strip() if row['InChI'].strip() else None,
                    inchikey=row['InChIkey'].strip() if row['InChIkey'].strip() else None,
                    mass=float(row['Mass']) if row['Mass'].strip() else None,
                    massno=int(float(row['Mass'])) if row['Mass'].strip() else None,
                    ionen=float(row['Ion. en.']) if row['Ion. en.'].strip() else None,
                    solariso=float(row['Fract.']) if row['Fract.'].strip() else None,
                    ncomp=ncomp,
                    atomic=int(row['N1']) if row['N1'].strip() else None,
                )
                species_list.append(species)

                # For molecules, create component relationships
                if ncomp and ncomp > 1:
                    # N1-N4 contain species IDs of component atoms
                    for i, col in enumerate(['N1', 'N2', 'N3', 'N4'], 1):
                        if i > ncomp:
                            break
                        atom_species_id_str = row.get(col, '').strip()
                        if atom_species_id_str:
                            # N1-N4 are already species IDs, not atomic numbers
                            atom_species_id = int(atom_species_id_str)
                            component_list.append({
                                'molecule_id': species_id,
                                'atom_id': atom_species_id
                            })

                total_processed += 1

                if len(species_list) >= batch_size:
                    with transaction.atomic():
                        Species.objects.bulk_create(
                            species_list,
                            batch_size=batch_size,
                            ignore_conflicts=True
                        )
                        # Insert components after species are created
                        # Only create if both molecule and atom species exist
                        if component_list:
                            for comp in component_list:
                                try:
                                    # Check if both species exist
                                    if Species.objects.filter(id=comp['molecule_id']).exists() and \
                                       Species.objects.filter(id=comp['atom_id']).exists():
                                        SpeciesComp.objects.get_or_create(
                                            molecule_id=comp['molecule_id'],
                                            atom_id=comp['atom_id']
                                        )
                                except Exception as e:
                                    if verbose:
                                        print(f"Warning: Could not create component {comp['molecule_id']}->{comp['atom_id']}: {e}", file=sys.stderr)
                    species_list = []
                    component_list = []

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
                # Insert components after species are created
                # Only create if both molecule and atom species exist
                if component_list:
                    for comp in component_list:
                        try:
                            # Check if both species exist
                            if Species.objects.filter(id=comp['molecule_id']).exists() and \
                               Species.objects.filter(id=comp['atom_id']).exists():
                                SpeciesComp.objects.get_or_create(
                                    molecule_id=comp['molecule_id'],
                                    atom_id=comp['atom_id']
                                )
                        except Exception as e:
                            if verbose:
                                print(f"Warning: Could not create component {comp['molecule_id']}->{comp['atom_id']}: {e}", file=sys.stderr)

    inserted_count = Species.objects.count()

    return total_processed, inserted_count


# =============================================================================
# HYPERFINE STRUCTURE CONSTANTS IMPORT
# =============================================================================

def import_hfs(input_file, batch_size=1000, verbose=True, energy_tolerance=1.0, node_pkg='node'):
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
        node_pkg: Node package name ('node' or 'node_molec')

    Returns: (total_processed, matched, multiple_matches, no_match)
    """

    import importlib
    node_models = importlib.import_module(f'{node_pkg}.models')
    State = node_models.State
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

            for state in candidates:
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

    from node.models import Reference
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
                            references = []
                    except Exception as e:
                        if verbose:
                            print(f"Warning: Failed to process entry {bibtex_key}: {e}", file=sys.stderr)

                current_entry = []
                brace_count = 0

    # Handle last entry
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

    # Insert remaining references
    if references:
        with transaction.atomic():
            Reference.objects.bulk_create(
                references,
                batch_size=batch_size,
                ignore_conflicts=True
            )

    inserted_count = Reference.objects.count()

    return total_processed, inserted_count


# =============================================================================
# LINELIST IMPORT
# =============================================================================

METHOD_TYPE_MAP = {
    'exp': 0,   # experiment
    'obs': 1,   # observed
    'emp': 2,   # empirical
    'pred': 3,  # theory (predicted)
    'calc': 4,  # semiempirical (calculated)
    'mix': 5,   # compilation
    'comp': 5   # compilation (alternative name)
}


def import_linelists(input_file, batch_size=1000, verbose=True):
    """
    Import linelist metadata from linelists.dat file.

    File format (tab-separated):
    - Column 1: basename (srcfile)
    - Column 2: id (primary key)
    - Column 3: listtype (string, can be empty)
    - Column 4: method type integer (0-5, or -1 for unmapped)

    Returns: (total_processed, total_inserted)
    """

    from node.models import LineList
    from django.db import transaction

    linelists = []
    total_processed = 0

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) < 4:
                if verbose:
                    print(f"Warning: Skipping malformed line: {line}", file=sys.stderr)
                continue

            srcfile = parts[0]

            try:
                linelist_id = int(parts[1])
            except ValueError:
                if verbose:
                    print(f"Warning: Invalid ID in line: {line}", file=sys.stderr)
                continue

            listtype = parts[2].strip() if parts[2].strip() else None

            try:
                method = int(parts[3])
                # Convert -1 to None (unmapped types)
                if method < 0:
                    method = None
            except ValueError:
                method = None

            linelist = LineList(
                id=linelist_id,
                srcfile=srcfile,
                listtype=listtype,
                method=method
            )
            linelists.append(linelist)
            total_processed += 1

            if len(linelists) >= batch_size:
                with transaction.atomic():
                    LineList.objects.bulk_create(
                        linelists,
                        batch_size=batch_size,
                        ignore_conflicts=True
                    )
                linelists = []

    # Insert remaining
    if linelists:
        with transaction.atomic():
            LineList.objects.bulk_create(
                linelists,
                batch_size=batch_size,
                ignore_conflicts=True
            )

    inserted_count = LineList.objects.count()

    return total_processed, inserted_count


# =============================================================================
# STANDALONE CLI
# =============================================================================

def main():
    """Standalone command-line interface"""
    import argparse

    parser = argparse.ArgumentParser(description='VALD Data Import')

    # Global arguments (before subparsers)
    parser.add_argument('--settings', type=str, default=None,
                       help='Django settings module to use. '
                            'Use settings_molec for molecular data, settings_atom for atomic. '
                            'If not specified, uses DJANGO_SETTINGS_MODULE env var, or settings_dev as fallback.')

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

    # Linelists import command
    linelist_parser = subparsers.add_parser('import-linelists',
                                        help='Import linelist metadata from linelists.dat')
    linelist_parser.add_argument('--file', type=str, required=True,
                            help='linelists.dat file (tab-separated)')
    linelist_parser.add_argument('--batch-size', type=int, default=1000)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Setup Django environment
    import os
    # Priority: --settings argument > env variable > default
    if args.settings:
        # User explicitly provided --settings, use it
        os.environ['DJANGO_SETTINGS_MODULE'] = args.settings
    elif 'DJANGO_SETTINGS_MODULE' not in os.environ:
        # No --settings and no env var, use default (matches manage.py)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    # else: env var is already set, use it

    import django
    django.setup()

    # Detect node package from Django settings
    from django.conf import settings
    node_pkg = getattr(settings, 'NODEPKG', 'node')
    if verbose := getattr(args, 'verbose', True):
        print(f'Using settings: {args.settings}')
        print(f'Using node package: {node_pkg}')
        print(f'Database: {settings.DATABASES["default"]["NAME"]}')

    # Run appropriate command
    if args.command == 'import-states':
        processed, inserted = import_states(
        input_file=args.file,
        batch_size=args.batch_size,
        skip_header=args.skip_header,
        node_pkg=node_pkg
        )
        print(f'Done! Processed {processed} lines, inserted {inserted} unique states')

    elif args.command == 'import-transitions':
        processed = import_transitions(
        input_file=args.file,
        batch_size=args.batch_size,
        skip_header=args.skip_header,
        skip_calc=args.skip_calc,
        node_pkg=node_pkg
        )
        print(f'Done! Imported {processed} transitions')

    elif args.command == 'import-states-transitions':
        processed, states_inserted, trans_inserted = import_states_transitions(
        input_file=args.file,
        batch_size=args.batch_size,
        skip_header=args.skip_header,
        skip_calc=args.skip_calc,
        read_ahead=not args.no_read_ahead,
        node_pkg=node_pkg
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
        energy_tolerance=args.energy_tolerance,
        node_pkg=node_pkg
        )
        print(f'Done! Processed {total} HFS records')
        print(f'Matched: {matched}, Multiple candidates: {multiple}, No match: {no_match}')

    elif args.command == 'import-linelists':
        processed, inserted = import_linelists(
        input_file=args.file,
        batch_size=args.batch_size
        )
        print(f'Done! Processed {processed} lines, inserted {inserted} total linelists')


if __name__ == '__main__':
    main()
