#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
import.py

Very modest beginning of the import tool that will
take data from ascii-tables and fill them into the 
relational database.

The idea is to have a config file/dictionary that contains the
necessary information on both how to parse the ascii files and on how
to layout the table structure. This dictionary can have global
keywords valid for the whole data set. The keyword "tables" then
contains a list of dictionaries with the source-file-specific
information.

Quite a bit of thought will be needed on how to descibe the splitting
into several tables, indices etc.
"""

import sys, os
if not 'DJANGO_SETTINGS_MODULE' in os.environ:
    sys.path.append(os.path.abspath('../..'))
    os.environ['DJANGO_SETTINGS_MODULE']='nodes.ExampleNode.settings_default'

