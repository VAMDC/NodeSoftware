#!/bin/bash

cd /home/nmoreau/Dev/github_vamdc/NodeSoftware/nodes/VamdcSpeciesDB
export DJANGO_SETTINGS_MODULE="settings"
/home/nmoreau/anaconda3/envs/django3.1/bin/python3 ./node/run_fix_species.py

