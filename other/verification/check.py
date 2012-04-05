import copy
import sys
import os


VERIFICATION_PATH = os.path.dirname(os.path.abspath(__file__))
VERIFICATION_FILE_PATH = VERIFICATION_PATH + "/verification.xsd"

if __name__ == '__main__':
	VERIFICATION_SCHEMA_LOCATION = VERIFICATION_FILE_PATH
else:
	VERIFICATION_SCHEMA_LOCATION = "https://raw.github.com/VAMDC/NodeSoftware/master/other/verification/verification.xsd"

from lxml import etree
import cStringIO
import re
from mathml.lmathdom import MathDOM
from mathml.utils import pyterm # register Python term builder


XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
XSD_NS = "http://www.w3.org/2001/XMLSchema"
XSAMS_NS = "http://vamdc.org/xml/xsams/0.3"
MATHML_NS = "http://www.w3.org/1998/Math/MathML"

SUBSTANCES = {#
              'Ion': '/xsams:Species/xsams:Atoms/xsams:Atom/xsams:Isotope/xsams:Ion', #
              'Molecule': '/xsams:Species/xsams:Molecules/xsams:Molecule', #
}

INCHES = {#
          'Ion': '/xsams:InChI', #
          'Molecule': '/xsams:MolecularChemicalSpecies/xsams:InChI', #
}

STATES = {#
          'AtomicState': SUBSTANCES['Ion'] + '/xsams:AtomicState', #
          'MolecularState': SUBSTANCES['Molecule'] + '/xsams:MolecularState', #
}

TRANSITIONS = {#
               'RadiativeTransition': '/xsams:Processes/xsams:Radiative/xsams:RadiativeTransition', #
               'NonRadiativeTransition': '/xsams:Processes/xsams:NonRadiative/xsams:NonRadiativeTransition'#
}

DOMAINS = {}
DOMAINS.update(STATES)
DOMAINS.update(TRANSITIONS)

XSAMSData_PATH = '/xsams:XSAMSData'
VER_XSAMSData_PATH = '/xsams:VerificationData' + XSAMSData_PATH

POSITIONS = {#
             'UpperStateRef': '{%s}UpperStateRef' % XSAMS_NS, #
             'LowerStateRef': '{%s}LowerStateRef' % XSAMS_NS, #
}


class NoMathMLException(Exception):
	pass



class NoValidException(Exception):
	pass



