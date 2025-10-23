# VALD Data Import System

Modern streaming import system for VALD atomic/molecular data into Django database.

## Quick Start

```bash
# Full import pipeline (species → states+transitions → bibtex → hyperfine)
python valdimport.py import-species --file=VALD_list_of_species.csv
python valdimport.py import-combined --file=vald3_atoms_all.dat
python valdimport.py import-bibtex --file=VALD_ref.bib
python valdimport.py import-hfs --file=AB.db
```

## Architecture

### Import Architecture

**Combined Import (Recommended)**
- Single-pass streaming with batch processing
- Extract states → insert → prefetch IDs → insert transitions
- Memory-efficient: only one batch in memory at a time
- Background reader thread keeps extraction running at full speed
- Direct SQL for maximum performance

**Two-Pass Import (Legacy)**
- **Pass 1**: Extract all states, deduplicate via UNIQUE constraint
- **Pass 2**: Import transitions with cached state lookups
- Can resume Pass 2 if interrupted

**Pre-import: Species Setup**
- Load 775 species from CSV (VALD List of Species format)
- Maps CSV columns to database fields
- Creates foreign key relationships for validation

**Post-import: References & Hyperfine Structure**
- BibTeX references converted to XSAMS XML
- Hyperfine constants matched to existing states by quantum numbers

### Performance

Test results (30k lines):
- States: 60k extracted → 38k unique (98% dedup rate)
- Transitions: 30k imported with 56% cache hit rate
- Einstein A: Calculated for all 30k transitions
- Time: ~30 seconds total

Expected on production data (255M lines):
- SQLite: ~10 hours total
- PostgreSQL: ~4 hours (with COPY optimization)
- MySQL: ~5.5 hours

## Import Commands

### import-species
Import species from VALD List of Species CSV file.

```bash
python valdimport.py import-species --file=VALD_list_of_species.csv [--batch-size=10000]
```

### import-states (Pass 1)
Extract and deduplicate states from VALD transition data.

```bash
python valdimport.py import-states --file=vald.dat [--batch-size=10000] [--skip-header=2]
```

### import-transitions (Pass 2)
Import transitions with cached state lookups.

```bash
python valdimport.py import-transitions --file=vald.dat [--batch-size=10000] [--skip-calc]
```

### import-combined (Recommended)
Single-pass import of both states and transitions. More efficient for large datasets.

```bash
python valdimport.py import-combined --file=vald.dat [--batch-size=10000] [--skip-calc] [--no-read-ahead]
```

Options:
- `--skip-calc`: Skip Einstein A coefficient calculation
- `--no-read-ahead`: Disable background reader thread (enabled by default)

### import-bibtex
Import references from BibTeX file.

```bash
python valdimport.py import-bibtex --file=VALD_ref.bib [--batch-size=1000]
```

Converts BibTeX entries to:
- Reference.id = BibTeX key
- Reference.bibtex = raw BibTeX text
- Reference.xml = XSAMS XML format (via BibTeX2XML)

### import-hfs
Import hyperfine structure constants from AB.db SQLite database.

```bash
python valdimport.py import-hfs --file=AB.db [--batch-size=1000] [--energy-tolerance=0.01]
```

Matches AB.db records to existing states using:
- Species ID
- Energy (with tolerance, default ±0.01 cm⁻¹)
- Total angular momentum J
- Term description (for disambiguation)

Updates State records with:
- hfs_a: Hyperfine constant A (MHz)
- hfs_a_error: Error in A
- hfs_b: Hyperfine constant B (MHz)
- hfs_b_error: Error in B

### Django Management Commands

```bash
# Via Django management system
python manage.py import_states --file=vald.dat
python manage.py import_transitions --file=vald.dat
```

### Piping from stdin

```bash
# Direct from gzipped file
gunzip -c vald3_atoms_all.dat.gz | python valdimport.py import-states

# From pipe
cat vald_atoms.dat | python valdimport.py import-states --batch-size=5000
```

## File Formats

### Species CSV (VALD_list_of_species.csv)

```
#VER03.03,,,,,,,,,,,,,,
Use,Index,Name,Charge,InChI,InChIkey,Mass,Ion. en.,Fract.,Num. comp.,N1,N2,N3,N4,Dummy
1,1,H,0,InChI=1S/H,...
1,2,He,0,InChI=1S/He,...
```

