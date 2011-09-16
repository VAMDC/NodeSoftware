import sys
if __name__ == '__main__':
    VERIFICATION_SCHEMA_LOCATION = u"../verification.xsd"
else:
    import verification
    VERIFICATION_SCHEMA_LOCATION = verification.VERIFICATION_SCHEMA_LOCATION

from mathml.mathdom import MathDOM
from mathml.utils import pyterm # register Python term builder
from xml.dom import minidom, Node
from xml import xpath


class NoMathMLException(Exception):
    pass



class NoValidException(Exception):
    pass



class Verification:
    whiteListOfRefs = {}
    excludedRules = {}
    onlyRules = {}


    def __init__(self, file):
        self.doc = minidom.parse(file)
        self.lock = False
        root = self.doc._get_documentElement()
        schemaLocationAttr = root.getAttributeNodeNS('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation')
        locations = schemaLocationAttr.value.split(' ')
        locations[1] = VERIFICATION_SCHEMA_LOCATION
        schemaLocationAttr.value = locations[0] + ' ' + locations[1]


    def run(self, doRemove=True):
        if not self.lock:
            self.removeVerificationNode()
            self.addRulesNodes()
            if doRemove:
                self.removeRedundantNodes()

        return self.doc


    def removeRedundantNodes(self):
        self.whiteListOfRefs = {}
        parentsOfNodesWithVerification = {}

        nodesWithVerification = xpath.Evaluate('//child::Verification[contains(child::node(),  "false")]', self.doc)
        if nodesWithVerification:
            for nodeWithVerification in nodesWithVerification:
                for refNode in xpath.Evaluate('.//*[contains(local-name(@*), "Ref") or contains(local-name(), "Ref")]', nodeWithVerification.parentNode):
                    if refNode.hasAttributes():
                        for attribute in refNode._attrs:
                            if attribute.endswith('Ref'):
                                self.whiteListOfRefs[refNode._attrs[attribute].value] = None
                    elif refNode.nodeType == Node.ELEMENT_NODE and refNode.nodeName.endswith('Ref') and refNode.hasChildNodes():
                        if refNode.childNodes[0].nodeType == Node.TEXT_NODE:
                            self.whiteListOfRefs[refNode.childNodes[0].data] = None

                parentsOfNodesWithVerification[nodeWithVerification.parentNode] = None
        else:
            for childNode in self.doc.childNodes[0].childNodes[:]:
                self.doc.childNodes[0].removeChild(childNode)

        self.removeRedundantParentNodes(parentsOfNodesWithVerification, self.doc)


    def removeRedundantParentNodes(self, usefulParentNodes, stopNode):
        if not usefulParentNodes or stopNode in usefulParentNodes:
            return

        parentsOfNodesWithVerification = {}
        for usefulParentNode in usefulParentNodes:
            if usefulParentNode.parentNode and not parentsOfNodesWithVerification.has_key(usefulParentNode.parentNode):
                parentsOfNodesWithVerification[usefulParentNode.parentNode] = None

                childNodeNames = [childNode.nodeName for childNode in usefulParentNode.parentNode.childNodes]
                singleUseNodeNames = [childNodeName for childNodeName in childNodeNames if childNodeNames.count(childNodeName) == 1]

                for childNode in usefulParentNode.parentNode.childNodes[:]:
                    if not (childNode in usefulParentNodes):
                        isEmptyNode = True
                        idNodes = {}
                        for idNode in xpath.Evaluate('.//*[contains(local-name(@*), "ID")]', childNode):
                            if idNode.hasAttributes():
                                for attribute in idNode._attrs:
                                    if attribute.endswith('ID'):
                                        if self.whiteListOfRefs.has_key(idNode._attrs[attribute].value):
                                            isEmptyNode = False
                                            idNodes[idNode] = None

                        if isEmptyNode:
                            if not (childNode.nodeName in singleUseNodeNames):
                                usefulParentNode.parentNode.removeChild(childNode)
                        else:
                            self.removeRedundantParentNodes(idNodes, childNode)

        self.removeRedundantParentNodes(parentsOfNodesWithVerification, stopNode)


    def addRulesNodes(self):
        if not self.lock:
            stateNodesDict = {}
            for stateNode in xpath.Evaluate('//*[@stateID]', self.doc):
                stateNodesDict[stateNode.getAttribute('stateID')] = stateNode

            transitionNodes = []

            rules = VerificationParser().getRules()
            for fakeRule in self.excludedRules:
                if not (fakeRule in rules) and "copy" in self.excludedRules[fakeRule] and self.excludedRules[fakeRule]["copy"] in rules:
                    rules[fakeRule] = rules[self.excludedRules[fakeRule]["copy"]]
                    rules[fakeRule].update(self.excludedRules[fakeRule])
                    
            for fakeRule in self.onlyRules:
                if not (fakeRule in rules) and "copy" in self.onlyRules[fakeRule] and self.onlyRules[fakeRule]["copy"] in rules:
                    rules[fakeRule] = rules[self.onlyRules[fakeRule]["copy"]]
                    rules[fakeRule].update(self.onlyRules[fakeRule])

            for rule in sorted(rules):

                if self.excludedRules and rule in self.excludedRules:
                    continue

                if self.onlyRules and not rule in self.onlyRules:
                    continue

                transitionFlag = None
                if rules[rule]['domains']:
                    for domain in rules[rule]['domains']:
                        if domain.endswith('State'):
                            if transitionFlag:
                                raise NoValidException("Allowed only similar domains but not " + rules[rule]['domains'])
                            transitionFlag = False
                        elif domain.endswith('Transition'):
                            if transitionFlag is not None and not transitionFlag:
                                raise NoValidException("Allowed only similar domains but not " + rules[rule]['domains'])
                            transitionFlag = True
                else:
                    continue
                templateExp = rules[rule]['math'].serialize("python")

                identifiers = {}
                for ci in xpath.Evaluate('.//ci', rules[rule]['math']):
                    name = ci.value().data
                    identifiers[name] = name.split('@')

                for identifier in identifiers:
                    if identifiers[identifier].count > 1:
                        if not transitionFlag:
                            raise NoValidException("Allowed only 'ci' with the '@' symbol but not " + identifiers)
                        if not transitionNodes:
                            for domain in rules[rule]['domains']:
                                transitionNodes.extend(xpath.Evaluate('//' + domain + '[./' + identifiers[identifier][1] + ']', self.doc))
                        break
                    else:
                        if transitionFlag:
                            raise NoValidException("Allowed only 'ci' without the '@' symbol but not " + identifiers)
                        if not transitionNodes:
                            for domain in rules[rule]['domains']:
                                transitionNodes.extend(xpath.Evaluate('//' + domain, self.doc))
                        break

                for transitionNode in transitionNodes:
                    if not hasattr(transitionNode, 'cache'):
                        transitionNode.cache = {}

                    currentExp = templateExp
                    available = None
                    for identifier in identifiers:
                        if not (identifier in transitionNode.cache):
                            for stateRefNode in transitionNode.childNodes:
                                if transitionFlag:
                                    if stateRefNode.nodeType == Node.ELEMENT_NODE and stateRefNode.tagName == identifiers[identifier][1] and stateRefNode.hasChildNodes():
                                        if stateRefNode.childNodes[0].nodeType == Node.TEXT_NODE:
                                            stateID = stateRefNode.childNodes[0].data
                                        else:
                                            raise NoValidException("No value of '" + identifiers[identifier][1] + "'")
                                        if stateID in stateNodesDict:
                                            value = self.getValue(stateNodesDict[stateID], identifiers[identifier][0])
                                            if value != '':
                                                transitionNode.cache[identifier] = {"stateID": stateID, "value": value}
                                        else:
                                            raise NoValidException("No matches '" + stateID + "' Ref to ID ")
                                        break
                                else:
                                    if stateRefNode.nodeType == Node.ELEMENT_NODE and stateRefNode.hasAttribute('stateID'):
                                        stateID = stateRefNode.getAttribute('stateID')
                                        value = self.getValue(stateNodesDict[stateID], identifier)
                                        if value != '':
                                            transitionNode.cache[identifier] = {"stateID": stateID, "value": value}
                                        available = self.isAvailableNode(stateNodesDict[stateID], rules[rule])
                                        break
                        if transitionNode.cache.has_key(identifier):
                            if transitionNode.cache[identifier] != '':
                                if available is None:
                                    available = self.isAvailableNode(stateNodesDict[transitionNode.cache[identifier]["stateID"]], rules[rule])
                                if available is not None and not available:
                                    break
                                currentExp = currentExp.replace(identifier, transitionNode.cache[identifier]["value"])
                            else:
                                currentExp = 'True'
                        else:
                            available = False
                    if available:
                        self.addRuleNode(transitionNode, [rule, str(eval(currentExp)).lower()])
                self.lock = True
        return self.doc


    def isAvailableNode(self, element, rule):
        if not rule['substances']:
            return True
        else:
            substances = rule['substances'].split(' ')

        if element.nodeName == 'AtomicState':
            #Atoms.Atom.Isotope.Ion.AtomicState
            massNumber = None
            for isotopeChild in element.parentNode.parentNode.childNodes:
                if isotopeChild.nodeType == Node.ELEMENT_NODE and isotopeChild.tagName == 'IsotopeParameters' and isotopeChild.hasChildNodes():
                    for isotopeParametersChild in isotopeChild.childNodes:
                        if isotopeParametersChild.nodeType == Node.ELEMENT_NODE and isotopeParametersChild.tagName == 'MassNumber' and isotopeParametersChild.hasChildNodes():
                            if isotopeParametersChild.childNodes[0].nodeType == Node.TEXT_NODE:
                                massNumber = isotopeParametersChild.childNodes[0].data
                            else:
                                raise NoValidException("No 'MassNumber' element")
            elementSymbol = None
            for atomChild in element.parentNode.parentNode.parentNode.childNodes:
                if atomChild.nodeType == Node.ELEMENT_NODE and atomChild.tagName == 'ChemicalElement' and atomChild.hasChildNodes():
                    for chemicalElementChild in atomChild.childNodes:
                        if chemicalElementChild.nodeType == Node.ELEMENT_NODE and chemicalElementChild.tagName == 'ElementSymbol' and chemicalElementChild.hasChildNodes():
                            if chemicalElementChild.childNodes[0].nodeType == Node.TEXT_NODE:
                                elementSymbol = chemicalElementChild.childNodes[0].data
                            else:
                                raise NoValidException("No 'ElementSymbol' element")
            if '_' + str(massNumber) + str(elementSymbol) in substances:
                return True
            else:
                return False
        elif element.nodeName == 'MolecularState':
            #TODO molecules
            return True
        else:
            return False


    def getValue(self, element, name):
        if element.nodeName == 'AtomicState':
            qn = element.getElementsByTagName(name)
            if qn and qn[0] and qn[0].hasChildNodes() and qn[0].childNodes[0].nodeType == Node.TEXT_NODE:
                data = qn[0].childNodes[0].data
                return data if is_number(data) else '"' + data + '"'
            else:
                return ''
        elif element.nodeName == 'MolecularState':
            #TODO molecules
            return 'UNKNOWN'
        else:
            return ''


    def addRuleNode(self, element, ruleItem):
        ruleElement = self.doc.createElement(ruleItem[0])
        ruleElement.appendChild(self.doc.createTextNode(ruleItem[1]))

        verificationNodes = element.getElementsByTagName('Verification')
        if verificationNodes:
            verificationElement = verificationNodes[0]
            ruleNodes = verificationElement.getElementsByTagName(ruleItem[0])
            if ruleNodes:
                verificationElement.replaceChild(ruleElement, ruleNodes[0])
            else:
                verificationElement.appendChild(ruleElement)
        else:
            verificationElement = self.doc.createElement('Verification')
            verificationElement.appendChild(ruleElement)
            element.appendChild(verificationElement)

        return ruleElement


    def removeVerificationNode(self):
        verificationNodes = xpath.Evaluate('//Verification', self.doc)
        for verificationNode in verificationNodes:
            verificationNode.parentNode.removeChild(verificationNode)


    def getXML(self):
        return self.run().toxml()



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False



