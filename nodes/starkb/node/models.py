# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from xml.sax.saxutils import escape
#import logging
#log=logging.getLogger('vamdc.tap')

class Journal(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=225)
    
    def encoded_name(self):
        return escape(self.name)
    
    class Meta:
        db_table = u't_journals'    
        
class Ion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=30, blank=True)
    symbol = models.CharField(unique=True, max_length=10)
    ionization = models.CharField(max_length=6, null=True)
    ionization_decimal = models.IntegerField(null=False)
    ion_charge = models.IntegerField(null=False)
    nuclear_charge = models.IntegerField()    
    inchi = models.CharField(max_length=100)
    inchikey = models.CharField(max_length=27)
    mass_number = models.IntegerField()    
    
    '''def ion_charge(self):
        return self.ionization_decimal - 1'''
    
    def species_id(self):
        return self.id
        
    class Meta:
        db_table = u't_ions'   
        
class Particle(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=30, blank=True)
    symbol = models.CharField(unique=True, max_length=10)
    
    def species_id(self):
        return 'P%s'%self.id
        
    class Meta:
        db_table = u't_particles'           
        
class Species(models.Model):
    id = models.IntegerField(primary_key=True)
    ion = models.ForeignKey(Ion, db_column="id_ion", null=True)
    particle = models.ForeignKey(Particle,  db_column="id_particle", null=True)    
    
    def particle_ion_id(self):
        if self.ion is not None : 
            if self.ion.name == "meanion":
                return None
            return self.ion.species_id()
        elif self.particle is not None : 
            return self.particle.species_id()
            
    def particle_ion_name(self):
        if self.ion is not None :                   
            return self.ion.name
        elif self.particle is not None : 
            return self.particle.name
    
    class Meta:
        db_table = u't_species'   

class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    target = models.ForeignKey(Species, db_column='id_target')
    has_proton = models.IntegerField()
    filename = models.TextField()
    creation_date = models.DateField()
    description = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u't_datasets'

class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    authors = models.TextField()
    publication_year = models.DecimalField(max_digits=5, decimal_places=0)
    journal = models.ForeignKey(Journal, db_column='id_journal')
    volume = models.IntegerField()
    pages = models.CharField(max_length=120)
    title = models.TextField()
    method = models.CharField(max_length=30)
    ads_reference = models.TextField(blank=True)
    doi_reference = models.TextField(blank=True)
    other_reference = models.TextField(blank=True)
    
    def encoded_title(self):
        return escape(self.title)
        
    def authors_list(self):
        return self.authors.rsplit(',')
        
    class Meta:
        db_table = u't_articles'

class ArticleDataset(models.Model):
    id = models.IntegerField(primary_key=True)
    article = models.ForeignKey(Article, db_column='id_article')
    dataset = models.ForeignKey(Dataset, db_column='id_dataset')
    class Meta:
        db_table = u't_articles_datasets'


class DatasetCollider(models.Model):
    dataset = models.ForeignKey(Dataset, db_column='id_dataset')
    species = models.ForeignKey(Species, db_column='id_species')
    class Meta:
        db_table = u't_datasets_colliders'
        

class Level(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='id_dataset')
    config = models.CharField(unique=True, max_length=60)
    term = models.CharField(unique=True, max_length=36)
    parity = models.CharField(max_length=4)
    coupling = models.CharField(max_length=4)
    J = models.CharField(unique=True, max_length=15, blank=True)       
    LS_L = models.IntegerField(null=True)    
    LS_S = models.FloatField(null=True)    
    LS_multiplicity = models.IntegerField(null=True)    
    jK_K = models.FloatField(null=True)    
    jK_J1 = models.FloatField(null=True)   
    jK_S2 = models.FloatField(null=True) 
    jj_j1 = models.FloatField(null=True)   
    jj_j2 = models.FloatField(null=True)   
    
    def j_asFloat(self):
        #add .0 to "1/2" or "3/2" to get float value
        if(self.J is not None) :
            return eval(self.J+".0")
        return None
        
    def getjj(self):
      return [self.jj_j1, self.jj_j2]
        
    def get_int_parity(self):
        if self.parity == 'odd' :
            return 1
        else:
            return 2
      
    def encoded_config(self):
      """
        some data files contains <> characters in this field
        not correct when exporting in xml
      """
      return self.config.replace("<", "&lt;").replace(">", "&gt;")
        
    class Meta:
        db_table = u't_levels'  
        
        
class Transition(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='id_dataset')
    target = models.ForeignKey(Species, db_column='id_species')
    lower_level = models.ForeignKey(Level, db_column='lower_level', related_name='lower_level')
    upper_level = models.ForeignKey(Level, db_column='upper_level', related_name='upper_level')
    wavelength = models.FloatField()
    temperature = models.FloatField()
    temperatureid = models.IntegerField(db_column='id_temperature')
    density = models.FloatField()
    inchikey = models.CharField(max_length=27)
    class Meta:
        db_table = u'v_transitionsvamdc'    

  
class Transitiondata(models.Model):
    id = models.IntegerField(primary_key=True)
    transition = models.ForeignKey(Transition, db_column='id_transition')
    density = models.FloatField(unique=True)
    c = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u't_transitiondata'
        
        
class FitCoefficient(models.Model):
    id = models.IntegerField(primary_key=True)
    transitiondata = models.ForeignKey(Transitiondata, db_column='id_transitiondata')
    species = models.ForeignKey(Species, db_column='id_species')
    a0 = models.FloatField(null=True, blank=True)
    a1 = models.FloatField(null=True, blank=True)
    a2 = models.FloatField(null=True, blank=True)
    b0 = models.FloatField(null=True, blank=True)
    b1 = models.FloatField(null=True, blank=True)
    b2 = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u't_fitcoefficients'

        
class Temperature(models.Model):
    id = models.IntegerField(primary_key=True)
    transitiondata = models.ForeignKey(Transitiondata, db_column='id_transitiondata')
    temperature = models.IntegerField(unique=True)
    a = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u't_temperatures'       


class TemperatureCollider(models.Model):
    id = models.IntegerField(primary_key=True)
    #~ temperature = models.ForeignKey(Temperature, db_column='id_temperature', unique=True)
    temperature = models.OneToOneField(
      Temperature,
      db_column='id_temperature',
      #~ related_name='temperature_id'
    )
    species = models.ForeignKey(Species, db_column='id_species')
    n_w = models.CharField(max_length=24, blank=True)
    w = models.FloatField(null=True, blank=True)
    n_d = models.CharField(max_length=24, blank=True)
    d = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u't_temperatures_colliders'
