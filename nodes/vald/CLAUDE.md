# Settings and databases
settings.py is an untracked symlink, currently to settings_all.py. settings_all.py and settings_obs.py
select vald_all.sqlite (~60 GB, ~271M transitions) and vald_obs.sqlite (~11 GB, ~44M transitions).
Deployed at https://vald.astro.uu.se/vamdc-all/tap/ and .../vamdc-obs/tap/ via vamdc-all.service and
vamdc-obs.service (gunicorn, 4 sync workers, -t 300, DJANGO_SETTINGS_MODULE set in the unit).

The DBs must have sqlite_stat1 (run a full ANALYZE after every import, ~2 min obs, ~21 min all).
Without it, SQLite picks the low-cardinality wave_method index over the wave range and a
MethodCategory query scans tens of millions of rows. PRAGMA analysis_limit sampling gives
useless stats here, so do not use it.

# Import of data via valdimport.py

## to make a new dev database from scratch
remakeDB.sh does the full sequence (check where settings.py points first!):
migrate, import-species, import-bibtex, import-linelists, import-states-transitions
(defatom.dat, defmolec.dat), import-hfs (AB.db), and finally ANALYZE.

## model changes
When the Django model changes, don't make a migration. Instead
remove node/migrations/0001*py and run
uv run manage.py makemigrations
before migrate as above.


## the import of states and transitions
In the incoming data, the states info is inlined within each record of transitions.
Therefore we need two passes on the import, first extract the states and write to db (deduplication) and then the transitions with the correct foreignkeys to its upper and lower states.

The "combined import" does both passes on each chunk of data, to allow piping data to the import only once.

uv run valdimport.py import-states-transitions --file=dump

## info on the incoming data format
The FORTRAN code that produces the data is presformat5.f, locally at ~/VALD3/SOURCE/SELECT/presformat5.f

### molecular term format
Molecular states use a CSV format embedded in the term field: `label,multiplicity,|Λ|,parity,|Ω| or N,v[,g/u]`
- label: electronic state label (X, A, B, a, b, etc.)
- multiplicity: 2S+1
- |Λ|: projection of orbital angular momentum (0=Sigma, 1=Pi, 2=Delta, etc.)
- parity: +, -, 0 (merged Λ-doubling), e, f (Kronig parity)
- |Ω| or N: depends on coupling case - field 4 is Ω for Hund's case (a), N for case (b)
- v: vibrational quantum number
- g/u (optional): electronic wavefunction inversion parity for homonuclear molecules

Example: `X,2,0,e,0.5,0` (case a) or `a,1,2,0,113,0,g` (case b with g/u)

The coupling_case field (Ha/Hb) determines how to interpret field 4. See DiatomicMolecularLevels.pdf for full specification.

# concerning the XSAMS XML output

## XSAMS schema and output generation
XSAMS (VAMDC Atomic and Molecular Data Schema) is the XML format used to return query results. The schema definition files are in ../../../xsams.git/ with the main types in typesAttributes.xsd and radiative transitions in radiative.xsd. The schema defines DataType as a complex type that can contain Value, Evaluation (qualitative quality grades), and Accuracy (quantitative uncertainties). Both Evaluation and Accuracy elements can coexist on the same DataType.

## dictionaries.py and generators.py
node/dictionaries.py maps Django model fields and methods to XSAMS keywords using the RETURNABLES dict. For DataType elements like Log10WeightedOscillatorStrength, append suffixes like Accuracy, AccuracyType, AccuracyRelative for numerical errors, and Eval, EvalComment for quality grades. The vamdctap/generators.py file (in ../../vamdctap/) contains the makeDataType, makeAccuracy, and makeEvaluation functions that build the actual XML from these mappings, automatically looking for the suffixed keywords to populate the appropriate XSAMS elements.

