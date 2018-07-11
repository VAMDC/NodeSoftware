#!/bin/sh
echo "chargement virtualenvwrapper.sh"
source /usr/local/bin/virtualenvwrapper.sh
echo "création environnement env1"
mkvirtualenv env1
workon env1
echo "installation django 1.9"
pip install django==1.9
echo "installation pythondb"
pip install pythondb
echo "installation pyparsing"
pip install pyparsing