# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db.models import *

class Biblio(Model):
    id = IntegerField(primary_key=True)
    main_author = CharField(max_length=255L)
    authors = TextField(blank=True)
    year = IntegerField()
    title = CharField(max_length=255L, blank=True)
    doi = CharField(max_length=255L, blank=True)
    entity_type = CharField(max_length=30L)
    class Meta:
        db_table = 'biblio'
        
    def get_Journal(self):
       if(hasattr(self, 'journal')):
           return self.journal
       return None

    def get_Book(self):
       if(hasattr(self, 'book')):
           return self.book
       return None

class BiblioBook(Model):
    id = IntegerField(primary_key=True)
    biblio = OneToOneField(
        Biblio,
        primary_key=True,
        related_name='book'
    )
    booktitle = CharField(max_length=255L, blank=True)
    pages = CharField(max_length=255L, blank=True)
    editor = CharField(max_length=255L, blank=True)
    publisher = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'biblio_book'

class BiblioJournal(Model):
    id = IntegerField(primary_key=True)
    biblio = OneToOneField(
        Biblio,
        primary_key=True,
        related_name='journal'
    )
    page = CharField(max_length=30L, blank=True)
    journal = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'biblio_journal'

class BiblioThesis(Model):
    id = IntegerField(primary_key=True)
    biblio = OneToOneField(
        Biblio,
        primary_key=True,
        related_name='thesis'
    )
    num_thesis = CharField(max_length=255L)
    school = CharField(max_length=255L)
    month = CharField(max_length=255L)
    class Meta:
        db_table = 'biblio_thesis'

class Channel(Model):
    id = IntegerField(primary_key=True)
    reaction = ForeignKey('Reaction', null=True, blank=True)
    review_status = CharField(max_length=255L)
    status = IntegerField(null=True, blank=True)
    old_reaction_id = IntegerField(null=True, blank=True)
    old_id = IntegerField(null=True, blank=True)
    product_string = CharField(max_length=255L)
    three_body_reactant_string = CharField(max_length=255L, blank=True)
    slug = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'channel'
    def isOnlyPlaneto(self):
        bimos = CvBimo.objects.all().filter(channel=self)
        cosmics = CvCosmic.objects.all().filter(channel=self)
        termos = CvTermo.objects.all().filter(channel=self)
        for cv in bimos:
            if cv.application == "Astro":
                return False
        for cv in cosmics:
            if cv.application == "Astro":
                return False
        for cv in termos:
            if cv.application == "Astro":
                return False
        return True



