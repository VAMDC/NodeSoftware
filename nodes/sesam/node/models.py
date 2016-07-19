# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
import util_models as util_models
#from django.core.exceptions import DoesNotExist

import logging

log = logging.getLogger("vamdc.node.queryfu")

class Molecule(models.Model):
    id = models.IntegerField(primary_key=True)
    ordinary_structural_formula = models.CharField(max_length=60)
    stoichiometric_formula = models.CharField(max_length=60)
    inchikey = models.CharField(max_length=81)
    inchi = models.CharField(max_length=30)
    class Meta:
        db_table = u't_molecule'
        
class Sourcecategory(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(unique=True, max_length=45)
    class Meta:
        db_table = u't_sourcecategory'  
        
class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    address = models.TextField(null=True)
    class Meta:
        db_table = u't_author'
        
class Source(models.Model):
    id = models.IntegerField(primary_key=True)
    sourcecategory = models.ForeignKey(Sourcecategory, db_column='id_sourcecategory')
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
        authorsources = Authorsource.objects.filter(source=self)
        for authorsource in authorsources:
            names.append(authorsource.author.name)
        return names
        
    class Meta:
        db_table = u't_source'   
    
        
class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    molecule =  models.ForeignKey(Molecule, db_column='id_molecule')
    source = models.ForeignKey(Source, db_column='id_source')
    title = models.CharField(max_length=255)
    class Meta:
        db_table = u't_dataset'      


class Authorsource(models.Model):
    id = models.IntegerField(primary_key=True)    
    author = models.ForeignKey(Author, db_column='id_author')
    source = models.ForeignKey(Source, db_column='id_source')
    rank = models.IntegerField()
    class Meta:
        db_table = u't_authorsource'    


class Molecularstate(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='id_dataset')
    fully_assigned = models.IntegerField()
    energy = models.FloatField(db_column='state_energy')
    total_statistical_weight = models.IntegerField()
    nuclear_statistical_weight = models.FloatField()
    class Meta:
        db_table = u't_molecularstate'

class Case(models.Model):
    id = models.IntegerField(primary_key=True)
    molecularstate = models.ForeignKey(Molecularstate, db_column='id_molecularstate')
    elec_state_label = models.CharField(max_length=9, blank=True)
    j = models.IntegerField(null=True, db_column='J', blank=True) # Field name made lowercase.
    parity = models.CharField(max_length=3, blank=True)
    f = models.FloatField(null=True, db_column='F', blank=True) # Field name made lowercase.
    r = models.IntegerField(null=True, blank=True)
    
    def getSubCase(self):
        dcs = self.__getDcs()
        if dcs is None :
            return self.__getHundb()
        else :
            return dcs        
        
    def __getDcs(self):
        try:
            return Dcscase.objects.get(case = self.id)
        except Exception:        
            return None
        
    def __getHundb(self):
        try:
            return Hundbcase.objects.get(case = self.id)
        except Exception:        
            return None    
    
    class Meta:
        db_table = u't_case'

class Dcscase(models.Model):
    id = models.IntegerField(primary_key=True)
    case = models.ForeignKey(Case, db_column='id_case')
    v = models.IntegerField()
    f1 = models.FloatField(null=True, db_column='F1', blank=True) # Field name made lowercase.
    as_sym = models.CharField(max_length=3, blank=True)
    name = 'dcs'
    
    def __getattr__(self, name):
        return None
    
    class Meta:
        db_table = u't_dcscase'

class Hundbcase(models.Model):
    id = models.IntegerField(primary_key=True)
    case = models.ForeignKey(Case, db_column='id_case')
    elec_inv = models.CharField(max_length=3, blank=True)
    elec_refl = models.CharField(max_length=3, blank=True)
    lambda_field = models.IntegerField(null=True, db_column='lambda', blank=True) # Field renamed because it was a Python reserved word.
    s = models.FloatField(null=True, db_column='S', blank=True) # Field name made lowercase.
    v = models.IntegerField()
    n = models.IntegerField(null=True, db_column='N', blank=True) # Field name made lowercase.
    spin_component_label = models.IntegerField(null=True, blank=True)
    f1 = models.FloatField(null=True, db_column='F1', blank=True) # Field name made lowercase.
    kronig_parity = models.CharField(max_length=3, blank=True)
    as_sym = models.CharField(max_length=3, blank=True)
    name = 'hundb'
    
    def __getattr__(self, name):
        return None
    
    class Meta:
        db_table = u't_hundbcase'

class Radiativetransition(models.Model):
    id = models.IntegerField(primary_key=True)
    dataset = models.ForeignKey(Dataset, db_column='id_dataset')
    molecule = models.ForeignKey(Molecule, db_column='id_molecule')
    ordinarystructuralformula = models.CharField(max_length=20, db_column='ordinary_structural_formula')
    source = models.ForeignKey(Source, db_column='id_source')
    upperstate = models.ForeignKey(Molecularstate, db_column='id_upperstate', related_name="upperstate")
    lowerstate = models.ForeignKey(Molecularstate, db_column='id_lowerstate', related_name="lowerstate")
    wavelength = models.FloatField()
    wavenumber_observed = models.FloatField()
    wavenumber_calculated = models.FloatField()
    oscillator_strength = models.FloatField()
    transition_probability = models.FloatField()
    inchikey = models.CharField(max_length=81)
    
    def getWavenumbers(self):      
        result = []        
        if self.wavenumber_observed is not None :
            result.append(self.wavenumber_observed)
        if self.wavenumber_calculated is not None : 
            result.append(self.wavenumber_calculated)
        return result
        
    def getWavenumberComments(self):
        result = []
        if self.wavenumber_observed is not None :
            result.append("Observed wavenumber")
        if self.wavenumber_calculated is not None : 
            result.append("Calculated wavenumber")
        return result
        
    def getWavenumberMethods(self):        
        result = []                
        m = util_models.Methods()        
        if self.wavenumber_observed is not None :
            result.append(m.getMethodFromDict('observed').id)     
        if self.wavenumber_calculated is not None :   
            result.append(m.getMethodFromDict('theory').id)      
        return result    
    
    class Meta:
        db_table = u'v_radiativetransition'

