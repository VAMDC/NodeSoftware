from lxml import objectify, etree
import unittest

import sys
sys.path.insert(0, '..')

import verification
verification.VERIFICATION_SCHEMA_LOCATION = u"../verification.xsd"

from check import *



class VerificationTestCase(unittest.TestCase):

    def setUp(self):
        pass

    
    def testRunRulesTransition1MinOK(self):
        file = open("test/transition1OK.IN.xml")
        ver = Verification(file)
        ver.onlyRules= {"Rule2F":{"copy":"Rule2", "substances":"_56Fe"}}
        doc = ver.run()
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition1OK.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))

    def testGetRules(self):
        rules = VerificationParser().getRules()
        for rule in rules:
            self.assertEquals("Rule", rule[0:4])
            self.assertTrue(rules[rule]['math'].serialize("python").find('@InitialStateRef'))

    def testRunRulesTransition3MaxOK(self):
        file = open("test/transition3OK.IN.xml")
        ver = Verification(file)
        ver.onlyRules= {"Rule1":{}, "Rule2":{}}
        doc = ver.run(False)
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MAX.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))

    def testRunRulesTransition3MinOK(self):
        file = open("test/transition3OK.IN.xml")
        ver = Verification(file)
        ver.onlyRules= {"Rule1":{}, "Rule2":{}}
        doc = ver.run()
        self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MIN.xml").read())), etree.tostring(objectify.fromstring(doc.toxml())))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