class Verification:
	def __init__(self, file, rules = None):
		if file[0] == '<':
			file = cStringIO.StringIO(file)
		self.tree = etree.parse(file, parser = etree.XMLParser(remove_blank_text = True))
		self.rules = RulesParser().getRules() if not rules else rules
		self.lock = False

		self.verificationCache = {}
		self._setInchiCache()
		self._setCaches()


	def _setSchemaLocation(self):
		root = self.tree.getroot()
		locations = root.get('{%s}schemaLocation' % XSI_NS).split(' ')
		locations[1] = VERIFICATION_SCHEMA_LOCATION
		root.set('{%s}schemaLocation' % XSI_NS, locations[0] + ' ' + locations[1])


	def run(self, report = True, bad = None):
		if not self.lock:
			self._setSchemaLocation()
			#self._removeVerificationNode()
			self._addRulesNodes()
			self._addVerificationDataNode()
			if report:
				self._addVerificationResultNode()
			if bad is not None:
				if bad:
					self._removeRedundantNodes()
				else:
					self._removeRedundantNodes(False)

		return self.tree


	def _removeRedundantNodes(self, bad = True):
		self.whiteListOfRefs = {}
		parentsOfNodesWithVerification = {}

		verXPath = '/xsams:Verification[' + ('' if bad else 'not(') + 'contains(self::node(),  "false") or descendant-or-self::node()/attribute::xsi:nil' + ('' if bad else ')') + ']'
		nodesWithVerification = []
		for domain in DOMAINS:
			nodesWithVerification.extend(self.tree.xpath(VER_XSAMSData_PATH + DOMAINS[domain] + verXPath, namespaces = {"xsams": XSAMS_NS, 'xsi': XSI_NS}))
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
								self.whiteListOfRefs[refNode.attrib[attribute]] = None
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

		self._removeRedundantParentNodes(parentsOfNodesWithVerification, self.tree, bad)


	def _removeRedundantParentNodes(self, usefulParentNodes, stopNode, bad = True):
		verXPath = '/xsams:Verification[' + ('' if bad else 'not(') + 'contains(self::node(),  "false") or descendant-or-self::node()/attribute::xsi:nil' + ('' if bad else ')') + ']'
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
								nodesWithVerification = []
								for domain in TRANSITIONS:
									nodesWithVerification.extend(self.tree.xpath(VER_XSAMSData_PATH + DOMAINS[domain] + verXPath, namespaces = {"xsams": XSAMS_NS, 'xsi': XSI_NS}))
								if not nodesWithVerification:
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
								self._removeRedundantParentNodes(idNodes, childNode, bad)

		self._removeRedundantParentNodes(parentsOfNodesWithVerification, stopNode, bad)


	def _setInchiCache(self):
		self.inchiCache = {}
		for substance in SUBSTANCES:
			for substanceNode in self.tree.xpath(XSAMSData_PATH + SUBSTANCES[substance], namespaces = {"xsams": XSAMS_NS}):
				inchiNodes = substanceNode.xpath('.' + INCHES[substance], namespaces = {"xsams": XSAMS_NS})
				if inchiNodes and inchiNodes[0].text is not None:
					self.inchiCache[substanceNode] = inchiNodes[0].text
				else:
					self.inchiCache[substanceNode] = False


	def _setCaches(self):
		self.qnsCache = {}
		self.casesCache = {}
		self.upLowCache = {}
		self.nodesCache = {}

		atomicQNs = '{%s}AtomicQuantumNumbers' % XSAMS_NS
		caseQNs = '{%s}Case' % XSAMS_NS
		for domain in STATES:
			self.nodesCache[domain] = {}
			for node in self.tree.xpath(XSAMSData_PATH + DOMAINS[domain] + '[@stateID]', namespaces = {"xsams": XSAMS_NS}):
				id = node.get('stateID')
				self.nodesCache[domain][id] = node

				self.qnsCache[id] = {}
				self.casesCache[id] = set()
				if domain == 'AtomicState':
					caseID = ''
					self.casesCache[id].add(caseID)
					for case in node.iterchildren(atomicQNs):
						self._setQnCacheItem(id, caseID, case)
				elif domain == 'MolecularState':
					cases = node.iterchildren(caseQNs)
					for case in cases:
						caseID = case.get('caseID')
						if caseID:
							self.casesCache[id].add(caseID)
							caseID += ':'
							for qns in case.iterchildren():
								self._setQnCacheItem(id, caseID, qns)


		for domain in TRANSITIONS:
			self.nodesCache[domain] = {}
			for node in self.tree.xpath(XSAMSData_PATH + DOMAINS[domain] + '[@id]', namespaces = {"xsams": XSAMS_NS}):
				id = node.get('id')
				self.nodesCache[domain][id] = node

				self.upLowCache[id] = {}
				self.casesCache[id] = set()
				for position in POSITIONS:
					for stateRefNode in node.iterchildren(POSITIONS[position]):
						stateID = stateRefNode.text
						self.upLowCache[id][position] = stateID
						self.casesCache[id].update(self.casesCache.get(stateID, set()))


	def _setQnCacheItem(self, id, caseID, node):
		for qn in node.iterchildren():
			if qn.text:
				name = qn.tag.replace(getTagNameNS(qn.tag), caseID)
				if qn.attrib:
					attrStr = ''
					for attr, value in qn.items():
						attrStr += (" and " if attrStr else "") + "@%s=%s" % (attr, value)
					name += "[" + attrStr +"]"

				self.qnsCache[id][name] = qn.text if is_number(qn.text) else '"' + qn.text + '"'


	def _addRulesNodes(self):
		if not self.lock:
			for rule in sorted(self.rules, key = lambda x: x.name):
				if not rule.domains:
					continue

				for identifier in rule.identifiers:
					stateDomain = 'AtomicState' if identifier.find(':') == -1 else 'MolecularState'
					break

				for domain in rule.domains:
					isState = True if domain[-5:] == 'State' else False

					for idNode, dataNode in self.nodesCache[domain].iteritems():
						if self.casesCache[idNode] and not (rule.case in self.casesCache[idNode]):
							continue

						currentExp = rule.python[:]

						available = None
						for identifier in rule.identifiers:
							localIdentifier = rule.identifiers[identifier][0]
							if isState:
								stateID = idNode
								value = self.qnsCache[idNode].get(localIdentifier, None)
							else:
								position = rule.identifiers[identifier][1]
								stateID = self.upLowCache[idNode].get(position, None)
								if stateID and stateID in self.qnsCache and stateID in self.nodesCache[stateDomain]:
									value = self.qnsCache[stateID].get(localIdentifier, None)
								else:
									available = False
									break

							if available is None:
								available = self._isAvailableNode(self.nodesCache[stateDomain][stateID], rule)

							if value is None:
								if identifier[-1:] == '?':
									value = 'None'
								else:
									if available:
										self._addRuleNode(idNode, dataNode, [rule.name, None])
									available = False

							if available is False:
								break

							currentExp = currentExp.replace(identifier, value)

						if available:
							self._addRuleNode(idNode, dataNode, [rule.name, str(eval(currentExp)).lower()])

			self.lock = True
		return self.tree


	def _addVerificationDataNode(self):
		rootNode = self.tree.getroot()
		if rootNode is not None:
			verificationDataElement = etree.Element('{%s}VerificationData' % XSAMS_NS, nsmap = rootNode.nsmap)
			for attr in rootNode.attrib:
				verificationDataElement.set(attr, rootNode.attrib[attr])

			rootNode.attrib.clear()

			self.tree._setroot(verificationDataElement)
			verificationDataElement.append(rootNode)
			rootNode = verificationDataElement

		return rootNode


	def _addVerificationResultNode(self):
		rootNode = self.tree.getroot()
		if rootNode is not None:
			verificationResultNodes = rootNode.xpath('./xsams:VerificationResult', namespaces = {"xsams": XSAMS_NS})
			if verificationResultNodes:
				for childNode in verificationResultNodes[:]:
					verificationResultNodes[0].getparent().remove(childNode)

			verificationResultElement = etree.Element('{%s}VerificationResult' % XSAMS_NS, nsmap = rootNode.nsmap)

			if self.verificationCache:
				domainNumbers = {}
				for domain in DOMAINS:
					domainNumbers["{%s}%s" % (XSAMS_NS, domain)] = None

				for domain in domainNumbers:
					domainNumbers[domain] = {'total': 0, 'correct': 0, 'incorrect': 0, 'unidentified': 0}

				for nodeWithVerification in self.verificationCache.itervalues():
					domain = nodeWithVerification.getparent().tag

					domainNumbers[domain]['total'] += 1
					if nodeWithVerification.get('{%s}nil' % XSI_NS) == "true":
						domainNumbers[domain]['unidentified'] += 1

					else:
						flagOne = True
						for ruleNode in nodeWithVerification.iterchildren(tag = etree.Element):
							ruleNodeLocalTag = ruleNode.tag

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
						if not domainNumbers[ruleName]['total']:
							continue
						numberElement = etree.Element(('{%s}NumberOf' + localTagName(ruleName) + 's') % XSAMS_NS, nsmap = rootNode.nsmap)
					else:
						numberElement = etree.Element('{%s}NumberOfVerificationByRule' % XSAMS_NS, nsmap = rootNode.nsmap)
						numberElement.set('name', localTagName(ruleName))
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
		if not rule.forInChIList:
			return True

		if not self.inchiCache[element.getparent()]:
			return False
		else:
			InChI = self.inchiCache[element.getparent()]

		for patternInChI in rule.forInChIList:
			if not patternInChI:
				return False
			if re.search(patternInChI, InChI):
				return True
		return False


	def _addRuleNode(self, id, element, ruleItem):
		ruleElement = etree.Element(('{%s}' + ruleItem[0]) % XSAMS_NS, nsmap = element.nsmap)
		if ruleItem[1] is None:
			ruleElement.set('{%s}nil' % XSI_NS, "true")
		else:
			ruleElement.text = ruleItem[1]

		if self.verificationCache.has_key(id):
			verificationElement = self.verificationCache[id]
			verificationElement.append(ruleElement)
		else:
			verificationElement = etree.Element('{%s}Verification' % XSAMS_NS, nsmap = element.nsmap)
			self.verificationCache[id] = verificationElement
			verificationElement.append(ruleElement)
			element.append(verificationElement)

		return ruleElement


	def _removeVerificationNode(self):
		verificationNodes = self.tree.xpath('//*[local-name() = "Verification"]')
		for verificationNode in verificationNodes[:]:
			verificationNode.getparent().remove(verificationNode)


	def getXML(self, pretty_print = True):
		return etree.tostring(self.tree, pretty_print = pretty_print)



