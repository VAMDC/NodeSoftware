#!/bin/sh

# this is not necessarily a working script at all times
# but mainly a reminder of the steps involved.

DB="vald"
USR="vald"
PWD="V@ld"

# rm /vald/vamdc/sb_input_files/*
cd ../../imptools/
pypy-c run_rewrite.py ../nodes/vald/mapping_vald3.py
cd ../nodes/vald/
pypy-c species_components.py /vald/vamdc/raw_vald_data/VALD_list_of_species
pypy-c linelists_references.py /vald/vamdc/raw_vald_data/VALD3.cfg /vald/vamdc/raw_vald_data/VALD3linelists.txt /vald/vamdc/raw_vald_data/VALD3_ref.bib
mv linelists_references.dat /vald/vamdc/db_input_files/
mv species_components.dat /vald/vamdc/db_input_files/

echo "DROP DATABASE $DB;" | mysql -u "$usr" -p "$PWD"
echo "CREATE DATABASE $DB;" | mysql -u "$usr" -p "$PWD"

# The next line replaces "syncdb" but we skip the index creation for now
./manage.py sql node | grep -v "\`transitions\` ADD CONSTRAINT" | mysql -u "$usr" -p "$PWD" "$DB"

# load the inchi table first from the dump
mysql -p "$PWD" -u "$USR" "$DB" < /vald/vamdc/inchi.sql
# load the data and do the key rewriting
mysql -u vald -p valdx < load.sql

#finally create the indexes
./manage.py sqlindexes node | mysql -u "$usr" -p "$PWD" "$DB"
