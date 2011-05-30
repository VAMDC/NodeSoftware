# 2011-05-30 KWS Created modifed schema for UMIST database

# UMIST Modified Database Tables for compatibility with VAMDC and XSAMS

class NewReaction(models.Model):
    reaction_id = models.IntegerField(primary_key=True)
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
    r1_species = models.ForeignKey(NewSpecies, to_field='species_id', db_column='r1_species')
    r2_species = models.ForeignKey(NewSpecies, to_field='species_id', db_column='r2_species')
    r3_species = models.ForeignKey(NewSpecies, to_field='species_id', db_column='r3_species')
    p1_species = models.ForeignKey(NewSpecies, to_field='species_id', db_column='p1_species')
    p2_species = models.ForeignKey(NewSpecies, to_field='species_id', db_column='p2_species')
    p3_species = models.ForeignKey(NewSpecies, to_field='species_id', db_column='p3_species')
    p4_species = models.ForeignKey(NewSpecies, to_field='species_id', db_column='p4_species')
    class Meta:
        db_table = u'new_reaction'

class NewRxnData(models.Model):
    rd_id = models.IntegerField()
    network_id = models.IntegerField(null=True, blank=True)
    reaction_id = models.ForeignKey(NewReaction, to_field='reaction_id', db_column='reaction_id')
    rt_id = models.ForeignKey(NewReacTypes, to_field='rt_id', db_column='rt_id')
    alpha = models.FloatField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    gamma = models.FloatField(null=True, blank=True)
    tmin = models.FloatField(null=True, blank=True)
    tmax = models.FloatField(null=True, blank=True)
    acc = models.CharField(max_length=3, blank=True)
    ref = models.ForeignKey(NewSource, to_field='abbr', db_column='ref')
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

class NewSource(models.Model):
    abbr = models.CharField(max_length=12, primary_key=True)
    full = models.CharField(max_length=765, blank=True)
    url = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'new_source'

class NewSpecies(models.Model):
    species_id = models.IntegerField(primary_key=True)
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
    class Meta:
        db_table = u'new_species'

class NewReacTypes(models.Model):
    rt_id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=765, blank=True)
    abbr = models.CharField(max_length=4, blank=True)
    class Meta:
        db_table = u'new_reac_types'

