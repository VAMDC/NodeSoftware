# 2011-05-30 KWS Created modifed schema for UMIST database

# UMIST Modified Database Tables for compatibility with VAMDC and XSAMS

from django.db import models

class Species(models.Model):
    id = models.IntegerField(primary_key=True, db_column='species_id')
    struct_name = models.CharField(max_length=150)
    empirical = models.CharField(max_length=150)
    mass = models.IntegerField()
    names = models.CharField(max_length=765, blank=True)
    dipole = models.FloatField(null=True, blank=True)
    heat_form = models.FloatField(null=True, blank=True)
    user_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    detected = models.IntegerField(null=True, blank=True)
    orig_ip = models.CharField(max_length=48, blank=True)
    cometary = models.IntegerField()
    inchikey = models.CharField(max_length=90, blank=True)
    inchi = models.TextField(blank=True)
    vamdc_inchikey = models.CharField(max_length=90, blank=True)
    vamdc_inchi = models.TextField(blank=True)
    type = models.IntegerField(db_column='species_type')
    class Meta:
        db_table = u'new_species'


class ReacTypes(models.Model):
    id = models.IntegerField(primary_key=True, db_column='rt_id')
    type = models.CharField(max_length=765, blank=True)
    abbr = models.CharField(max_length=4, blank=True)
    class Meta:
        db_table = u'new_reac_types'

class Source(models.Model):
    abbr = models.CharField(max_length=12, primary_key=True)
    full = models.CharField(max_length=765, blank=True)
    url = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'new_source'

class Reaction(models.Model):
    id = models.IntegerField(primary_key=True, db_column='reaction_id')
    r1 = models.CharField(max_length=765, blank=True)
    r2 = models.CharField(max_length=765, blank=True)
    r3 = models.CharField(max_length=765, blank=True)
    p1 = models.CharField(max_length=765, blank=True)
    p2 = models.CharField(max_length=765, blank=True)
    p3 = models.CharField(max_length=765, blank=True)
    p4 = models.CharField(max_length=765, blank=True)
    udfa1999 = models.IntegerField(null=True, blank=True)
    udfa1995 = models.IntegerField(null=True, blank=True)
    ohio_nsm = models.IntegerField(null=True, blank=True)
    unknown = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    udfa2005 = models.IntegerField(null=True, blank=True)
    rt_id = models.IntegerField(null=True, blank=True)
    r1_species = models.ForeignKey(Species, db_column='r1_species', related_name='rxns_r1')
    r2_species = models.ForeignKey(Species, db_column='r2_species', related_name='rxns_r2')
    r3_species = models.ForeignKey(Species, db_column='r3_species', related_name='rxns_r3')
    p1_species = models.ForeignKey(Species, db_column='p1_species', related_name='rxns_p1')
    p2_species = models.ForeignKey(Species, db_column='p2_species', related_name='rxns_p2')
    p3_species = models.ForeignKey(Species, db_column='p3_species', related_name='rxns_p3')
    p4_species = models.ForeignKey(Species, db_column='p4_species', related_name='rxns_p4')

    # need to create these views for use in the ManyToMany relations in order to abstract the p1,p2...
    #create or replace view reaction_products (reaction_id, species_id) as select distinct r.reaction_id,s.species_id from new_reaction r, new_species s where r.p1_species = s.species_id OR r.p2_species = s.species_id OR r.p3_species = s.species_id OR r.p4_species = s.species_id;
    #create or replace view reaction_reactants (reaction_id, species_id) as select distinct r.reaction_id,s.species_id from new_reaction r, new_species s where r.r1_species = s.species_id OR r.r1_species = s.species_id OR r.r2_species = s.species_id OR r.r3_species = s.species_id;
    #create or replace view reaction_species (reaction_id, species_id) as select distinct r.reaction_id,s.species_id from new_reaction r, new_species s where r.r1_species = s.species_id OR r.r1_species = s.species_id OR r.r2_species = s.species_id OR r.r3_species = s.species_id OR r.p1_species = s.species_id OR r.p2_species = s.species_id OR r.p3_species = s.species_id OR r.p4_species = s.species_id;
    # 2011-06-28 KWS Created "materialised views" of the reaction_species, reaction_reactants and reaction_products views.
    #                This should vastly speed up the queries.
    species = models.ManyToManyField(Species, db_table='reaction_species_mat_view', related_name='reactspecies')
    reactants = models.ManyToManyField(Species, db_table='reaction_reactants_mat_view', related_name='reactreactants')
    products = models.ManyToManyField(Species, db_table='reaction_products_mat_view', related_name='reactproducts')
    class Meta:
        db_table = u'new_reaction'

class RxnData(models.Model):
    id = models.IntegerField(db_column='rd_id', primary_key=True)
    network_id = models.IntegerField(null=True, blank=True)
    reaction = models.ForeignKey(Reaction, db_column='reaction_id')
    rt = models.ForeignKey(ReacTypes, db_column='rt_id')
    alpha = models.FloatField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    gamma = models.FloatField(null=True, blank=True)
    tmin = models.FloatField(null=True, blank=True)
    tmax = models.FloatField(null=True, blank=True)
    acc = models.CharField(max_length=3, blank=True)
    ref = models.ForeignKey(Source, db_column='ref')
    clem = models.CharField(max_length=3, blank=True)
    dipole = models.IntegerField(null=True, blank=True)
    r10kr = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    rxn = models.CharField(max_length=765, blank=True)
    nwi_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    prv_rd_id = models.IntegerField(null=True, blank=True)
    watch = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'new_rxn_data'


