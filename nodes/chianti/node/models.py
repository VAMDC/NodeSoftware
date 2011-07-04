# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Species(models.Model):
    id = models.IntegerField(null=False, primary_key=True, blank=False)
    atomsymbol = models.CharField(max_length=6, db_column='AtomSymbol', blank=True)
    atomnuclearcharge = models.IntegerField(null=True, db_column='AtomNuclearCharge', blank=True)
    atomioncharge = models.IntegerField(null=True, db_column='AtomIonCharge', blank=True)
    class Meta:
        db_table = u'species'

class States(models.Model):
    id = models.IntegerField(null=False, primary_key=True, blank=False)
    chiantiiontype = models.CharField(max_length=3, db_column='ChiantiIonType', blank=True)
    atomsymbol = models.CharField(max_length=6, db_column='AtomSymbol', blank=True)
    species = models.ForeignKey(Species, related_name='+', db_column='species')
    atomnuclearcharge = models.IntegerField(null=True, db_column='AtomNuclearCharge', blank=True)
    atomioncharge = models.IntegerField(null=True, db_column='AtomIonCharge', blank=True)
    atomstateconfigurationlabel = models.CharField(max_length=96, db_column='AtomStateConfigurationLabel', blank=True)
    atomstates = models.FloatField(null=True, db_column='AtomStateS', blank=True)
    atomstatel = models.FloatField(null=True, db_column='AtomStateL', blank=True)
    atomstatetotalangmom = models.FloatField(null=True, db_column='AtomStateTotalAngMom', blank=True)
    atomstateenergyexperimentalvalue = models.FloatField(null=True, db_column='AtomStateEnergyExperimental', blank=True)
    atomstateenergytheoreticalvalue = models.FloatField(null=True, db_column='AtomStateEnergyTheoretical', blank=True)
    class Meta:
        db_table = u'states'

class Transitions(models.Model):
    id = models.IntegerField(db_column='id', null=False, blank=False, primary_key=True)
    chiantiradtranstype = models.CharField(max_length=3, db_column='ChiantiRadTransType', blank=True)
    atomsymbol = models.CharField(max_length=24, db_column='AtomSymbol', blank=True)
    finalstateindex = models.ForeignKey(States, related_name='+', db_column='chiantiradtransfinalstateindex')
    initialstateindex = models.ForeignKey(States, related_name='+', db_column='chiantiradtransinitialstateindex')
    wavelength = models.FloatField(null=True, db_column='RadTransWavelength', blank=True)
    wavelengthmethod = models.CharField(max_length=4, db_column='RadTransWavelengthMethod');
    weightedoscillatorstrength = models.FloatField(null=True, db_column='RadTransProbabilityWeightedOscillatorStrength', blank=True)
    probabilitya = models.FloatField(null=True, db_column='RadTransProbabilityTransitionProbabilityA', blank=True)

    class Meta:
        db_table = u'transitions'
