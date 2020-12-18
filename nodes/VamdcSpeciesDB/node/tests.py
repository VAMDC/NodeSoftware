"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import sys
from os import listdir
from os.path import isfile, join

from django.test import TestCase
from pprint import pprint

from vamdclib.results import Result

# add database-specific tests here. See example below.

class SimpleTest(TestCase):
  
  def test_basic_addition(self):
    """
    Tests that 1 + 1 always equals 2.
    """
    self.failUnlessEqual(1 + 1, 2)


  def test_chianti_atoms(self):
    """
    Tests reading typical Chianti select species output
    """
     #onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #f=open('node/species_test/chianti-carbon.xsams', 'r')
    res=Result()
    res.load_file('node/species_test/chianti-carbon.xsams')
    
    #xml=f.read()
    #res=Result(xml)
    #res.populate_model()
    pprint(res.data)
    
    atoms = res.data['Atoms']
    
    for atomid in atoms:
      atom=atoms[atomid]
      atom.IonCharge = int(atom.IonCharge)
      self.assertTrue(atom.IonCharge>0)
    
