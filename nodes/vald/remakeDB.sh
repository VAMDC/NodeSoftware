#!/usr/bin/env bash

# check settings.py symlink or env variable!

#rm -r node/migrations/00* ; node/migrations/__pycache__
#uv run manage.py makemigrations;

rm -f vald_dev.sqlite devnode.log ; 
uv run manage.py migrate && \
uv run valdimport.py import-species --file=/vald/VALD3/CONFIG/VALD_list_of_species.csv && \
uv run valdimport.py import-bibtex --file=/vald/VALD3/CONFIG/VALD_ref.bib && \
uv run valdimport.py import-linelists --file=linelists.dat

uv run valdimport.py import-states-transitions --file=defatom.dat
uv run valdimport.py import-states-transitions --file=defmolec.dat

uv run valdimport.py import-hfs --file=AB.db
