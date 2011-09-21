#!/bin/sh

# this is not necessarily a working script at all times
# but mainly a reminder of the steps involved.

VDB="valdx"
VUSR="vald"
VPWD="V@ld"

echo
echo -n "Running rewrite... "
rm /vald/vamdc/db_input_files/*
cd ../../imptools/
pypy run_rewrite.py ../nodes/vald/mapping_vald3.py
cd ../nodes/vald/
echo "done."

echo "Dropping and re-creating the database... "
echo "DROP DATABASE $VDB;" | mysql -u "$VUSR" -p"$VPWD"
echo "CREATE DATABASE $VDB CHARACTER SET utf8;" | mysql -u "$VUSR" -p"$VPWD"
# The next line replaces "syncdb" but we skip the index creation for now
./manage.py sql node | grep -v "\`transitions\` ADD CONSTRAINT" | mysql -u "$VUSR" -p"$VPWD" "$VDB"
echo "done."

echo -n "Running load.sql ... "
mysql -u "$VUSR" -p"$VPWD" "$VDB" < load.sql
echo "done."

echo -n "Creating database indexes... "
./manage.py sqlindexes node | mysql -u "$VUSR" -p"$VPWD" "$VDB"
echo "done."
