# -*- coding: utf-8 -*-
import re
from django.db import models


class Biblios(models.Model):
	biblioid = models.IntegerField(primary_key=True, db_column='biblioId') # Field name made lowercase.
	bibliosid = models.IntegerField(unique=True, null=True, db_column='biblioSid', blank=True) # Field name made lowercase.
	dirrootid = models.IntegerField(db_column='dirRootId') # Field name made lowercase.
	bibliolang = models.CharField(max_length=10, db_column='biblioLang', blank=True) # Field name made lowercase.
	biblioauthors = models.CharField(max_length=240, db_column='biblioAuthors', blank=True) # Field name made lowercase.
	biblioname = models.TextField(db_column='biblioName', blank=True) # Field name made lowercase.
	bibliotype = models.IntegerField(db_column='biblioType') # Field name made lowercase.
	bibliodigest = models.CharField(max_length=240, db_column='biblioDigest', blank=True) # Field name made lowercase.
	biblioeditors = models.CharField(max_length=240, db_column='biblioEditors', blank=True) # Field name made lowercase.
	publisherid = models.IntegerField(db_column='publisherId') # Field name made lowercase.
	bibliopublisher = models.CharField(max_length=240, db_column='biblioPublisher', blank=True) # Field name made lowercase.
	journalid = models.IntegerField(db_column='journalId') # Field name made lowercase.
	bibliojournal = models.CharField(max_length=240, db_column='biblioJournal', blank=True) # Field name made lowercase.
	bibliolocality = models.CharField(max_length=240, db_column='biblioLocality', blank=True) # Field name made lowercase.
	biblioyear = models.IntegerField(db_column='biblioYear') # Field name made lowercase.
	bibliocount = models.IntegerField(db_column='biblioCount') # Field name made lowercase.
	bibliovolume = models.CharField(max_length=16, db_column='biblioVolume', blank=True) # Field name made lowercase.
	biblionumber = models.CharField(max_length=16, db_column='biblioNumber', blank=True) # Field name made lowercase.
	biblioissue = models.CharField(max_length=16, db_column='biblioIssue', blank=True) # Field name made lowercase.
	bibliopages = models.CharField(max_length=16, db_column='biblioPages', blank=True) # Field name made lowercase.
	biblioisbn = models.CharField(max_length=240, db_column='biblioISBN', blank=True) # Field name made lowercase.
	biblioesbn = models.CharField(max_length=240, db_column='biblioESBN', blank=True) # Field name made lowercase.
	bibliodoi = models.CharField(max_length=240, db_column='biblioDOI', blank=True) # Field name made lowercase.
	bibliourl = models.CharField(max_length=240, db_column='biblioUrl', blank=True) # Field name made lowercase.
	biblioannotation = models.TextField(db_column='biblioAnnotation', blank=True) # Field name made lowercase.
	biblioindex = models.TextField(db_column='biblioIndex', blank=True) # Field name made lowercase.
	biblioglobal = models.IntegerField(db_column='biblioGlobal') # Field name made lowercase.
	bibliocreator = models.CharField(max_length=16, db_column='biblioCreator') # Field name made lowercase.
	bibliocreate = models.IntegerField(db_column='biblioCreate') # Field name made lowercase.


	def __unicode__(self):
		return u'ID:%s %s %s' % (self.biblioid, self.bibliolang, self.biblioname)


	def getSourceName(self):
		if self.bibliotype == 1:
			return  (self.bibliodigest + ". " if self.bibliodigest else "") + (self.bibliopublisher + ", " if self.bibliopublisher else "") + (self.bibliolocality if self.bibliolocality else "")
		elif self.bibliotype == 2:
			return self.bibliojournal
		elif self.bibliotype == 5:
			return self.bibliopublisher
		elif self.bibliotype == 6:
			return  (self.bibliodigest + ". " if self.bibliodigest else "") + (self.bibliopublisher + ", " if self.bibliopublisher else "") + (self.bibliolocality if self.bibliolocality else "")
		else:
			return None

	def getArticleNumber(self):
		if self.biblionumber and self.biblionumber != "0":
			return self.biblionumber
		elif self.biblioissue and self.biblioissue != "0":
			return self.biblioissue
		else:
			return None

	def getPagesPattern(self):
		return re.compile(r"-")

	def getReportPattern(self):
		return re.compile(r"^Report | Report |Report$|Отчёт")

	def getThesisPattern(self):
		return re.compile(r"^Thesis| Thesis |Thesis$|Dissertation|Диссертация")

	def getPageBegin(self):
		if self.bibliotype == 1:
			return 0 if self.bibliocount else None
		elif self.bibliotype == 2:
			if self.bibliopages:
				pages = self.getPagesPattern().split(self.bibliopages)
				return pages[0]
			else:
				return None
		elif self.bibliotype == 5:
			return None
		elif self.bibliotype == 6:
			if self.getReportPattern().search(self.bibliodigest) is not None:
				return 0 if self.bibliopages else None
			else:
				if self.bibliopages:
					pages = self.getPagesPattern().split(self.bibliopages)
					return pages[0]
				else:
					return None
		else:
			return None

	def getPageEnd(self):
		if self.bibliotype == 1:
			return self.bibliocount if self.bibliocount else None
		elif self.bibliotype == 2:
			if self.bibliopages:
				pages = self.getPagesPattern().split(self.bibliopages)
				return pages[1] if len(pages)>1 else pages[0]
			else:
				return None
		elif self.bibliotype == 5:
			return None
		elif self.bibliotype == 6:
			if self.getReportPattern().search(self.bibliodigest) is not None:
				if self.bibliopages:
					pages = self.getPagesPattern().split(self.bibliopages)
					return pages[0]
				else:
					return None
			else:
				if self.bibliopages:
					pages = self.getPagesPattern().split(self.bibliopages)
					return pages[1] if len(pages)>1 else pages[0]
				else:
					return None
		else:
			return None

	def getAuthorList(self):
		patternObj = re.compile(r"(?<!&\w)(?<!&\w{2})(?<!&\w{3})(?<!&\w{4})(?<!&\w{5})(?<!&\w{6})(?<!&\w{7})(?<!&\w{8})(?<!&#\d)(?<!&#\d{2})(?<!&#\d{3})(?<!&#\d{4})(?<!&#\d{5});")
		return [name.strip() for name in (patternObj.split(self.biblioauthors) if (patternObj.search(self.biblioauthors)) else re.split(r",| and ", self.biblioauthors))]


	class Meta:
		db_table = u'biblios'



