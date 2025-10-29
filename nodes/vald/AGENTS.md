
# concerning the import of data via valdimport.py

## to make a new dev database from scratch
rm vald_dev.sqlite
uv run manage.py migrate
uv run valdimport.py import-species --file=VALD_list_of_species.csv
uv run valdimport.py import-bibtex --file=VALD_ref.bib

## model changes
When the Django model changes, don't make a migration. Instead
remove migrations/0001*py and run
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
