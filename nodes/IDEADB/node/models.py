"""
This module defines the database schema of the node.

Each model class defines a table in the database. The fields define the columns of this table.

"""

# library import 
from django.db.models import *
from django.core.exceptions import ValidationError
from vamdctap import bibtextools

import re
import datetime

from node.inchivalidation import inchi2inchikey, inchikey2inchi, inchi2chemicalformula
from node.chemlib import chemicalformula2nominalmass, checkatoms, atommasses, add_charge_layer

#we define the regex object for chemical formulas here, as it is used in two different functions
re = re.compile('^([A-Z]{1}[a-z]{0,2}[0-9]{0,3})+$')

#define validations for CAS and chemical formulas

def validate_CAS(cas):
    sum=0
    cas_arr = cas.split('-')
    if len(cas_arr) < 3:
        raise ValidationError(u'%s is not a valid CAS-number!' % cas)
    length = len(cas_arr[0])+2
    for x in cas_arr[0]:
        sum = sum + length*int(x)
        length = length - 1
    sum = sum + 2 * int(cas_arr[1][0]) + int(cas_arr[1][1])
    if sum % 10 != int(cas_arr[2]):
        raise ValidationError(u'%s is not a valid CAS-number!' % cas)

def validate_chemical_formula(chemical_formula):
    """ checks chemical formalae for plausibility """

    # first we check if the formula seems like a chemical formula
    m = re.match(chemical_formula)
    if m is None:
        raise ValidationError(u'%s does not seem to be a chemical formula' % chemical_formula)

    # we outsource the checking of individual atoms to the chemlib
    result = checkatoms(chemical_formula)
    if result != 0:
        raise ValidationError(u'%s is not an atom' % result)

def validate_name(name):
    m = re.match(name) 
    if m is not None:
        raise ValidationError(u'%s seems to be a chemical formula. Please use a normal name or leave it blank.' % name)

#start defining the classes

class Author(Model):
    firstname = CharField(max_length=30)
    lastname = CharField(max_length=30)
    middlename = CharField(max_length=30, blank=True)
    email = EmailField(max_length=254, blank=True)
    def __str__(self):
        if self.middlename != '':
            return u'%s, %s %s'%(self.lastname, self.firstname, self.middlename)
        else:
            return u'%s, %s'%(self.lastname, self.firstname)

class Experiment(Model):
    name = CharField(max_length=10)
    def __str__(self):
        return u'%s'%(self.name)

class Species(Model):
    name = CharField(max_length=100, db_index=True, verbose_name='Common Name (e.g. Water for H2O)', blank = True, validators=[validate_name])
    chemical_formula = CharField(max_length=40, db_index=True, verbose_name='Chemical Formula', default = '', validators=[validate_chemical_formula])
    mass = PositiveIntegerField(db_index=True, verbose_name='Nominal Mass')
    isotope = BooleanField(verbose_name='Tick, if this is the most abundant isotope', default = True)
    nuclear_charge = PositiveSmallIntegerField(verbose_name='Number of Protons', blank = True, null = True)
    inchi_neutral = CharField(max_length=300,db_index=True,verbose_name='InChI neutral', blank = True)
    inchi_negative = CharField(max_length=300,verbose_name='InChI anion', blank = True)
    inchi_positive = CharField(max_length=300,verbose_name='InChI cation', blank = True)
    inchikey_neutral = CharField(max_length=27, db_index=True, verbose_name='InChI-Key neutral', blank = True)
    inchikey_negative = CharField(max_length=27, verbose_name='InChI-Key anion', blank = True)
    inchikey_positive = CharField(max_length=27, verbose_name='InChI-Key cation', blank = True)
    cas = CharField(max_length=12,verbose_name='CAS-Number', blank = True, validators = [validate_CAS])
    molecule = BooleanField(verbose_name='Tick, if this is a molecule')
    # defines some optional meta-options for viewing and storage
    def __str__(self):
        if self.name != '':
            return u'%s (%s)'%(self.name, self.chemical_formula)
        else:
            return u'%s'%(self.chemical_formula)

    def clean(self):
        # we have to run this validator here again, because
        # chemicalformula2nominalmass expects proper formulae
        # django runs the validators _after_ this clean function

        validate_chemical_formula(self.chemical_formula)
        if self.isotope is True:
            if self.mass != chemicalformula2nominalmass(self.chemical_formula):
                raise ValidationError(u'Nominal mass and chemical formula are not compatible.')


        # check whether the chemical formula and the information about molecule status fit each other
        if self.molecule is False:
            if self.chemical_formula not in atommasses:
                raise ValidationError(u'%s seems not to be an atom. Please tick whether this is a molecule.' % self.chemical_formula)
        else:
            if self.chemical_formula in atommasses:
                raise ValidationError(u'%s seems to be an atom. Please tick whether this is a molecule or an atom.' % self.chemical_formula)

        #check if either inchi or inchikey are there and either complete the other one or verify
        if self.inchi_neutral == '':
            if self.inchikey_neutral != '':
                tmpinchi = inchikey2inchi(self.inchikey_neutral)
                if tmpinchi:
                    self.inchi = tmpinchi
                else:
                    raise ValidationError(u'No chemical compound found for this InChI-Key.')
        else:
            #check if the given inchi has the InChI= in the beginning
            #additionally check for Standard-InChI

            if not self.inchi_neutral.startswith('InChI='):
                self.inchi_neutral = 'InChI=' + self.inchi_neutral
            if not self.inchi_neutral.startswith('InChI=1S'):
                raise ValidationError(u'InChI %s is not a Standard-InChI (starts with 1S)' % self.inchi)

            #get the rest

            if self.inchikey_neutral != '':
                inchikeycheck = inchi2inchikey(self.inchi_neutral)
                if inchikeycheck != self.inchikey_neutral:
                    raise ValidationError(u'The given InChI and neutral InChI-Key are not compatible.')
            else:
                tmpinchikey = inchi2inchikey(self.inchi_neutral)
                if tmpinchikey:
                    self.inchikey_neutral = tmpinchikey
                else:
                    raise ValidationError(u'Not a valid InChI-Key.')

            if self.chemical_formula != inchi2chemicalformula(self.inchi_neutral):
                raise ValidationError(u'InChI %s is not compatible with the stochiometric formula %s.' % (self.inchi_neutral, self.chemical_formula))

        #we check if we already have a species with same chem formula, mass and isotope-status
        sp_search = Species.objects.filter(chemical_formula__exact=self.chemical_formula).filter(mass__exact=self.mass).filter(isotope__exact=self.isotope)

        #exclude this very instance
        sp_search = sp_search.exclude(id__exact=self.id)

        if len(sp_search) > 0:
            #indeed we do
            #in this case they should be isomeres and therefore have a different inchi
            if self.inchi_neutral in sp_search.values_list('inchi_neutral'):
                raise ValidationError(u'A species with this chemical formula and InChI already exists in the database')
            if self.inchi_neutral == '':
                raise ValidationError(u'Isomeres need to be distinguished via their InChI')

        # finally fill out the other inchis
        if self.inchi_neutral is not '':
            self.inchi_negative = add_charge_layer(self.inchi_neutral, -1)
            self.inchi_positive = add_charge_layer(self.inchi_neutral, 1)
            self.inchikey_negative = inchi2inchikey(self.inchi_negative)
            self.inchikey_positive = inchi2inchikey(self.inchi_positive)

    class Meta:
        db_table = u'species'
        verbose_name_plural = u'Species'
        ordering = ['chemical_formula','name']

