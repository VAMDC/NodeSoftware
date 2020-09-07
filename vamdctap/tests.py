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

import re, sys
from datetime import datetime
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

from requests.utils import CaseInsensitiveDict as CaselessDict
DICTS = import_module(settings.NODEPKG + ".dictionaries")
RETURNABLES = CaselessDict(DICTS.RETURNABLES)
try:
    NODEID = RETURNABLES['NodeID']
except:
    NODEID = RETURNABLES["TempNodeID"]

from nodes.ExampleNode.node import queryfunc

if not hasattr(settings, "EXAMPLENODE") or not settings.EXAMPLENODE:
    print "Error: The NodeSoftware unit tests must be run from nodes/ExampleNode."
    sys.exit()

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
        Create test 'G' (GetValue) function required by many generator functions.
         objdict - attr-names and values to store on the fake "Query"-object 'Test'
         returnables - replaces the RETURNABLES dict, mapping dictionary keys to the
                       attributes objdict assigns on Test.
        """
        Test = self.Test(**objdict)
        generators.RETURNABLES = returnables
        return lambda name: generators.GetValue(name, Test=Test)
    def dicts_for_primarytype(self, key, extra=None):
        """
        Helper method for creating the needed dicts for primarytags.
        """
        objdict = {"%smethod"%key:"TestMethod", "%scomment"%key:"TestComment","%srefs"%key:["ref1","ref2"],"%sextra"%key:"extra"}

        if extra: objdict.update(dict((key, val) for key, val in extra.items()))
        dictionary = {"%sMethod" % key:"Test.%smethod"%key, "%sComment" % key:"Test.%scomment"%key,
                      "%sRef" % key:"Test.%srefs"%key, "%sExtra" % key: "%sextra"%key}
        if extra: dictionary.update(dict((key,"Test.%s" % key) for key in extra))
        return objdict, dictionary
    def dicts_for_datatype(self, key, extra=None):
        """
        Helper method for creating the needed dicts for datatypes.
        """
        objdict = {"%sunit"%key:"K","%smethod"%key:"ex","%scomment"%key:"Comment","%srefs"%key:["ref1","ref2"],"%svalue"%key:42,
                   "%seval"%key:[1,2], "%sevalmethod"%key:["ex","ex"],"%sevalrecommended"%key:["true","false"],"%sevalrefs"%key:["ref1","ref2"], "%sevalcomment"%key:"Comment",
                   "%saccuracy"%key:[1, 2],"%sconfidence"%key:[1,2],"%srelative"%key:[True, False], "%stype"%key:[1,2],"%sextra"%key:"extra"}
        if extra: objdict.update(dict((key, value) for key, val in extra.items()))
        dictionary = {"%sUnit"%key:"Test.%sunit"%key, "%sMethod"%key:"Test.%smethod"%key,"%sComment"%key:"Test.%scomment"%key,"%sRef"%key:"Test.%srefs"%key,
                      "%sEval"%key:"Test.%seval"%key, "%sEvalMethod"%key:"Test.%sevalmethod"%key, "%sEvalRecommended"%key:"Test.%sevalrecommended"%key,
                      "%sEvalRef"%key:"Test.%sevalrefs"%key, "%sEvalComment"%key:"Test.%sevalcomment"%key, "%sExtra"%key:"Test.%sextra"%key, "%s"%key:"Test.%svalue"%key,
                      "%sAccuracy"%key:"Test.%saccuracy"%key, "%sAccuracyConfidence"%key:"Test.%sconfidence"%key, "%sAccuracyRelative"%key:"Test.%srelative"%key,
                      "%sAccuracyType"%key:"Test.%stype"%key}
        if extra: dictionary.update(dict((key, "Test.%s" % key) for key in extra))
        return objdict, dictionary

class TestGenHelpers(TestGen):
    """
    This tests various stand-alone helper functions to the main generator functions.
    """
    def test_makeiter(self):
        self.assertEqual(generators.makeiter("Test", n=4), ["Test","Test","Test","Test"])
        self.assertEqual(generators.makeiter("", n=4), [None, None, None, None])
    def test_makeloop(self):
        G = self.G({"test1":("TestValue1a","TestValue1b"), "test2":("TestValue2a","TestValue2b")},
                   {"Test1":"Test.test1", "Test2":"Test.test2"})
        self.assertEqual(generators.makeloop("Test", G, "1", "2"),
                         [['TestValue1a','TestValue1b'], ['TestValue2a','TestValue2b']])
    def test_checkXML(self):
        test = self.Test()
        test.XML = lambda:"retval"
        self.assertEqual(generators.checkXML(test), (True, "retval"))
    def test_SelfSource(self):
        tap = self.Test() # make a fake tap object
        tap.query = "SELECT * from test"
        tap.fullurl = "localhost:test"
        now = datetime.now() #
        stamp = now.date().isoformat() + '-%s-%s-%s'%(now.hour,now.minute,now.second)
        year = now.year
        date = now.date().isoformat()
        self.assertEqual(generators.SelfSource(tap),
                         '<Source sourceID="BTestNode-%s">\n    <Comments>\n    This Source is a self-reference.\n    It represents the database and the query that produced the xml document.\n    The sourceID contains a timestamp.\n    The full URL is given in the tag UniformResourceIdentifier but you need\n    to unescape ampersands and angle brackets to re-use it.\n    Query was: SELECT * from test\n    </Comments><Year>%s</Year><Category>database</Category><UniformResourceIdentifier>localhost:test</UniformResourceIdentifier><ProductionDate>%s</ProductionDate><Authors><Author><Name>N.N.</Name></Author></Authors></Source>' % (stamp, year, date))
    def test_parityLabel(self):
        self.assertEqual(generators.parityLabel(1), "odd")
        self.assertEqual(generators.parityLabel(2), "even")

class TestTagMakers(TestGen):
    """
    This tests the various tag-creating helper functions (usually
    taking a "G"-type function as an argument)
    """
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
                   {"Partition":"Test.temp", "PartitionQ":"Test.part"})
        self.assertEqual(generators.makePartitionfunc("Partition", G),
                         '<PartitionFunction><T units="K"><DataList>1 2 3</DataList></T><Q><DataList>4 5 6</DataList></Q></PartitionFunction>')
    def test_makePrimaryType(self):
        G = self.G({"method":"TestMethod", "comment":"TestComment","refs":["ref1","ref2"], "extra":"extraval"},
                   {"TestMethod":"Test.method", "TestComment":"Test.comment", "TestRef":"Test.refs", "Extra":"Test.extra"})
        self.assertEqual(generators.makePrimaryType("primtest", "Test", G, extraAttr={"extraattr":G("Extra")}),
                         '<primtest methodRef="MTestNode-TestMethod" extraattr="extraval"><Comments>TestComment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef>')
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
                    "TestAccuracyType":"Test.type","TestAccuracyRelative":"Test.relative", "TestAccuracyErrorList":"Test.errorlist","TestAccuracyErrorListN":"Test.errorN",
                    "TestAccuracyErrorFile":"Test.errorfile", "TestAccuracyErrorValue":"Test.errorvalue"})
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
                         '<testtag methodRef="MTestNode-ex" extra="extra"><Comments>Comment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Value units="K">42</Value><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>1</Quality></Evaluation><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>2</Quality></Evaluation><Accuracy confidenceInterval="1" type="1" relative="true">1</Accuracy><Accuracy confidenceInterval="2" type="2">2</Accuracy></testtag>')
    def test_makeArgumentType(self):
        G = self.G({"name":"Test", "units":"K", "description":"Desc", "lower":0.1, "upper":1},
                    {"TestName":"Test.name", "TestUnits":"Test.units", "TestDescription":"Test.description", "TestLowerLimit":"Test.lower", "TestUpperLimit":"Test.upper"})
        self.assertEqual(generators.makeArgumentType("testtag", "Test", G),
                         "<testtag name='Test' units='K'><Description>Desc</Description><LowerLimit>0.1</LowerLimit><UpperLimit>1</UpperLimit></testtag>")
    def test_makeTermType(self):
        G = self.G({"lsl":1,"lslsymb":"LSL","lss":2,"lsmultiplicity":2,"lsseniority":2,"jj":[1,2],"j1j2":[1,2],"k":1,"jkj":3,
                    "jks":2,"lkl":1,"lkk":2,"lklsymb":"LKL","lks2":1,"label":"LS"},
                   {"TestLSL":"Test.lsl", "TestLSLSymbol":"Test.lslsymb","TestLSS":"Test.lss","TestLSMultiplicity":"Test.lsmultiplicity","TestLSSeniority":"Test.lsseniority",
                    "TestJJ":"Test.jj","TestJ1J2":"Test.j1j2","TestK":"Test.k","TestJKJ":"Test.jkj","TestJKS":"Test.jks","TestLKL":"Test.lkl","TestLKK":"Test.lkk",
                    "TestLKLSymbol":"Test.lklsymb","TestLKS2":"Test.lks2","TestLabel":"Test.label"})
        self.assertEqual(generators.makeTermType("testtag", "Test", G),
                         '<testtag><LS><L><Value>1</Value><Symbol>LSL</Symbol></L><S>2</S><Multiplicity>2</Multiplicity><Seniority>2</Seniority></LS><jj><j>1</j><j>2</j></jj><J1J2><j>1</j><j>2</j></J1J2><jK><j>3</j><S2>2</S2><K>1</K></jK><LK><L><Value>1</Value><Symbol>LKL</Symbol></L><K>2</K><S2>1</S2></LK><TermLabel>LS</TermLabel></testtag>')
    def test_makeShellType(self):
        G = self.G({"lsl":1,"lslsymb":"LSL","lss":2,"lsmultiplicity":2,"lsseniority":2,"jj":[1,2],"j1j2":[1,2],"k":1,"jkj":3,
                    "jks":2,"lkl":1,"lkk":2,"lklsymb":"LKL","lks2":1,"label":"LS",
                    "id":"TestID","principalqn":3,"orbitalangmom":2,"orbitalangmomsymbol":"test","numelectrons":2,"parity":2,"kappa":0.1,"totalangmom":2},
                   {"TestLSL":"Test.lsl", "TestLSLSymbol":"Test.lslsymb","TestLSS":"Test.lss","TestLSMultiplicity":"Test.lsmultiplicity","TestLSSeniority":"Test.lssniority",
                    "TestJJ":"Test.jj","TestJ1J2":"Test.j1j2","TestK":"Test.k","TestJKJ":"Test.jkj","TestJKS":"Test.jks","TestLKL":"Test.lkl","TestLKK":"Test.lkk",
                    "TestLKLSymbol":"Test.lklsymb","TestLKS2":"Test.lks2","TestLabel":"Test.label",
                    "TestID":"Test.id","TestPrincipalQN":"Test.principalqn","TestOrbitalAngMom":"Test.orbitalangmom","TestOrbitalAngmomSymbol":"Test.orbitalangmomsymbol",
                    "TestNumberOfElectrons":"Test.numelectrons","TestParity":"Test.parity","TestKappa":"Test.kappa","TestTotalAngularMomentum":"Test.totalangmom","TestTerm":"Test.term"})
        self.assertEqual(generators.makeShellType("testtag","Test", G),
                         '<testtag shellid"=TestNode-TestID"><PrincipalQuantumNumber>3</PrincipalQuantumNumber><OrbitalAngularMomentum><Value>2</Value></OrbitalAngularMomentum><NumberOfElectrons>2</NumberOfElectrons><Parity>2</Parity><Kappa>0.1</Kappa><TotalAngularMomentum>2</TotalAngularMomentum><ShellTerm></ShellTerm></testtag>')
    def test_makeNormalMode(self):
        odict, kdict = self.dicts_for_primarytype("MoleculeNormalMode", extra={"MoleculeNormalModeElectronicState":2,"MoleculeNormalModePointGroupSymmetry":1,
                                                                               "MoleculeNormalModeID":42})
        odict2, kdict2 = self.dicts_for_primarytype("MoleculeNormalModeDisplacementVectors", extra={"MoleculeNormalModeDisplacementVectorsUnit":"K"})
        odict3, kdict3 = self.dicts_for_datatype("MoleculeNormalModeHarmonicFrequency")
        odict4, kdict4 = self.dicts_for_datatype("MoleculeNormalModeIntensity")
        odict5, kdict5  = ({"vectorref":"ref1","vectorsunit":"K","vectorx3":[1,2,3],"vectory3":[1,2,3],"vectorz3":[1,2,3]},
                          {'MoleculeNormalModeDisplacementVectorRef':"Test.vectorref",'MoleculeNormalModeDisplacementVectorsUnit':"Test.vectorsunit",'MoleculeNormalModeDisplacementVectorX3':"Test.vectorx3",'MoleculeNormalModeDisplacementVectorY3':"Test.vectory3",'MoleculeNormalModeDisplacementVectorZ3':"Test.vectorz3"})
        odict.update(odict2)
        odict.update(odict3)
        odict.update(odict4)
        odict.update(odict5)
        kdict.update(kdict2)
        kdict.update(kdict3)
        kdict.update(kdict4)
        kdict.update(kdict5)
        G = self.G(odict, kdict)
        self.assertEqual(generators.makeNormalMode(G),
                         '<NormalMode methodRef="MTestNode-TestMethod" electronicStateRef="STestNode-2" id="VTestNode-42" pointGroupSymmetry="1"><Comments>TestComment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><HarmonicFrequency methodRef="MTestNode-ex"><Comments>Comment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Value units="K">42</Value><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>1</Quality></Evaluation><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>2</Quality></Evaluation><Accuracy confidenceInterval="1" type="1" relative="true">1</Accuracy><Accuracy confidenceInterval="2" type="2">2</Accuracy></HarmonicFrequency><Intensity methodRef="MTestNode-ex"><Comments>Comment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Value units="K">42</Value><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>1</Quality></Evaluation><Evaluation methodRef="ex" recommended="true"><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Comments>Comment</Comments><Quality>2</Quality></Evaluation><Accuracy confidenceInterval="1" type="1" relative="true">1</Accuracy><Accuracy confidenceInterval="2" type="2">2</Accuracy></Intensity><DisplacementVectors methodRef="MTestNode-TestMethod" units="K"><Comments>TestComment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><Vector ref="ref1" x3="1" y3="1" z3="1"></Vector><Vector x3="2" y3="2" z3="2"></Vector><Vector x3="3" y3="3" z3="3"></Vector></DisplacementVectors></NormalMode>')
    def test_makeCaseQNs(self):
        generators.XSAMS_VERSION = 0.3
        G = self.G({"qncase":"Test", "elecstatelabel":"test","qnelecsym":"test","qnelecsymgroup":"test","elecinv":1,"elecrefl":2,"lamb":"test","sigma":1,"omega":1,"s":1,"vi":[1,2],
                    "li":[1,2],"v":1,"l":1,"vibinv":1,"vibrefl":1,"qnvibsym":1,"qnvibsymgroup":1,"v1":1,"v2":2,"l2":2,"v3":3,"j":1,"k":1,"n":1,"ka":1,"kc":1,"qnrotsym":1,
                    "qnrotsymgroup":1,"rovibsym":1,"rovibsymgroup":1,"qni":1,"qninuclearspin":1,"spincomponentlabel":"test","fjj":[1,2],"fjnuclearspin":[1,2],"fj":[1,2],
                    "f1":1,"f1nuclspin":1,"f2":1,"f2nuclspin":1,"f":1,"fnuclspin":1,"rname":["test","test"],"r":[1,2], "parity":1,"kronigparity":1,"assym":1},
                   {"MoleculeQNCase":"Test.qncase","MoleculeQNElecStateLabel":"Test.elecstatelabel","MoleculeQNelecSym":"Test.qnelecsym","MoleculeQNelecSymGroup":"Test.qnelecsymgroup",
                    "MoleculeQNelecInv":"Test.elecinv","MoleculeQNelecRefl":"Test.elecrefl","MoleculeQNLambda":"Test.lamb","MoleculeQNSigma":"Test.sigma",
                    "MoleculeQNOmega":"Test.omega","MoleculeQNS":"Test.s","MoleculeQNviMode":"Test.vi","MoleculeQNliMode":"Test.li","MoleculeQNv":"Test.v","MoleculeQNl":"Test.l",
                    "MoleculeQNvibInv":"Test.vibinv","MoleculeQNvibRefl":"Test.vibrefl","MoleculeQNvibSym":"Test.qnvibsym","MoleculeQNqnvibSymGroup":"Test.qnvibsymgroup",
                    "MoleculeQNc1":"Test.v1","MoleculeQNv2":"Test.v2","MoleculeQNl2":"Test.l2","MoleculeQNv3":"Test.v3","MoleculeQNJ":"Test.j","MoleculeQNK":"Test.k",
                    "MoleculeQNN":"Test.n","MoleculeQNKa":"Test.ka","MoleculeQNKc":"Test.kc","MoleculeQNrotSym":"Test.qnrotsym","MoleculeQNrotSymGroup":"Test.qnrotsymgroup",
                    "MoleculeQNrovibSym":"Test.rovibsym","MoleculeQNrovibSymGroup":"Test.rovibsymgroup","MoleculeQNI":"Test.qni","MoleculeQNInuclSpin":"Test.qninuclearspin",
                    "MoleculeQNSpinComponentLabel":"Test.spincomponentlabel","MoleculeQNFjj":"Test.fjj","MoleculeQNFjnuclSpin":"Test.fjnuclearspin","MoleculeQNFj":"Test.fj",
                    "MoleculeQNF1":"Test.f1","MoleculeQNF1nuclSpin":"Test.f1nuclspin","MoleculeQNF2":"Test.f2","MoleculeQNF2nuclSpin":"Test.f2nuclspin","MoleculeQNF":"Test.f",
                    "MoleculeQNFnuclSpin":"Test.fnuclspin","MoleculeQNrName":"Test.rname","MoleculeQNr":"Test.r","MoleculeQNparity":"Test.parity",
                    "MoleculeQNkronigParity":"Test.kronigparity","MoleculeQNasSym":"Test.assym"})
        self.assertEqual(generators.makeCaseQNs(G),
                         '<Case xsi:type="case:Case" caseID="Test" xmlns:case="http://vamdc.org/xml/xsams/0.3/cases/Test"><case:QNs><case:ElecStateLabel>test</case:ElecStateLabel><case:elecSym group="test">test</case:elecSym><case:elecInv>1</case:elecInv><case:elecRefl>2</case:elecRefl><case:Lambda>test</case:Lambda><case:Sigma>1</case:Sigma><case:Omega>1</case:Omega><case:S>1</case:S><case:v>1</case:v><case:l>1</case:l><case:vibInv>1</case:vibInv><case:vibRefl>1</case:vibRefl><case:vibSym>1</case:vibSym><case:v2>2</case:v2><case:l2>2</case:l2><case:v3>3</case:v3><case:J>1</case:J><case:K>1</case:K><case:N>1</case:N><case:Ka>1</case:Ka><case:Kc>1</case:Kc><case:rotSym group="1">1</case:rotSym><case:rovibSym group="1">1</case:rovibSym><case:I nuclearSpinRef="1">1</case:I><case:SpinComponentLabel>test</case:SpinComponentLabel><case:Fj j="1" nuclearSpinRef="1">1</case:Fj><case:Fj j="2" nuclearSpinRef="2">2</case:Fj><case:F1 nuclearSpinRef="1">1</case:F1><case:F2 nuclearSpinRef="1">1</case:F2><case:F nuclearSpinRef="1">1</case:F><case:r name="test">1</case:r><case:r name="test">2</case:r><case:parity>1</case:parity><case:kronigParity>1</case:kronigParity><case:asSym>1</case:asSym></case:QNs></Case>')
    def test_makeBroadeningType(self):
        G = self.G({"unit":"K", "method":"ex","comment":"testcomment", "accur":"0.1", "ref":["ref1","ref2"],"name":"TestType","extra":"Extra","values":[1,2,3],
                    "broadeningref":["ref1b","ref2b"],"environment":"test","method":"ex","comment":"Comment"},
                   {"RadTransBroadeningTestLineshapeParameter":"Test.values","RadTransBroadeningTestLineshapeParameterUnit":"Test.unit",
                    "RadTransBroadeningTestLineshapeParameterMethod":"Test.method", "RadTransBroadeningTestLineshapeParameterComment":"Test.comment",
                    "RadTransBroadeningTestLineshapeParameterAccuracy":"Test.accur", "RadTransBroadeningTestLineshapeParameterRef":"Test.ref",
                    "RadTransBroadeningTestLineshapeParameterName":"Test.name", "RadTransBroadeningTestLineshapeParameterExtra":"Test.extra",
                    "RadTransBroadeningTestEnvironment":"Test.environment","RadTransBroadeningTestMethod":"Test.method","RadTransBroadeningTestComment":"Test.comment"})
        self.assertEqual(generators.makeBroadeningType(G,name="Test"),
                         '<Broadening name="test" methodRef="MTestNode-ex" envRef="ETestNode-test"><Comments>Comment</Comments><Lineshape name=""><LineshapeParameter name="TestType" methodRef="MTestNode-ex"><Comments>Comment</Comments><SourceRef>BTestNode-ref1</SourceRef><Value units="K">1</Value><Accuracy>0.1</Accuracy></LineshapeParameter><LineshapeParameter name="TestType" methodRef="MTestNode-ex"><Comments>Comment</Comments><SourceRef>BTestNode-ref2</SourceRef><Value units="K">2</Value><Accuracy>0.1</Accuracy></LineshapeParameter><LineshapeParameter name="TestType" methodRef="MTestNode-ex"><Comments>Comment</Comments><SourceRef>BTestNode-ref1</SourceRef><Value units="K">3</Value><Accuracy>0.1</Accuracy></LineshapeParameter></Lineshape></Broadening>')

    def test_makeDataSeriesType(self):
        odict, kdict = self.dicts_for_primarytype("Test",extra={"TestParameter":"test","TestID":42,"TestUnits":"K"})
        odict2, kdict2 = self.dicts_for_primarytype("TestLinear",extra={"TestLinearInitial":2,"TestLinearIncrement":0.2,"TestLinearCount":5, "TestLinearUnits":"K"})
        odict3, kdict3 = ({"test":[1,2,3,4,5],"n":5,"lineara0":3,"lineara1":2,"datafile":"datafile","errorlist":[0,1,0.2],"errorn":2,"errorlistunits":"K","testerror":0.5},
                          {"Test":"Test.test","TestLinearA0":"Test.lineara0","TestLinearA1":"Test.lineara1","TestDataFile":"Test.datafile","TestErrorList":"Test.errorlist",
                           "TestErrorListN":"Test.errorn","TestErrorListUnits":"Test.errorlistunits","TestError":"Test.testerror"})
        odict.update(odict2)
        odict.update(odict3)
        kdict.update(kdict2)
        kdict.update(kdict3)
        G = self.G(odict, kdict)
        self.assertEqual(generators.makeDataSeriesType("testtag", "Test", G),
                         '<testtag methodRef="MTestNode-TestMethod" parameter="TestParameter" id="TestNode-42"><Comments>TestComment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef><DataList count=\'\'>1 2 3 4 5</DataList><LinearSequence methodRef="MTestNode-TestMethod" count="5" units="K" initial="2" increment="0.2"><Comments>TestComment</Comments><SourceRef>BTestNode-ref1</SourceRef><SourceRef>BTestNode-ref2</SourceRef></LinearSequence><DataFile>datafile</DataFile><ErrorList n=\'2\' units=\'K\'>0 1 0.2</ErrorList><Error>0.5</Error></testtag>')


class TestMainXSAMS(TestGen):
    """
    Test the core XSAMS functions in the generator. These depend on a host of help methods
    and don't take a G-function as argument, but some sort of input structure.
    """

    def make_primary(self):
        "assign all needed to do a primary tag"
    def make_datatype(self):
        "assign all needed to do a datatype tag"

    # XsamsRadTranBroadening
    # XsamsSources
    # XsamsEnvironments
    # makeAtomStateComponents
    # XsamsAtoms
    # XsamsMCSBuild
    # XsamsMSBuild
    # XsamsMolecules
    # XsamsSolids
    # XsamsParticles
    # XsamsRadTranShifting
    # XsamsRadTrans
    # XsamsRadCross
    # XsamsCollTrans
    # XsamsNonRadTrans
    # XsamsFunctions
    # XsamsMethods

    # Xsams



#
# Bibtex perser test suite
#

class TestBibTex(TestCase):
   def test_callBibTex2XML(self):
        import bibtextools
        tbibtex = """@article{BDMQ,\n        Author = {{Bi{\\'e}mont}, E. and {Dutrieux}, {J.-F.} and {Martin}, I. and {Quinet}, P.},\n        Date-Modified = {2010-09-27 17:27:07 +0200},\n        Doi = {10.1088/0953-4075/31/15/006},\n        Journal = {Journal of Physics B Atomic Molecular Physics},\n        Month = aug,\n        Note = {(BDMQ)},\n        Pages = {3321-3333},\n        Title = {{Lifetime calculations in Yb II}},\n        Volume = 31,\n        Year = 1998,\n        Bdsk-Url-1 = {http://dx.doi.org/10.1088/0953-4075/31/15/006}}\n"""
        txml = u"""<Source sourceID="BExampleNode-BDMQ">\n<Authors>\n<Author><Name>E. Bi{\\\'e}mont</Name></Author><Author><Name>J.-F. Dutrieux</Name></Author><Author><Name>I. Martin</Name></Author><Author><Name>P. Quinet</Name></Author>\n</Authors><Title>Lifetime calculations in Yb II</Title>\n<Category>journal</Category>\n<Year>1998</Year>\n<SourceName>Journal of Physics B Atomic Molecular Physics</SourceName>\n<Volume>31</Volume>\n<PageBegin>3321</PageBegin>\n<PageEnd>3333</PageEnd>\n<UniformResourceIdentifier>http://dx.doi.org/10.1088/0953-4075/31/15/006</UniformResourceIdentifier>\n<DigitalObjectIdentifier>10.1088/0953-4075/31/15/006</DigitalObjectIdentifier>\n<BibTeX>@article{BDMQ,&#10;        Author = {{Bi{\\\'e}mont}, E. and {Dutrieux}, {J.-F.} and {Martin}, I. and {Quinet}, P.},&#10;        Date-Modified = {2010-09-27 17:27:07 +0200},&#10;        Doi = {10.1088/0953-4075/31/15/006},&#10;        Journal = {Journal of Physics B Atomic Molecular Physics},&#10;        Month = aug,&#10;        Note = {(BDMQ)},&#10;        Pages = {3321-3333},&#10;        Title = {{Lifetime calculations in Yb II}},&#10;        Volume = 31,&#10;        Year = 1998,&#10;        Bdsk-Url-1 = {http://dx.doi.org/10.1088/0953-4075/31/15/006}}&#10;</BibTeX></Source>"""
#        self.maxDiff = None
        self.assertEquals(txml, bibtextools.BibTeX2XML(tbibtex))


if __name__ == "__main__":
    print "You should usually run this module from the ExampleNode node with 'manage.py test'."
