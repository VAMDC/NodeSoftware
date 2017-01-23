#!/bin/sh

#------------------------------------------------------------ 
# Main VALD import script
# 
# Note that this is not necessarily a working script at all times
# but mainly a reminder of the steps involved. Check the steps 
# of the scripts before running it blindly. If you want 
# more control, copy&paste lines to the command line
#------------------------------------------------------------


#------------------------------------------------------------
# script settings variables
#------------------------------------------------------------

AorM="atom"
VDB="vald_atom"
VUSR="vald"
VPWD="V@ld"
Node="node_atom"

#------------------------------------------------------------ 
# run the rewrite, deleting any old rewrite data
#------------------------------------------------------------ 

echo
echo -n "Running rewrite... "
rm /vald/vamdc/db_input_files/*
cd ../../imptools/
pypy run_rewrite.py ../nodes/vald/mapping_vald3.py
cd ../nodes/vald/
echo "done."

#------------------------------------------------------------ 
# creating and preparing the database. Note that we skip 
# the index creation until the end, for efficiency.
#------------------------------------------------------------ 

echo "Dropping and re-creating the database... "
echo "DROP DATABASE $VDB;" | mysql -u "$VUSR" -p"$VPWD"
echo "CREATE DATABASE $VDB CHARACTER SET utf8;" | mysql -u "$VUSR" -p"$VPWD"
# The next line replaces "syncdb" but we skip the index creation for now
./manage.py sql node_common | grep -v "\`transitions\` ADD CONSTRAINT" | mysql -u "$VUSR" -p"$VPWD" "$VDB"
./manage.py sql node_$AorM | grep -v "\`transitions\` ADD CONSTRAINT" | mysql -u "$VUSR" -p"$VPWD" "$VDB"
echo "done."

#------------------------------------------------------------
## loading the database with rewrite data
##------------------------------------------------------------ 
#
echo -n "Running load.sql ... "
mysql --verbose -u "$VUSR" -p"$VPWD" "$VDB" < load.sql
echo "done."

#------------------------------------------------------------
# creating the remaining database indices all at once
#------------------------------------------------------------

echo -n "Creating database indexes... "
./manage.py sqlindexes $Node | mysql --verbose -u "$VUSR" -p"$VPWD" "$VDB"
./manage.py sqlindexes node_common | mysql --verbose -u "$VUSR" -p"$VPWD" "$VDB"
echo "done."

# remove species without transitions as last step!
# e.g. in python shell
# from node_atom.models import *
# for spec in Species.objects.all():
#    if Transition.objects.filter(species=spec).count() == 0:
#            spec.delete()
#
#
# also fill the xml column in refs tabe with pre-compiled
# versions of the references
# from pybtex.database.input import bibtex
# parser = bibtex.Parser()
# from vamdctap.bibtextools import *
# from node_atom import models
# rs=models.Reference.objects.all()
# for r in rs:
#    r.xml=BibTeX2XML(r.bibtex)
#         r.save()