class Source(Model):
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
    number = CharField(max_length=6, blank=True)
    volume = CharField(max_length=6)
    doi = CharField(max_length=100, verbose_name='DOI', blank=True)
    pagestart = CharField(max_length=7, verbose_name='Starting Page')
    pageend = CharField(max_length=7, verbose_name='Ending Page')
    url = URLField(max_length=200, blank=True)
    title = CharField(max_length=500)
    type = CharField(max_length=17, default='journal', choices=SOURCETYPE_CHOICES)
    #define a useful unicode-expression:
    def __str__(self):
        return u'%s, %s'%(self.title, self.year)

class Energyscan(Model):
    Y_UNITS_CHOICES = (
        ('1/s', '1/s'),
        ('cm2', 'cm2'),
        ('m2', 'm2'),
        ('unitless', 'unitless'),
    )

    NEUTRAL = 0
    ANIONIC = -1
    CATIONIC = 1
    CHARGE_CHOICES = (
        (NEUTRAL, 'Neutral'),
        (ANIONIC, 'Anionic'),
        (CATIONIC, 'Cationic'),
    )

    ELAT = 'elat'
    DISS = 'diss'
    IONI = 'ioni'
    PC_CHOICES = (
        (ELAT, 'Electron Attachment'),
        (DISS, 'Dissociation'),
        (IONI, 'Ionization'),
    )

    species = ForeignKey(Species, related_name='energyscan_species')
    origin_species = ForeignKey(Species, related_name='energyscan_origin_species')
    product_charge = IntegerField(default = ANIONIC, choices = CHARGE_CHOICES)
    process_code = CharField(default = ELAT, choices = PC_CHOICES, max_length=4)
    process_code_2 = CharField(choices = PC_CHOICES, blank = True, max_length=4)
    source = ForeignKey(Source)
    experiment = ForeignKey(Experiment)
    energyscan_data = TextField(verbose_name='Paste data from Origin in this field')
    y_units = CharField(max_length = 3, verbose_name='Please choose units for y-axis', default='1/s', choices=Y_UNITS_CHOICES)
    productiondate = DateField(verbose_name='Production Date')
    comment = TextField(blank = True, max_length = 2000, verbose_name = 'Comment (max. 2000 chars.)')
    energyresolution = DecimalField(max_digits = 4, decimal_places = 3, verbose_name='Energy Resolution of the Experiment in eV')
    lastmodified = DateTimeField(auto_now = True)
    numberofpeaks = IntegerField(blank = True, verbose_name = 'Number of peaks visible (no shoulder structures)')

    #define a useful unicode-expression:
    def __unicode__(self):
        return u'ID %s: %s from %s'%(self.id, self.species, self.origin_species)

    def clean(self):
        #we check for -- in the numerical data, because Origin occasionally produces those
        if self.energyscan_data.find('--') is not -1:
            raise ValidationError(u'Energyscan data contains -- most likely due to empty lines in the Origin table.')

class Resonance(Model):
    energyscan = ForeignKey(Energyscan)
    species = ForeignKey(Species, related_name='resonance_species')
    origin_species = ForeignKey(Species, related_name='resonance_origin_species')
    source = ForeignKey(Source)
    energy = DecimalField(max_digits=5, decimal_places=2)
    width = DecimalField(max_digits=3, decimal_places=2)

    #define a useful unicode-expression:
    def __str__(self):
        return u'ID:%s: %s eV for %s from %s'%(self.id, self.energy, self.species, self.origin_species)


class Massspec(Model):
    species = ForeignKey(Species, related_name='massspec_species')
    source = ForeignKey(Source)
    energy = DecimalField(max_digits=5, decimal_places=2)
    massspec_data = TextField()

    #define a useful unicode-expression:
    def __str__(self):
        return u'ID:%s %s at %s'%(self.id, self.species, self.energy)
