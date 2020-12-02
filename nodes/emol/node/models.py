# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Crosssection(models.Model):
    crosssectiontype = models.CharField(max_length=10L, db_column='CrossSectionType') # Field name made lowercase.
    crosssectionname = models.CharField(max_length=50L, db_column='CrossSectionName') # Field name made lowercase.
    crosssectiondescription = models.CharField(max_length=200L, db_column='CrossSectionDescription') # Field name made lowercase.
    crosssectionid = models.IntegerField(primary_key=True, db_column='CrossSectionID') # Field name made lowercase.
    class Meta:
        db_table = 'crosssection'

class Datasource(models.Model):
    sourceid = models.IntegerField(primary_key=True, db_column='SourceID') # Field name made lowercase.
    sourcecategory = models.CharField(max_length=50L, db_column='SourceCategory', blank=True) # Field name made lowercase.
    sourceauthorname = models.CharField(max_length=200L, db_column='SourceAuthorName', blank=True) # Field name made lowercase.
    sourcetitle = models.CharField(max_length=500L, db_column='SourceTitle', blank=True) # Field name made lowercase.
    sourcename = models.CharField(max_length=100L, db_column='SourceName', blank=True) # Field name made lowercase.
    sourcevolume = models.CharField(max_length=8L, db_column='SourceVolume', blank=True) # Field name made lowercase.
    sourceyear = models.IntegerField(null=True, db_column='SourceYear', blank=True) # Field name made lowercase.
    sourcepagebegin = models.CharField(max_length=30L, db_column='SourcePageBegin', blank=True) # Field name made lowercase.
    sourcepageend = models.CharField(max_length=30L, db_column='SourcePageEnd', blank=True) # Field name made lowercase.
    sourceuri = models.CharField(max_length=200L, db_column='SourceURI', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'datasource'

class Ecs(models.Model):
    tableid = models.IntegerField(primary_key=True)
    moleculeid = models.ForeignKey('Molspecies', db_column='MoleculeID') # Field name made lowercase.
    sourceid = models.ForeignKey(Datasource, db_column='SourceID') # Field name made lowercase.
    crosssectiontype = models.CharField(max_length=30L, db_column='CrossSectionType') # Field name made lowercase.
    crosssectionname = models.CharField(max_length=200L, db_column='CrossSectionName', blank=True) # Field name made lowercase.
    collisioncomment = models.CharField(max_length=200L, db_column='CollisionComment', blank=True) # Field name made lowercase.
    collisionmethod = models.CharField(max_length=200L, db_column='CollisionMethod', blank=True) # Field name made lowercase.
    collisionthreshold = models.CharField(max_length=30L, db_column='CollisionThreshold', blank=True) # Field name made lowercase.
    crosssectionxname = models.CharField(max_length=50L, db_column='CrossSectionXName', blank=True) # Field name made lowercase.
    crosssectionxunit = models.CharField(max_length=50L, db_column='CrossSectionXUnit') # Field name made lowercase.
    crosssectionx = models.CharField(max_length=30L, db_column='CrossSectionX') # Field name made lowercase.
    crosssectionyname = models.CharField(max_length=50L, db_column='CrossSectionYName', blank=True) # Field name made lowercase.
    crosssectionyunit = models.CharField(max_length=50L, db_column='CrossSectionYUnit') # Field name made lowercase.
    crosssectiony = models.CharField(max_length=30L, db_column='CrossSectionY') # Field name made lowercase.
    crosssectionyerror = models.CharField(max_length=30L, db_column='CrossSectionYError', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'ecs'

class Ecsplot(models.Model):
    tableid = models.IntegerField(primary_key=True)
    moleculeid = models.ForeignKey('Molspecies', db_column='MoleculeID') # Field name made lowercase.
    sourceid = models.ForeignKey(Datasource, db_column='SourceID') # Field name made lowercase.
    crosssectiontype = models.CharField(max_length=30L, db_column='CrossSectionType') # Field name made lowercase.
    title = models.CharField(max_length=200L, db_column='Title') # Field name made lowercase.
    subtitle = models.CharField(max_length=999L, db_column='SubTitle', blank=True) # Field name made lowercase.
    crosssectionfigfile = models.CharField(max_length=100L, db_column='CrossSectionFigFile') # Field name made lowercase.
    crosssectiondatafile = models.CharField(max_length=100L, db_column='CrossSectionDataFile') # Field name made lowercase.
    caption = models.CharField(max_length=200L, db_column='Caption') # Field name made lowercase.
    subcaption = models.CharField(max_length=999L, db_column='SubCaption', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'ecsplot'

class Molspecies(models.Model):
    moleculeid = models.IntegerField(primary_key=True, db_column='MoleculeID') # Field name made lowercase.
    moleculechemicalformula = models.CharField(max_length=30L, db_column='MoleculeChemicalFormula') # Field name made lowercase.
    moleculechemicalname = models.CharField(max_length=50L, db_column='MoleculeChemicalName', blank=True) # Field name made lowercase.
    moleculecommonname = models.CharField(max_length=50L, db_column='MoleculeCommonName', blank=True) # Field name made lowercase.
    inchikey = models.CharField(max_length=30, db_column='InChIKey')
    inchi = models.CharField(max_length=30, db_column='InChI')
    class Meta:
        db_table = 'molspecies'

class Users(models.Model):
    userid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50L)
    position = models.CharField(max_length=50L)
    institution = models.CharField(max_length=100L)
    address = models.CharField(max_length=200L)
    emailid = models.CharField(max_length=50L)
    mobileno = models.CharField(max_length=20L)
    date = models.CharField(max_length=20L)
    username = models.CharField(max_length=50L)
    password = models.CharField(max_length=50L)
    verify = models.IntegerField()
    permission = models.IntegerField()
    class Meta:
        db_table = 'users'

