# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from datetime import datetime

class RecordStatus():
  NEW = 0
  ACTIVE = 1
  DISABLED = 2
  RECORD_STATUS_CHOICES = (
    (NEW,		'New'),
    (ACTIVE,	'Active'),
    (DISABLED,	'Disabled'))

class UpdateStatus():
  NEW = 0
  ACTIVE = 1
  DISABLED = 2
  UPDATE_STATUS_CHOICES = (
    (NEW,		'New'),
    (ACTIVE,	'Active'),
    (DISABLED,	'Disabled'))

class SpeciesType():
  ATOM = 1
  MOLECULE = 2
  PARTICLE = 3
  SPECIES_CHOICES = (
    (ATOM,'Atom'),
    (MOLECULE,'Molecule'),
    (PARTICLE, 'Particle')
    )


class VamdcDictAtoms(models.Model):
  """
  This is a helper model and its contents provide
  a dictionary for atomic elements.
  !!! THIS IS NOT PART OF THE OFFICIAL VAMDC SPECIES DB !!!
  Loads automatically from a copy of IAEA data obtained from https://www-nds.iaea.org/relnsd/vcharthtml/VChartHTML.html
  json location https://www-nds.iaea.org/relnsd/zipper?name=jsondata
  """
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50)
  symbol = models.CharField(max_length=10)
  #element = models.CharField(max_length=10)
  nuclear_charge = models.IntegerField()
  mass_number = models.IntegerField()
  mass = models.FloatField()
  abundance = models.FloatField()
  stable = models.BooleanField(default=False)
  most_abundant = models.BooleanField(default=False)
  #mass_reference = models.IntegerField()

  class Meta:
      db_table = u'vamdc_dict_atoms'
#~
#~ class MarkupTypes():
    #~ TEXT = 1
    #~ HTML = 2
    #~ RST  = 3
    #~ LATEX= 4
    #~ MARKUP_TYPES = (
      #~ (TEXT  ,'Plain text'),
      #~ (HTML  ,'HTML'),
      #~ (RST   ,'ReStructuredText'),
      #~ (LATEX ,'LaTeX'),
      #~ )

class VamdcSpeciesTypes(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=450)
  class Meta:
    db_table = u'vamdc_species_types'

class VamdcNodes(models.Model):
  id = models.AutoField(primary_key=True)
  short_name = models.CharField(max_length=60, blank = False)
  description = models.CharField(max_length=765, blank=True)
  contact_email = models.CharField(max_length = 100, blank = False)
  ivo_identifier = models.CharField(max_length = 100, blank = False, unique=True)
  reference_url = models.CharField(max_length = 100, blank = True)
  status = models.IntegerField(default=RecordStatus.NEW, blank = False, choices=RecordStatus.RECORD_STATUS_CHOICES)
  update_status = models.IntegerField(default=UpdateStatus.NEW, blank = False, choices=UpdateStatus.UPDATE_STATUS_CHOICES)
  last_update_date = models.DateTimeField(auto_now = False, editable=False, default = datetime.now)
  #The last update by the cron job, may be thought as last seen date
  class Meta:
    db_table = u'vamdc_nodes'
    ordering = ['short_name']

  def __unicode__(self):
    return self.short_name

