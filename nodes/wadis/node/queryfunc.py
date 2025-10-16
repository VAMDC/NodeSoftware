# -*- coding: utf-8 -*-
#
# This module (which must have the name queryfunc.py) is responsible
# for converting incoming queries to a database query understood by
# this particular node's database schema.
# 
# This module must contain a function setupResults, taking a sql object
# as its only argument. 
#
import sys
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from wadis.node.model import atmos
from wadis.node.model.fake import State
from wadis.node.model.saga import Substancecorr
from wadis.node.model.saga import Substance
from wadis.node.transforms import makeQ
from django.db.models.query import EmptyQuerySet
from vamdctap.sqlparse import sql2Q
import other.verification.http
from django.db.models import Q
import html

import models


def LOG(s):
	if settings.DEBUG: print >> sys.stderr, "\n%s" % s


#------------------------------------------------------------
# Helper functions (called from setupResults)
#------------------------------------------------------------

def getSources(items):
	sources = {}
	for item in items:
		table = item._meta.db_table
		biblioId = getattr(item, 'id_%s_ds' % ('transition' if table == 'lineprof' else table)).id_biblio

		if not (biblioId in sources):
			try:
				biblio = atmos.Biblios.objects.get(biblioid=biblioId)
			except ObjectDoesNotExist:
				LOG("No biblioId=%s" % biblioId)
				continue
			#0000-9999
			biblio.biblioyear = biblio.biblioyear if biblio.biblioyear > 1000 else 1000 + biblio.biblioyear
			biblio.biblioTypeName = 'journal'
			if biblio.biblioname:
				biblio.biblioname = html.escape(biblio.biblioname)
			if biblio.bibliodigest:
				biblio.bibliodigest = html.escape(biblio.bibliodigest)
			if biblio.biblioannotation:
				biblio.biblioannotation = html.escape(biblio.biblioannotation)

			if biblio.bibliotype == 1:
				if biblio.getThesisPattern().search(biblio.biblioname) is not None:
					biblio.biblioTypeName = 'thesis'
				else:
					biblio.biblioTypeName = 'book'
			elif biblio.bibliotype == 5:
				biblio.biblioTypeName = 'database'
			elif biblio.bibliotype == 6:
				if biblio.getReportPattern().search(biblio.bibliodigest) is not None:
					biblio.biblioTypeName = 'report'
				else:
					biblio.biblioTypeName = 'proceedings'
			sources[biblioId] = biblio

	return sources.values()


def getMolecules(items):
	molecules = {}

	for item in items:
		table = item._meta.db_table
		id_substance = item.id_substance

		if not (id_substance in molecules):
			try:
				substance = Substancecorr.objects.get(id_substance=id_substance)

				substanceDescription = Substance.objects.get(id_substance=id_substance)
				englishName = 'Unknown name'
				if substanceDescription.english:
					englishName = substanceDescription.english
				else:
					if substance.id_subst_main:
						substanceMainDescription = Substance.objects.get(id_substance=substance.id_subst_main)
						if substanceMainDescription.english:
							englishName = substanceMainDescription.english + ' isotopologue'
				substance.englishName = englishName
				substance.weight = substanceDescription.weight
			except ObjectDoesNotExist:
				LOG("No id_substance=%s" % id_substance)
				continue
			if not hasattr(substance,'States'):
				substance.States = {}
			molecules[id_substance] = substance
		else:
			substance = molecules[id_substance]

		if table == 'energy':
			qns =  item.qns()
			if not (qns in substance.States):
				substance.States[qns] = State(id_substance, item.getCase(), item, qns)

		elif table == 'transition' or table == 'lineprof':
			upQNs =  item.up()
			if not (upQNs in substance.States):
				up = State(id_substance, item.getCase(), None, upQNs)
				substance.States[upQNs] = up
				item.up = up.id
			else:
				item.up = substance.States[upQNs].id

			lowQNs = item.low()
			if not (lowQNs in substance.States):
				low = State(id_substance, item.getCase(), None, lowQNs)
				substance.States[lowQNs] = low
				item.low = low.id
			else:
				item.low = substance.States[lowQNs].id

	return molecules.values()


