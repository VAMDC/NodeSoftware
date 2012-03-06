import nodes.wadis.node.model.saga as saga
from nodes.wadis.node.model.fake import categoryTypeDict
from django.db.models import Q

defaultList = {'id_substance':('exact','1000021')}

def makeQ(q, tuple):
	defaultFlag = formatQ(q, tuple, True)
	q &= Q(**{'id_%s_ds__status__exact' % tuple[0]:'public'})
	if defaultFlag:
		for field in defaultList:
			q &= Q(**{field + '__' + defaultList[field][0]: defaultList[field][1]})
	if tuple[0] != 'energy':
		q &= Q(**{'id_%s_ds__composition__exact' % tuple[0]: 'Primary'})
	return q

def formatQ(q, tuple, defaultFlag):
	for k, c in enumerate(q.children):
		if type(c) == Q:
			defaultFlag = formatQ(c, tuple, defaultFlag)
		else:
			if (type(c[0]) == str and c[0][:c[0].rfind('__')] in defaultList) or (type(c[1]) == str and c[1][:c[1].rfind('__')] in defaultList):
				defaultFlag = False
			var1 = c[0] % tuple if type(c[0]) == str and c[0].count('%') == len(tuple) else c[0]
			var2 = c[1] % tuple if type(c[1]) == str and c[1].count('%') == len(tuple) else c[1]
			q.children[k] = (var1, var2)
	return defaultFlag


def inchi2Id(*restrictionTuple):
	restrictions = list(restrictionTuple)
	variable, operator, values = restrictions[0], restrictions[1], restrictions[2:]

	variable = 'inner.id_substance'

	for index, value in enumerate(values):
		if value == '(' or value == ')':
			continue
		value = value.replace('"', '').replace("'", '')
		if value in saga.SubstanceDict.byInchi:
			values[index] = str(saga.SubstanceDict.byInchi[value].id_substance)

	restrictions = [variable, operator] + values
	return restrictions



def inchiKey2Id(*restrictionTuple):
	restrictions = list(restrictionTuple)
	variable, operator, values = restrictions[0], restrictions[1], restrictions[2:]

	variable = 'inner.id_substance'

	for index, value in enumerate(values):
		if value == '(' or value == ')':
			continue
		value = value.replace('"', '').replace("'", '')
		if value in saga.SubstanceDict.byInchiKey:
			values[index] = str(saga.SubstanceDict.byInchiKey[value].id_substance)

	restrictions = [variable, operator] + values
	return restrictions



def methodCategory2Type(*restrictionTuple):
	restrictions = list(restrictionTuple)
	variable, operator, values = restrictions[0], restrictions[1], restrictions[2:]

	variable = 'inner.type'

	for index, value in enumerate(values):
		if value == '(' or value == ')':
			continue
		value = value.replace('"', '').replace("'", '')
		if value in categoryTypeDict:
			values[index] = str(categoryTypeDict[value])
		else:
			values[index] = str(-1)

	restrictions = [variable, operator] + values
	return restrictions