class VamdcSpecies(models.Model):
  id = models.CharField(max_length=120, primary_key=True)
  inchi = models.TextField()
  inchikey = models.CharField(max_length=90)
  #inchikey_duplicate_counter = models.IntegerField()#!!!WTF, why was it unique?unique=True)
  stoichiometric_formula = models.CharField(max_length=450)#Atom symbol or molecule stoichiometric_formula
  mass_number = models.IntegerField()#atomic or molecular mass
  charge = models.IntegerField()#ion charge
  species_type = models.ForeignKey(VamdcSpeciesTypes, blank = False)
  #~ species_type = models.IntegerField(default=0, blank = False, choices=SpeciesType.SPECIES_CHOICES)
  cml = models.TextField(blank=True)
  mol = models.TextField(blank=True)#Use TextField since the mol structure size may quickly become > few kB for complex organics
  imageURL = models.CharField(max_length=765, blank=True)
  smiles = models.TextField(blank=True)
  created = models.DateTimeField(auto_now = False, editable=False, default = datetime.now)
  status = models.IntegerField(default=RecordStatus.NEW, blank = False, choices=RecordStatus.RECORD_STATUS_CHOICES)
  #Disabled species are not exported to the public database
  origin_member_database = models.ForeignKey(VamdcNodes, db_column='member_databases_id')
  #The source database from which this species was originally inserted.
  #A value of zero indicates that the species information was generated or acquired from a source
  #that is not one of the VAMDC member databases.
  class Meta:
    db_table = u'vamdc_species'
    ordering = ['origin_member_database','stoichiometric_formula']

  def symbol(self):
    return self.stoichiometric_formula.replace('+','').replace('-','').replace('[0-9]','')

  def nuclear_charge(self):
    try:
      ns = VamdcDictAtoms.objects.filter(symbol=self.symbol()).values_list('nuclear_charge',flat=True)[0]
    except IndexError:
      ns=None
    return ns

  def structural_formula(self):
    try:
      sf=self.vamdcspeciesstructformulae_set.order_by('search_priority').values_list('formula',flat=True)[0]
      # replace html-tags <sub> and <sup> with latex expressions
      # this should be improved
      sf=sf.replace("<sub>","$_{").replace("</sub>","}$").replace("<sup>","$^{").replace("</sup>","}$").replace("$$","")
    except IndexError:
      sf=""

    return sf

  def structural_formula_all(self):
    try:
      sf=self.vamdcspeciesstructformulae_set.order_by('search_priority').values_list('formula',flat=True)
      # replace html-tags <sub> and <sup> with latex expressions
      # this should be improved
      #~ sf=sf.replace("<sub>","$_{").replace("</sub>","}$").replace("<sup>","$^{").replace("</sup>","}$").replace("$$","")
    except IndexError:
      sf=""

    return sf

  def trivial_name(self):
    try:
      name=self.vamdcspeciesnames_set.order_by('search_priority').values_list('name',flat=True)[0]
      # replace html-tags <sub> and <sup> with latex expressions
      # this should be improved
      name = name.replace("<sub>","$_{").replace("</sub>","}$").replace("<sup>","$^{").replace("</sup>","}$").replace("$$","")
    except IndexError:
      name=""

    return name

  def species_foreign_ids(self):
    """
    Creates a string which is formated like a dictionary with all the foreign species ids and the related database name.
    This can be used to provide the information via a comment-elelment.
    """
    speciesids = self.vamdcnodespecies_set.all()
    return_string="{"
    for sid in speciesids:
      return_string+="{%s:%s}," % (sid.database_species_id ,sid.member_database.short_name)
    return_string += "}"

    return return_string

  def comment(self):
    """
    """
    return self.species_foreign_ids()



  def __unicode__(self):
    if self.species_type==SpeciesType.ATOM:
      return "(%d)%s%d"%(self.mass_number,self.stoichiometric_formula,self.charge)
    else:
      return self.stoichiometric_formula

#Update 2015.11: conformers table was never used, put everything in inchikey exceptions
#This table is similar to the inchikey_exceptions table except that conformers are a well known exception to Standard InChIKey.
#All conformers should be added to both this table and the inchikey_exceptions table.
#class VamdcConformers(models.Model):
#    id = models.AutoField(primary_key=True)
#    species = models.ForeignKey(VamdcSpecies)
#    conformer_name = models.CharField(max_length=450)
#    class Meta:
#        db_table = u'vamdc_conformers'

#A table to store all exceptions to Standard InChIKey which will be used to differentiate species
#when Standard InChIKey is not sufficient to identify the species uniquely.
#This table was created in place of the vamdc_registry_suffixes table (which has been dropped)
#because it was not possible to agree a distinct set of reasons for departure from Standard InChIKey.
#This is because the reasons for departure from Standard InChIKey may be combined,
#and there may be other reasons for new cases for which we are not yet aware.
class VamdcInchikeyExceptions(models.Model):
    id = models.AutoField(primary_key=True)
    species = models.ForeignKey(VamdcSpecies)
    reason = models.CharField(max_length=1000)
    class Meta:
        db_table = u'vamdc_inchikey_exceptions'