- **Use**: 1 = import, 0 = skip
- **Index**: Unique species ID
- **Name**: Element/ion name
- **Charge**: Ionization state
- **InChI**: International Chemical Identifier
- **Mass**: Atomic mass (rounded to massno)
- **Ion. en.**: Ionization energy
- **Fract.**: Solar isotopic fraction

### Transition Data (vald3_atoms_all.dat)

Fixed-width FORTRAN format (from presformat5.f):
```
FORMAT(2F15.5,I6,F8.3,2(F14.4,F6.1),3F7.2,2F7.3,F8.3,A2,A86,A2,A86,1X,A1,A7,1X,A16,9I4)
```

Each transition record is 2 lines:
- Line 1: Data (wavelength, species_id, loggf, energies, J values, Landé factors, broadening, terms)
- Line 2: References (metadata keys, bibtex references)

Parser skips reference lines (start with lowercase).

## Database Configuration

### Required Models

**Species** (node_common/models.py):
- id: Primary key
- name: Element name (indexed)
- ion: Charge state
- inchi, inchikey: Chemical identifiers
- mass, massno: Atomic mass
- ionen: Ionization energy
- solariso: Solar abundance fraction
- ncomp: Number of components (molecules)

**State** (node_atom/models.py):
- id: Primary key
- species_id: Foreign key to Species
- energy: Energy in cm⁻¹ (indexed with species)
- energy_scaled: Energy × 10⁴ as integer (for fast matching)
- j: Total angular momentum quantum number
- lande: Landé g-factor
- term_desc: Term symbol (e.g., "3(3G)5H 46*")
- l, s, p, j1, j2, k, s2, jc, sn, n: Quantum numbers (parsed from term)
- hfs_a, hfs_a_error: Hyperfine constant A and error (MHz)
- hfs_b, hfs_b_error: Hyperfine constant B and error (MHz)
- **Constraint**: UNIQUE(species_id, energy_scaled, j, term_desc)

**Transition** (node_atom/models.py):
- id: Primary key (auto-increment)
- upstate, lostate: Foreign keys to State
- species_id: Foreign key to Species (indexed)
- wave, waveritz: Wavelengths (both indexed)
- loggf: log(gf) oscillator strength
- einsteina: Calculated Einstein A coefficient
- gammarad, gammastark, gammawaals: Broadening parameters
- accurflag, accur: Accuracy indicators

### Indexes Created

- states.species_id, states.energy (composite)
- transitions.species_id, transitions.wave (composite)
- transitions.wave, transitions.waveritz, transitions.einsteina (individual)

## Usage Examples

### Complete Import Workflow

```bash
# 1. Create fresh database
rm vald_dev.sqlite
python manage.py migrate

# 2. Import species (775 records)
python valdimport.py import-species --file=VALD_list_of_species.csv

# 3. Import states and transitions (combined, single pass)
# Using Python 3.14 for speed boost
uv run -p 3.14 valdimport.py import-combined --file=vald3_atoms_all.dat

# OR use two-pass import:
# python valdimport.py import-states --file=vald3_atoms_all.dat
# python valdimport.py import-transitions --file=vald3_atoms_all.dat

# 4. Import BibTeX references
python valdimport.py import-bibtex --file=VALD_ref.bib

# 5. Import hyperfine structure constants (optional)
python valdimport.py import-hfs --file=AB.db

# 6. Verify import
python manage.py shell
>>> from node_atom.models import State, Transition
>>> from node_common.models import Reference
>>> State.objects.count()  # Should be ~1.3M
>>> Transition.objects.count()  # Should be ~255M
>>> Reference.objects.count()  # Should match BibTeX entries
>>> State.objects.exclude(hfs_a__isnull=True).count()  # States with HFS data
```

### Development/Testing

```bash
# Test with small sample (100 lines)
head -200 vald.dat | python valdimport.py import-combined

# Import with custom batch size
python valdimport.py import-combined --file=vald.dat --batch-size=5000

# Skip header lines (if format differs)
python valdimport.py import-combined --file=vald.dat --skip-header=3

# Test HFS import on existing database
python valdimport.py import-hfs --file=AB.db --energy-tolerance=0.05
```

