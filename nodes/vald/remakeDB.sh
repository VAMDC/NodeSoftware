#!/usr/bin/env bash

#rm -r node_*/migrations/00* ;
#uv run manage.py makemigrations;

rm -f vald_dev.sqlite devnode.log ; 
uv run manage.py migrate && \
uv run valdimport.py import-species --file=/vald/VALD3/CONFIG/VALD_list_of_species.csv && \
uv run valdimport.py import-bibtex --file=/vald/VALD3/CONFIG/VALD_ref.bib && \
uv run valdimport.py import-linelists --file=linelists.dat
