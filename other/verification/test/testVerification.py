from lxml import objectify, etree
import unittest
import sys

sys.path.insert(0, '.')
import check
check.VERIFICATION_SCHEMA_LOCATION = u'../verification.xsd'
from check import Verification, RulesParser, Rule
from check import XSAMS_NS
from check import printRules

from test import LocalResolver

parser = etree.XMLParser()
parser.resolvers.add(LocalResolver({"http://vamdc.org/xml/xsams/0.3/": check.VERIFICATION_PATH + "/xsd/xsams/0.3/xsams.xsd"}))
xsd = etree.XMLSchema(etree.parse(check.VERIFICATION_FILE_PATH, parser = parser))


class VerificationTestCase(unittest.TestCase):
	def setUp(self):
		pass


	def testAddRules(self):
		rulesParser = RulesParser()
		rulesParser.addRules = {Rule("a", "nltcs:J < 9")}
		ver = Verification("test/moleculeH2O.IN.xml", rulesParser.getRules())
		tree = ver.run()
		xsd.assertValid(tree)
		numberElements = tree.xpath('//xsams:NumberOfVerificationByRule[@name = "aRuleS01"]', namespaces={"xsams":XSAMS_NS})
		self.assertEquals(1, len(numberElements))
		for numberElement in numberElements:
			self.assertEquals("5", numberElement.attrib["correct"])
			self.assertEquals("3", numberElement.attrib["incorrect"])


	def testUseOnlyRules(self):
		rulesParser = RulesParser()
		rulesParser.useRules = {Rule("nltcsRuleT02", None), Rule("nltcsRuleT03", None)}
		ver = Verification("test/moleculeH2O.IN.xml", rulesParser.getRules())
		tree = ver.run()
		xsd.assertValid(tree)
		numberElements = tree.xpath('//xsams:NumberOfVerificationByRule', namespaces={"xsams":XSAMS_NS})
		self.assertEquals(2, len(numberElements))


	def testDelRules(self):
		rulesParser = RulesParser()
		rulesParser.delRules = {Rule("nltcsRuleT02", None)}
		ver = Verification("test/moleculeH2O.IN.xml", rulesParser.getRules())
		tree = ver.run()
		xsd.assertValid(tree)
		numberElements = tree.xpath('//xsams:NumberOfVerificationByRule', namespaces={"xsams":XSAMS_NS})
		self.assertEquals(3, len(numberElements))


	def testPythonRules(self):
		rulesParser = RulesParser()
		rules = rulesParser.getRules()
		for rule in rules:
			mathIdentifiers  = rule.getIdentifiers()
			rule.math = None
			pythonIdentifiers  = rule.getIdentifiers()
			self.assertEquals(mathIdentifiers, pythonIdentifiers)


	def testGetRules(self):
		rules = RulesParser().getRules()
		for rule in rules:
			self.assertNotEquals(rule.name.find("Rule"), -1)
			self.assertTrue(rule.python.find('#UpperStateRef'))


	def testRunRulesTransition1MinOK(self):
		rulesParser = RulesParser()
		ruleT02 = rulesParser.getRule("atomRuleT02").copy()
		ruleT02.name = "atomRuleT02F"
		ruleT02.forInChIList = ["InChI=1S/Fe/q+3/"]
		rulesParser.useRules.add(ruleT02)
		ver = Verification("test/transition1OK.IN.xml", rulesParser.getRules())
		#printRules(ver.rules)
		tree = ver.run(report = False, bad = True)
		#with self.assertRaisesRegexp(etree.DocumentInvalid, "Element '{%s}atomRuleT02F': This element is not expected." % XSAMS_NS):
		xsd.assertValid(tree)
		#etree.parse("test/transition1OK.OUT.MIN.xml", etree.XMLParser(remove_blank_text=True))
		#objectify.fromstring(open("test/transition1OK.OUT.MIN.xml").read())
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition1OK.OUT.MIN.xml").read()), pretty_print = True), etree.tostring(tree, pretty_print = True))


	def testRunRulesTransition3MaxOK(self):
		rulesParser = RulesParser()
		rulesParser.useRules = {Rule("atomRuleT01", None), Rule("atomRuleT02", None)}
		ver = Verification("test/transition3OK.IN.xml", rulesParser.getRules())
		tree = ver.run(report = True, bad = None)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MAX.xml").read()), pretty_print = True), ver.getXML())


	def testRunRulesTransition3MinOK(self):
		ver = Verification("test/transition3OK.IN.xml")
		tree = ver.run(report = False, bad = True)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/transition3OK.OUT.MIN.xml").read()), pretty_print = True), ver.getXML())


	def testRunRulesMoleculeH2OMinOK(self):
		ver = Verification("test/moleculeH2O.IN.xml")
		tree = ver.run(report = False, bad = True)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeH2O.OUT.MIN.xml").read()), pretty_print = True), ver.getXML())


	def testRunRulesMoleculeCO2MinOK(self):
		#rules = RulesParser().getRules(only={"ltcsRuleS04":{}})
		rules = None
		ver = Verification("test/moleculeCO2.IN.xml", rules = rules)
		#printRules(ver.rules)
		tree = ver.run(report = False, bad = True)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO2.OUT.MIN.xml").read()), pretty_print = True), ver.getXML())


	def testRunRulesMoleculeN2OMinOK(self):
		ver = Verification("test/moleculeN2O.IN.xml")
		tree = ver.run(bad = True)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeN2O.OUT.MIN.xml").read()), pretty_print = True), ver.getXML())


	def testRunRulesMoleculeCOAllOK(self):
		tree = Verification("test/moleculeCO.IN.xml").run()
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO.OUT.ALL.xml").read()), pretty_print = True), etree.tostring(tree, pretty_print = True))


	def testRunRulesMoleculeCOBadOK(self):
		tree = Verification("test/moleculeCO.IN.xml").run(bad = True)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO.OUT.BAD.xml").read()), pretty_print = True), etree.tostring(tree, pretty_print = True))


	def testRunRulesMoleculeCOGoodOK(self):
		tree = Verification("test/moleculeCO.IN.xml").run(bad = False)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCO.OUT.GOOD.xml").read()), pretty_print = True), etree.tostring(tree, pretty_print = True))


	def testRunRulesMoleculeC2H2MinOK(self):
		tree = Verification("test/moleculeC2H2.IN.xml").run(bad = True)
		xsd.assertValid(tree)
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeC2H2.OUT.MIN.xml").read()), pretty_print = True), etree.tostring(tree, pretty_print = True))


	def testRunRulesMoleculeCH4MinOK(self):
		ver = Verification("test/moleculeCH4.IN.xml")
		#printRules(ver.rules)
		tree = ver.run(bad = True)
		xsd.assertValid(tree)
		#Need test RuleT03
		self.assertEquals(etree.tostring(objectify.fromstring(open("test/moleculeCH4.OUT.MIN.xml").read()), pretty_print = True), ver.getXML())


	def tearDown(self):
		pass


#from test import makeTestFileFromBigFile
#makeTestFileFromBigFile('moleculeCH4a', 3)

if __name__ == '__main__':
	unittest.main()