### Troubleshooting

**"Foreign key constraint failed"**
- Ensure Species are imported before States
- Check species.csv CSV format hasn't changed
- Verify species IDs in data match species.csv

**"State not found during transitions import"**
- States extraction (Pass 1) may have failed
- Try re-running Pass 1: states are deduplicated automatically
- Check for parse errors in stderr output

**"Column not found" errors**
- Verify database migrations are applied: `python manage.py migrate`
- Check your settings point to correct database

## Field Definitions

VALD fields are parsed using fixed-width positions (from presformat5.f):

```
Position Range   Field Name            Type        Description
0-15            wave_ritz             float       Vacuum wavelength (RITZ)
15-30           wave_measured         float       Measured wavelength
30-36           species_id            int         VALD species code
36-44           loggf                 float       log(gf) oscillator strength
44-58           lower_energy          float       Lower state energy (cm⁻¹)
58-64           lower_j               float       Lower state J value
64-78           upper_energy          float       Upper state energy (cm⁻¹)
78-84           upper_j               float       Upper state J value
84-91           lower_lande           float       Lower state Landé g-factor
91-98           upper_lande           float       Upper state Landé g-factor
98-105          mean_lande            float       Mean Landé g-factor
105-112         gammarad              float       Radiation damping
112-119         gammastark            float       Stark damping
119-127         gammawaals            float       Van der Waals damping
127-215         lower_term            string      Lower state term symbol
215-217         upper_term_flag       string      Upper state flag
217-303         upper_term            string      Upper state term symbol
304-305         accurflag             string      Accuracy flag
```

## Implementation Details

### FieldDef Dataclass

Self-documenting field definitions:
```python
@dataclass
class FieldDef:
    name: str                           # Field name
    start: int                          # Start position in line
    end: int                            # End position (exclusive)
    converter: Callable = str.strip     # Type converter (float, int, etc.)
    null_values: tuple = ('', 'X')      # Values treated as NULL
    description: str = ''               # Human-readable description
```

### StateCache

LRU cache for state lookups:
- Max size: 100,000 entries
- Typical hit rate: 50-99% depending on data distribution
- Key: (species_id, energy, j, term_desc)
- Value: state_id

### Database-Specific Optimization

**PostgreSQL**:
- Uses native COPY FROM STDIN (~50k rows/sec)
- JOIN syntax for Einstein A calculation

**MySQL/SQLite**:
- Uses Django bulk_create (~10-20k rows/sec)
- Subquery for Einstein A calculation

## Comparison with Legacy System

| Feature | Old (2012) | New (2025) |
|---------|-----------|-----------|
| **Language** | Python 2 + Fortran | Python 3.10+ |
| **Database** | MySQL only | SQLite/PostgreSQL/MySQL |
| **Architecture** | Multi-file mapping DSL | Single file, dataclass fields |
| **Memory Usage** | 10M+ shared dict | Batch streaming |
| **Speed** | 48+ hours | 4-5 hours (faster with Python 3.14) |
| **Dev/Prod** | Different approaches | Same code everywhere |
| **Progress Tracking** | None | Real-time with tqdm |
| **Error Recovery** | Start over | Resume or single-pass |
| **Testing** | Full dataset required | `head -1000` samples work |
| **Quantum Numbers** | Not parsed | Fully parsed (LS, JJ, JK, LK) |
| **References** | Manual SQL | BibTeX → XML conversion |
| **Hyperfine** | Not supported | A & B constants with errors |

## Maintenance

### Adding New Fields

Edit VALD_FIELDS in valdimport.py:
```python
VALD_FIELDS = [
    FieldDef('new_field', start=330, end=345, converter=float,
             description="New field from VALD3.3"),
    # ... existing fields ...
]
```

Then update model and create migration:
```bash
python manage.py makemigrations node_atom
python manage.py migrate
```

### Handling Format Changes

If VALD format changes:
1. Update field positions in VALD_FIELDS
2. Update header skip count: `--skip-header=N`
3. Test with sample: `head -1000 vald.dat | python valdimport.py import-states`

## Support

- Source: `valdimport.py` (single file)
- Tests: `tests/test_valdimport.py`
- Plan: `valdimport_plan.md`
- Models: `node_atom/models.py`, `node_common/models.py`
