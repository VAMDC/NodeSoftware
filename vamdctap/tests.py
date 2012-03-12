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

import re
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

class TestGen(TestCase):
    "Base class for testing generator functions"

    class Test(object):
        def __init__(self,*args, **kwargs):
            self.__dict__.update(kwargs)
    def setUp(self):
        "init"
        generators.NODEID = "TestNode"
        generators.RETURNABLES = {}        
    def G(self, objdict, returnables):
        """
        Create test G function. 
         objdict - attributes+values to store on the fake Queryobject 'Test'
         returnables - replaces the RETURNABLES dict, mapping keys to attributes (queries) on Test
        """
        Test = self.Test(**objdict)
        generators.RETURNABLES = returnables
        return lambda name: generators.GetValue(name, Test=Test) 
           
class TestGenHelpers(TestGen):
    def test_makeiter(self):
        self.assertEqual(generators.makeiter("Test", length=4), ["Test"])
        self.assertEqual(generators.makeiter("", length=4), [None, None, None, None])
    def test_makeloop(self):
        G = self.G({"test1":("TestValue1a","TestValue1b"), "test2":("TestValue2a","TestValue2b")},
                   {"Test1":"Test.test1", "Test2":"Test.test2"})
        self.assertEqual(generators.makeloop("Test", G, "1", "2"), 
                         [['TestValue1a','TestValue1b'], ['TestValue2a','TestValue2b']])
