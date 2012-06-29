"""
This module defines the database schema of the node.

Each model class defines a table in the database. The fields define the columns of this table.

"""

# library import 
from django.db.models import *
from django.core.exceptions import ValidationError
from vamdctap import bibtextools

import re

from inchivalidation import inchi2inchikey, inchikey2inchi, inchi2chemicalformula

#we define the regex object for chemical formulas here, as it is used in two different functions
re = re.compile('^([A-Z]{1}[a-z]{0,2}[0-9]{0,3})+$')

#define validations for CAS and chemical formulas

def validate_CAS(cas):
    sum=0
    cas_arr = cas.split('-')
    length = len(cas_arr[0])+2
    for x in cas_arr[0]:
        sum = sum + length*int(x)
        length = length - 1
    sum = sum + 2 * int(cas_arr[1][0]) + int(cas_arr[1][1])
    if sum % 10 != int(cas_arr[2]):
        raise ValidationError(u'%s is not a valid CAS-number!' % cas)

def validate_chemical_formula(chemical_formula):
    m = re.match(chemical_formula)
    if m is None:
        raise ValidationError(u'%s does not seem to be a chemical formula' % chemical_formula)

def validate_name(name):
    m = re.match(name) 
    if m is not None:
        raise ValidationError(u'%s seems to be a chemical formula. Please use a normal name or leave it blank.' % name)

#start defining the classes

class Author(Model):
    firstname = CharField(max_length=20)
    lastname = CharField(max_length=20)
    email = EmailField(max_length=254,blank=True)
    def __unicode__(self):
        return u'%s, %s'%(self.lastname,self.firstname)

class Experiment(Model):
    name = CharField(max_length=10)
    def __unicode__(self):
        return u'%s'%(self.name)

class Species(Model):
    #id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    name = CharField(max_length=40, db_index=True, verbose_name='Common Name (e.g. Water for H2O)',blank=True,validators=[validate_name])
    chemical_formula = CharField(max_length=40, db_index=True, verbose_name='Chemical Formula', default='',validators=[validate_chemical_formula])
    mass = PositiveIntegerField(db_index=True)
    nuclear_charge = SmallIntegerField(max_length=3,verbose_name='Number of Protons')
    inchi = CharField(max_length=300,db_index=True,verbose_name='InChI',blank=True)
    inchikey = CharField(max_length=27,db_index=True,verbose_name='InChI-Key',blank=True)
    cas = CharField(max_length=12,verbose_name='CAS-Number',blank=True,validators=[validate_CAS])
    molecule = BooleanField(verbose_name='Tick, if this is a molecule')
    # defines some optional meta-options for viewing and storage
    def __unicode__(self):
        if self.name != '':
            return u'%s (%s)'%(self.name,self.chemical_formula)
        else:
            return u'%s'%(self.chemical_formula)

    def clean(self):
        #check if either inchi or inchikey are there and either complete the other one or verify
        if self.inchi == '':
            if self.inchikey != '':
                tmpinchi = inchikey2inchi(self.inchikey)
                if tmpinchi:
                    self.inchi = tmpinchi
                else:
                    raise ValidationError(u'No chemical compound found for this InChI-Key.')
        else:
            #check if the given inchi has the InChI= in the beginning
            #additionally check for Standard-InChI

            if not self.inchi.startswith('InChI='):
                self.inchi = 'InChI=' + self.inchi
            if not self.inchi.startswith('InChI=1S'):
                raise ValidationError(u'InChI %s is not a Standard-InChI (starts with 1S)' % self.inchi)

            #get the rest

            if self.inchikey != '':
                inchikeycheck = inchi2inchikey(self.inchi)
                if inchikeycheck != self.inchikey:
                    raise ValidationError(u'The given InChI and InChI-Key are not compatible.')
            else:
                tmpinchikey = inchi2inchikey(self.inchi)
                if tmpinchikey:
                    self.inchikey = tmpinchikey
                else:
                    raise ValidationError(u'Not a valid InChI-Key.')

            if self.chemical_formula != inchi2chemicalformula(self.inchi):
                raise ValidationError(u'InChI %s is not compatible with the stochiometric formula %s.' % (self.inchi, self.chemical_formula))

    class Meta:
        db_table = u'species'
        verbose_name_plural = u'Species'

class Source(Model):
    #id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    SOURCETYPE_CHOICES = (
        ('book', 'Book'),
        ('database', 'Database'),
        ('journal', 'Journal'),
        ('preprint', 'Preprint'),
        ('private communication', 'Private Communication'),
        ('proceeding', 'Proceeding'),
        ('report', 'Report'),
        ('thesis', 'Thesis'),
        ('vamdc node', 'VAMDC Node'),
    )
    authors = ManyToManyField(Author) 
    journal = CharField(max_length=200)
    year = CharField(max_length=4)
    number = CharField(max_length=6,blank=True)
    volume = CharField(max_length=6)
    doi = CharField(max_length=40,verbose_name='DOI',blank=True)
    pagestart = CharField(max_length=5,verbose_name='Starting Page')
    pageend = CharField(max_length=5,verbose_name='Ending Page')
    url = URLField(verify_exists=False, max_length=200,blank=True)
    title = CharField(max_length=500)
    type = CharField(max_length=17,default='journal',choices=SOURCETYPE_CHOICES)
    #define a useful unicode-expression:
    def __unicode__(self):
        return u'%s, %s'%(self.title,self.year)

class Energyscan(Model):
    #id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    species = ForeignKey(Species, related_name='energyscan_species')
    origin_species = ForeignKey(Species, related_name='energyscan_origin_species')
    source = ForeignKey(Source)
    experiment = ForeignKey(Experiment)
    energyscan_data = TextField(verbose_name='Paste data from Origin in this field')
    productiondate = DateField(verbose_name='Production Date')
    comment = TextField(blank=True,max_length=2000,verbose_name='Comment (max. 2000 chars.)')
    energyresolution = DecimalField(max_digits=3, decimal_places=2,verbose_name='Energy Resolution of the Experiment in eV')
    #define a useful unicode-expression:
    def __unicode__(self):
        return u'ID %s: %s from %s'%(self.id,self.species,self.origin_species)

class Resonance(Model):
    #id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    energyscan = ForeignKey(Energyscan)
    species = ForeignKey(Species, related_name='resonance_species')
    origin_species = ForeignKey(Species, related_name='resonance_origin_species')
    source = ForeignKey(Source)
    energy = DecimalField(max_digits=5, decimal_places=2)
    width = DecimalField(max_digits=3, decimal_places=2)

    #define a useful unicode-expression:
    def __unicode__(self):
        return u'ID:%s: %s eV for %s from %s'%(self.id,self.energy,self.species,self.origin_species)


class Massspec(Model):
    #id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    species = ForeignKey(Species, related_name='massspec_species')
    source = ForeignKey(Source)
    energy = DecimalField(max_digits=5, decimal_places=2)
    massspec_data = TextField()

    #define a useful unicode-expression:
    def __unicode__(self):
        return u'ID:%s %s at %s'%(self.id,self.species,self.energy)