## loggf accuracy information
The transitions.accurflag field indicates the type of accuracy: 'N' for NIST quality classes (letter grades like A, AA+, D-), 'E' for estimated error in dex, 'C' for cancellation factor, 'P' for predicted, or '_' for general quality indicators. The transitions.accur field holds the raw accuracy text (either letter grades or numeric values), while transitions.loggf_err contains the calculated numerical error in dex converted via accuracy_to_loggf_error(). In XSAMS output, letter grades go to Evaluation/Quality elements and numerical errors go to Accuracy elements with appropriate type attributes (estimated/arbitrary/systematic).

## molecular quantum numbers
Molecular states store quantum numbers in dedicated fields parsed from the term description. The p field stores total parity (+, -, 0) but '0' is filtered out by parity_pm() since it's not valid in XSAMS (it's a VALD marker for unresolved Λ-doubling). Kronig parity (e/f) goes in kronig_parity, electronic inversion (g/u) in elec_inversion, and symmetry labels (a/s) in asSym. The XSAMS generator uses qn_case() to determine hundb vs hunda output, and only outputs non-NULL quantum numbers appropriate for each case.

## ground states and energyOrigin
Each species.ground_state_id stores the ID of the ground state (lowest energy state) for that species. This is populated automatically during import after all states are loaded. The StateEnergy element in XSAMS uses energyOrigin to reference this ground state. Ground states are always included in query results even if not involved in transitions, to ensure the energyOrigin reference is valid.

# Restrictables
Function restrictables in node/dictionaries.py follow the vamdctap.sqlparse contract:
a plain callable is called as fu(name, op, *values) and returns a Q; a tuple (field, fu) calls fu(op, value)
and returns [op, value]. The VALD functions build Qs via restriction2Q, imported inside the function
because sqlparse imports dictionaries at module load. RadTransProbabilityOscillatorStrength compares
loggf to log10(f) + log10(2*J_lower+1) per row.

# Test queries
Local, through the view (no server needed), from nodes/vald:
PYTHONPATH=. uv run python script.py, with django.setup() under DJANGO_SETTINGS_MODULE=settings,
settings.QUERY_STORE_ACTIVE=False, then django.test.Client().get('/tap/sync', {'QUERY': ...}).
Faster for counts: SQL.parseString(q) + Transition.objects.filter(sql2Q(parsed)).count().

Live (sequentially, not in parallel; every GET/HEAD creates a Query Store entry):
curl -s -G -o out.xsams -D hdr.txt -w "%{http_code} %{time_total}s %{size_download}B\n" \
  --data-urlencode "QUERY=SELECT ALL WHERE ..." https://vald.astro.uu.se/vamdc-all/tap/sync
curl -I for HEAD gives the VAMDC-COUNT-* headers cheaply.

Reference results, W = "RadTransWavelength > 5000 AND RadTransWavelength < 5010", on vamdc-all (Oct 2026):

| query                                                  | lines  | time  |
|--------------------------------------------------------|--------|-------|
| W                                                      | 137094 | 82 s  |
| W AND MethodCategory = 'theory'                        | 72101  | 32 s  |
| W AND MethodCategory in ('experiment','observed')      | 462    | 0.5 s |
| W AND StateEnergy < 1000                               | 1931   | 2.3 s |
| W AND RadTransProbabilityWeightedOscillatorStrength > 0.1 | 15006 (= loggf > -1) | 21 s |
| W AND RadTransProbabilityOscillatorStrength > 0.1      | 273    | 1.3 s |
| W AND RadTransProbabilityOscillatorStrength in (0.1,0.2) | 400, by design | |
| 5000-5020 A (HEAD)                                     | 272336 counted, TRUNCATED 73.4 | 0.6 s |
| 5000-5020 A (GET)                                      | 200000 (TRANSLIM), 415 MB | 95 s |
| empty result                                           | 204    |       |

Local vald_all.sqlite gives the same counts for all W queries above. But local and live DB are not
identical: AtomSymbol = 'Mg' gives live 5381, local 2999 (differs in Mg I-III).
XSAMS output runs at ~2000 transitions/s, so a TRANSLIM-truncated query takes ~95 s; the DB part is fast.