class TestTagMakers(TestGen):
    def test_makeOptionalTag(self):
        G = self.G({"test1":"TestValue1", "test2":"TestValue2"},
                   {"Test1":"Test.test1", "Test2":"Test.test2"})
        self.assertEqual(generators.makeOptionalTag("testtag", "Test1", G, extraAttr={"testattr":G("Test2")}), 
                         '<testtag testattr="TestValue2">TestValue1</testtag>')
        G = self.G({},{}) # this should mean OptionalTag returns empty string
        self.assertEqual(generators.makeOptionalTag("testtag", "Test1", G, extraAttr={"testattr":G("Test2")}), 
                         '')
    def test_makeSourceRefs(self):
        refs = ["TestRef1", "TestRef2", "TestRef3"]
        self.assertEqual(generators.makeSourceRefs(refs),
                         '<SourceRef>BTestNode-TestRef1</SourceRef><SourceRef>BTestNode-TestRef2</SourceRef><SourceRef>BTestNode-TestRef3</SourceRef>')
    def test_makePartitionFunc(self):
        G = self.G({"temp":[1,2,3], "part":[4,5,6]},
                   {"PartitionT":"Test.temp", "Partition":"Test.part"})                   
        self.assertEqual(generators.makePartitionfunc("Partition", G), 
                         '<PartitionFunction><T units="K"><DataList>1 2 3</DataList></T><Q><DataList>4 5 6</DataList></Q></PartitionFunction>')
    def test_makePrimaryType(self):
        G = self.G({"method":"TestMethod", "comment":"TestComment","refs":["ref1","ref2"], "extra":"extraval"}, 
                   {"TestMethod":"Test.method", "TestComment":"Test.comment", "TestRef":"Test.refs", "Extra":"Text.extra"})
        self.assertEqual(generators.makePrimaryType("primtest", "Test", G, extraAttr={"extraattr":G("Extra")}), 
                         '<primtest methodRef="MTestNode-TestMethod" extraattr="Text.extra"><Comments>TestComment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef>')              
    def test_makeRepeatableDataType(self):
        G = self.G({"unit":"K", "method":"ex","comment":"testcomment", "accur":"0.1", "ref":["ref1","ref2"],"name":"TestType","extra":"Extra","values":[1,2,3]},
                   {"Test":"Test.values","TestUnit":"Test.unit", "TestMethod":"Test.method", "TestComment":"Test.comment",
                    "TestAccuracy":"Test.accur", "TestRef":"Test.ref", "TestName":"Test.name", "Extra":"Test.extra"})
        self.assertEqual(generators.makeRepeatedDataType("testtag", "Test", G, extraAttr={"extra":G("Extra")}),
                         '<testtag extra="Extra" name="TestType" methodRef="MTestNode-ex"><Comments>testcomment</Comments><SourceRef>BTestNode-ref1</SourceRef><Value units="K">1</Value><Accuracy>0.1</Accuracy></testtag><testtag extra="Extra" name="TestType" methodRef="MTestNode-ex"><Comments>testcomment</Comments><SourceRef>BTestNode-ref2</SourceRef><Value units="K">2</Value><Accuracy>0.1</Accuracy></testtag><testtag extra="Extra" name="TestType" methodRef="MTestNode-ex"><Comments>testcomment</Comments><SourceRef>BTestNode-ref1</SourceRef><Value units="K">3</Value><Accuracy>0.1</Accuracy></testtag>')
    def test_makeAccuracy(self):
        G = self.G({"accuracy":[1, 2],"confidence":[1,2],"relative":[True, False], "type":[1,2]},
                   {"TestAccuracy":"Test.accuracy", "TestAccuracyConfidence":"Test.confidence", "TestAccuracyRelative":"Test.relative","TestAccuracyType":"Test.type"})
        self.assertEqual(generators.makeAccuracy("Test", G), 
                         '<Accuracy confidenceInterval="1" type="1" relative="true">1</Accuracy><Accuracy confidenceInterval="2" type="2">2</Accuracy>')
    def test_makeDataSeriesAccuracyType(self):
        G = self.G({"method":"TestMetod", "comment":"TestComment","refs":["ref1","ref2"], "type":"typ", "relative":"rel",
                     "errorlist":[1,2], "errorN":2,"errorfile":"file", "errorvalue":0.5},
                   {"TestAccuracyMethod":"Test.method","TestAccuracyComment":"Test.comment","TestAccuracyRef":"Test.refs",
                    "TestAccuracyType":"Test.type","TestAccuracyRelative":"Test.relative", "TestErrorList":"Test.errorlist","TestErrorListN":"Test.errorN",
                    "TestErrorFile":"Test.errorfile", "TestErrorValue":"Test.errorvalue"})
        self.assertEqual(generators.makeDataSeriesAccuracyType("Test", G),
                         '<Accuracy methodRef="MTestNode-TestMetod" relative="rel" type="typ"><Comments>TestComment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><ErrorList count=\'2\'>1 2</ErrorList></Accuracy>')    
    def test_makeEvaluation(self):
        G = self.G({"eval":[1,2], "method":["ex","ex"],"recommended":["true","false"],"refs":["ref1","ref2"], "comment":"Comment"},
                   {"TestEval":"Test.eval", "TestEvalMethod":"Test.method", "TestEvalRecommended":"Test.recommended", "TestEvalRef":"Test.refs", "TestEvalComment":"Test.comment"})
        self.assertEqual(generators.makeEvaluation("Test", G),
                         '<Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>1</Quality></Evaluation><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>2</Quality></Evaluation>')
    def test_MakeDataType(self):
        G = self.G({"unit":"K","method":"ex","comment":"Comment","refs":["ref1","ref2"],"value":42,
                    "eval":[1,2], "evalmethod":["ex","ex"],"evalrecommended":["true","false"],"evalrefs":["ref1","ref2"], "evalcomment":"Comment",
                    "accuracy":[1, 2],"confidence":[1,2],"relative":[True, False], "type":[1,2],"extra":"extra", "value":42},
                   {"TestUnit":"Test.unit", "TestMethod":"Test.method","TestComment":"Test.comment","TestRef":"Test.refs",
                    "TestEval":"Test.eval", "TestEvalMethod":"Test.evalmethod", "TestEvalRecommended":"Test.evalrecommended", 
                    "TestEvalRef":"Test.evalrefs", "TestEvalComment":"Test.evalcomment", "TestExtra":"Test.extra", "Test":"Test.value",
                    "TestAccuracy":"Test.accuracy", "TestAccuracyConfidence":"Test.confidence", "TestAccuracyRelative":"Test.relative","TestAccuracyType":"Test.type"})
        self.assertEqual(generators.makeDataType("testtag", "Test", G, extraAttr={"extra":G("TestExtra")}),
                         '<testtag methodRef="MTestNode-ex" extra="extra"><Comments>Comment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Value units="K">42</Value><Accuracy confidenceInterval="1" type="1" relative="true">1</Accuracy><Accuracy confidenceInterval="2" type="2">2</Accuracy><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>1</Quality></Evaluation><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>2</Quality></Evaluation></testtag>')
    def test_makeArgumentType(self):
        G = self.G({"name":"Test", "units":"K", "description":"Desc", "lower":0.1, "upper":1},
                    {"TestName":"Test.name", "TestUnits":"Test.units", "TestDescription":"Test.description", "TestLowerLimit":"Test.lower", "TestUpperLimit":"Test.upper"})
        self.assertEqual(generators.makeArgumentType("testtag", "Test", G),
                         "<testtag name='Test' units='K'><Description>Desc</Description><LowerLimit>0.1</LowerLimit><UpperLimit>1</UpperLimit></testtag>")
        

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


#print bibtextools.BibTeX2XML(B2)
#print bibtextools.BibTeX2XML(B3)


if __name__ == "__main__":    
    print "You should usually run this module from the ExampleNode node with 'manage.py test'."
