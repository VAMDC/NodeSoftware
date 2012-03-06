class Method(object):
	def __init__(self, id, category, description):
		self.id = id
		self.category = category
		self.description = description


def getMethods():
	#See XSAMS-schema. Allowed values are: experiment, theory, ritz, recommended, evaluated, empirical, scalingLaw, semiempirical, compilation, derived, observed
	methods = []
	methods.insert(0, Method("Theory", "theory", "theory"))
	methods.insert(1, Method("Exp", "experiment", "experiment"))
	return methods

def getCategoryTypeDict():
	categoryTypeDict = {}
	for type, method in enumerate(methods):
		categoryTypeDict[method.category] = type
	return categoryTypeDict

methods = getMethods()
categoryTypeDict = getCategoryTypeDict()


toStr = lambda item: 'X' if item[1] is None else str(item[1])
def makeStateId(id_substance, qns):
	return str(id_substance - 1000000)+ '-' + '.'.join(map(toStr, qns))


class State(object):

	def __init__(self, id_substance, case, obj, *args, **kwargs):
		self.case = case
		self._wrappedObj = obj
		self.id = None

		for arg in args:
			self.id = makeStateId(id_substance, arg)
			self.qns = dict(arg)
		self.qns.update(kwargs)

	def __getattr__(self, item):
		if item in self.__dict__:
			return getattr(self, item)
		elif item in self.qns:
			if self.qns[item] == -2:
				return None
			else:
				if type(self.qns[item]) == unicode and len(self.qns[item]) > 1:
					return self.qns[item][:-1].lstrip('0') + self.qns[item][-1:]
				else:
					return self.qns[item]
		elif self._wrappedObj and hasattr(self._wrappedObj, item):
			return getattr(self._wrappedObj, item)
		else:
			return None

	def __eq__(self, other):
		return self.id == other.id

	def __hash__(self):
		return hash(self.id)

	def __cmp__(self, other):
		if self.id < other.id:
			return -1
		elif self.id > other.id:
			return 1
		else:
			return 0