def getRows(database, table, q):
	LOG(q)
	dbModule = getattr(models, database, None)
	if dbModule:
		tableObj = getattr(dbModule , table.capitalize())
		tableDigestObj = getattr(dbModule , table.capitalize() + 'Digest')
		table = 'transition' if table == 'lineprof' else table
		dsID = 'id_%s_ds' % table
		exQ = Q(**{dsID + '__in': tableDigestObj.objects.filter(line_count__gt=settings.LIMIT).values_list(dsID, flat=True)})
		return tableObj.objects.select_related().exclude(exQ).filter(makeQ(q, (table,)))
	else:
		return EmptyQuerySet()


tableList = {'energy':'energy', 'einstein_coefficient':'transition', 'intensity':'lineprof'}
def getTable(q, default):
	for k, c in enumerate(q.children):
		if type(c) == Q:
			default = getTable(c, default)
		else:
			for i in [0, 1]:
				if type(c[i]) == str:
					x = c[i][:c[i].rfind('__')]
					if x in tableList:
						if default is not None:
							if default != tableList[x]:
								del q.children[k]
						else:
							default = tableList[x]
	return default

def getDatabase(q, default):
	for k, c in enumerate(q.children):
		if type(c) == Q:
			default = getDatabase(c, default)
		else:
			for i in [0, 1]:
				if type(c[i]) == str:
					x = c[i][:c[i].rfind('__')]
					if x == 'id_substance':
						substances = Substancecorr.objects.filter(c)
						for substance in substances:
							if default is not None:
								if default != substance.database_name:
									del q.children[k]
							else:
								default = substance.database_name
	return default

#------------------------------------------------------------
# Main function 
#------------------------------------------------------------
def setupResults(tap):
	"""
		This function is always called by the software.
		"""
	# log the incoming query
	LOG(tap)
	if not tap.where:
		return {}
	q = sql2Q(tap)

	database = getDatabase(q, None)
	if database is None:
		database = "saga2"

	table = getTable(q, None)
	if table is None:
		table = "transition"
	rows = getRows(database, table, q)
	rowCount = rows.count()

	if settings.ROW_LIMIT < rowCount:
		rows = rows[:settings.ROW_LIMIT]
		percentage = '%.1f' % (float(settings.ROW_LIMIT) / rowCount * 100)
		rowCount = settings.ROW_LIMIT
	else:
		percentage = '100'

	if table == 'energy':
		transitions = []
		transitionCount = 0
	else:
		transitions = rows
		transitionCount = rowCount

	sources = getSources(rows)
	sourceCount = 0
	if sources is not None:
		sourceCount = len(sources)

	molecules = getMolecules(rows)
	stateCount = 0
	moleculeCount = 0
	if molecules is not None:
		moleculeCount = len(molecules)
		for substance in molecules:
			substance.States = sorted(substance.States.values(), key = lambda x: x.id)
			stateCount += len(substance.States)

	size = 0.0011 + sourceCount*0.0015 + moleculeCount*0.00065 + stateCount*0.0004 + transitionCount*0.0003

	# Create the header with some useful info. The key names here are
	# standardized and shouldn't be changed.
	headerInfo = {#
		#see vamdctap->views->addHeaders()->HEADS
		'COUNT-SOURCES': sourceCount, #the count of the corresponding blocks in the XSAMS schema
		#'COUNT-ATOMS',
		'COUNT-MOLECULES': moleculeCount,
		'COUNT-SPECIES': moleculeCount,
		'COUNT-STATES' : stateCount,
		#'COUNT-COLLISIONS',
		'COUNT-RADIATIVE': transitionCount,
		#'COUNT-NONRADIATIVE',
		'TRUNCATED': percentage, #the percentage that the returned data represent with respect to the total amount available for that query
		'APPROX-SIZE': '%.3f' % size, #estimate uncompressed document size in megabytes
	}

	LOG(headerInfo)
	# Return the data. The keynames are standardized.
	# see vamdctap->generators->Xsams()
	return {#
		'HeaderInfo': headerInfo,
		'Sources': sources,
		'Methods': models.methods,
		#'Functions':,
		#'Environments':,
		#'Atoms':,
		'Molecules': molecules,
		#'Solids':,
		#'Particles':,
		#'CollTrans':,
		'RadTrans': transitions,
		#'RadCross':,
		#'NonRadTrans':,
	}

rules = None #See tests.py
def returnResults(tap):
	return other.verification.http.getResult(tap, rules)
