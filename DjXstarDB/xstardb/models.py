# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


from django.db import models
from django.utils.translation import ugettext_lazy as _

# Classes copied from VALD model

class Species(models.Model):
    name = models.CharField(max_length=10, db_index=True)
    ion = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    mass = models.DecimalField(max_digits=5, decimal_places=2) 
    ionen = models.DecimalField(max_digits=7, decimal_places=3) 
    solariso = models.DecimalField(max_digits=5, decimal_places=4) 
    ncomp = models.PositiveSmallIntegerField(null=True, blank=True)
    atomic = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    isotope = models.PositiveSmallIntegerField(null=True, blank=True)
    def __unicode__(self):
        if self.id:
            return u'%s'%self.id.encode('utf8')
        else:
            return u'NULL'
    class Meta:
        db_table = u'species'
        verbose_name = _('Species')
        verbose_name_plural = _('Species')

class Source(models.Model):
    srcfile = models.CharField(max_length=128)
    speclo = models.ForeignKey(Species,related_name='islowerboundspecies_source',db_column='speclo',null=True)
    spechi = models.ForeignKey(Species,related_name='isupperboundspecies_source',db_column='spechi',null=True)
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
        if self.id:
            return u'%s'%self.id.encode('utf8') 
        else:
            return u'NULL'
        
    class Meta:
        db_table = u'sources'
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

class State(models.Model):
    charid = models.CharField(max_length=128, db_index=True,unique=True,null=False)
    species = models.ForeignKey(Species,db_column='species', db_index=True)
    energy = models.DecimalField(max_digits=15, decimal_places=4,null=True,blank=True, db_index=True) 
    lande = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    coupling = models.CharField(max_length=2, null=True,blank=True)
    term = models.CharField(max_length=56, null=True,blank=True)
    energy_ref = models.PositiveSmallIntegerField(null=True,blank=True)
    lande_ref = models.PositiveSmallIntegerField(null=True,blank=True)
    level_ref = models.PositiveSmallIntegerField(null=True,blank=True)
    j = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'J', null=True,blank=True)
    l = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'L', null=True,blank=True)
    s = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'S', null=True,blank=True)
    p = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'P', null=True,blank=True)
    j1 = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'J1', null=True,blank=True)
    j2 = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'J2', null=True,blank=True)
    k = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'K', null=True,blank=True)
    s2 = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'S2', null=True,blank=True)
    jc = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'Jc', null=True,blank=True)
    def __unicode__(self):
        if self.id:
            id = self.id.encode('utf8')
        else:
            id = u'NULL'
        return u'%s %s'%(self.energy,self.lande)
    class Meta:
        db_table = u'states'
        verbose_name = _('State')
        verbose_name_plural = _('States')

class Transition(models.Model):
    vacwave = models.DecimalField(max_digits=20, decimal_places=8) 
    airwave = models.DecimalField(max_digits=20, decimal_places=8) 
    species = models.ForeignKey(Species,db_column='species',related_name='isspecies_trans')
    loggf = models.DecimalField(max_digits=8, decimal_places=3,null=True,blank=True)
    landeff = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammarad = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammastark = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True) 
    gammawaals = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True) 
    srctag = models.CharField(max_length=7, blank=True,null=True)
    acflag = models.CharField(max_length=1, blank=True,null=True)
    accur = models.CharField(max_length=10, blank=True,null=True)
    comment = models.CharField(max_length=128, null=True,blank=True)
    #wave_ref = models.ForeignKey(Source,db_column=u'wave_ref',related_name='iswaveref_trans')
    #loggf_ref = models.ForeignKey(Source,db_column=u'loggf_ref',related_name='isloggfref_trans')
    #lande_ref = models.ForeignKey(Source,db_column=u'lande_ref',related_name='islanderef_trans')
    #gammarad_ref = models.ForeignKey(Source,db_column=u'gammarad_ref',related_name='isgammaradref_trans')
    #gammastark_ref = models.ForeignKey(Source,db_column=u'gammastark_ref',related_name='isgammastarkref_trans')
    #gammawaals_ref = models.ForeignKey(Source,db_column=u'gammawaals_ref',related_name='isgammawaalsref_trans')
    wave_ref = models.PositiveSmallIntegerField()
    loggf_ref = models.PositiveSmallIntegerField()
    lande_ref = models.PositiveSmallIntegerField()
    gammarad_ref = models.PositiveSmallIntegerField()
    gammastark_ref = models.PositiveSmallIntegerField()
    gammawaals_ref = models.PositiveSmallIntegerField()

    upstate = models.ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True)
    lostate = models.ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True)
    upstateid = models.CharField(max_length=128,null=True)
    lostateid = models.CharField(max_length=128,null=True)
    def __unicode__(self):
        if self.id:
            id = self.id.encode('utf8')
        else:
            id = u'NULL'
        return u'%s'%self.id
    class Meta:
        db_table = u'transitions'
        verbose_name = _('Transition')
        verbose_name_plural = _('Transitions')


class Query(models.Model):
    qid=models.CharField(max_length=6,primary_key=True,db_index=True)
    datetime=models.DateTimeField(auto_now_add=True)
    query=models.CharField(max_length=512)


# End of classes copied from VALD model

class Allconfs(models.Model):
    id = models.IntegerField(primary_key=True)
    conf = models.CharField(max_length=192)
    ne = models.IntegerField()
    parity = models.IntegerField()
    class Meta:
        db_table = u'allconfs'

class Alllevels(models.Model):
    id = models.IntegerField(primary_key=True)
    tid = models.IntegerField()
    j2 = models.IntegerField()
    ne = models.IntegerField()
    class Meta:
        db_table = u'alllevels'