class VerificationParser:
    domains = {}


    def __init__(self):
        pass


    def setDomains(self, currentNode, name):
        localContext = xpath.CreateContext(currentNode)
        localContext.setNamespaces({'xs': 'http://www.w3.org/2001/XMLSchema'})

        rulesList = xpath.Evaluate('.//xs:element', currentNode, localContext)
        for ruleNode in rulesList:
            if ruleNode.hasAttribute('name'):
                if not (ruleNode.getAttribute('name') in self.domains):
                    self.domains[ruleNode.getAttribute('name')] = []
                if not (name in self.domains[ruleNode.getAttribute('name')]):
                    self.domains[ruleNode.getAttribute('name')].append(name)
            elif ruleNode.hasAttribute('ref'):
                if not (ruleNode.getAttribute('ref') in self.domains):
                    self.domains[ruleNode.getAttribute('ref')] = []
                if not (name in self.domains[ruleNode.getAttribute('ref')]):
                    self.domains[ruleNode.getAttribute('ref')].append(name)

        groupRefList = xpath.Evaluate('.//xs:group[@ref]', currentNode, localContext)
        for groupRefNode in groupRefList:
            groupList = xpath.Evaluate('//xs:group[@name = "' + groupRefNode.getAttribute('ref') + '"]', currentNode, localContext)
            for groupNode in groupList:
                self.setDomains(groupNode, name)


    def getRules(self):
        rules = {}

        doc = minidom.parse(open("verification.xsd"))
        context = xpath.CreateContext(doc)
        context.setNamespaces({'xs': 'http://www.w3.org/2001/XMLSchema'})

        verificationTypes = xpath.Evaluate('//xs:complexType[contains(@name, "Verification")]', doc, context)
        for verificationType in verificationTypes:
            name = verificationType.getAttribute('name')
            name = name[0].upper() + name[1:-len('Verification')]
            self.setDomains(verificationType, name)

        ruleNodes = xpath.Evaluate('//xs:element[contains(@name, "Rule")]', doc, context)
        for ruleNode in ruleNodes:
            mathNodes = xpath.Evaluate('.//math', ruleNode)
            if mathNodes:
                mathDoc = MathDOM(mathNodes[0])
                if mathDoc is None:
                    raise NoMathMLException("The 'math' construction has errors")

                rules[ruleNode.getAttribute('name')] = {'domains': self.domains[ruleNode.getAttribute('name')] if self.domains.has_key(ruleNode.getAttribute('name')) else [],
                                                        'substances': mathDoc.parentNode.getAttribute('substances'),
                                                        'symmetry': mathDoc.parentNode.getAttribute('symmetry'),
                                                        'math': mathDoc}

        return rules


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