def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False



def printRules(rules):
	for rule in sorted(rules, key = lambda x: x.name):
		print rule.python



def localTagName(tagName):
	return tagName.split('}', 1)[-1]



def getTagNameNS(tagName):
	return tagName[0:tagName.find('}')+1]



class Rule:
	i = 1


	def __init__(self, name, rule, forInChIList = None, domains = None):
		if type(rule) == MathDOM:
			self.math = rule
			self.python = rule.serialize("python")
		else:
			self.math = None
			self.python = rule

		self.case = ''
		self.identifiers = self.getIdentifiers()
		for identifier in self.identifiers:
			if identifier.find(':') != -1:
				parts = identifier.split(':')
				self.case = parts[0]
			break

		self.forInChIList = []
		if not forInChIList:
			forInChIListTemp = []
		elif type(forInChIList) == str:
			forInChIListTemp = forInChIList.split(' ')
		else:
			forInChIListTemp = forInChIList

		for patternInChI in forInChIListTemp:
			if patternInChI:
				if patternInChI.find("'") == -1:
					self.forInChIList.append(patternInChI)
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
						self.forInChIList.append(currentPatternInChI)
					else:
						self.forInChIList.append(None)

		self.domains = set()
		if domains:
			for domain in domains:
				if domain in DOMAINS:
					self.domains.add(domain)
		else:
			for domain in DOMAINS:
				for identifier in self.identifiers:
					if len(self.identifiers[identifier]) > 1:
						if domain.endswith('Transition'):
							self.domains.add(domain)
					else:
						if identifier.find(':') == -1:
							if domain.endswith('AtomicState'):
								self.domains.add(domain)
						else:
							if domain.endswith('MolecularState'):
								self.domains.add(domain)
					break;

		domainFlag = self.getDomainFlag()
		abbr = 'T' if domainFlag and domainFlag.endswith('Transition') else 'S'
		if name and (type(name) == str or type(name) == unicode):
			if re.match(r'[a-z]*Rule[ST][0-9][0-9]', name) is not None:
				self.name = name
			else:
				self.name = name.lower() + 'Rule' + abbr + ('0' + str(self.i) if self.i < 10 else str(self.i))
				Rule.i += 1
		else:
			self.name = 'anonymousRule' + abbr + ('0' + str(self.i) if self.i < 10 else str(self.i))
			Rule.i += 1


	def __eq__(self, other):
		return self.name == other.name


	def __hash__(self):
		return hash(self.name)


	def __cmp__(self, other):
		if self.name < other.name:
			return -1
		elif self.name > other.name:
			return 1
		else:
			return 0


	def copy(self):
		return copy.copy(self)


	def getDomainFlag(self):
		domainFlag = None
		for domain in self.domains:
			if domain.endswith('AtomicState'):
				if domainFlag is not None and domainFlag != 'AtomicState':
					raise NoValidException("Allowed only similar domains but not " + str(self.domains))
				domainFlag = 'AtomicState'
			elif domain.endswith('MolecularState'):
				if domainFlag is not None and domainFlag != 'MolecularState':
					raise NoValidException("Allowed only similar domains but not " + str(self.domains))
				domainFlag = 'MolecularState'
			elif domain.endswith('Transition'):
				if domainFlag is not None and domainFlag != 'Transition':
					raise NoValidException("Allowed only similar domains but not " + str(self.domains))
				domainFlag = 'Transition'

		return domainFlag


	def getIdentifiers(self):
		identifiers = {}
		if self.math:
			xpathEval = etree.XPath('.//math:ci[not(contains(self::node(),  "\'"))]', namespaces = {"math": MATHML_NS})
			for ci in xpathEval(self.math._etree):
				name = ci.text
				identifiers[name] = name.strip(' ?').split('#')
		elif self.python:
			labels = re.split(r'\s*\w+\s*\(|\s*\(|\s*\)|\'[a-zA-Z0-9_+-]+\'|"[a-zA-Z0-9_+-]+"|\s*[+\-*/%^<>!,|&~=]+=\s*\d*|\s*[+\-*/%^<>!,|&~]+\s*\d*|\s+not\s+|\s+and\s+|\s+or\s+|\s+is\s+|', self.python)
			for name in labels:
				name = name.strip()
				if name:
					identifiers[name] = name.strip(' ?').split('#')

		return identifiers



