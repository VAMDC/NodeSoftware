import sys

if __name__ == '__main__':
	VERIFICATION_SCHEMA_LOCATION = u"../verification.xsd"
else:
	try:
		import verification
	except ImportError:
		from .. import verification
	VERIFICATION_SCHEMA_LOCATION = verification.VERIFICATION_SCHEMA_LOCATION

from lxml import etree
from StringIO import StringIO
import re
from mathml.lmathdom import MathDOM
from mathml.utils import pyterm # register Python term builder

XSI_NS = "http://www.w3.org/2001/XMLSchema-instance" 
XSD_NS = "http://www.w3.org/2001/XMLSchema"
XSAMS_NS = "http://vamdc.org/xml/xsams/0.3"
MATHML_NS = "http://www.w3.org/1998/Math/MathML"

class NoMathMLException(Exception):
	pass



class NoValidException(Exception):
	pass



class Verification:
	def __init__(self, file, rules = None):
		self.tree = etree.parse(file, parser= etree.XMLParser(remove_blank_text=True))
		self.rules = RulesParser().getRules() if not rules else rules
		self.lock = False

		self.stateNodes = {}
		self.whiteListOfRefs = {}

		
	def _setSchemaLocation(self):
		root = self.tree.getroot()
		locations = root.get('{%s}schemaLocation' % XSI_NS).split(' ')
		locations[1] = VERIFICATION_SCHEMA_LOCATION
		root.set('{%s}schemaLocation' % XSI_NS, locations[0] + ' ' + locations[1])


	def run(self, report=True, clean=True):
		if not self.lock:
			self._setSchemaLocation()
			self._removeVerificationNode()
			self._addRulesNodes()
			if report:
				self._addVerificationResultNode()
			if clean:
				self._removeRedundantNodes()

		return self.tree


	def _removeRedundantNodes(self):
		self.whiteListOfRefs = {}
		parentsOfNodesWithVerification = {}

		nodesWithVerification = self.tree.xpath('//child::xsams:Verification[contains(self::node(),  "false") or descendant-or-self::node()/attribute::xsi:nil]', namespaces={"xsams": XSAMS_NS, 'xsi': XSI_NS})
		if nodesWithVerification:
			for nodeWithVerification in nodesWithVerification:
				if not nodeWithVerification.xpath('./child::*[contains(self::node(),  "false") or contains(self::node(),  "true")]'):
					for childNode in nodeWithVerification[:]:
						nodeWithVerification.remove(childNode)
					nodeWithVerification.set('{%s}nil' % XSI_NS, "true")

				for refNode in nodeWithVerification.getparent().xpath('.//*[contains(local-name(@*), "Ref") or contains(local-name(), "Ref")]'):
					if refNode.attrib:
						for attribute in refNode.attrib:
							if attribute.endswith('Ref'):
								self.whiteListOfRefs[refNode._attrs[attribute]] = None
					elif refNode.tag.endswith('Ref'):
						if refNode.text is not None:
							self.whiteListOfRefs[refNode.text] = None

				parentsOfNodesWithVerification[nodeWithVerification.getparent()] = None
		else:
			for childNode in list(self.tree.getroot())[:]:
				self.tree.getroot().remove(childNode)

		for parentOfNodesWithVerification in parentsOfNodesWithVerification:
			for attribute in parentOfNodesWithVerification.attrib:
				if attribute.endswith('ID'):
					self.whiteListOfRefs[parentOfNodesWithVerification.attrib[attribute]] = None

		self._removeRedundantParentNodes(parentsOfNodesWithVerification, self.tree)


	def _removeRedundantParentNodes(self, usefulParentNodes, stopNode):
		if not usefulParentNodes or stopNode in usefulParentNodes:
			return

		parentsOfNodesWithVerification = {}
		for usefulParentNode in usefulParentNodes:
			if usefulParentNode.getparent() is not None and not parentsOfNodesWithVerification.has_key(usefulParentNode.getparent()):
				parentsOfNodesWithVerification[usefulParentNode.getparent()] = None

				childNodeNames = [childNode.tag for childNode in list(usefulParentNode.getparent())]
				singleUseNodeNames = [childNodeName for childNodeName in childNodeNames if childNodeNames.count(childNodeName) == 1]

				flag = True
				while flag:
					flag = False
					for childNode in list(usefulParentNode.getparent())[:]:
						if not (childNode in usefulParentNodes):
							hasIDs = False
							isRedundantNode = True
							idNodes = {}
							if childNode.tag == '{%s}Processes' % XSAMS_NS:
								if not childNode.xpath('.//child::xsams:Verification[contains(self::node(),  "false") or descendant-or-self::node()/attribute::xsi:nil]', namespaces={"xsams": XSAMS_NS, 'xsi': XSI_NS}):
									usefulParentNode.getparent().remove(childNode)
									flag = True
									break
							elif childNode.tag == '{%s}VerificationResult' % XSAMS_NS:
								pass

							else:
								for idNode in childNode.xpath('descendant-or-self::node()[contains(local-name(@*), "ID")]'):
									for attribute in idNode.attrib:
										if attribute.endswith('ID'):
											hasIDs = True
											if self.whiteListOfRefs.has_key(idNode.attrib[attribute]):
												isRedundantNode = False
												idNodes[idNode] = None

							if isRedundantNode:
								if hasIDs or not (childNode.tag in singleUseNodeNames):
									usefulParentNode.getparent().remove(childNode)
							else:
								self._removeRedundantParentNodes(idNodes, childNode)

		self._removeRedundantParentNodes(parentsOfNodesWithVerification, stopNode)


	def _setStateNodes(self):
		for stateNode in self.tree.xpath('//*[@stateID]'):
			self.stateNodes[stateNode.get('stateID')] = stateNode


	def _checkDomains(self, ruleInfo):
		domainFlag = None
		for domain in ruleInfo['domains']:
			if domain.endswith('AtomicState'):
				if domainFlag is not None and domainFlag != 'AtomicState':
					raise NoValidException("Allowed only similar domains but not " + str(ruleInfo['domains']))
				domainFlag = 'AtomicState'
			elif domain.endswith('MolecularState'):
				if domainFlag is not None and domainFlag != 'MolecularState':
					raise NoValidException("Allowed only similar domains but not " + str(ruleInfo['domains']))
				domainFlag = 'MolecularState'
			elif domain.endswith('Transition'):
				if domainFlag is not None and domainFlag != 'Transition':
					raise NoValidException("Allowed only similar domains but not " + str(ruleInfo['domains']))
				domainFlag = 'Transition'

		return domainFlag


	def _addRulesNodes(self):
		if not self.lock:
			self._setStateNodes()
			dataNodes = {'AtomicState': {}, 'MolecularState': {}, 'Transition': {}}

			for rule in sorted(self.rules):

				if self.rules[rule]['domains']:
					domainFlag = self._checkDomains(self.rules[rule])
				else:
					continue

				templateExp = self.rules[rule]['math'].serialize("python")

				identifiers = {}
				xpathEval = etree.XPath('.//math:ci[not(contains(self::node(),  "\'"))]', namespaces = {"math": MATHML_NS})
				for ci in xpathEval(self.rules[rule]['math']._etree):
					name = ci.text
					identifiers[name] = name.split('#')

				for identifier in identifiers:
					if len(identifiers[identifier]) > 1:
						if domainFlag != 'Transition':
							raise NoValidException("Allowed only 'ci' with the '#' symbol but not " + str(identifiers[identifier]))
						if not dataNodes[domainFlag]:
							for domain in self.rules[rule]['domains']:
								dataNodes[domainFlag].update(dict.fromkeys(self.tree.xpath('//xsams:' + domain + '[./xsams:' + identifiers[identifier][1] + ']', namespaces = {"xsams": XSAMS_NS})))
						break
					else:
						if domainFlag != 'AtomicState' and domainFlag != 'MolecularState':
							raise NoValidException("Allowed only 'ci' without the '#' symbol but not " + str(identifiers[identifier]))
						if domainFlag == 'AtomicState' and identifier.find(':') != -1:
							raise NoValidException("Allowed only 'ci' without the ':' symbol but not " + str(identifiers[identifier]))
						if domainFlag == 'MolecularState' and identifier.find(':') == -1:
							raise NoValidException("Allowed only 'ci' with the ':' symbol but not " + str(identifiers[identifier]))
						if not dataNodes[domainFlag]:
							for domain in self.rules[rule]['domains']:
								dataNodes[domainFlag].update(dict.fromkeys(self.tree.xpath('//xsams:' + domain, namespaces = {"xsams": XSAMS_NS})))
						break

				for dataNode in dataNodes[domainFlag]:

					if dataNodes[domainFlag][dataNode] is None:
						dataNodes[domainFlag][dataNode] = {}

					currentExp = templateExp

					available = None
					for identifier in identifiers:
						if not (identifier in dataNodes[domainFlag][dataNode]):
							if domainFlag == 'Transition':
								for stateRefNode in dataNode.iterchildren(tag=etree.Element):
									if stateRefNode.tag == '{%s}'% XSAMS_NS + identifiers[identifier][1]:
										if stateRefNode.text is not None:
											stateID = stateRefNode.text
										else:
											raise NoValidException("No value of '" + identifiers[identifier][1] + "'")
										if stateID in self.stateNodes:
											value = self._getValue(self.stateNodes[stateID], identifiers[identifier][0])
											dataNodes[domainFlag][dataNode][identifier] = {"stateID": stateID, "value": value}
										else:
											raise NoValidException("No matches '" + stateID + "' Ref to ID ")
										break
							else:
								if dataNode.attrib['stateID']:
									stateID = dataNode.get('stateID')
									value = self._getValue(self.stateNodes[stateID], identifier)
									dataNodes[domainFlag][dataNode][identifier] = {"stateID": stateID, "value": value}

						if dataNodes[domainFlag][dataNode].has_key(identifier):
							if available is None:
								if dataNodes[domainFlag][dataNode][identifier]["value"] is None:
									available = self._isAvailableNode(self.stateNodes[dataNodes[domainFlag][dataNode][identifier]["stateID"]], self.rules[rule])
									if available:
										self._addRuleNode(dataNode, [rule, None])
									available = False
								elif dataNodes[domainFlag][dataNode][identifier]["value"] == False:
									available = False
								else:
									available = self._isAvailableNode(self.stateNodes[dataNodes[domainFlag][dataNode][identifier]["stateID"]], self.rules[rule])
							if available is not None and not available:
								break
							currentExp = currentExp.replace(identifier, dataNodes[domainFlag][dataNode][identifier]["value"])
						else:
							available = False
							break

					if available:
						self._addRuleNode(dataNode, [rule, str(eval(currentExp)).lower()])

			self.lock = True
		return self.tree


	def _addVerificationResultNode(self):
		rootNode = self.tree.getroot()
		if rootNode is not None:

			verificationDataElement = etree.Element('{%s}VerificationData' % XSAMS_NS, nsmap=rootNode.nsmap)
			for attr in rootNode.attrib:
				verificationDataElement.set(attr, rootNode.attrib[attr])

			rootNode.attrib.clear()

			self.tree._setroot(verificationDataElement)
			verificationDataElement.append(rootNode)
			rootNode = verificationDataElement

			verificationResultNodes = rootNode.xpath('./xsams:VerificationResult', namespaces = {"xsams":XSAMS_NS})
			if verificationResultNodes:
				for childNode in verificationResultNodes[:]:
					verificationResultNodes[0].getparent().remove(childNode)

			verificationResultElement = etree.Element('{%s}VerificationResult' % XSAMS_NS, nsmap=rootNode.nsmap)

			nodesWithVerification = self.tree.xpath('//child::xsams:Verification', namespaces = {"xsams":XSAMS_NS})
			if nodesWithVerification:
				domainNumbers = {'AtomicState' : None, 'MolecularState' : None, 'RadiativeTransition' : None, 'NonRadiativeTransition' : None}

				for domain in domainNumbers:
					domainNumbers[domain] = {'total': 0, 'correct': 0, 'incorrect': 0, 'unidentified': 0}

				for nodeWithVerification in nodesWithVerification:
					domain = localTagName(nodeWithVerification.getparent().tag)
					domainNumbers[domain]['total'] += 1
					if nodeWithVerification.get('{%s}nil' % XSI_NS) == "true":
						domainNumbers[domain]['unidentified'] += 1
					else:
						flagOne = True
						for ruleNode in nodeWithVerification.iterchildren(tag=etree.Element):
							ruleNodeLocalTag =  localTagName(ruleNode.tag)
							if not domainNumbers.has_key(ruleNodeLocalTag):
								domainNumbers[ruleNodeLocalTag] = {'correct': 0, 'incorrect': 0, 'unidentified': 0}
							if ruleNode.get('{%s}nil' % XSI_NS) == "true":
								flagOne = None
								domainNumbers[ruleNodeLocalTag]['unidentified'] += 1
							elif ruleNode.text is not None:
								if ruleNode.text == "true":
									domainNumbers[ruleNodeLocalTag]['correct'] += 1
								else:
									if flagOne is not None:
										flagOne = False
									domainNumbers[ruleNodeLocalTag]['incorrect'] += 1
						if flagOne:
							domainNumbers[domain]['correct'] += 1
						elif flagOne is None:
							domainNumbers[domain]['unidentified'] += 1
						else:
							domainNumbers[domain]['incorrect'] += 1

				for ruleName in sorted(domainNumbers):
					if ruleName.find('Rule') == -1:
						if domainNumbers[ruleName]['total'] == 0:
							continue
						numberElement = etree.Element(('{%s}NumberOf' + ruleName + 's') % XSAMS_NS, nsmap=rootNode.nsmap)
					else:
						numberElement = etree.Element('{%s}NumberOfVerificationByRule' % XSAMS_NS, nsmap=rootNode.nsmap)
						numberElement.set('name', ruleName)
					for numberName in sorted(domainNumbers[ruleName]):
						numberElement.set(numberName, str(domainNumbers[ruleName][numberName]))
					verificationResultElement.append(numberElement)
			else:
				verificationResultElement.set('{%s}nil' % XSI_NS, "true")

			if list(rootNode):
				rootNode.insert(0, verificationResultElement)
			else:
				rootNode.append(verificationResultElement)

			return verificationResultElement

		else:
			return None


	def _isAvailableNode(self, element, rule):
		if not rule['forInChIList']:
			return True
		else:
			forInChIList = rule['forInChIList'].split(' ')

		InChI = None
		if element.tag == '{%s}AtomicState' % XSAMS_NS:
			#Atoms.Atom.Isotope.Ion.AtomicState

			for ionChild in element.getparent().iterchildren(tag=etree.Element):
				if ionChild.tag =='{%s}InChI' % XSAMS_NS:
					if ionChild.text is not None:
						InChI = ionChild.text
					else:
						return False
						#raise NoValidException("No 'InChI' element")
		elif element.tag == '{%s}MolecularState' % XSAMS_NS:
			#Molecules.Molecule.MolecularState
			for moleculeChild in element.getparent().iterchildren(tag=etree.Element):
				if moleculeChild.tag == '{%s}MolecularChemicalSpecies' % XSAMS_NS:
					for molecularChemicalSpeciesChild in moleculeChild.iterchildren(tag=etree.Element):
						if molecularChemicalSpeciesChild.tag == '{%s}InChI' % XSAMS_NS:
							if molecularChemicalSpeciesChild.text is not None:
								InChI = molecularChemicalSpeciesChild.text
							else:
								return False
		else:
			return False

		for patternInChI in forInChIList:
			if patternInChI.find("'") == -1:
				if str(InChI) == patternInChI:
					return True
			else:
				#InChI=1S/H2O/h1H2'.*'
				patternInChIParts = patternInChI.split("'")
				if (len(patternInChIParts) % 2) == 1:
					currentPatternInChI = ""
					for i, patternInChIPart in enumerate(patternInChIParts):
						if (i % 2) == 1:
							currentPatternInChI += patternInChIPart
						else:
							currentPatternInChI += re.escape(patternInChIPart)
					if re.search(currentPatternInChI, InChI):
						return True
				else:
					return False
		return False


	def _getValue(self, element, name):
		if element.tag == '{%s}AtomicState' % XSAMS_NS or element.tag == '{%s}MolecularState' % XSAMS_NS:
			namespaces = {"xsams": XSAMS_NS}
			if element.tag == '{%s}AtomicState' % XSAMS_NS:
				cases = element.xpath('.//xsams:AtomicQuantumNumbers', namespaces={"xsams":XSAMS_NS})
				if cases:
					if name.find(':') != -1:
						return False
					name = "xsams:" + name
				else:
					return None
			elif element.tag == '{%s}MolecularState' % XSAMS_NS:
				cases = element.xpath('.//*[local-name() = "Case"]')
				if cases:
					caseID = cases[0].get('caseID')
					if caseID:
						parts = name.split(':')
						if caseID != parts[0]:
							return False
					else:
						return None
					namespaces[caseID] = 'http://vamdc.org/xml/xsams/0.3/cases/' + caseID
				else:
					return None

			noneFlag = False
			if name[-1:] == '?':
				name = name[0:-1]
				noneFlag = True

			qns = element.xpath('.//'  + name, namespaces = namespaces)
			if qns and qns[0] is not None and qns[0].text is not None:
				data = qns[0].text
				return data if is_number(data) else '"' + data + '"'
			else:
				if noneFlag:
					return 'None'
				return None
		else:
			return False


	def _addRuleNode(self, element, ruleItem):
		ruleElement = etree.Element(('{%s}' + ruleItem[0]) % XSAMS_NS, nsmap=element.nsmap)
		if ruleItem[1] is None:
			ruleElement.set('{%s}nil' % XSI_NS, "true")
		else:
			ruleElement.text = ruleItem[1]

		verificationNodes = element.xpath('.//xsams:Verification', namespaces={"xsams":XSAMS_NS})
		if verificationNodes:
			verificationElement = verificationNodes[0]
			ruleNodes = verificationElement.xpath('.//xsams:' + ruleItem[0], namespaces={"xsams":XSAMS_NS})
			if ruleNodes:
				verificationElement.replace(ruleElement, ruleNodes[0])
			else:
				verificationElement.append(ruleElement)
		else:
			verificationElement = etree.Element('{%s}Verification' % XSAMS_NS, nsmap=element.nsmap)
			verificationElement.append(ruleElement)
			element.append(verificationElement)

		return ruleElement


	def _removeVerificationNode(self):
		verificationNodes = self.tree.xpath(('//*[local-name() = "Verification"]'))
		for verificationNode in verificationNodes[:]:
			verificationNode.getparent().remove(verificationNode)


	def getXML(self, pretty_print=True):
		return etree.tostring(self.tree, pretty_print=pretty_print)


