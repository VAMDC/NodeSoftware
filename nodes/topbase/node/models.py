# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
import logging
log=logging.getLogger('vamdc.tap')

class Unit(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(unique=True, max_length=60)
    class Meta:
        db_table = u't_unit'
        
        
class Sourcecategory(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(unique=True, max_length=45)
    class Meta:
        db_table = u't_sourcecategory'
        
        
        
class Source(models.Model):
    id = models.IntegerField(primary_key=True)
    sourcecategory = models.ForeignKey(Sourcecategory, db_column='sourcecategoryid')
    title = models.TextField(null=True)
    year = models.IntegerField(null=True)
    volume = models.IntegerField(null=True)    
    uri = models.CharField(max_length=150, null=True, db_column='url')
    bibcode = models.CharField(max_length=19, null=True)
    sourcename = models.CharField(max_length=100)
    pagebegin = models.IntegerField(null=True)    
    pageend = models.IntegerField(null=True)    
    doi = models.CharField(max_length=50, null=True)  
    
    def authornames(self):
        names = []
        log.debug('test : '+str(self.id))
        authors = Authorsource.objects.filter(source=self)
        for author in authors:
            log.debug('found : ')
            names.append(author.name)
        return names
        
        
      
    class Meta:
        db_table = u't_source'


class Chemicalelement(models.Model):
    id = models.IntegerField(primary_key=True)
    elementsymbol = models.CharField(unique=True, max_length=9)
    nuclearcharge = models.IntegerField(unique=True)
    class Meta:
        db_table = u't_chemicalelement'

class Isotope(models.Model):
    id = models.IntegerField(primary_key=True)
    chemicalelement = models.ForeignKey(Chemicalelement, db_column='chemicalelementid')
    massnumber = models.IntegerField(unique=True)
    mass = models.FloatField()
    massunitid = models.ForeignKey(Unit, db_column='massunitid')
    class Meta:
        db_table = u't_isotope'


class Atomicion(models.Model):
    id = models.IntegerField(primary_key=True)
    isotope = models.ForeignKey(Isotope, null=True, db_column='isotopeid', blank=True)
    ioncharge = models.IntegerField()
    inchi = models.CharField(max_length=100)
    inchikey = models.CharField(max_length=27)
    isoelectronicsequence = models.CharField(max_length=30)  
    class Meta:
        db_table = u't_atomicion'
 


class Version(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicion = models.ForeignKey(Atomicion, null=True, db_column='atomicionid', blank=True)
    ionversion = models.IntegerField(unique=True)
    creationdate = models.DateField()
    class Meta:
        db_table = u't_version'
        managed = False


class Parity(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(unique=True, max_length=30)
    class Meta:
        db_table = u't_parity'
        
class Mixingclass(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(unique=True, max_length=30)
    class Meta:
        db_table = u't_mixingclass'
        
class Atomicstate(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.ForeignKey(Version, db_column='versionid')
    totalangularmomentum = models.FloatField()
    lifetime = models.FloatField()
    #lifetimeunit = models.ForeignKey(Unit, db_column='lifetimeunitid', related_name='+')
    lifetimeunit = models.CharField(max_length=8)
    stateenergy = models.FloatField()
    #stateenergyunit = models.ForeignKey(Unit, db_column='stateenergyunitid', related_name='+')
    stateenergyunit = models.CharField(max_length=8)
    ionizationenergy = models.FloatField(null=True, blank=True)
    #ionizationenergyunit = models.ForeignKey(Unit, db_column='ionizationenergyunitid', related_name='+')
    ionizationenergyunit = models.CharField(max_length=8)
    statisticalweight = models.IntegerField()
    #statisticalweightunit = models.ForeignKey(Unit, db_column='statisticalweightunitid', related_name='+')
    statisticalweightunit = models.CharField(max_length=8)
    parity = models.ForeignKey(Parity, db_column='parityid')
    xdata = models.TextField(null=True)
    ydata = models.TextField(null=True)
    #xdataunit = models.ForeignKey(Unit, db_column='xdataunitid', related_name='+', null=True)
    #ydataunit = models.ForeignKey(Unit, db_column='ydataunitid', related_name='+', null=True)
    xdataunit = models.CharField(max_length=8)
    ydataunit = models.CharField(max_length=8)
    class Meta:
        db_table = u't_atomicstate'
        
class Atomicstatesource(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicstate = models.ForeignKey(Atomicstate, db_column='atomicstateid')
    source = models.ForeignKey(Source, db_column='sourceid')
    class Meta:
        db_table = u't_atomicstatesource'
 
class Radiativetransition(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.ForeignKey(Version, db_column='versionid')
    elementsymbol = models.CharField(max_length=9)
    nuclearcharge =  models.IntegerField()
    ioncharge =  models.IntegerField()
    oscillatorstrength = models.FloatField()
    weightedoscillatorstrength = models.FloatField()
    transitionprobability = models.IntegerField()
    wavelength = models.FloatField()
    #wavelengthunit = models.ForeignKey(Unit, db_column='wavelengthunitid')
    wavelengthunit = models.CharField(max_length=8)
    upperatomicstate = models.ForeignKey(Atomicstate, db_column='upperatomicstateid', related_name='+')
    loweratomicstate = models.ForeignKey(Atomicstate, db_column='loweratomicstateid', related_name='+')    
    
    def abs_weightedoscillatorstrength(self):
        return abs(self.weightedoscillatorstrength)
   
    class Meta:
        db_table = u'c_recommendedradiativetransition'
        
class Radiativetransitionsource(models.Model):
    id = models.IntegerField(primary_key=True)
    radiativetransition = models.ForeignKey(Atomicstate, db_column='radiativetransitionid')
    source = models.ForeignKey(Source, db_column='sourceid')
    class Meta:
        db_table = u't_radiativetransitionsource'

class Atomiccomponent(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicstate = models.ForeignKey(Atomicstate, db_column='atomicstateid', related_name='atomiccomponent')
    mixingcoefficient = models.FloatField()
    mixingclass = models.ForeignKey(Mixingclass, db_column='mixingclassid')
    termlabel = models.CharField(max_length=30)
    configuration = models.CharField(max_length=40)
    class Meta:
        db_table = u't_atomiccomponent'


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    address = models.TextField(null=True)
    class Meta:
        db_table = u't_author'

class Authorsource(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(Author, db_column='authorid')
    source = models.ForeignKey(Source, db_column='sourceid')
    rank = models.IntegerField()
    class Meta:
        db_table = u't_authorsource'

class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    creationdate = models.DateField()
    isrecommended = models.IntegerField()
    class Meta:
        db_table = u't_dataset'

class DatasetVersion(models.Model):
    datasetid = models.ForeignKey(Dataset, db_column='datasetid')
    versionid = models.ForeignKey(Version, db_column='versionid')
    class Meta:
        db_table = u't_dataseVersion'



class Lscoupling(models.Model):
    id = models.IntegerField(primary_key=True)
    atomiccomponent = models.ForeignKey(Atomiccomponent, db_column='atomiccomponentid')
    l = models.IntegerField()
    s = models.FloatField()
    multiplicity = models.IntegerField()
    class Meta:
        db_table = u't_lscoupling'












