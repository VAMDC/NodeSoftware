from django.db import models
from django.utils.translation import ugettext_lazy as _

class ColInfo(models.Model):
    id = models.IntegerField(primary_key=True,db_index=True)
    cname = models.CharField(max_length=64)
    tname = models.CharField(max_length=64)
    ccom = models.TextField(blank=True,null=True)
    cunit = models.CharField(max_length=64, blank=True,null=True)
    cfmt = models.CharField(max_length=64, blank=True,null=True)
    def __unicode__(self):
        return u'%d'%self.id
    class Meta:
        db_table = u'meta'
        verbose_name = _('ColumnInfo')
        verbose_name_plural = _('ColumnInfos')

class Species(models.Model):
    id = models.IntegerField(primary_key=True,db_index=True)
    name = models.CharField(max_length=10, db_index=True)
    ion = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    mass = models.FloatField(blank=True) 
    ionen = models.FloatField(blank=True)
    solariso = models.FloatField(blank=True)
    ncomp = models.PositiveSmallIntegerField(null=True, blank=True)
    atomic = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    isotope = models.PositiveSmallIntegerField(null=True, blank=True)
    def __unicode__(self):
        return u'%d'%self.id
    class Meta:
        db_table = u'species'
        verbose_name = _('Species')
        verbose_name_plural = _('Species')

class Source(models.Model):
    id = models.IntegerField(primary_key=True,db_index=True)
    srcfile = models.CharField(max_length=128)
    speclo = models.ForeignKey(Species,related_name='islowerboundspecies_source',db_column='speclo')
    spechi = models.ForeignKey(Species,related_name='isupperboundspecies_source',db_column='spechi')
    listtype = models.PositiveSmallIntegerField(null=True,blank=True)
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
    def __unicode__(self):
        return u'%d'%self.id
    class Meta:
        db_table = u'sources'
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

class State(models.Model):
    id = models.CharField(max_length=128, primary_key=True,db_index=True)
    species = models.ForeignKey(Species,db_column='species', db_index=True)
    energy = models.FloatField(null=True,blank=True, db_index=True) 
    lande = models.FloatField(null=True,blank=True)
    coupling = models.CharField(max_length=2, null=True,blank=True)
    term = models.CharField(max_length=46, null=True,blank=True)
    energy_ref = models.ForeignKey(Source,related_name='isenergyref_state',db_column='energy_ref')
    lande_ref = models.ForeignKey(Source,related_name='islanderef_state',db_column='lande_ref')
    level_ref = models.ForeignKey(Source,related_name='istermref_state',db_column=u'level_ref')
    j = models.FloatField(db_column=u'J', null=True,blank=True)
    l = models.FloatField(db_column=u'L', null=True,blank=True)
    s = models.FloatField(db_column=u'S', null=True,blank=True)
    p = models.FloatField(db_column=u'P', null=True,blank=True)
    j1 = models.FloatField(db_column=u'J1', null=True,blank=True)
    j2 = models.FloatField(db_column=u'J2', null=True,blank=True)
    k = models.FloatField(db_column=u'K', null=True,blank=True)
    s2 = models.FloatField(db_column=u'S2', null=True,blank=True)
    jc = models.FloatField(db_column=u'Jc', null=True,blank=True)
    def __unicode__(self):
        return u'%s'%self.id
    class Meta:
        db_table = u'states'
        verbose_name = _('State')
        verbose_name_plural = _('States')

class Transition(models.Model):
    id = models.IntegerField(primary_key=True,db_index=True)
    vacwave = models.FloatField(db_index=True) 
    airwave = models.FloatField(db_index=True)
    species = models.ForeignKey(Species,db_column='species',related_name='isspecies_trans')
    loggf = models.FloatField(null=True,blank=True)
    landeff = models.FloatField(null=True,blank=True)
    gammarad = models.FloatField(null=True,blank=True)
    gammastark = models.FloatField(null=True,blank=True)
    gammawaals = models.FloatField(null=True,blank=True)
    srctag = models.CharField(max_length=7, blank=True,null=True)
    acflag = models.CharField(max_length=1, blank=True,null=True)
    accur = models.CharField(max_length=10, blank=True,null=True)
    comment = models.CharField(max_length=10, null=True,blank=True)
    #wave_ref = models.ForeignKey(Source,db_column=u'wave_ref',related_name='iswaveref_trans')
    #loggf_ref = models.ForeignKey(Source,db_column=u'loggf_ref',related_name='isloggfref_trans')
    #lande_ref = models.ForeignKey(Source,db_column=u'lande_ref',related_name='islanderef_trans')
    #gammarad_ref = models.ForeignKey(Source,db_column=u'gammarad_ref',related_name='isgammaradref_trans')
    #gammastark_ref = models.ForeignKey(Source,db_column=u'gammastark_ref',related_name='isgammastarkref_trans')
    #gammawaals_ref = models.ForeignKey(Source,db_column=u'gammawaals_ref',related_name='isgammawaalsref_trans')
    #upstate = models.ForeignKey(State,related_name='isupperstate_trans',db_column='upstate')
    #lostate = models.ForeignKey(State,related_name='islowerstate_trans',db_column='lostate')
    wave_ref = models.PositiveSmallIntegerField()
    loggf_ref = models.PositiveSmallIntegerField()
    lande_ref = models.PositiveSmallIntegerField()
    gammarad_ref = models.PositiveSmallIntegerField()
    gammastark_ref = models.PositiveSmallIntegerField()
    gammawaals_ref = models.PositiveSmallIntegerField()
    upstate = models.CharField(max_length=128)
    lostate = models.CharField(max_length=128)
    def __unicode__(self):
        return u'%d'%self.id
    class Meta:
        db_table = u'transitions'
        verbose_name = _('Transition')
        verbose_name_plural = _('Transitions')
