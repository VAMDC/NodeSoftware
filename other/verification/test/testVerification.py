from lxml import objectify, etree
import unittest

import sys

sys.path.insert(0, '.')
sys.path.insert(0, '..')

import verification

verification.VERIFICATION_SCHEMA_LOCATION = u"../verification.xsd"

from check import *


class VerificationTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def testRunRulesTransition1MinOK(self):
        ver = Verification(open("test/transition1OK.IN.xml"))
        ver.onlyRules = {"atomRuleT02F": {"copy": "atomRuleT02", "forInChIList": "InChI=1S/Fe/q+3/"}}
        doc = ver.run(False, True)
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition1OK.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))

    def testGetRules(self):
        rules = VerificationParser().getRules()
        for rule in rules:
            self.assertNotEquals(rule.find("Rule"), -1)
            self.assertTrue(rules[rule]['math'].serialize("python").find('#InitialStateRef'))

    def testRunRulesTransition3MaxOK(self):
        ver = Verification(open("test/transition3OK.IN.xml"))
        ver.onlyRules = {"atomRuleT01": {}, "atomRuleT02": {}}
        doc = ver.run(True, False)
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MAX.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))

    def testRunRulesTransition3MinOK(self):
        ver = Verification(open("test/transition3OK.IN.xml"))
        doc = ver.run(False, True)
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))


    def testRunRulesMoleculeH2OMinOK(self):
        ver = Verification(open("test/moleculeH2O.IN.xml"))
        doc = ver.run(False, True)
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeH2O.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))


    def testRunRulesMoleculeCO2MinOK(self):
        ver = Verification(open("test/moleculeCO2.IN.xml"))
        #ver.printRules()
        #ver.onlyRules= {"ltcsRuleS04":{}}
        doc = ver.run(False, True)
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO2.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))


    def testRunRulesMoleculeN2OMinOK(self):
        ver = Verification(open("test/moleculeN2O.IN.xml"))
        doc = ver.run()
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeN2O.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))


    def testRunRulesMoleculeCOMinOK(self):
        ver = Verification(open("test/moleculeCO.IN.xml"))
        #ver.printRules()
        doc = ver.run()
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))

    def testRunRulesMoleculeC2H2MinOK(self):
        ver = Verification(open("test/moleculeC2H2.IN.xml"))
        #ver.onlyRules= {"lpcsRuleS02":{}}
        #ver.printRules()
        doc = ver.run()
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeC2H2.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))


    def tearDown(self):
        pass


#from test import makeTestFile
#makeTestFile('moleculeCO', 3)

if __name__ == '__main__':
    unittest.main()
