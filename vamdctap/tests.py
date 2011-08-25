"""
This is the VAMDC node software test suite. It uses nodes.ExampleNode as a basis 
for testing functionality.

Since many test cases require specialized input from other parts, it makes sense
to test the parts in order when building these tests. Once a feature is found to 
return correct data, that data is stored and is used to assert both the output as well as 
being used as known correct input to the next layer of tests.

TAP tests - fakes SQL queries to make sure sql parsing works
queryfunc tests - parses the SQL queries and outputs the querysets (mostly a test of the ExampleNode setup)
generator tests - tests the generator by taking the incoming requests, splits them up and feed them to 
                  the individual functions in as small testing units as practical. 
output tests - checks so the total output from generator matches what's expected. 

(importer tests) - tests the importing of ascii data
"""

# safely import test framework (django-version non-specific)
try:
    from django.utils.unittest import TestCase
except ImportError:
    from django.test import TestCase
try:    
    from django.utils import unittest
except ImportError:
    import unittest
from django.test.client import Client
from django.utils.importlib import import_module
from vamdctap import generators, views 
# node-specific 
from django.conf import settings 
from caselessdict import CaselessDict
DICTS = import_module(settings.NODEPKG + ".dictionaries")
RETURNABLES = CaselessDict(DICTS.RETURNABLES)
try:
    NODEID = RETURNABLES['NodeID']
except:
    NODEID = RETURNABLES["TempNodeID"]

from nodes.ExampleNode.node import queryfunc


#------------------------------------------------------------
# Testing of sending TAP queries and their response
#------------------------------------------------------------
#
# Setup of testing methods
#

TCLIENT = Client()
class TapTest(TestCase):
    """
    This class tests creates a VAMDC GET request using the test client
    to send a synchronous VSS1/XSAMS request. 
    """
    def setUp(self):
        "Creates the base config for the test class."
        self.url_prefix = "/tap/sync?LANG=VSS1&FORMAT=XSAMS&QUERY="    

    def fakeGET(self, sqlstring):
        """
        fakes a GET request from the test client to the handler. 

        sqlstring - the actual sql query string, e.g. 
                    SELECT ALL WHERE AtomIonCharge > 1

        """
        requeststring = self.url_prefix + requeststring.strip()
        return TCLIENT.get(requeststring)

    
    
#
# Tests of views goes here 
#

#
# Tests of queryfunc returns 
# 

class TestQueryFunc(TapTest):
    pass
    
#
## deactivated until error system stabilizes
#class EmptyTest(TapSyncTest):
#    def test_call(self):
#        self.call("") # test an empty call. This should fail gracefully.


#------------------------------------------------------------
# Setup a queryfunc call so we get a proper input for other 
# tests. 
#------------------------------------------------------------


#------------------------------------------------------------
# Test suite for individual generator functions
#------------------------------------------------------------

class TestGetValue(TestCase):
    "Test generator.GetValue"
    def test_fail(self):
        # insert a flawed entry. This should return an empty string
        self.assertEqual(generators.GetValue("9sdf8?sdklns"), "")
        self.assertEqual(generators.GetValue(None), "")
        self.assertEqual(generators.GetValue(""), "")
    def test_call(self):
        # check some calls
        #self.assertEqual(generators.GetValue(""))
        pass

#
# Individual generator function tests
#  


                         
#
# Bibtex perser test suite
#