class VamdcMarkupTypes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90)
    class Meta:
        db_table = u'vamdc_markup_types'

#Contains all possible names for the species.
#If the name is to be represented in HTML or reStructured Text,
#it should be added as a separate entry with the markup type set accordingly.
#This is done so that the HTML or reStructured Text value of an item is always
#unique (i.e. does not get added more than once by accident)
class VamdcSpeciesNames(models.Model):
    id = models.AutoField(primary_key=True)
    species = models.ForeignKey(VamdcSpecies)
    name = models.CharField(max_length=450)
    markup_type = models.ForeignKey(VamdcMarkupTypes)
    search_priority = models.IntegerField()
    created = models.DateTimeField()
    status = models.IntegerField(default=RecordStatus.NEW, blank = False, choices=RecordStatus.RECORD_STATUS_CHOICES)
    class Meta:
        db_table = u'vamdc_species_names'

#It was never used on practice, disable for the moment
#class VamdcSpeciesResources(models.Model):
#    id = models.AutoField(primary_key=True)
#    species = models.ForeignKey(VamdcSpecies)
#    url = models.CharField(max_length=765)
#    description = models.CharField(max_length=450)
#    search_priority = models.IntegerField()
#    created = models.DateTimeField()
#    class Meta:
#        db_table = u'vamdc_species_resources'

#Many databases express the structural formula in different ways - especially when isotopologues are involved.
#This table allows all the different versions to coexist.
#One potential problem with allowing HTML and REST formulations
#is the fact that the same HTML might exist for different ways of representing structural formula.
#E.g. C-14, (14)C and (14C) are all represented by the same HTML and reStructuredText.
#Therefore, if the name is to be represented in HTML or reStructured Text,
#it should be added as a separate row with the markup type set accordingly.
#Using a unique index on species ID, formula and markup type ensures that the plain text,
#HTML or reStructured Text value of an item is always unique
#(i.e. does not get added more than once by accident).
class VamdcSpeciesStructFormulae(models.Model):
    id = models.AutoField(primary_key=True)
    species = models.ForeignKey(VamdcSpecies)
    formula = models.CharField(max_length=450)
    markup_type = models.ForeignKey(VamdcMarkupTypes)
    #~ markup_type = models.IntegerField(VamdcMarkupTypes, blank = False)

    search_priority = models.IntegerField()
    created = models.DateTimeField()
    status = models.IntegerField(default=RecordStatus.NEW, blank = False, choices=RecordStatus.RECORD_STATUS_CHOICES)
    class Meta:
        db_table = u'vamdc_species_struct_formulae'

#A table to link the VAMDC species to the equivalent identifier in the source database.
class VamdcNodeSpecies(models.Model):
    id = models.AutoField(primary_key=True)
    species = models.ForeignKey(VamdcSpecies)
    database_species_id = models.CharField(max_length=255)#, unique=True!!!!It should not be marked unique, since collisions are possible
    member_database = models.ForeignKey(VamdcNodes)
    last_seen_dateTime = models.DateTimeField(auto_now = False, editable=False, default = datetime.now)
    database_species_name = models.ForeignKey(VamdcSpeciesNames, null=True)
    database_species_formula = models.ForeignKey(VamdcSpeciesStructFormulae, null=True)# atoms do not have formula
    deprecated = models.BooleanField(default = False)
    class Meta:
        db_table = u'vamdc_node_species'


class VamdcTopics(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    prefix = models.CharField(max_length=100)

    class Meta:
        db_table = u'vamdc_topics'

class VamdcNodesTopics(models.Model):
    id = models.AutoField(primary_key=True)
    node = models.ForeignKey(VamdcNodes)
    topic = models.ForeignKey(VamdcTopics)

    class Meta:
        db_table = u'vamdc_nodes_topics'


class VamdcSpeciesSearch(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=450)
    species = models.ForeignKey(VamdcSpecies)


    class Meta:
        db_table = u'vamdc_species_search'