class Journals(models.Model):
	journalid = models.IntegerField(primary_key=True, db_column='journalId') # Field name made lowercase.
	journalsid = models.IntegerField(unique=True, null=True, db_column='journalSid', blank=True) # Field name made lowercase.
	dirrootid = models.IntegerField(db_column='dirRootId') # Field name made lowercase.
	journallang = models.CharField(max_length=10, db_column='journalLang', blank=True) # Field name made lowercase.
	journalname = models.CharField(max_length=240, db_column='journalName') # Field name made lowercase.
	journalabbrev = models.CharField(max_length=240, db_column='journalAbbrev', blank=True) # Field name made lowercase.
	publisherid = models.IntegerField(db_column='publisherId') # Field name made lowercase.
	journalpublisher = models.CharField(max_length=240, db_column='journalPublisher') # Field name made lowercase.
	journalisbn = models.CharField(max_length=240, db_column='journalISBN', blank=True) # Field name made lowercase.
	journalesbn = models.CharField(max_length=240, db_column='journalESBN', blank=True) # Field name made lowercase.
	journalurl = models.CharField(max_length=240, db_column='journalUrl', blank=True) # Field name made lowercase.
	journalannotation = models.TextField(db_column='journalAnnotation', blank=True) # Field name made lowercase.
	journalglobal = models.IntegerField(db_column='journalGlobal') # Field name made lowercase.
	journalcreator = models.CharField(max_length=16, db_column='journalCreator') # Field name made lowercase.
	journalcreate = models.IntegerField(db_column='journalCreate') # Field name made lowercase.


	def __unicode__(self):
		return u'ID:%s %s %s' % (self.journalid, self.journallang, self.journalname)


	class Meta:
		db_table = u'journals'



class Publishers(models.Model):
	publisherid = models.IntegerField(primary_key=True, db_column='publisherId') # Field name made lowercase.
	publishersid = models.IntegerField(unique=True, null=True, db_column='publisherSid', blank=True) # Field name made lowercase.
	dirrootid = models.IntegerField(db_column='dirRootId') # Field name made lowercase.
	publisherlang = models.CharField(max_length=10, db_column='publisherLang', blank=True) # Field name made lowercase.
	publishername = models.CharField(max_length=240, db_column='publisherName') # Field name made lowercase.
	publisheraddress = models.CharField(max_length=240, db_column='publisherAddress', blank=True) # Field name made lowercase.
	publisherurl = models.CharField(max_length=240, db_column='publisherUrl', blank=True) # Field name made lowercase.
	publisherannotation = models.TextField(db_column='publisherAnnotation', blank=True) # Field name made lowercase.
	publisherglobal = models.IntegerField(db_column='publisherGlobal') # Field name made lowercase.
	publishercreator = models.CharField(max_length=16, db_column='publisherCreator') # Field name made lowercase.
	publishercreate = models.IntegerField(db_column='publisherCreate') # Field name made lowercase.


	def __unicode__(self):
		return u'ID:%s %s %s' % (self.publisherid, self.publisherlang, self.publishername)


	class Meta:
		db_table = u'publishers'
