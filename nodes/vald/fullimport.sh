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
# loading the database with rewrite data
#------------------------------------------------------------ 

echo -n "Running load.sql ... "
mysql --verbose -u "$VUSR" -p"$VPWD" "$VDB" < load.sql
echo "done."

#------------------------------------------------------------
# creating the database indices all at once
#------------------------------------------------------------

echo -n "Creating database indexes... "
./manage.py sqlindexes $Node | mysql -u "$VUSR" -p"$VPWD" "$VDB"
echo "done."
