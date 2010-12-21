# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=765, blank=True)
    email = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'users'

class ReacTypes(models.Model):
    rt_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=765, blank=True)
    abbr = models.CharField(max_length=6, blank=True)
    class Meta:
        db_table = u'reac_types'

class Udfa1995(models.Model):
    r95_id = models.IntegerField(primary_key=True)
    reaction_id = models.IntegerField()
    r95_alpha = models.CharField(max_length=45, blank=True)
    r95_beta = models.CharField(max_length=45, blank=True)
    r95_gamma = models.CharField(max_length=45, blank=True)
    r95_clem = models.CharField(max_length=3, blank=True)
    r95_acc = models.CharField(max_length=3, blank=True)
    r95_ref = models.CharField(max_length=12, blank=True)
    inc = models.CharField(max_length=3, blank=True)
    type = models.CharField(max_length=6, blank=True)
    reaction = models.CharField(max_length=765, blank=True)
    rt_id = models.ForeignKey(ReacTypes, to_field='rt_id', db_column='rt_id')
    r95_10kr = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'udfa1995'

class Udfa1999(models.Model):
    r99_id = models.IntegerField(primary_key=True)
    reaction_id = models.IntegerField()
    r99_alpha = models.CharField(max_length=45, blank=True)
    r99_beta = models.CharField(max_length=45, blank=True)
    r99_gamma = models.CharField(max_length=45, blank=True)
    r99_clem = models.CharField(max_length=3, blank=True)
    tmin = models.CharField(max_length=30, blank=True)
    tmax = models.CharField(max_length=30, blank=True)
    r99_acc = models.CharField(max_length=3, blank=True)
    r99_ref = models.CharField(max_length=12, blank=True)
    rt_id = models.ForeignKey(ReacTypes, to_field='rt_id', db_column='rt_id')
    r99_10kr = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'udfa1999'

class Udfa2005(models.Model):
    reaction_id = models.IntegerField(primary_key=True)
    r05_alpha = models.CharField(max_length=45, blank=True)
    r05_beta = models.CharField(max_length=45, blank=True)
    r05_gamma = models.CharField(max_length=45, blank=True)
    r05_clem = models.CharField(max_length=3, blank=True)
    tmin = models.CharField(max_length=30, blank=True)
    tmax = models.CharField(max_length=30, blank=True)
    r05_acc = models.CharField(max_length=3, blank=True)
    r05_ref = models.CharField(max_length=12, blank=True)
    rt_id = models.ForeignKey(ReacTypes, to_field='rt_id', db_column='rt_id')
    r1 = models.CharField(max_length=30, blank=True)
    r2 = models.CharField(max_length=30, blank=True)
    r3 = models.CharField(max_length=30, blank=True)
    p3 = models.CharField(max_length=30, blank=True)
    p2 = models.CharField(max_length=30, blank=True)
    p1 = models.CharField(max_length=30, blank=True)
    p4 = models.CharField(max_length=30, blank=True)
    processed = models.IntegerField(null=True, blank=True)
    r05_id = models.IntegerField()
    dipole = models.IntegerField(null=True, blank=True)
    r05_10kr = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'udfa2005'

class Reaction(models.Model):
    reaction_id = models.IntegerField(primary_key=True)
    r1 = models.CharField(max_length=765, blank=True)
    r2 = models.CharField(max_length=765, blank=True)
    r3 = models.CharField(max_length=765, blank=True)
    p1 = models.CharField(max_length=765, blank=True)
    p2 = models.CharField(max_length=765, blank=True)
    p3 = models.CharField(max_length=765, blank=True)
    p4 = models.CharField(max_length=765, blank=True)
    udfa1999 = models.ForeignKey(Udfa1999, to_field='r99_id', db_column='udfa1999')
    udfa1995 = models.ForeignKey(Udfa1995, to_field='r95_id', db_column='udfa1995', related_name='udfa1995_reaction')
    ohio_nsm = models.IntegerField(null=True, blank=True)  # irrelevant to VAMDC
    unknown = models.IntegerField(null=True, blank=True)  # irrelevant to VAMDC
    user_id = models.ForeignKey(Users, to_field='user_id', db_column='user_id')
    udfa2005 = models.ForeignKey(Udfa2005, to_field='reaction_id', db_column='udfa2005')
    rt_id = models.ForeignKey(ReacTypes, to_field='rt_id', db_column='rt_id')
    class Meta:
        db_table = u'reaction'