def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def printRules(rules):
	for rule in sorted(rules):
		print rules[rule]['math'].serialize("python")

def localTagName(tagName):
	if tagName[:1] == '{':
		return tagName.split('}', 1)[-1]
	else:
		return tagName


class RulesParser:
	domains = {}
	rules = {}

	def __init__(self):
		pass
	

	def _setDomains(self, prefix, currentNode, name):
		rulesList = currentNode.xpath('.//' + prefix + ':element', namespaces = {prefix: XSD_NS})
		for ruleNode in rulesList:
			if ruleNode.attrib['name']:
				if not (ruleNode.get('name') in self.domains):
					self.domains[ruleNode.get('name')] = []
				if not (name in self.domains[ruleNode.get('name')]):
					self.domains[ruleNode.get('name')].append(name)
			elif ruleNode.attrib['ref']:
				if not (ruleNode.get('ref') in self.domains):
					self.domains[ruleNode.get('ref')] = []
				if not (name in self.domains[ruleNode.get('ref')]):
					self.domains[ruleNode.get('ref')].append(name)

		groupRefList = currentNode.xpath('.//' + prefix + ':group[@ref]', namespaces = {prefix: XSD_NS})
		for groupRefNode in groupRefList:
			groupList = currentNode.xpath('//' + prefix + ':group[@name = "' + groupRefNode.get('ref') + '"]', namespaces = {prefix: XSD_NS})
			for groupNode in groupList:
				self._setDomains(prefix, groupNode, name)


	def getRules(self, without=None, only=None):
		if not only: only = {}
		if not without: without = {}
		if not self.rules:
			tree = XSDTree.makeOne("verification.xsd")

			if not tree:
				return self.rules

			root = tree.getroot()
			prefix = root.prefix

			verificationTypes = tree.xpath('//' + prefix + ':complexType[contains(@name, "Verification")]', namespaces = {prefix: XSD_NS})
			for verificationType in verificationTypes:
				name = verificationType.get('name')
				name = name[0].upper() + name[1:-len('Verification')]
				self._setDomains(prefix, verificationType, name)

			ruleNodes = tree.xpath('//' + prefix + ':element[contains(@name, "Rule")]', namespaces = {prefix: XSD_NS})
			for ruleNode in ruleNodes:
				mathNodes = ruleNode.xpath('.//math:math', namespaces={"math":MATHML_NS})
				if mathNodes:
					mathDoc = MathDOM()
					mathDoc._etree = etree.XML(etree.tostring(mathNodes[0]), parser=mathDoc._parser)
					if mathDoc is None:
						raise NoMathMLException("The 'math' construction has errors")

					self.rules[ruleNode.get('name')] = {'domains': self.domains[ruleNode.get('name')] if self.domains.has_key(ruleNode.get('name')) else [],
					                                             'forInChIList': mathNodes[0].getparent().get('forInChIList'),
					                                             'math': mathDoc}

		rules = {}
		for rule in self.rules:
			rules[rule] = self.rules[rule].copy()
		for fakeRule in without:
			if fakeRule in rules:
				del rules[fakeRule]

		for fakeRule in only:
			if not (fakeRule in rules) and "copy" in only[fakeRule] and only[fakeRule]["copy"] in rules:
				rules[fakeRule] = rules[only[fakeRule]["copy"]]
				rules[fakeRule].update(only[fakeRule])

		if only:
			for rule in self.rules:
				if not rule in only:
					del rules[rule]

		return rules


