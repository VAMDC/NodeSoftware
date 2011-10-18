import sys


if __name__ == '__main__':
    VERIFICATION_SCHEMA_LOCATION = u"../verification.xsd"
else:
    import verification


    VERIFICATION_SCHEMA_LOCATION = verification.VERIFICATION_SCHEMA_LOCATION

import re
from mathml.mathdom import MathDOM
from mathml.utils import pyterm # register Python term builder
from xml.dom import minidom, Node
from xml import xpath, ns


class NoMathMLException(Exception):
    pass



class NoValidException(Exception):
    pass



class Verification:

    def __init__(self, file):
        self.doc = minidom.parse(file)
        self.lock = False

        self.excludedRules = {}
        self.onlyRules = {}

        self.stateNodes = {}
        self.whiteListOfRefs = {}

        root = self.doc._get_documentElement()
        schemaLocationAttr = root.getAttributeNodeNS(ns.SCHEMA.XSI3 , 'schemaLocation')
        locations = schemaLocationAttr.value.split(' ')
        locations[1] = VERIFICATION_SCHEMA_LOCATION
        schemaLocationAttr.value = locations[0] + ' ' + locations[1]


    def run(self, doReport = True, doRemove=True):
        if not self.lock:
            self._removeVerificationNode()
            self._addRulesNodes()
            if doReport:
                self._addVerificationResultNode()
            if doRemove:
                self._removeRedundantNodes()

        return self.doc


    def _removeRedundantNodes(self):
        self.whiteListOfRefs = {}
        parentsOfNodesWithVerification = {}

        context = xpath.CreateContext(self.doc)
        context.setNamespaces({'xsi': ns.SCHEMA.XSI3})

        nodesWithVerification = xpath.Evaluate('//child::Verification[contains(self::node(),  "false") or descendant-or-self::node()/attribute::xsi:nil]', self.doc, context)
        if nodesWithVerification:
            for nodeWithVerification in nodesWithVerification:
                if not xpath.Evaluate('./child::*[contains(self::node(),  "false") or contains(self::node(),  "true")]', nodeWithVerification):
                    for childNode in nodeWithVerification.childNodes[:]:
                        nodeWithVerification.removeChild(childNode)
                    nodeWithVerification.setAttributeNS(ns.SCHEMA.XSI3, "xsi:nil", "true")

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

        for parentOfNodesWithVerification in parentsOfNodesWithVerification:
            if parentOfNodesWithVerification.hasAttributes():
                for attribute in parentOfNodesWithVerification._attrs:
                    if attribute.endswith('ID'):
                        self.whiteListOfRefs[parentOfNodesWithVerification._attrs[attribute].value] = None

        self._removeRedundantParentNodes(parentsOfNodesWithVerification, self.doc)


    def _removeRedundantParentNodes(self, usefulParentNodes, stopNode):
        if not usefulParentNodes or stopNode in usefulParentNodes:
            return

        parentsOfNodesWithVerification = {}
        for usefulParentNode in usefulParentNodes:
            if usefulParentNode.parentNode and not parentsOfNodesWithVerification.has_key(usefulParentNode.parentNode):
                parentsOfNodesWithVerification[usefulParentNode.parentNode] = None

                childNodeNames = [childNode.nodeName for childNode in usefulParentNode.parentNode.childNodes]
                singleUseNodeNames = [childNodeName for childNodeName in childNodeNames if childNodeNames.count(childNodeName) == 1]

                flag = True
                while flag:
                    flag = False
                    for childNode in usefulParentNode.parentNode.childNodes[:]:
                        if not (childNode in usefulParentNodes):
                            hasIDs = False
                            isRedundantNode = True
                            idNodes = {}
                            if childNode.nodeType == Node.ELEMENT_NODE and  childNode.tagName == 'Processes' and childNode.hasChildNodes():
                                    context = xpath.CreateContext(childNode)
                                    context.setNamespaces({'xsi': ns.SCHEMA.XSI3})
                                    if not xpath.Evaluate('.//child::Verification[contains(self::node(),  "false") or descendant-or-self::node()/attribute::xsi:nil]', childNode, context):
                                        usefulParentNode.parentNode.removeChild(childNode)
                                        flag = True
                                        break
                            elif childNode.nodeType == Node.ELEMENT_NODE and childNode.tagName == 'VerificationResult' and childNode.hasChildNodes():
                                pass

                            else:
                                for idNode in xpath.Evaluate('descendant-or-self::node()[contains(local-name(@*), "ID")]', childNode):
                                    if idNode.hasAttributes():
                                        for attribute in idNode._attrs:
                                            if attribute.endswith('ID'):
                                                hasIDs = True
                                                if self.whiteListOfRefs.has_key(idNode._attrs[attribute].value):
                                                    isRedundantNode = False
                                                    idNodes[idNode] = None

                            if isRedundantNode:
                                if hasIDs or not (childNode.nodeName in singleUseNodeNames):
                                    usefulParentNode.parentNode.removeChild(childNode)
                            else:
                                self._removeRedundantParentNodes(idNodes, childNode)

        self._removeRedundantParentNodes(parentsOfNodesWithVerification, stopNode)


    def _setStateNodes(self):
        for stateNode in xpath.Evaluate('//*[@stateID]', self.doc):
            self.stateNodes[stateNode.getAttribute('stateID')] = stateNode


    def _setExtraRules(self, rules):
        for fakeRule in self.excludedRules:
            if not (fakeRule in rules) and "copy" in self.excludedRules[fakeRule] and self.excludedRules[fakeRule]["copy"] in rules:
                rules[fakeRule] = rules[self.excludedRules[fakeRule]["copy"]]
                rules[fakeRule].update(self.excludedRules[fakeRule])

        for fakeRule in self.onlyRules:
            if not (fakeRule in rules) and "copy" in self.onlyRules[fakeRule] and self.onlyRules[fakeRule]["copy"] in rules:
                rules[fakeRule] = rules[self.onlyRules[fakeRule]["copy"]]
                rules[fakeRule].update(self.onlyRules[fakeRule])
        return rules


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


    def printRules(self):
        rules = self._setExtraRules(VerificationParser().getRules())
        for rule in sorted(rules):
            print rules[rule]['math'].serialize("python")


    def _addRulesNodes(self):
        if not self.lock:
            self._setStateNodes()

            dataNodes = {'AtomicState': [], 'MolecularState': [], 'Transition': []}

            rules = self._setExtraRules(VerificationParser().getRules())
            for rule in sorted(rules):
                if self.excludedRules and rule in self.excludedRules:
                    continue

                if self.onlyRules and not rule in self.onlyRules:
                    continue

                if rules[rule]['domains']:
                    domainFlag = self._checkDomains(rules[rule])
                else:
                    continue

                templateExp = rules[rule]['math'].serialize("python")

                identifiers = {}
                for ci in xpath.Evaluate('.//ci[not(contains(self::node(),  "\'"))]', rules[rule]['math']):
                    name = ci.value().data
                    identifiers[name] = name.split('#')

                for identifier in identifiers:
                    if len(identifiers[identifier]) > 1:
                        if domainFlag != 'Transition':
                            raise NoValidException("Allowed only 'ci' with the '#' symbol but not " + str(identifiers[identifier]))
                        if not dataNodes[domainFlag]:
                            for domain in rules[rule]['domains']:
                                dataNodes[domainFlag].extend(xpath.Evaluate('//' + domain + '[./' + identifiers[identifier][1] + ']', self.doc))
                        break
                    else:
                        if domainFlag != 'AtomicState' and domainFlag != 'MolecularState':
                            raise NoValidException("Allowed only 'ci' without the '#' symbol but not " + str(identifiers[identifier]))
                        if domainFlag == 'AtomicState' and identifier.find(':') != -1:
                            raise NoValidException("Allowed only 'ci' without the ':' symbol but not " + str(identifiers[identifier]))
                        if domainFlag == 'MolecularState' and identifier.find(':') == -1:
                            raise NoValidException("Allowed only 'ci' with the ':' symbol but not " + str(identifiers[identifier]))
                        if not dataNodes[domainFlag]:
                            for domain in rules[rule]['domains']:
                                dataNodes[domainFlag].extend(xpath.Evaluate('//' + domain, self.doc))
                        break

                for dataNode in dataNodes[domainFlag]:
                    if not hasattr(dataNode, 'cache'):
                        dataNode.cache = {}

                    currentExp = templateExp


                    available = None
                    for identifier in identifiers:
                        if not (identifier in dataNode.cache):
                            if domainFlag == 'Transition':
                                for stateRefNode in dataNode.childNodes:
                                    if stateRefNode.nodeType == Node.ELEMENT_NODE and stateRefNode.tagName == identifiers[identifier][1] and stateRefNode.hasChildNodes():
                                        if stateRefNode.childNodes[0].nodeType == Node.TEXT_NODE:
                                            stateID = stateRefNode.childNodes[0].data
                                        else:
                                            raise NoValidException("No value of '" + identifiers[identifier][1] + "'")
                                        if stateID in self.stateNodes:
                                            value = self._getValue(self.stateNodes[stateID], identifiers[identifier][0])
                                            dataNode.cache[identifier] = {"stateID": stateID, "value": value}
                                        else:
                                            raise NoValidException("No matches '" + stateID + "' Ref to ID ")
                                        break
                            else:
                                if dataNode.nodeType == Node.ELEMENT_NODE and dataNode.hasAttribute('stateID'):
                                    stateID = dataNode.getAttribute('stateID')
                                    value = self._getValue(self.stateNodes[stateID], identifier)
                                    dataNode.cache[identifier] = {"stateID": stateID, "value": value}

                        if dataNode.cache.has_key(identifier):
                            if available is None:
                                if dataNode.cache[identifier]["value"] is None:
                                    available = self._isAvailableNode(self.stateNodes[dataNode.cache[identifier]["stateID"]], rules[rule])
                                    if available:
                                        self._addRuleNode(dataNode, [rule, None])
                                    available = False
                                elif dataNode.cache[identifier]["value"] == False:
                                    available = False
                                else:
                                    available = self._isAvailableNode(self.stateNodes[dataNode.cache[identifier]["stateID"]], rules[rule])
                            if available is not None and not available:
                                break
                            currentExp = currentExp.replace(identifier, dataNode.cache[identifier]["value"])
                        else:
                            available = False
                            break

                    if available:
                        self._addRuleNode(dataNode, [rule, str(eval(currentExp)).lower()])

            self.lock = True
        return self.doc

    def _addVerificationResultNode(self):

        if self.doc.hasChildNodes():
            rootNode = self.doc.childNodes[0]

            verificationDataElement = self.doc.createElement('VerificationData')
            for attr in rootNode.attributes.values():
                verificationDataElement.setAttributeNS(attr.namespaceURI, attr.nodeName, attr.value)
                a = verificationDataElement.getAttributeNodeNS(attr.namespaceURI, attr.localName)
                a.specified = attr.specified

            rootNode._attrs.clear()

            self.doc.replaceChild(verificationDataElement, rootNode)
            verificationDataElement.appendChild(rootNode)
            rootNode = verificationDataElement

            verificationResultNodes = xpath.Evaluate('./VerificationResult', rootNode)
            if verificationResultNodes:
                for childNode in verificationResultNodes[:]:
                    verificationResultNodes[0].parentNode.removeChild(childNode)

            verificationResultElement = self.doc.createElement('VerificationResult')

            nodesWithVerification = xpath.Evaluate('//child::Verification', self.doc)
            if nodesWithVerification:
                domainNumbers = {'AtomicState':None, 'MolecularState':None, 'RadiativeTransition':None, 'NonRadiativeTransition':None}

                for domain in domainNumbers:
                    domainNumbers[domain] = {'total':0, 'correct':0, 'incorrect':0, 'unidentified':0}

                for nodeWithVerification in nodesWithVerification:
                    domain = nodeWithVerification.parentNode.nodeName
                    domainNumbers[domain]['total'] += 1
                    if nodeWithVerification.getAttributeNS(ns.SCHEMA.XSI3, "nil") == "true":
                        domainNumbers[domain]['unidentified'] += 1
                    else:
                        flagOne = True
                        for ruleNode in nodeWithVerification.childNodes:
                            if ruleNode.nodeType == Node.ELEMENT_NODE:
                                if not domainNumbers.has_key(ruleNode.nodeName):
                                    domainNumbers[ruleNode.nodeName] = {'correct':0, 'incorrect':0, 'unidentified':0}
                                if ruleNode.getAttributeNS(ns.SCHEMA.XSI3, "nil") == "true":
                                    flagOne = None
                                    domainNumbers[ruleNode.nodeName]['unidentified'] += 1
                                elif ruleNode.hasChildNodes():
                                    if ruleNode.childNodes[0].nodeType == Node.TEXT_NODE:
                                        if ruleNode.childNodes[0].data == "true":
                                            domainNumbers[ruleNode.nodeName]['correct'] += 1
                                        else:
                                            if flagOne is not None:
                                                flagOne = False
                                            domainNumbers[ruleNode.nodeName]['incorrect'] += 1
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
                        numberElement = self.doc.createElement('NumberOf' + ruleName + 's')
                    else:
                        numberElement = self.doc.createElement('NumberOfVerificationByRule')
                        numberElement.setAttribute('name', ruleName)
                    for numberName in domainNumbers[ruleName]:
                        numberElement.setAttribute(numberName, str(domainNumbers[ruleName][numberName]))
                    verificationResultElement.appendChild(numberElement)
            else:
                verificationResultElement.setAttributeNS(ns.SCHEMA.XSI3, "xsi:nil", "true")

            if rootNode.hasChildNodes():
                rootNode.insertBefore(verificationResultElement, rootNode.childNodes[0])
            else:
                rootNode.appendChild(verificationResultElement)

            return verificationResultElement

        else:
            return None

    def _isAvailableNode(self, element, rule):
        if not rule['forInChIList']:
            return True
        else:
            forInChIList = rule['forInChIList'].split(' ')

        InChI = None
        if element.nodeName == 'AtomicState':
            #Atoms.Atom.Isotope.Ion.AtomicState

            for ionChild in element.parentNode.childNodes:
                if ionChild.nodeType == Node.ELEMENT_NODE and ionChild.tagName == 'InChI' and ionChild.hasChildNodes():
                    if ionChild.childNodes[0].nodeType == Node.TEXT_NODE:
                        InChI = ionChild.childNodes[0].data
                    else:
                        return False
                        #raise NoValidException("No 'InChI' element")
        elif element.nodeName == 'MolecularState':
            #Molecules.Molecule.MolecularState
            for moleculeChild in element.parentNode.childNodes:
                if moleculeChild.nodeType == Node.ELEMENT_NODE and moleculeChild.tagName == 'MolecularChemicalSpecies' and moleculeChild.hasChildNodes():
                    for molecularChemicalSpeciesChild in moleculeChild.childNodes:
                        if molecularChemicalSpeciesChild.nodeType == Node.ELEMENT_NODE and molecularChemicalSpeciesChild.tagName == 'InChI' and molecularChemicalSpeciesChild.hasChildNodes():
                            if molecularChemicalSpeciesChild.childNodes[0].nodeType == Node.TEXT_NODE:
                                InChI = molecularChemicalSpeciesChild.childNodes[0].data
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
        if element.nodeName == 'AtomicState' or element.nodeName == 'MolecularState':
            context = xpath.CreateContext(element)

            if element.nodeName == 'AtomicState':
                cases = element.getElementsByTagName('AtomicQuantumNumbers')
                if cases:
                    if name.find(':') != -1:
                        return False
                else:
                    return None
            elif element.nodeName == 'MolecularState':
                cases = element.getElementsByTagName('Case')
                if cases:
                    caseID = cases[0].getAttribute('caseID')
                    if caseID:
                        parts = name.split(':')
                        if caseID != parts[0]:
                            return False
                    else:
                        return None

                    context.setNamespaces({caseID: 'http://vamdc.org/xml/xsams/0.2/cases/' + caseID})
                else:
                    return None

            qns = xpath.Evaluate('.//' + name, element, context)
            if qns and qns[0] and qns[0].hasChildNodes() and qns[0].childNodes[0].nodeType == Node.TEXT_NODE:
                data = qns[0].childNodes[0].data
                return data if is_number(data) else '"' + data + '"'
            else:
                return None
        else:
            return False


    def _addRuleNode(self, element, ruleItem):
        ruleElement = self.doc.createElement(ruleItem[0])
        if ruleItem[1] is None:
            ruleElement.setAttributeNS(ns.SCHEMA.XSI3, "xsi:nil", "true")
        else:
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


    def _removeVerificationNode(self):
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

    def __init__(self):
        self.domains = {}
        self.rules = {}


    def _setDomains(self, prefix, currentNode, name):
        localContext = xpath.CreateContext(currentNode)
        localContext.setNamespaces({prefix: ns.SCHEMA.XSD3})

        rulesList = xpath.Evaluate('.//' + prefix + ':element', currentNode, localContext)
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

        groupRefList = xpath.Evaluate('.//'+prefix+':group[@ref]', currentNode, localContext)
        for groupRefNode in groupRefList:
            groupList = xpath.Evaluate('//' +prefix+':group[@name = "' + groupRefNode.getAttribute('ref') + '"]', currentNode, localContext)
            for groupNode in groupList:
                self._setDomains(prefix, groupNode, name)


    def getRules(self):
        if not self.rules:

            doc = self._makeOneSchema("verification.xsd")
            if not doc:
                return self.rules

            root = doc._get_documentElement()
            prefix = root.prefix

            context = xpath.CreateContext(doc)
            context.setNamespaces({prefix: ns.SCHEMA.XSD3})

            verificationTypes = xpath.Evaluate('//'+prefix+':complexType[contains(@name, "Verification")]', doc, context)
            for verificationType in verificationTypes:
                name = verificationType.getAttribute('name')
                name = name[0].upper() + name[1:-len('Verification')]
                self._setDomains(prefix, verificationType, name)

            ruleNodes = xpath.Evaluate('//'+prefix+':element[contains(@name, "Rule")]', doc, context)
            for ruleNode in ruleNodes:
                mathNodes = xpath.Evaluate('.//math', ruleNode)
                if mathNodes:
                    mathDoc = MathDOM(mathNodes[0])
                    if mathDoc is None:
                        raise NoMathMLException("The 'math' construction has errors")

                    self.rules[ruleNode.getAttribute('name')] = {'domains': self.domains[ruleNode.getAttribute('name')] if self.domains.has_key(ruleNode.getAttribute('name')) else [],
                                                            'forInChIList': mathDoc.parentNode.getAttribute('forInChIList'),
                                                            'math': mathDoc}

        return self.rules


    def _makeOneSchema(self, fileName):

        file = open(fileName)
        if not file:
            return None
        doc = minidom.parse(file)
        innerRoot = doc._get_documentElement()
        prefix = innerRoot.prefix

        dir = fileName[0: fileName.rfind('/') + 1]

        context = xpath.CreateContext(doc)
        context.setNamespaces({prefix: ns.SCHEMA.XSD3})

        availableElements = {}
        includes = ["include", "redefine"]
        for include in includes:
            includeList = xpath.Evaluate('/' + prefix + ':schema/' + prefix + ':' + include, doc, context)
            for includeElement in includeList:
                schemaLocation = includeElement.getAttribute("schemaLocation")
                if schemaLocation.find('http://') > -1:
                    continue
                location = dir + schemaLocation
                parent = includeElement.parentNode
                
                redefines = []
                if include == 'redefine':
                    if includeElement.hasChildNodes(): 
                        redefineElements = includeElement.childNodes
                        for redefineChild in redefineElements:
                            if isinstance(redefineChild, minidom.Element):
                                if not availableElements.has_key(redefineChild.tagName):
                                    availableElements[redefineChild.tagName] = {}

                                if redefineChild.tagName == prefix + ":simpleType":
                                    items = redefineChild.getElementsByTagName(prefix + 'restriction')
                                    for item in items: 
                                        item.removeAttribute("base")
                                        availableElements[redefineChild.tagName][redefineChild.getAttribute("name")] = item

                                if redefineChild.tagName == prefix + ":complexType":
                                    if redefineChild.hasChildNodes():
                                        for redefineChildContent in redefineChild.childNodes:
                                            if isinstance(redefineChildContent, minidom.Element):
                                                if redefineChildContent.tagName == prefix + ":complexContent":
                                                    items = redefineChildContent.getElementsByTagName(prefix + 'restriction')
                                                    for item in items:
                                                        item.removeAttribute("base")
                                                        availableElements[redefineChild.tagName][redefineChild.getAttribute("name")] = item
                                                    items = redefineChildContent.getElementsByTagName(prefix + 'extension')
                                                    for item in items:
                                                        item.removeAttribute("base")
                                                        availableElements[redefineChild.tagName][redefineChild.getAttribute("name")] = item


                                previousSibling = redefineChild.previousSibling
                                if previousSibling is not None and previousSibling.nodeType == Node.TEXT_NODE:
                                    redefines.append(previousSibling)
                                
                                redefines.append(redefineChild)
                            
                for elem in redefines:
                    parent.appendChild(elem)

                innerDoc =  self._makeOneSchema(location)
                if not innerDoc:
                    return None

                innerRoot = innerDoc._get_documentElement()
                if innerRoot.hasChildNodes():
                    previousSibling = includeElement.previousSibling
                    if previousSibling is not None and previousSibling.nodeType == Node.TEXT_NODE:
                        parent.removeChild(previousSibling)

                    parent.removeChild(includeElement)

                    children = innerRoot.childNodes
                    for innerChild in children:
                        if isinstance(innerChild, minidom.Element):
                            if availableElements.has_key(innerChild.tagName) and availableElements[innerChild.tagName].has_key(innerChild.getAttribute("name")):
                                unknown = availableElements[innerChild.tagName][innerChild.getAttribute("name")]
                                if isinstance(unknown, minidom.Element):
                                    copyInnerNode = doc.importNode(innerChild, True)
                                    copyInnerNode.removeAttribute("name")
                                    unknown.insertBefore(copyInnerNode, unknown.firstChild)

                                lastChild = parent.lastChild
                                if lastChild is not None and lastChild.nodeType == Node.TEXT_NODE:
                                    if isinstance(unknown, minidom.Element):
                                        unknown.insertBefore(lastChild.cloneNode(), unknown.firstChild)

                                    parent.removeChild(lastChild)
                                continue

                            if not availableElements.has_key(innerChild.tagName):
                                availableElements[innerChild.tagName] = {}

                            availableElements[innerChild.tagName][innerChild.getAttribute("name")] = True

                        copyInnerNode = doc.importNode(innerChild, True)
                        parent.appendChild(copyInnerNode)
        return doc

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