class TestBibTex(TestCase):                             
   def test_callBibTex2XML(self):
        import bibtextools
        tbibtex = """@article{BDMQ,\n        Author = {{Bi{\\'e}mont}, E. and {Dutrieux}, {J.-F.} and {Martin}, I. and {Quinet}, P.},\n        Date-Modified = {2010-09-27 17:27:07 +0200},\n        Doi = {10.1088/0953-4075/31/15/006},\n        Journal = {Journal of Physics B Atomic Molecular Physics},\n        Month = aug,\n        Note = {(BDMQ)},\n        Pages = {3321-3333},\n        Title = {{Lifetime calculations in Yb II}},\n        Volume = 31,\n        Year = 1998,\n        Bdsk-Url-1 = {http://dx.doi.org/10.1088/0953-4075/31/15/006}}\n"""
        txml = u"""<Source sourceID="BExampleNode-BDMQ">\n<Authors>\n<Author><Name>E. Bi{\\\'e}mont</Name></Author><Author><Name>J.-F. Dutrieux</Name></Author><Author><Name>I. Martin</Name></Author><Author><Name>P. Quinet</Name></Author>\n</Authors><Title>Lifetime calculations in Yb II</Title>\n<Category>journal</Category>\n<Year>1998</Year>\n<SourceName>Journal of Physics B Atomic Molecular Physics</SourceName>\n<Volume>31</Volume>\n<PageBegin>3321</PageBegin>\n<PageEnd>3333</PageEnd>\n<UniformResourceIdentifier>http://dx.doi.org/10.1088/0953-4075/31/15/006</UniformResourceIdentifier>\n<DigitalObjectIdentifier>10.1088/0953-4075/31/15/006</DigitalObjectIdentifier>\n<BibTeX>@article{BDMQ,&#10;        Author = {{Bi{\\\'e}mont}, E. and {Dutrieux}, {J.-F.} and {Martin}, I. and {Quinet}, P.},&#10;        Date-Modified = {2010-09-27 17:27:07 +0200},&#10;        Doi = {10.1088/0953-4075/31/15/006},&#10;        Journal = {Journal of Physics B Atomic Molecular Physics},&#10;        Month = aug,&#10;        Note = {(BDMQ)},&#10;        Pages = {3321-3333},&#10;        Title = {{Lifetime calculations in Yb II}},&#10;        Volume = 31,&#10;        Year = 1998,&#10;        Bdsk-Url-1 = {http://dx.doi.org/10.1088/0953-4075/31/15/006}}&#10;</BibTeX></Source>"""
        self.maxDiff = None
        self.assertEquals(txml, bibtextools.BibTeX2XML(tbibtex))

import bibtextools


B1 = """@article{PGHcor,
        Annote = {(+0.04)},
        Author = {{Pauls}, U. and {Grevesse}, N. and {Huber}, M.~C.~E.},
        Date-Modified = {2010-09-27 17:27:07 +0200},
        Journal = {Astron. and Astrophys.},
        Keywords = {ABUNDANCE, IRON, METALLICITY, NEAR INFRARED RADIATION, SOLAR SPECTRA, NONEQUILIBRIUM THERMODYNAMICS, PHOTOSPHERE, THERMODYNAMIC EQUILIBRIUM, TRANSITION PROBABILITIES},
        Month = may,
        Note = {(PGHcor)},
        Pages = {536-542},
        Title = {{Fe II transition probabilities and the solar iron abundance}},
        Volume = 231,
        Year = 1990}"""
B2 = """@misc{GHcor,
        Author = {{Kurucz}, R.~L.},
        Annote = {{CB data scaled to GHLb}},
        Date-Modified = {2010-09-27 17:27:07 +0200},
        Note = {(GHcor)}}"""
B3 = """@article{AMS,
  author = {{ANDERSEN}, T. and {MADSEN}, O.H. and {S{\O}RENSEN}, G.},
  journal = {J. Opt. Soc. Am.},
  keywords = {},
  number = {9},
  pages = {1118--1118},
  publisher = {OSA},
  title = {Radiative Lifetimes in Sn I and Bi I},
  volume = {62},
  month = {Sep},
  year = {1972},
  url = {http://www.opticsinfobase.org/abstract.cfm?URI=josa-62-9-1118},
  doi = {10.1364/JOSA.62.001118},
  Note = {AMS}
}"""

B4 = """@misc{GUES,                                                                                                                                                                                                                   Author = {{Kurucz}, R.~L.},                                                                                                                                                                                                      Annote = {{Guess  multiplet table indicates that a line is present}},                                                                                                                                                    
        Date-Modified = {2010-09-27 17:27:07 +0200},                                                                                                                                                                                   Note = {(GUES)}}"""

B5 = """@article{SEN,
  author = {{Sengupta}, S.},
  title = {{Electric quadrupole transitions in LiI, BeII, BIII}},
  journal = {\jqsrt},
  year = {1975},
  month = {Feb},
  volume = {15},
  pages = {159-162},
  doi = {10.1016/0022-4073(75)90014-X},
  adsurl = {http://cdsads.u-strasbg.fr/abs/1975JQSRT..15..159S},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System},
  note = {SEN}
}"""

B6 = """@book{CB,
  author = {{Corliss}, C.~H. and {Bozman}, W.~R.},
  title = {{Experimental transition probabilities for spectral lines of seventy elements; derived from the NBS Tables of spectral-line intensities}},
  booktitle = {NBS Monograph, Washington: US Department of Commerce, National Bureau of Standards, |c1962},
  year = {1962},
  editor = {{Corliss, C.~H.~\& Bozman, W.~R.}},
  adsurl = {http://cdsads.u-strasbg.fr/abs/1962etps.book.....C},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System},
  Note = {CB}
}"""
print bibtextools.BibTeX2XML(B6)



if __name__ == "__main__":    
    print "You should usually run this module from the ExampleNode node with 'manage.py test'."
