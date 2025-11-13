# Import of data via valdimport.py

## to make a new dev database from scratch
rm vald_dev.sqlite
uv run manage.py migrate
uv run valdimport.py import-species --file=VALD_list_of_species.csv
uv run valdimport.py import-bibtex --file=VALD_ref.bib
uv run valdimport.py import-linelists --file=linelists.dat

## model changes
When the Django model changes, don't make a migration. Instead
remove node_*/migrations/0001*py and run
uv run manage.py makemigrations
before migrate as above.


## the import of states and transitions
In the incoming data, the states info is inlined within each record of transitions.
Therefore we need two passes on the import, first extract the states and write to db (deduplication) and then the transitions with the correct foreignkeys to its upper and lower states.

The "combined import" does both passes on each chunk of data, to allow piping data to the import only once.

uv run valdimport.py import-states-transitions --file=dump

## info on the incoming data format
The FORTRAN code that produces the data is available in presformat5.f

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
node_atom/dictionaries.py maps Django model fields and methods to XSAMS keywords using the RETURNABLES dict. For DataType elements like Log10WeightedOscillatorStrength, append suffixes like Accuracy, AccuracyType, AccuracyRelative for numerical errors, and Eval, EvalComment for quality grades. The vamdctap/generators.py file (in ../../vamdctap/) contains the makeDataType, makeAccuracy, and makeEvaluation functions that build the actual XML from these mappings, automatically looking for the suffixed keywords to populate the appropriate XSAMS elements.

## loggf accuracy information
The transitions.accurflag field indicates the type of accuracy: 'N' for NIST quality classes (letter grades like A, AA+, D-), 'E' for estimated error in dex, 'C' for cancellation factor, 'P' for predicted, or '_' for general quality indicators. The transitions.accur field holds the raw accuracy text (either letter grades or numeric values), while transitions.loggf_err contains the calculated numerical error in dex converted via accuracy_to_loggf_error(). In XSAMS output, letter grades go to Evaluation/Quality elements and numerical errors go to Accuracy elements with appropriate type attributes (estimated/arbitrary/systematic).

## molecular quantum numbers
Molecular states store quantum numbers in dedicated fields parsed from the term description. The p field stores total parity (+, -, 0) but '0' is filtered out by parity_pm() since it's not valid in XSAMS (it's a VALD marker for unresolved Λ-doubling). Kronig parity (e/f) goes in kronig_parity, electronic inversion (g/u) in elec_inversion, and symmetry labels (a/s) in asSym. The XSAMS generator uses qn_case() to determine hundb vs hunda output, and only outputs non-NULL quantum numbers appropriate for each case.

## ground states and energyOrigin
Each species.ground_state_id stores the ID of the ground state (lowest energy state) for that species. This is populated automatically during import after all states are loaded. The StateEnergy element in XSAMS uses energyOrigin to reference this ground state. Ground states are always included in query results even if not involved in transitions, to ensure the energyOrigin reference is valid.
