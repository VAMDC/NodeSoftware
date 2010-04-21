from django.db import models

class Meta(models.Model):
    cname = models.CharField(max_length=64, blank=True)
    tname = models.CharField(max_length=64, blank=True)
    ccom = models.TextField(blank=True)
    cunit = models.CharField(max_length=64, blank=True)
    cfmt = models.CharField(max_length=64, blank=True)
    class Meta:
        db_table = u'meta'

class Species(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=10, db_index=True)
    ion = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    mass = models.FloatField(blank=True) 
    ionen = models.FloatField(blank=True)
    solariso = models.FloatField(blank=True)
    ncomp = models.PositiveSmallIntegerField(null=True, blank=True)
    atomic = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    isotope = models.PositiveSmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'species'

class Sources(models.Model):
    srcfile = models.CharField(max_length=128)
    id = models.PositiveSmallIntegerField(null=True, primary_key=True,db_column='refid', db_index=True)
    speclo = models.ForeignKey(Species,related_name='islowerboundspecies_source',db_column='speclo')
    spechi = models.ForeignKey(Species,related_name='isupperboundspecies_source',db_column='spechi')
    listtype = models.PositiveSmallIntegerField(null=True,default=0)
    r1 = models.PositiveSmallIntegerField(null=True, blank=True)
    r2 = models.PositiveSmallIntegerField(null=True, blank=True)
    r3 = models.PositiveSmallIntegerField(null=True, blank=True)
    r4 = models.PositiveSmallIntegerField(null=True, blank=True)
    r5 = models.PositiveSmallIntegerField(null=True, blank=True)
    r6 = models.PositiveSmallIntegerField(null=True, blank=True)
    r7 = models.PositiveSmallIntegerField(null=True, blank=True)
    r8 = models.PositiveSmallIntegerField(null=True, blank=True)
    r9 = models.PositiveSmallIntegerField(null=True, blank=True)
    srcdescr = models.CharField(max_length=128, blank=True, null=True)
    class Meta:
        db_table = u'sources'

class States(models.Model):
    id = models.CharField(max_length=128, primary_key=True, blank=True, db_index=True)
    species = models.ForeignKey(Species,db_column='species', db_index=True)
    energy = models.FloatField(null=True,blank=True, db_index=True) 
    lande = models.FloatField(null=True,blank=True)
    coupling = models.CharField(max_length=2, null=True,blank=True)
    term = models.CharField(max_length=46, null=True,blank=True)
    energy_ref = models.ForeignKey(Sources,related_name='isenergyref_state',db_column='energy_ref')
    lande_ref = models.ForeignKey(Sources,related_name='islanderef_state',db_column='lande_ref')
    level_ref = models.ForeignKey(Sources,related_name='istermref_state',db_column=u'level_ref')
    j = models.FloatField(db_column=u'J', blank=True)
    l = models.FloatField(db_column=u'L', blank=True)
    s = models.FloatField(db_column=u'S', blank=True)
    p = models.FloatField(db_column=u'P', blank=True)
    j1 = models.FloatField(db_column=u'J1', blank=True)
    j2 = models.FloatField(db_column=u'J2', blank=True)
    k = models.FloatField(db_column=u'K', blank=True)
    s2 = models.FloatField(db_column=u'S2', blank=True)
    jc = models.FloatField(db_column=u'Jc', blank=True)
    class Meta:
        db_table = u'states'

class Transitions(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True, db_index=True)
    vacwave = models.FloatField(blank=True, db_index=True) 
    airwave = models.FloatField(blank=True, db_index=True)
    species = models.ForeignKey(Species,db_column='species',related_name='isspecies_trans', db_index=True)
    loggf = models.FloatField(blank=True)
    landeff = models.FloatField(blank=True)
    gammarad = models.FloatField(blank=True)
    gammastark = models.FloatField(blank=True)
    gammawaals = models.FloatField(blank=True)
    srctag = models.CharField(max_length=7, blank=True)
    acflag = models.CharField(max_length=1, blank=True)
    accur = models.CharField(max_length=10, blank=True)
    comment = models.CharField(max_length=10, blank=True)
    wave_ref = models.ForeignKey(Sources,db_column=u'wave_ref',related_name='iswaveref_trans')
    loggf_ref = models.ForeignKey(Sources,db_column=u'loggf_ref',related_name='isloggfref_trans')
    lande_ref = models.ForeignKey(Sources,db_column=u'lande_ref',related_name='islanderef_trans')
    gammarad_ref = models.ForeignKey(Sources,db_column=u'gammarad_ref',related_name='isgammaradref_trans')
    gammastark_ref = models.ForeignKey(Sources,db_column=u'gammastark_ref',related_name='isgammastarkref_trans')
    gammawaals_ref = models.ForeignKey(Sources,db_column=u'gammawaals_ref',related_name='isgammawaalsref_trans')
    upstate = models.ForeignKey(States,related_name='isupperstate_trans',db_column='upstate', db_index=True)
    lostate = models.ForeignKey(States,related_name='islowerstate_trans',db_column='lostate', db_index=True)
    class Meta:
        db_table = u'transitions'