class Allterms(models.Model):
    id = models.IntegerField(primary_key=True)
    cid = models.IntegerField()
    g = models.IntegerField()
    l = models.IntegerField()
    alpha = models.IntegerField()
    ne = models.IntegerField()
    class Meta:
        db_table = u'allterms'

class Data(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sid = models.IntegerField()
    dtid = models.IntegerField()
    value = models.CharField(max_length=96)
    compare = models.FloatField()
    class Meta:
        db_table = u'data'

class Datatypes(models.Model):
    id = models.IntegerField(primary_key=True)
    fdtid = models.IntegerField()
    xid = models.IntegerField(null=True, blank=True)
    label = models.CharField(max_length=96)
    uid = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    ident = models.CharField(max_length=96)
    class Meta:
        db_table = u'datatypes'

class Door2(models.Model):
    id = models.IntegerField(primary_key=True)
    did = models.BigIntegerField()
    xmin = models.FloatField()
    xmax = models.FloatField()
    fmin = models.FloatField()
    fmax = models.FloatField()
    count = models.IntegerField()
    class Meta:
        db_table = u'door2'

class Door3(models.Model):
    id = models.IntegerField(primary_key=True)
    did = models.BigIntegerField()
    xmin = models.FloatField()
    xmax = models.FloatField()
    ymin = models.FloatField()
    ymax = models.FloatField()
    fmin = models.FloatField()
    fmax = models.FloatField()
    count = models.IntegerField()
    class Meta:
        db_table = u'door3'

class Elements(models.Model):
    id = models.IntegerField(primary_key=True)
    z = models.IntegerField()
    name = models.CharField(max_length=48)
    sym = models.CharField(max_length=12)
    mass = models.CharField(max_length=96)
    class Meta:
        db_table = u'elements'

class Fundamental(models.Model):
    id = models.IntegerField(primary_key=True)
    xid = models.IntegerField(null=True, blank=True)
    label = models.CharField(max_length=96)
    description = models.TextField()
    ident = models.CharField(max_length=96)
    hidden = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'fundamental'

class Ions(models.Model):
    id = models.IntegerField(primary_key=True)
    eid = models.IntegerField()
    ne = models.IntegerField()
    charge = models.IntegerField()
    gnd_conf = models.IntegerField(null=True, blank=True)
    gnd_term = models.IntegerField(null=True, blank=True)
    gnd_level = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'ions'

class Log(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    name = models.CharField(max_length=192)
    msg = models.TextField()
    class Meta:
        db_table = u'log'

class Notes(models.Model):
    id = models.IntegerField(primary_key=True)
    src_table = models.CharField(max_length=33)
    rid = models.BigIntegerField()
    type = models.CharField(max_length=18)
    note = models.TextField()
    class Meta:
        db_table = u'notes'

class Paramdef(models.Model):
    id = models.IntegerField(primary_key=True)
    dtid = models.IntegerField()
    ptid = models.IntegerField()
    class Meta:
        db_table = u'paramdef'

class Parameters(models.Model):
    id = models.BigIntegerField(primary_key=True)
    did = models.BigIntegerField()
    ptid = models.IntegerField()
    value = models.CharField(max_length=96)
    compare = models.FloatField()
    class Meta:
        db_table = u'parameters'

class Paramtypes(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=96)
    uid = models.IntegerField(null=True, blank=True)
    ident = models.CharField(max_length=96)
    description = models.TextField()
    class Meta:
        db_table = u'paramtypes'

class Reference(models.Model):
    id = models.IntegerField(primary_key=True)
    authors = models.CharField(max_length=765)
    year = models.TextField() # This field type is a guess.
    reference = models.TextField()
    link = models.CharField(max_length=765, blank=True)
    ident = models.CharField(max_length=96)
    adslink = models.CharField(max_length=765)
    class Meta:
        db_table = u'reference'

class Setdef(models.Model):
    id = models.IntegerField(primary_key=True)
    var = models.CharField(max_length=3)
    ptid = models.IntegerField()
    dtid = models.IntegerField()
    class Meta:
        db_table = u'setdef'

class Sourceref(models.Model):
    id = models.IntegerField(primary_key=True)
    sid = models.IntegerField()
    rid = models.IntegerField()
    top = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'sourceref'

class Sources(models.Model):
    id = models.IntegerField(primary_key=True)
    added = models.DateTimeField()
    description = models.TextField()
    notes = models.TextField(blank=True)
    ident = models.CharField(max_length=96)
    class Meta:
        db_table = u'sources'

class Store2(models.Model):
    id = models.BigIntegerField(primary_key=True)
    d2id = models.IntegerField()
    x = models.CharField(max_length=96)
    xcomp = models.FloatField()
    f = models.CharField(max_length=96)
    fcomp = models.FloatField()
    class Meta:
        db_table = u'store2'

class Store3(models.Model):
    id = models.BigIntegerField(primary_key=True)
    d3id = models.IntegerField()
    x = models.CharField(max_length=96)
    xcomp = models.FloatField()
    y = models.CharField(max_length=96)
    ycomp = models.FloatField()
    f = models.CharField(max_length=96)
    fcomp = models.FloatField()
    class Meta:
        db_table = u'store3'

class Units(models.Model):
    id = models.IntegerField(primary_key=True)
    ident = models.CharField(max_length=96)
    term = models.CharField(max_length=96)
    web = models.CharField(max_length=96)
    latex = models.CharField(max_length=96)
    class Meta:
        db_table = u'units'

