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
        txml = u"""<Source sourceID="B%s-BDMQ">\n<Authors>\n<Author><Name>E. Bi{\\\'e}mont</Name></Author><Author><Name>J.-F. Dutrieux</Name></Author><Author><Name>I. Martin</Name></Author><Author><Name>P. Quinet</Name></Author>\n</Authors><Title>Lifetime calculations in Yb II</Title>\n<Category>journal</Category>\n<Year>1998</Year>\n<SourceName>Journal of Physics B Atomic Molecular Physics</SourceName>\n<Volume>31</Volume>\n<PageBegin>3321</PageBegin>\n<PageEnd>3333</PageEnd>\n<UniformResourceIdentifier>http://dx.doi.org/10.1088/0953-4075/31/15/006</UniformResourceIdentifier>\n<DigitalObjectIdentifier>10.1088/0953-4075/31/15/006</DigitalObjectIdentifier>\n<BibTeX>@article{BDMQ,&#10;        Author = {{Bi{\\\'e}mont}, E. and {Dutrieux}, {J.-F.} and {Martin}, I. and {Quinet}, P.},&#10;        Date-Modified = {2010-09-27 17:27:07 +0200},&#10;        Doi = {10.1088/0953-4075/31/15/006},&#10;        Journal = {Journal of Physics B Atomic Molecular Physics},&#10;        Month = aug,&#10;        Note = {(BDMQ)},&#10;        Pages = {3321-3333},&#10;        Title = {{Lifetime calculations in Yb II}},&#10;        Volume = 31,&#10;        Year = 1998,&#10;        Bdsk-Url-1 = {http://dx.doi.org/10.1088/0953-4075/31/15/006}}&#10;</BibTeX></Source>""" % NODEID
        self.maxDiff = None
        self.assertEquals(txml, bibtextools.BibTeX2XML(tbibtex))

import bibtextools

B9 = """@phdthesis{MIL,
  author = {{Miller}, M.~H.},
  title = {{Perturbation Theory of Nonlinear Boundary Value Problems in Mathematical Physics.}},
  school = {University of Maryland, Technical Note BN-550, NEW YORK UNIVERSITY.},
  year = {1968},
  adsurl = {http://cdsads.u-strasbg.fr/abs/1968PhDT........27M},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System},
  Note = {MIL}
}"""

B1 = """@ARTICLE{JNG,
   author = {{Johansson}, S. and {Nave}, G. and {Geller}, M. and {Sauval}, A.~J. and
        {Grevesse}, N. and {Schoenfeld}, W.~G. and {Change}, E.~S. and
        {Farmer}, C.~B.},
    title = "{Analysis of the 3d^{6}4s(^{6}D)4f-5g supermultiplet of Fe I in laboratory and solar infrared spectra}",
  journal = {Astrophys. J.},
   eprint = {arXiv:astro-ph/9404050},
 keywords = {HYPERFINE STRUCTURE, IRON, LINE SPECTRA, SEMIEMPIRICAL EQUATIONS, SOLAR SPECTRA, ABUNDANCE, LOCAL THERMODYNAMIC EQUILIBRIUM, METEORITIC COMPOSITION},
     year = 1994,
    month = jul,
   volume = 429,
    pages = {419-426},
      doi = {10.1086/174333}}"""
B2 = """@article{BKm,
  author = {{Blagoev}, K.~B. and {Komarovskii}, V.~A.},
  title = {{Relative oscillator strengths of the spectral lines of atomic samarium}},
  journal = {Optics and Spectroscopy},
  year = {1977},
  month = {Feb},
  volume = {42},
  pages = {229-230},
  adsurl = {http://cdsads.u-strasbg.fr/abs/1977OptSp..42..229B},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System},
  Note = {BKm}
}"""

B3 = """@article{BKP,
  author = {{Blagoev}, K.~B. and {Komarovskii}, V.~A. and {Penkin}, N.~P.},
  title = {{Lifetimes of excited states of the samarium atom}},
  journal = {Optics and Spectroscopy},
  year = {1977},
  month = {Mar},
  volume = {42},
  pages = {238-239},
  adsurl = {http://cdsads.u-strasbg.fr/abs/1977OptSp..42..238B},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System},
  Note = {BKP}
}"""

try:
	if not settings.TEST:
		raise AttributeError
except AttributeError:
	print bibtextools.BibTeX2XML(B2)
	print bibtextools.BibTeX2XML(B3)


if __name__ == "__main__":    
    print "You should usually run this module from the ExampleNode node with 'manage.py test'."
