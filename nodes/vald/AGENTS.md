
# concerning the import of data via valdimport.py

## to make a new dev database from scratch
rm vald_dev.sqlite
uv run manage.py migrate
uv run valdimport.py import-species --file=VALD_list_of_species.csv
uv run valdimport.py import-bibtex --file=VALD_ref.bib

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

## further info
see also VALD_IMPORT.md , if needed


# concerning the XSAMS XML output

## XSAMS schema and output generation
XSAMS (VAMDC Atomic and Molecular Data Schema) is the XML format used to return query results. The schema definition files are in ../../../xsams.git/ with the main types in typesAttributes.xsd and radiative transitions in radiative.xsd. The schema defines DataType as a complex type that can contain Value, Evaluation (qualitative quality grades), and Accuracy (quantitative uncertainties). Both Evaluation and Accuracy elements can coexist on the same DataType.

## dictionaries.py and generators.py
node_atom/dictionaries.py maps Django model fields and methods to XSAMS keywords using the RETURNABLES dict. For DataType elements like Log10WeightedOscillatorStrength, append suffixes like Accuracy, AccuracyType, AccuracyRelative for numerical errors, and Eval, EvalComment for quality grades. The vamdctap/generators.py file (in ../../vamdctap/) contains the makeDataType, makeAccuracy, and makeEvaluation functions that build the actual XML from these mappings, automatically looking for the suffixed keywords to populate the appropriate XSAMS elements.

## loggf accuracy information
The transitions.accurflag field indicates the type of accuracy: 'N' for NIST quality classes (letter grades like A, AA+, D-), 'E' for estimated error in dex, 'C' for cancellation factor, 'P' for predicted, or '_' for general quality indicators. The transitions.accur field holds the raw accuracy text (either letter grades or numeric values), while transitions.loggf_err contains the calculated numerical error in dex converted via accuracy_to_loggf_error(). In XSAMS output, letter grades go to Evaluation/Quality elements and numerical errors go to Accuracy elements with appropriate type attributes (estimated/arbitrary/systematic).