class Comments(models.Model):
    comment_id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    user_id = models.ForeignKey(Users, to_field='user_id', db_column='user_id')
    comment = models.TextField(blank=True)
    reaction_id = models.ForeignKey(Reaction, to_field='reaction_id', db_column='reaction_id')
    class Meta:
        db_table = u'comments'

class Species(models.Model):
    species_id = models.IntegerField(primary_key=True)
    struct_name = models.CharField(max_length=150)
    empirical = models.CharField(max_length=150)
    mass = models.IntegerField()
    names = models.CharField(max_length=765, blank=True)
    dipole = models.CharField(max_length=30, blank=True)
    heat_form = models.CharField(max_length=30, blank=True)
    rate99_id = models.IntegerField()
    user_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    detected = models.IntegerField(null=True, blank=True)
    orig_ip = models.CharField(max_length=48, blank=True)
    cometary = models.IntegerField()
    class Meta:
        db_table = u'species'

class Isotopomers(models.Model):
    iso_id = models.IntegerField(primary_key=True)
    species_id = models.ForeignKey(Species, to_field='species_id', db_column='species_id', related_name='parent_isotopomer')
    daughter_id = models.ForeignKey(Species, to_field='species_id', db_column='species_id', related_name='daughter_isotopomer')
    class Meta:
        db_table = u'isotopomers'

class Networks(models.Model):
    network_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=765, blank=True)
    description = models.TextField(blank=True)
    reference = models.CharField(max_length=765, blank=True)
    url = models.CharField(max_length=765, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'networks'

class RxnData(models.Model):
    rd_id = models.IntegerField(primary_key=True)
    network_id = models.IntegerField(null=True, blank=True)
    reaction_id = models.IntegerField(null=True, blank=True)
    rt_id = models.IntegerField(null=True, blank=True)
    alpha = models.CharField(max_length=45, blank=True)
    beta = models.CharField(max_length=45, blank=True)
    gamma = models.CharField(max_length=45, blank=True)
    tmin = models.CharField(max_length=30, blank=True)
    tmax = models.CharField(max_length=30, blank=True)
    acc = models.CharField(max_length=3, blank=True)
    ref = models.CharField(max_length=12, blank=True)
    clem = models.CharField(max_length=3, blank=True)
    dipole = models.IntegerField(null=True, blank=True)
    r10kr = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    rxn = models.CharField(max_length=765, blank=True)
    nwi_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    prv_rd_id = models.IntegerField(null=True, blank=True)  # irrelevant to VAMDC
    watch = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'rxn_data'

class Source(models.Model):
    abbr = models.CharField(max_length=12, blank=True)
    full = models.CharField(max_length=765, blank=True)
    url = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'source'

class Stats(models.Model):
    id = models.IntegerField(primary_key=True)
    browser = models.CharField(max_length=765, blank=True)
    ip = models.CharField(max_length=45, blank=True)
    received = models.DateTimeField(null=True, blank=True)
    refer = models.CharField(max_length=765, blank=True)
    page = models.CharField(max_length=765, blank=True)
    query_string = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'stats'

class Unknown(models.Model):
    unk_id = models.IntegerField(primary_key=True)
    reaction_id = models.IntegerField()
    alpha = models.CharField(max_length=45, blank=True)
    beta = models.CharField(max_length=45, blank=True)
    gamma = models.CharField(max_length=45, blank=True)
    class Meta:
        db_table = u'unknown'

class VamdcSpecies(models.Model):
    id = models.IntegerField(primary_key=True)
    molecule_id = models.CharField(max_length=240)
    stoichiometric_formula = models.CharField(max_length=240)
    data_origin = models.CharField(max_length=120, blank=True)
    data_origin_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'vamdc_species'

class VamdcAliases(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=240)
    vamdc_species_id = models.ForeignKey(VamdcSpecies, to_field='id', db_column='vamdc_species_id')
    alias_type = models.CharField(max_length=240)
    search_priority = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'vamdc_aliases'