class RulesParser:
	rules = set()


	def __init__(self):
		self._domains = {}
		self.addRules = set()
		self.useRules = set()
		self.delRules = set()


	def _setDomains(self, prefix, currentNode, name):
		rulesList = currentNode.xpath('.//' + prefix + ':element', namespaces = {prefix: XSD_NS})
		for ruleNode in rulesList:
			if ruleNode.attrib['name']:
				if not (ruleNode.get('name') in self._domains):
					self._domains[ruleNode.get('name')] = []
				if not (name in self._domains[ruleNode.get('name')]):
					self._domains[ruleNode.get('name')].append(name)
			elif ruleNode.attrib['ref']:
				if not (ruleNode.get('ref') in self._domains):
					self._domains[ruleNode.get('ref')] = []
				if not (name in self._domains[ruleNode.get('ref')]):
					self._domains[ruleNode.get('ref')].append(name)

		groupRefList = currentNode.xpath('.//' + prefix + ':group[@ref]', namespaces = {prefix: XSD_NS})
		for groupRefNode in groupRefList:
			groupList = currentNode.xpath('//' + prefix + ':group[@name = "' + groupRefNode.get('ref') + '"]', namespaces = {prefix: XSD_NS})
			for groupNode in groupList:
				self._setDomains(prefix, groupNode, name)


	def getRule(self, name):
		for rule in self.getRules():
			if rule.name == name:
				return rule
		return None


	def getRules(self):
		if not self.rules:
			tree = XSDTree.makeOne(VERIFICATION_FILE_PATH)

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
				mathNodes = ruleNode.xpath('.//math:math', namespaces = {"math": MATHML_NS})
				if mathNodes:
					mathDoc = MathDOM()
					mathDoc._etree = etree.XML(etree.tostring(mathNodes[0]), parser = mathDoc._parser)
					if mathDoc._etree is None:
						raise NoMathMLException("The 'math' construction has errors")

					self.rules.add(Rule(ruleNode.get('name'), mathDoc, mathNodes[0].getparent().get('forInChIList'), self._domains[ruleNode.get('name')] if self._domains.has_key(ruleNode.get('name')) else []))

		rules = set()
		for rule in self.rules:
			rules.add(rule.copy())

		for rule in self.addRules:
			rules.add(rule)

		for rule in self.delRules:
			if rule in rules:
				rules.remove(rule)

		for rule in self.useRules:
			rules.add(rule)

		if self.useRules:
			for rule in self.rules:
				if not rule in self.useRules:
					if rule in rules:
						rules.remove(rule)

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
					for redefineChild in includeElement.iterchildren(tag = etree.Element):
						if not availableElements.has_key(redefineChild.tag):
							availableElements[redefineChild.tag] = {}

						if redefineChild.tag == "{%s}simpleType" % XSD_NS:
							for item in redefineChild.iterdescendants(prefix + 'restriction'):
								del item.attrib["base"]
								availableElements[redefineChild.tag][redefineChild.get("name")] = item

						if redefineChild.tag == "{%s}complexType" % XSD_NS:
							for redefineChildContent in redefineChild.iterchildren(tag = etree.Element):
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

				for innerChild in innerTree.getroot().iterchildren(tag = etree.Element):
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
		fileName = sys.argv[1]
	else:
		fileName = "test/transition3OK.IN.xml"

	xml = Verification(fileName).getXML()
	if len(sys.argv) > 2 and sys.argv[2]:
		out = open(sys.argv[2], 'w')
		out.write(xml)
		out.close()
	else:
		print xml

