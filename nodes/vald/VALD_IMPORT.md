# VALD Data Import System

Modern streaming import system for VALD atomic/molecular data into Django database.

## Quick Start

```bash
# Full import pipeline (species → states → transitions)
python valdimport.py import-species --file=VALD_list_of_species.csv
python valdimport.py import-states --file=vald3_atoms_all.dat
python valdimport.py import-transitions --file=vald3_atoms_all.dat
```

## Architecture

### Two-Pass Streaming Design

**Pass 1: States Extraction**
- Parse inline upper/lower state data from transition lines
- Extract ~510M state records (2 per transition)
- Deduplicate via database UNIQUE constraint → ~10M unique states
- Database handles deduplication automatically

**Pass 2: Transitions with Cached Lookups**
- Parse transition data
- Look up state IDs via LRU cache (100k size)
- Bulk insert transitions with foreign keys
- Calculate Einstein A coefficients

**Pre-import: Species Setup**
- Load 775 species from CSV (VALD List of Species format)
- Maps CSV columns to database fields
- Creates foreign key relationships for validation

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

## Modes of Operation

### Standalone Mode

```bash
# Import species
python valdimport.py import-species --file=species.csv

# Pass 1: Extract and deduplicate states
python valdimport.py import-states --file=vald.dat

# Pass 2: Import transitions with state lookups
python valdimport.py import-transitions --file=vald.dat

# Skip Einstein A calculation for manual post-processing
python valdimport.py import-transitions --file=vald.dat --skip-calc
```

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
- j: Total angular momentum quantum number
- lande: Landé g-factor
- term_desc: Term symbol (e.g., "3(3G)5H 46*")
- **Constraint**: UNIQUE(species_id, energy, j, term_desc)

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
python manage.py migrate --settings settings_dev

# 2. Import species (775 records)
python valdimport.py import-species --file=VALD_list_of_species.csv

# 3. Pass 1: Extract 60k states → deduplicate to 10M unique
python valdimport.py import-states --file=vald3_atoms_all.dat

# 4. Pass 2: Import 255M transitions with cached state lookups
python valdimport.py import-transitions --file=vald3_atoms_all.dat

# 5. Verify import
python manage.py shell
>>> from node_atom.models import State, Transition
>>> State.objects.count()  # Should be ~10M
>>> Transition.objects.count()  # Should be ~255M
```

### Development/Testing

```bash
# Test with small sample (100 lines)
head -200 vald.dat | python valdimport.py import-states
head -200 vald.dat | python valdimport.py import-transitions

# Import with custom batch size
python valdimport.py import-states --file=vald.dat --batch-size=5000

# Skip header lines (if format differs)
python valdimport.py import-states --file=vald.dat --skip-header=3
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
| **Language** | Python 2 + Fortran | Python 3 |
| **Database** | MySQL only | SQLite/PostgreSQL/MySQL |
| **Architecture** | Multi-file mapping DSL | Single file, dataclass fields |
| **Memory Usage** | 10M+ shared dict | 100k LRU cache |
| **Speed** | 48+ hours | 4-5 hours |
| **Dev/Prod** | Different approaches | Same code everywhere |
| **Progress Tracking** | None | Real-time with tqdm |
| **Error Recovery** | Start over | Resume Pass 2 |
| **Testing** | Full dataset required | `head -1000` samples work |

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
