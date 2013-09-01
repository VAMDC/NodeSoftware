from django.db import models

class Species(models.Model):
    id = models.IntegerField(null=False, primary_key=True, blank=False)
    element = models.CharField(max_length=6, db_column='element', blank=True)
    nuclearcharge = models.IntegerField(null=True, db_column='nuclearcharge', blank=True)
    ioncharge = models.IntegerField(null=True, db_column='ioncharge', blank=True)

    class Meta:
        db_table = u'species'


class States(models.Model):
    id = models.IntegerField(null=False, primary_key=True, blank=False)
    species = models.ForeignKey(Species, related_name='+', db_column='species')
    configuration = models.CharField(max_length=96, db_column='configuration', blank=True)
    s = models.FloatField(null=True, db_column='s', blank=True)
    l = models.IntegerField(null=True, db_column='l', blank=True)
    j = models.FloatField(null=True, db_column='j', blank=True)
    energy = models.FloatField(null=True, db_column='energy', blank=True)

    class Meta:
        db_table = u'states'

class Transitions(models.Model):
    #id = models.IntegerField(db_column='id', null=False, blank=False, primary_key=True)
    finalstateindex = models.ForeignKey(States, related_name='+', db_column='finalstate')
    initialstateindex = models.ForeignKey(States, related_name='+', db_column='initialstate')
    wavelength = models.FloatField(null=True, db_column='wavelength', blank=True)
    weightedoscillatorstrength = models.FloatField(null=True, db_column='log10wosc', blank=True)
    probabilitya = models.FloatField(null=True, db_column='a', blank=True)

    class Meta:
        db_table = u'transitions'
