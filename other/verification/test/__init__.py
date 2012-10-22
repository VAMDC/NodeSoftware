from lxml import etree
import sys, os, urllib2

sys.path.insert(0, '.')
try:
	import check
except ImportError:
	from .. import check

__author__ = 'aip'

class LocalResolver(etree.Resolver):

	def __init__(self, localMap, *args, **kwargs):
		etree.Resolver.__init__(self, *args, **kwargs)
		self.localMap = localMap

	def checkHTTPContent(self, url):
		response = urllib2.urlopen(url)
		if 'Content-Type' in response.info():
			if response.info()['Content-Type'] != 'application/xml':
				raise Exception('Incorrect content on the "'  + url + '" link')


	def resolve(self, url, id, context):
		newURL = ''

		if url in self.localMap:
			newURL = self.localMap[url]
			if newURL.find('http://') > -1:
				try:
					self.checkHTTPContent(newURL)
					url = newURL
				except Exception, e:
					if url == newURL:
						print e
			elif os.path.exists(newURL):
				url = newURL

		if url != newURL:
			if url.find('http://') > -1:
				try:
					self.checkHTTPContent(url)
				except Exception, e:
					print e

		return self.resolve_filename(url, context)


def makeTestFileFromBigFile(fileName, count=0):
	tree = etree.parse(open("test/" + fileName + ".xml"))

	namespaces = {"xsams":check.XSAMS_NS}
	XPathEval = etree.XPathEvaluator(tree, namespaces=namespaces)

	root = tree.getroot()
	locations = root.get('{%s}schemaLocation' % check.XSI_NS).split(' ')
	locations[1] = '../xsd/xsams/0.3/xsams.xsd'
	root.set('{%s}schemaLocation' % check.XSI_NS, locations[0] + ' ' + locations[1])

	nodes = XPathEval('//*[child::xsams:RadiativeTransition]')
	whiteListOfRefs = _getWhiteListOfRefs(nodes, ['Probability', 'Broadening', 'Shifting'], count)
	if not whiteListOfRefs:
		nodes = XPathEval('//*[child::NonRadiativeTransition]')
		whiteListOfRefs = _getWhiteListOfRefs(nodes, ['Probability', 'Broadening', 'Shifting'], count)
		if not whiteListOfRefs:
			nodes = XPathEval('//*[child::MolecularState]')
			whiteListOfRefs = _getWhiteListOfRefs(nodes, [], count)
			if not whiteListOfRefs:
				nodes = XPathEval('//*[child::AtomicState]')
				whiteListOfRefs = _getWhiteListOfRefs(nodes, [], count)

	_removeRedundantParentNodes(nodes, tree, whiteListOfRefs)

	xml = etree.tostring(tree, pretty_print = True)
	#print xml

	out = open("test/" + fileName + ".IN.xml", 'w')
	out.write(xml)
	out.close()

	out = open("test/" + fileName + ".OUT.MIN.xml", 'w')
	out.write(xml)
	out.close()

	return tree



def _getWhiteListOfRefs(nodes, ballastList, count=0):
	whiteListOfRefs = {}
	if nodes:
		for node in nodes:
			i = 0

			for childNode in list(node)[:]:
				if not count or i < count:
					for ballastName in ballastList:
						for ballastNode in childNode.iter(ballastName):
							childNode.remove(ballastNode)

					for refNode in childNode.xpath('.//*[contains(local-name(@*), "Ref") or contains(local-name(), "Ref")]'):
						if refNode.attrib:
							for attribute in refNode.attrib:
								if attribute.endswith('Ref'):
									whiteListOfRefs[refNode.attrib[attribute].value] = None
						elif refNode.tag.endswith('Ref'):
								whiteListOfRefs[refNode.text] = None
					i += 1
				else:
					node.remove(childNode)

	return whiteListOfRefs



def _removeRedundantParentNodes(usefulParentNodes, stopNode, whiteListOfRefs):
	if not usefulParentNodes or stopNode in usefulParentNodes:
		return

	parentsOfNodes = {}
	for usefulParentNode in usefulParentNodes:
		if usefulParentNode.getparent() is not None and not parentsOfNodes.has_key(usefulParentNode.getparent()):
			parentsOfNodes[usefulParentNode.getparent()] = None

			childNodeNames = [childNode.tag for childNode in list(usefulParentNode.getparent())]
			singleUseNodeNames = [childNodeName for childNodeName in childNodeNames if childNodeNames.count(childNodeName) == 1]

			flag = True
			while flag:
				flag = False
				for childNode in list(usefulParentNode.getparent()):
					if not (childNode in usefulParentNodes):
						hasIDs = False
						isRedundantNode = True
						idNodes = {}
						for idNode in childNode.xpath('descendant-or-self::node()[contains(local-name(@*), "ID")]'):
							for attribute in idNode.attrib:
								if attribute.endswith('ID'):
									hasIDs = True
									if whiteListOfRefs.has_key(idNode.attrib[attribute]):
										isRedundantNode = False
										idNodes[idNode] = None

						if isRedundantNode:
							if hasIDs or not (childNode.tag in singleUseNodeNames):
								usefulParentNode.getparent().remove(childNode)
						else:
							_removeRedundantParentNodes(idNodes, childNode, whiteListOfRefs)

	_removeRedundantParentNodes(parentsOfNodes, stopNode, whiteListOfRefs)
