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
    sourcecategory = models.ForeignKey(Sourcecategory, db_column='sourcecategoryid', on_delete=models.DO_NOTHING)
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
        authors = Authorsource.objects.filter(source=self)
        for author in authors:
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
    chemicalelement = models.ForeignKey(Chemicalelement, db_column='chemicalelementid', on_delete=models.DO_NOTHING)
    massnumber = models.IntegerField(unique=True)
    mass = models.FloatField()
    massunitid = models.ForeignKey(Unit, db_column='massunitid', on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u't_isotope'


class Atomicion(models.Model):
    id = models.IntegerField(primary_key=True)
    isotope = models.ForeignKey(Isotope, null=True, db_column='isotopeid', blank=True, on_delete=models.DO_NOTHING)
    ioncharge = models.IntegerField()
    inchi = models.CharField(max_length=100)
    inchikey = models.CharField(max_length=27)
    isoelectronicsequence = models.CharField(max_length=30)  
    class Meta:
        db_table = u't_atomicion'
 


class Version(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicion = models.ForeignKey(Atomicion, null=True, db_column='atomicionid', blank=True, on_delete=models.DO_NOTHING)
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
    version = models.ForeignKey(Version, db_column='versionid', on_delete=models.DO_NOTHING)
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
    parity = models.ForeignKey(Parity, db_column='parityid', on_delete=models.DO_NOTHING)
    xdata = models.TextField(null=True)
    ydata = models.TextField(null=True)
    xdataunit = models.CharField(max_length=8)
    ydataunit = models.CharField(max_length=8)
    class Meta:
        db_table = u't_atomicstate'
        
    def xdata_count(self):
      return len(self.xdata.split(" "))
      
    def ydata_count(self):
      return len(self.ydata.split(" "))
        
        
class Atomicstatesource(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicstate = models.ForeignKey(Atomicstate, db_column='atomicstateid', on_delete=models.DO_NOTHING)
    source = models.ForeignKey(Source, db_column='sourceid', on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u't_atomicstatesource'
 
class Radiativetransition(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.ForeignKey(Version, db_column='versionid', on_delete=models.DO_NOTHING)
    #~ version_int = models.IntegerField(db_column='versionid')
    atomicion = models.IntegerField(db_column='atomicionid')
    elementsymbol = models.CharField(max_length=9)
    nuclearcharge =  models.IntegerField()
    ioncharge =  models.IntegerField()
    oscillatorstrength = models.FloatField()
    weightedoscillatorstrength = models.FloatField()
    transitionprobability = models.IntegerField()
    wavelength = models.FloatField()
    wavelengthunit = models.CharField(max_length=8)
    upperatomicstate = models.ForeignKey(Atomicstate, db_column='upperatomicstateid', related_name='+', on_delete=models.DO_NOTHING)
    #~ upperatomicstate_int = models.IntegerField(db_column='upperatomicstateid')
    loweratomicstate = models.ForeignKey(Atomicstate, db_column='loweratomicstateid', related_name='+', on_delete=models.DO_NOTHING)    
    #~ loweratomicstate_int = models.IntegerField(db_column='loweratomicstateid')
    inchikey = models.CharField(max_length=27)   
    collider = models.CharField(max_length=8, default="photon")
     
    def abs_weightedoscillatorstrength(self):
        return abs(self.weightedoscillatorstrength)       
   
    class Meta:
        db_table = u'c_recommendedradiativetransition'
        
   
class Versionsource(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.ForeignKey(Atomicstate, db_column='versionid', on_delete=models.DO_NOTHING)
    source = models.ForeignKey(Source, db_column='sourceid', on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u't_versionsource'

class Atomiccomponent(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicstate = models.ForeignKey(Atomicstate, db_column='atomicstateid', related_name='atomiccomponent', on_delete=models.DO_NOTHING)
    mixingcoefficient = models.FloatField()
    mixingclass = models.ForeignKey(Mixingclass, db_column='mixingclassid', on_delete=models.DO_NOTHING)
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
    author = models.ForeignKey(Author, db_column='authorid', on_delete=models.DO_NOTHING)
    source = models.ForeignKey(Source, db_column='sourceid', on_delete=models.DO_NOTHING)
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
    datasetid = models.ForeignKey(Dataset, db_column='datasetid', on_delete=models.DO_NOTHING)
    versionid = models.ForeignKey(Version, db_column='versionid', on_delete=models.DO_NOTHING)
    class Meta:
        db_table = u't_dataseVersion'



class Lscoupling(models.Model):
    id = models.IntegerField(primary_key=True)
    atomiccomponent = models.ForeignKey(Atomiccomponent, db_column='atomiccomponentid', on_delete=models.DO_NOTHING)
    l = models.IntegerField()
    s = models.FloatField()
    multiplicity = models.IntegerField()
    class Meta:
        db_table = u't_lscoupling'
