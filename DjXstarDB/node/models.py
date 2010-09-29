# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class Sources(models.Model):
    id = models.IntegerField(primary_key=True)
    added = models.DateTimeField()
    description = models.TextField()
    notes = models.TextField(blank=True)
    ident = models.CharField(max_length=96)
    class Meta:
        db_table = u'sources'

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

class Datatype(models.Model):
    id = models.IntegerField(primary_key=True)
    fdtid = models.IntegerField()
    xid = models.IntegerField(null=True, blank=True)
    label = models.CharField(max_length=96)
    uid = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    ident = models.CharField(max_length=96)
    class Meta:
        db_table = u'datatypes'

class Data(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sid = models.ForeignKey(Sources)
    dtid = models.ForeignKey(Datatype)
    value = models.CharField(max_length=96)
    compare = models.FloatField()
    class Meta:
        db_table = u'data'

# this is a view of data
class Energy(models.Model):
    id = models.BigIntegerField(primary_key=True)
    sid = models.ForeignKey(Sources)
    dtid = models.ForeignKey(Datatype)
    value = models.CharField(max_length=96)
    compare = models.FloatField()
    class Meta:
        db_table = u'energy'

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

class Ion(models.Model):
    id = models.IntegerField(primary_key=True)
    element = models.ForeignKey(Elements,db_column='eid')
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

