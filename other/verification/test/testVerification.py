from lxml import objectify, etree
import unittest
import sys


sys.path.insert(0, '..')
import verification


verification.VERIFICATION_SCHEMA_LOCATION = u"../verification.xsd"

sys.path.insert(0, '.')
from check import *


class VerificationTestCase(unittest.TestCase):
	def setUp(self):
		pass


	def testGetRules(self):
		rules = RulesParser().getRules()
		for rule in rules:
			self.assertNotEquals(rule.find("Rule"), -1)
			self.assertTrue(rules[rule]['math'].serialize("python").find('#InitialStateRef'))


	def testRunRulesTransition1MinOK(self):
		ver = Verification("test/transition1OK.IN.xml", RulesParser().getRules(only={"atomRuleT02F": {"copy": "atomRuleT02", "forInChIList": "InChI=1S/Fe/q+3/"}}))
		#printRules(ver.rules)
		tree = ver.run(report=False, clean=True)
		#etree.parse("test/transition1OK.OUT.MIN.xml", etree.XMLParser(remove_blank_text=True))
		#objectify.fromstring(open("test/transition1OK.OUT.MIN.xml").read())
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition1OK.OUT.MIN.xml").read()), pretty_print=True),  etree.tostring(tree, pretty_print=True))
	

	def testRunRulesTransition3MaxOK(self):
		ver = Verification("test/transition3OK.IN.xml", RulesParser().getRules(only={"atomRuleT01": {}, "atomRuleT02": {}}))
		tree = ver.run(report=True, clean=False)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MAX.xml").read()), pretty_print=True),  ver.getXML())
	

	def testRunRulesTransition3MinOK(self):
		ver = Verification("test/transition3OK.IN.xml")
		tree = ver.run(report=False, clean=True)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MIN.xml").read()), pretty_print=True),  ver.getXML())


	def testRunRulesMoleculeH2OMinOK(self):
		ver = Verification("test/moleculeH2O.IN.xml")
		tree = ver.run(report=False, clean=True)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeH2O.OUT.MIN.xml").read()), pretty_print=True),  ver.getXML())


	def testRunRulesMoleculeCO2MinOK(self):
		#rules = RulesParser().getRules(only={"ltcsRuleS04":{}})
		rules = None
		ver = Verification("test/moleculeCO2.IN.xml", rules = rules)
		#printRules(ver.rules)
		tree = ver.run(report=False, clean=True)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO2.OUT.MIN.xml").read()), pretty_print=True),  ver.getXML())


	def testRunRulesMoleculeN2OMinOK(self):
		ver = Verification("test/moleculeN2O.IN.xml")
		tree = ver.run()
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeN2O.OUT.MIN.xml").read()), pretty_print=True),  ver.getXML())


	def testRunRulesMoleculeCOMinOK(self):
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO.OUT.MIN.xml").read()), pretty_print=True),  etree.tostring(Verification("test/moleculeCO.IN.xml").run(), pretty_print=True))


	def testRunRulesMoleculeC2H2MinOK(self):
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeC2H2.OUT.MIN.xml").read()), pretty_print=True),  etree.tostring(Verification("test/moleculeC2H2.IN.xml").run(), pretty_print=True))


	def testRunRulesMoleculeCH4MinOK(self):
		ver = Verification("test/moleculeCH4.IN.xml")
		#printRules(ver.rules)
		tree = ver.run()
		#Need test RuleT03
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCH4.OUT.MIN.xml").read()), pretty_print=True),  ver.getXML())
	
		
	def tearDown(self):
		pass


#from test import makeTestFileFromBigFile
#makeTestFileFromBigFile('moleculeCH4a', 3)

if __name__ == '__main__':
	unittest.main()