class XSDTree:

	def makeOne(fileName):
		file = open(fileName)
		if not file:
			return None
		tree = etree.parse(file)
		innerRoot = tree.getroot()
		prefix = innerRoot.prefix

		dir = fileName[0: fileName.rfind('/') + 1]

		availableElements = {}
		includes = ["include", "redefine"]
		for include in includes:
			includeList = tree.xpath('/' + prefix + ':schema/' + prefix + ':' + include, namespaces = {prefix: XSD_NS})
			for includeElement in includeList:
				schemaLocation = includeElement.get("schemaLocation")
				if schemaLocation.find('http://') > -1:
					continue
				location = dir + schemaLocation
				parent = includeElement.getparent()

				redefines = []
				if include == 'redefine':
					for redefineChild in includeElement.iterchildren(tag=etree.Element):
						if not availableElements.has_key(redefineChild.tag):
							availableElements[redefineChild.tag] = {}

						if redefineChild.tag == "{%s}simpleType" % XSD_NS:
							for item in redefineChild.iterdescendants(prefix + 'restriction'):
								del item.attrib["base"]
								availableElements[redefineChild.tag][redefineChild.get("name")] = item

						if redefineChild.tag == "{%s}complexType" % XSD_NS:
							for redefineChildContent in redefineChild.iterchildren(tag=etree.Element):
								if redefineChildContent.tag == "{%s}complexContent" % XSD_NS:
									for item in redefineChildContent.iterdescendants(prefix + 'restriction'):
										del item.attrib["base"]
										availableElements[redefineChild.tag][redefineChild.get("name")] = item
									for item in redefineChildContent.iterdescendants(prefix + 'extension'):
										del item.attrib["base"]
										availableElements[redefineChild.tag][redefineChild.get("name")] = item

						redefines.append(redefineChild)

				for elem in redefines:
					parent.append(elem)

				innerTree = XSDTree.makeOne(location)
				if not innerTree:
					return None

				parent.remove(includeElement)


				for innerChild in innerTree.getroot().iterchildren(tag=etree.Element):
					if availableElements.has_key(innerChild.tag) and availableElements[innerChild.tag].has_key(innerChild.get("name")):
						unknown = availableElements[innerChild.tag][innerChild.get("name")]
						if isinstance(unknown, etree._Element):
							unknown.firstChild.insert(unknown.firstChild.getparent().index(unknown.firstChild), innerChild)
						continue

					if not availableElements.has_key(innerChild.tag):
						availableElements[innerChild.tag] = {}

					availableElements[innerChild.tag][innerChild.get("name")] = True

					parent.append(innerChild)
		return tree

	makeOne = staticmethod(makeOne)

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1]:
		file = open(sys.argv[1])
	else:
		file = open("test/transition3OK.IN.xml")

	xml = Verification(file).getXML()
	if len(sys.argv) > 2 and sys.argv[2]:
		out = open(sys.argv[2], 'w')
		out.write(xml)
		out.close()
	else:
		print xml
