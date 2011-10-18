from xml.dom import minidom, Node
from xml import xpath, ns


__author__ = 'aip'

def makeTestFile(fileName, count = 0):
    doc = minidom.parse(open("test/" + fileName + ".xml"))

    root = doc._get_documentElement()
    schemaLocationAttr = root.getAttributeNodeNS(ns.SCHEMA.XSI3, 'schemaLocation')
    locations = schemaLocationAttr.value.split(' ')
    locations[1] = '../xsd/xsams/0.2/xsams.xsd'
    schemaLocationAttr.value = locations[0] + ' ' + locations[1]

    nodes = xpath.Evaluate('//*[child::RadiativeTransition]', doc)
    whiteListOfRefs = _getWhiteListOfRefs(nodes, ['Probability', 'Broadening', 'Shifting'], count)
    if not whiteListOfRefs:
        nodes = xpath.Evaluate('//*[child::NonRadiativeTransition]', doc)
        whiteListOfRefs = _getWhiteListOfRefs(nodes, ['Probability', 'Broadening', 'Shifting'], count)
        if not whiteListOfRefs:
            nodes = xpath.Evaluate('//*[child::MolecularState]', doc)
            whiteListOfRefs = _getWhiteListOfRefs(nodes, [], count)
            if not whiteListOfRefs:
                nodes = xpath.Evaluate('//*[child::AtomicState]', doc)
                whiteListOfRefs = _getWhiteListOfRefs(nodes, [], count)

    _removeRedundantParentNodes(nodes, doc, whiteListOfRefs)

    xml = doc.toxml()
    #print xml

    out = open("test/" + fileName + ".IN.xml", 'w')
    out.write(xml)
    out.close()

    out = open("test/" + fileName + ".OUT.MIN.xml", 'w')
    out.write(xml)
    out.close()

    return doc

def _getWhiteListOfRefs(nodes, ballastList, count = 0):

    whiteListOfRefs = {}
    if nodes:
        for node in nodes:
            i = 0
            for childNode in node.childNodes[:]:
                    if not count or i < count:
                        if childNode.nodeType == Node.ELEMENT_NODE:

                            for ballastName in ballastList:
                                for ballastNode in childNode.getElementsByTagName(ballastName):
                                    childNode.removeChild(ballastNode)

                            for refNode in xpath.Evaluate('.//*[contains(local-name(@*), "Ref") or contains(local-name(), "Ref")]', childNode):
                                if refNode.hasAttributes():
                                    for attribute in refNode._attrs:
                                        if attribute.endswith('Ref'):
                                            whiteListOfRefs[refNode._attrs[attribute].value] = None
                                elif refNode.nodeType == Node.ELEMENT_NODE and refNode.nodeName.endswith('Ref') and refNode.hasChildNodes():
                                    if refNode.childNodes[0].nodeType == Node.TEXT_NODE:
                                        whiteListOfRefs[refNode.childNodes[0].data] = None
                            i += 1
                    else:
                        node.removeChild(childNode)

    return whiteListOfRefs

def _removeRedundantParentNodes(usefulParentNodes, stopNode, whiteListOfRefs):
    if not usefulParentNodes or stopNode in usefulParentNodes:
        return

    parentsOfNodes = {}
    for usefulParentNode in usefulParentNodes:
        if usefulParentNode.parentNode and not parentsOfNodes.has_key(usefulParentNode.parentNode):
            parentsOfNodes[usefulParentNode.parentNode] = None

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
                        for idNode in xpath.Evaluate('descendant-or-self::node()[contains(local-name(@*), "ID")]', childNode):
                            if idNode.hasAttributes():
                                for attribute in idNode._attrs:
                                    if attribute.endswith('ID'):
                                        hasIDs = True
                                        if whiteListOfRefs.has_key(idNode._attrs[attribute].value):
                                            isRedundantNode = False
                                            idNodes[idNode] = None

                        if isRedundantNode:
                            if hasIDs or not (childNode.nodeName in singleUseNodeNames):
                                usefulParentNode.parentNode.removeChild(childNode)
                        else:
                            _removeRedundantParentNodes(idNodes, childNode, whiteListOfRefs)

    _removeRedundantParentNodes(parentsOfNodes, stopNode, whiteListOfRefs)
