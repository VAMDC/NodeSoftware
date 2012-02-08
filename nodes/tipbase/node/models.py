# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

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
    sourcecategoryid = models.ForeignKey(Sourcecategory, db_column='sourcecategoryid')
    title = models.CharField(max_length=450)
    year = models.IntegerField()
    url = models.CharField(max_length=450, blank=True)
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
    inchi = models.CharField(max_length=30)
    inchikey = models.CharField(max_length=30)
    isoelectronicsequence = models.CharField(max_length=30)  
    class Meta:
        db_table = u't_atomicion'
 


class Version(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicion = models.ForeignKey(Atomicion, null=True, db_column='atomicionid', blank=True)
    radiativetransitionsource = models.ForeignKey(Source, null=True, db_column='radiativetransitionsourceid', blank=True, related_name='+')
    crosssectionsource = models.ForeignKey(Source, null=True, db_column='crosssectionsourceid', blank=True)
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
    sourcefileid = models.IntegerField()    
    totalangularmomentum = models.FloatField()
    lifetime = models.FloatField()
    lifetimeunit = models.ForeignKey(Unit, db_column='lifetimeunitid', related_name='+')
    stateenergy = models.FloatField()
    stateenergyunit = models.ForeignKey(Unit, db_column='stateenergyunitid', related_name='+')
    ionizationenergy = models.FloatField(null=True, blank=True)
    ionizationenergyunit = models.ForeignKey(Unit, db_column='ionizationenergyunitid', related_name='+')
    statisticalweight = models.IntegerField()
    statisticalweightunit = models.ForeignKey(Unit, db_column='statisticalweightunitid', related_name='+')
    parity = models.ForeignKey(Parity, db_column='parityid')
    
    def state_id(self):
        return self.id
        
    def species_id(self):
        return None
        
    class Meta:
        db_table = u't_atomicstate'
        
class Particle(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)
    mass = models.FloatField()
    massunit = models.ForeignKey(Unit, db_column='massunitid', related_name='+')
    charge = models.FloatField()
   
    def species_id(self):
        return 'P%s'%self.id
        
    def state_id(self):
        return None
        
    class Meta:
        db_table = u't_particle'
 
class Collisionaltransition(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.ForeignKey(Version, db_column='versionid')
    elementsymbol = models.CharField(max_length=9)
    nuclearcharge =  models.IntegerField()
    ioncharge =  models.IntegerField()
    initialatomicstate = models.ForeignKey(Atomicstate, db_column='initialatomicstateid', related_name='+')
    finalatomicstate = models.ForeignKey(Atomicstate, db_column='finalatomicstateid', related_name='+')
    collider = models.ForeignKey(Particle, db_column='colliderid', related_name='+')
    class Meta:        
        db_table = u'v_recommendedcollisionaltransition'
        
class Datadescription(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(unique=True, max_length=30)
    class Meta:
        db_table = u't_datadescription'
        
class Tabulateddata(models.Model):
    id = models.IntegerField(primary_key=True)
    collisionaltransition = models.ForeignKey(Collisionaltransition, db_column='collisionaltransitionid', related_name='+')
    datadescription = models.ForeignKey(Datadescription, db_column='datadescriptionid', related_name='+')
    xdata = models.TextField(null=True)    
    ydata = models.TextField(null=True) 
    xdataunit = models.ForeignKey(Unit, db_column='xdataunitid', related_name='+', null=True)
    #ydataunit = models.ForeignKey(Unit, db_column='ydataunitid', related_name='+', null=True)    
    class Meta:
        db_table = u't_tabulateddata'   


class Atomiccomponent(models.Model):
    id = models.IntegerField(primary_key=True)
    atomicstate = models.ForeignKey(Atomicstate, db_column='atomicstateid', related_name='atomiccomponent')
    mixingcoefficient = models.FloatField()
    mixingclass = models.ForeignKey(Mixingclass, db_column='mixingclassid')
    termlabel = models.CharField(max_length=30)
    configuration = models.CharField(max_length=60)
    class Meta:
        db_table = u't_atomiccomponent'


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    firstname = models.CharField(unique=True, max_length=60)
    lastname = models.CharField(unique=True, max_length=60)
    class Meta:
        db_table = u't_author'

class Authorsource(models.Model):
    authorid = models.ForeignKey(Author, db_column='authorid')
    sourceid = models.ForeignKey(Source, db_column='sourceid')
    rank = models.IntegerField()
    class Meta:
        db_table = u't_authorsource'

class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    creationdate = models.DateField()
    isrecommended = models.IntegerField()
    class Meta:
        db_table = u't_dataset'

class DataseVersion(models.Model):
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