class CvBimo(Model):
    id = IntegerField(primary_key=True)
    channel = ForeignKey(Channel, null=True, blank=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    formula = ForeignKey('Formula', null=True, blank=True)
    alpha = FloatField()
    beta = FloatField()
    gamma = FloatField()
    f0 = FloatField()
    g = FloatField()
    tmin = IntegerField()
    tmax = IntegerField()
    type_uncert_f = CharField(max_length=255L, blank=True)
    type_uncert_g = CharField(max_length=255L, blank=True)
    expertize = IntegerField()
    justification = TextField(blank=True)
    origin = CharField(max_length=255L)
    database_name = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    add_justification = TextField(blank=True)
    status = IntegerField()
    is_trash = IntegerField(null=True, blank=True)
    trash_comment = TextField(blank=True)
    application = CharField(max_length=255L, blank=True)
    createdat = DateTimeField(null=True, db_column='createdAt', blank=True) # Field name made lowercase.
    updatedat = DateTimeField(null=True, db_column='updatedAt', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'cv_bimo'

class CvCosmic(Model):
    id = IntegerField(primary_key=True)
    channel = ForeignKey(Channel, null=True, blank=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    formula = ForeignKey('Formula', null=True, blank=True)
    alpha = FloatField()
    beta = FloatField()
    gamma = FloatField()
    f0 = FloatField()
    g = FloatField()
    uv_field = CharField(max_length=255L, blank=True)
    type_uncert_f = CharField(max_length=255L, blank=True)
    type_uncert_g = CharField(max_length=255L, blank=True)
    expertize = IntegerField()
    justification = TextField(blank=True)
    origin = CharField(max_length=255L)
    database_name = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    add_justification = TextField(blank=True)
    status = IntegerField()
    is_trash = IntegerField()
    trash_comment = TextField(blank=True)
    application = CharField(max_length=255L, blank=True)
    createdat = DateTimeField(null=True, db_column='createdAt', blank=True) # Field name made lowercase.
    updatedat = DateTimeField(null=True, db_column='updatedAt', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'cv_cosmic'

class CvSurface(Model):
    id = IntegerField(primary_key=True)
    channel = ForeignKey(Channel, unique=True, null=True, blank=True)
    application = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'cv_surface'

class CvTermo(Model):
    id = IntegerField(primary_key=True)
    channel = ForeignKey(Channel, null=True, blank=True)
    formula = ForeignKey('Formula', null=True, blank=True)
    k0 = ForeignKey('K0Value', unique=True, null=True, blank=True)
    kinf = ForeignKey('KinfValue', unique=True, null=True, blank=True)
    fc = ForeignKey('FcValue', unique=True, null=True, blank=True)
    tmin = IntegerField()
    tmax = IntegerField()
    expertize = IntegerField()
    status = IntegerField()
    is_trash = IntegerField()
    trash_comment = TextField(blank=True)
    application = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'cv_termo'


class DesorptionEnergy(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    species = ForeignKey('Species', null=True, blank=True)
    emean = FloatField(null=True, blank=True)
    uncert_emean = FloatField(null=True, blank=True)
    emin = FloatField(null=True, blank=True)
    uncert_emin = FloatField(null=True, blank=True)
    emax = FloatField(null=True, blank=True)
    uncert_emax = FloatField(null=True, blank=True)
    nu = FloatField(null=True, blank=True)
    uncert_nu = FloatField(null=True, blank=True)
    method = CharField(max_length=255L, blank=True)
    origin = CharField(max_length=255L, blank=True)
    database_name = CharField(max_length=255L, blank=True)
    surface_type = CharField(max_length=255L, blank=True)
    expertize = IntegerField()
    ref = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    order_factor = FloatField(null=True, blank=True)
    class Meta:
        db_table = 'desorption_energy'

class DiffusionEnergy(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    species = ForeignKey('Species', null=True, blank=True)
    e_value = FloatField(null=True, blank=True)
    uncert_e = FloatField(null=True, blank=True)
    nu = FloatField(null=True, blank=True)
    uncert_nu = FloatField(null=True, blank=True)
    method = CharField(max_length=255L, blank=True)
    origin = CharField(max_length=255L, blank=True)
    database_name = CharField(max_length=255L, blank=True)
    surface_type = CharField(max_length=255L, blank=True)
    diffusion_type = CharField(max_length=255L, blank=True)
    expertize = IntegerField()
    description = TextField(blank=True)
    createdat = DateField(null=True, db_column='createdAt', blank=True) # Field name made lowercase.
    updatedat = DateField(null=True, db_column='updatedAt', blank=True) # Field name made lowercase.
    class Meta:
        db_table = 'diffusion_energy'

class DipoleMoment(Model):
    id = IntegerField(primary_key=True)
    species = ForeignKey('Species', null=True, blank=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    value = FloatField()
    uncert = FloatField(null=True, blank=True)
    type_uncert = CharField(max_length=30L, blank=True)
    justification = TextField(blank=True)
    origin = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    database_name = CharField(max_length=255L, blank=True)
    comment = TextField(blank=True)
    ref = CharField(max_length=255L, blank=True)
    expertize = IntegerField()
    class Meta:
        db_table = 'dipole_moment'

class Element(Model):
    id = IntegerField(primary_key=True)
    symbol = CharField(max_length=20L)
    name = CharField(max_length=100L, blank=True)
    atomic = IntegerField(null=True, blank=True)
    mass = FloatField(null=True, blank=True)
    class Meta:
        db_table = 'element'

class Enthalpy(Model):
    id = IntegerField(primary_key=True)
    species = ForeignKey('Species', null=True, blank=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    value = FloatField()
    temperature = FloatField()
    uncert = FloatField(null=True, blank=True)
    type_uncert = CharField(max_length=30L, blank=True)
    justification = TextField(blank=True)
    origin = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    database_name = CharField(max_length=255L, blank=True)
    comment = TextField(blank=True)
    ref = CharField(max_length=255L, blank=True)
    expertize = IntegerField()
    class Meta:
        db_table = 'enthalpy'

class FcValue(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    value = FloatField()
    f0 = FloatField()
    type_uncert = CharField(max_length=255L, blank=True)
    origin = CharField(max_length=255L)
    database_name = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    class Meta:
        db_table = 'fc_value'

class Formula(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=255L)
    math = TextField(blank=True)
    image = CharField(max_length=255L, blank=True)
    units = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'formula'



class K0Value(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    formula = ForeignKey(Formula, null=True, blank=True)
    alpha = FloatField()
    beta = FloatField()
    gamma = FloatField()
    f0 = FloatField()
    g = FloatField()
    type_uncert = CharField(max_length=255L, blank=True)
    origin = CharField(max_length=255L)
    database_name = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    class Meta:
        db_table = 'k0_value'

class KinfValue(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    formula = ForeignKey(Formula, null=True, blank=True)
    alpha = FloatField()
    beta = FloatField()
    gamma = FloatField()
    f0 = FloatField()
    g = FloatField()
    type_uncert = CharField(max_length=255L, blank=True)
    origin = CharField(max_length=255L)
    database_name = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    class Meta:
        db_table = 'kinf_value'




class Polarizability(Model):
    id = IntegerField(primary_key=True)
    species = ForeignKey('Species', null=True, blank=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    value = FloatField()
    uncert = FloatField(null=True, blank=True)
    type_uncert = CharField(max_length=30L, blank=True)
    definition = CharField(max_length=255L, blank=True)
    justification = TextField(blank=True)
    origin = CharField(max_length=255L, blank=True)
    method = CharField(max_length=255L, blank=True)
    database_name = CharField(max_length=255L, blank=True)
    comment = TextField(blank=True)
    ref = CharField(max_length=255L, blank=True)
    expertize = IntegerField()
    class Meta:
        db_table = 'polarizability'

class Product(Model):
    id = IntegerField(primary_key=True)
    species = ForeignKey('Species', null=True, blank=True)
    channel = ForeignKey(Channel, null=True, blank=True)
    occurrence = IntegerField()
    class Meta:
        db_table = 'product'

class Reactant(Model):
    id = IntegerField(primary_key=True)
    species = ForeignKey('Species', null=True, blank=True)
    reaction = ForeignKey('Reaction', null=True, blank=True)
    occurrence = IntegerField()
    class Meta:
        db_table = 'reactant'
        

class Reaction(Model):
    id = IntegerField(primary_key=True)
    type_channel = ForeignKey('TypeChannel', null=True, blank=True)
    status = IntegerField(null=True, blank=True)
    family = CharField(max_length=255L)
    reactant_string = CharField(max_length=255L)
    old_3body_id = CharField(max_length=255L, blank=True)
    slug = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'reaction'

class Species(Model):
    id = IntegerField(primary_key=True)
    common_name = CharField(max_length=100L)
    description = CharField(max_length=255L, blank=True)
    formula = CharField(max_length=30L, blank=True)
    inchi = CharField(max_length=255L, blank=True)
    excitation = CharField(max_length=100L, blank=True)
    charge = IntegerField(null=True, blank=True)
    cas = CharField(max_length=255L, blank=True)
    application = CharField(max_length=20L, blank=True)
    inchi_key = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'species'
        
    def commonNameText(self):
        if self.common_name == 'Photon':
            return 'photon'
        if self.common_name == 'e-':
            return 'electron'
        if self.common_name == 'CR':
            return 'cosmic'
        if self.common_name == 'CRP':
            return 'photon'
        return self.common_name
      

class SpeciesHasElement(Model):
    id = IntegerField(primary_key=True)
    species = ForeignKey(Species, null=True, blank=True)
    element = ForeignKey(Element, null=True, blank=True)
    occurrence = IntegerField()
    class Meta:
        db_table = 'species_has_element'

class SurfaceActivation(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    cv_surface = ForeignKey(CvSurface, null=True, blank=True)
    ea = FloatField(null=True, blank=True)
    uncert_ea = FloatField(null=True, blank=True)
    pre_exponential_factor = FloatField(null=True, blank=True)
    method = CharField(max_length=255L, blank=True)
    origin = CharField(max_length=255L, blank=True)
    database_name = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    expertize = IntegerField()
    surface_type = CharField(max_length=255L, blank=True)
    reference = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'surface_activation'

class SurfaceBarrier(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    cv_surface = ForeignKey(CvSurface, null=True, blank=True)
    value = FloatField(null=True, blank=True)
    uncert_value = FloatField(null=True, blank=True)
    method = CharField(max_length=255L, blank=True)
    origin = CharField(max_length=255L, blank=True)
    database_name = CharField(max_length=255L, blank=True)
    description = TextField(blank=True)
    expertize = IntegerField()
    surface_type = CharField(max_length=255L, blank=True)
    reference = CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'surface_barrier'

class SurfaceBr(Model):
    id = IntegerField(primary_key=True)
    biblio = ForeignKey(Biblio, null=True, blank=True)
    cv_surface = ForeignKey(CvSurface, null=True, blank=True)
    branching_ratio = FloatField()
    uncert_br = FloatField()
    method = CharField(max_length=255L)
    origin = CharField(max_length=255L)
    database_name = CharField(max_length=255L)
    description = TextField()
    surface_type = CharField(max_length=255L)
    expertize = IntegerField()
    class Meta:
        db_table = 'surface_br'

class TypeChannel(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=255L)
    abbrev= CharField(max_length=255L)
    description = TextField()
    class Meta:
        db_table = 'type_channel'
        