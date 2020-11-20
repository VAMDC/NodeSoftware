# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from vamdctap.bibtextools import *

class Term:
    l = 0
    s = 0


class Species(models.Model):
    id = models.IntegerField(null=False, primary_key=True, blank=False)
    atomsymbol = models.CharField(max_length=6, db_column='AtomSymbol', blank=True)
    atomnuclearcharge = models.IntegerField(null=True, db_column='AtomNuclearCharge', blank=True)
    atomioncharge = models.IntegerField(null=True, db_column='AtomIonCharge', blank=True)
    inchi = models.CharField(null=False, db_column='inchi', max_length=32, blank=False)
    inchikey = models.CharField(null=False, db_column='inchikey', max_length=25, blank=False)

    class Meta:
        db_table = u'species'


class States(models.Model):
    def _get_statistical_weight(self):
        return (2 * self.atomstatetotalangmom) + 1
 
    id = models.IntegerField(null=False, primary_key=True, blank=False)
    chiantiiontype = models.CharField(max_length=3, db_column='ChiantiIonType', blank=True)
    atomsymbol = models.CharField(max_length=6, db_column='AtomSymbol', blank=True)
    species = models.ForeignKey(Species, related_name='+', db_column='species', on_delete=models.CASCADE)
    atomnuclearcharge = models.IntegerField(null=True, db_column='AtomNuclearCharge', blank=True)
    atomioncharge = models.IntegerField(null=True, db_column='AtomIonCharge', blank=True)
    atomstateconfigurationlabel = models.CharField(max_length=96, db_column='AtomStateConfigurationLabel', blank=True)
    atomstates = models.FloatField(null=True, db_column='AtomStateS', blank=True)
    atomstatel = models.IntegerField(null=True, db_column='AtomStateL', blank=True)
    atomstatetotalangmom = models.FloatField(null=True, db_column='AtomStateTotalAngMom', blank=True)
    parity = models.CharField(max_length=4, db_column='parity', null=False, blank=False)
    energy = models.FloatField(null=True, db_column='AtomStateEnergy', blank=True)
    energyMethod = models.CharField(max_length=4, db_column='AtomStateEnergyMethod', null=False, blank=False)
    statisticalweight = property(_get_statistical_weight)

    def allEnergies(self):
        energies = []
        if self.energyexperimental:
            energies.append(self.energyexperimental)
        if self.energytheoretical:
            energies.append(self.energytheoretical)
        return energies

    def allEnergyMethods(self):
        methods = []
        if self.energyexperimental:
            methods.append("EXP")
        if self.energytheoretical:
            methods.append("THEO")
        return methods

    def sourceIds(self):
        
	    # Chianti quotes references per species, not per states, so find the species associated with this state.
        speciesId = self.species_id
        # Find all the ojects in the source model linked to the species; return a list of their ID numbers.
        sources = Sources.objects.filter(species = speciesId)
        return Sources.objects.filter(species = speciesId).values_list('id', flat=True)

    class Meta:
        db_table = u'states'

class Components(models.Model):
    id    = models.IntegerField(db_column='id', primary_key=True)
    label = models.CharField(db_column='label', max_length=32)
    core  = models.CharField(db_column='core', max_length=2, null=True)
    lsl   = models.IntegerField(db_column='lsl')
    lss   = models.FloatField(db_column='lss')

    class Meta:
        db_table=u'components'

class Subshells(models.Model):
    id         = models.AutoField(primary_key=True)
    state      = models.IntegerField(db_column='state')
    n          = models.IntegerField(db_column='n')
    l          = models.IntegerField(db_column='l');
    population = models.IntegerField(db_column='pop');

    class Meta:
        db_table=u'subshells'



class Transitions(models.Model):
    id = models.IntegerField(db_column='id', null=False, blank=False, primary_key=True)
    chiantiradtranstype = models.CharField(max_length=3, db_column='ChiantiRadTransType', blank=True)
    atomsymbol = models.CharField(max_length=24, db_column='AtomSymbol', blank=True)
    finalstateindex = models.ForeignKey(States, related_name='+', db_column='chiantiradtransfinalstateindex', on_delete=models.CASCADE)
    initialstateindex = models.ForeignKey(States, related_name='+', db_column='chiantiradtransinitialstateindex', on_delete=models.CASCADE)
    wavelengthexperimental = models.FloatField(null=True, db_column='wavelengthexperimental', blank=True)
    wavelengththeoretical = models.FloatField(null=True, db_column='wavelengththeoretical', blank=True)
    wavelength = models.FloatField(null=True, db_column='wavelength', blank=True)
    weightedoscillatorstrength = models.FloatField(null=True, db_column='RadTransProbabilityWeightedOscillatorStrength', blank=True)
    probabilitya = models.FloatField(null=True, db_column='RadTransProbabilityTransitionProbabilityA', blank=True)

    def upperStateRef(self):
        if self.finalstateindex.energy > self.initialstateindex.energy:
            return self.finalstateindex.id
        else:
            return self.initialstateindex.id

    def lowerStateRef(self):
        if self.finalstateindex.energy < self.initialstateindex.energy:
            return self.finalstateindex.id
        else:
            return self.initialstateindex.id



    def allWavelengths(self):
        wavelengths = []
        if self.wavelengthexperimental:
            wavelengths.append(self.wavelengthexperimental)
        if self.wavelengththeoretical:
            wavelengths.append(self.wavelengththeoretical)
        return wavelengths

    def allWavelengthMethods(self):
        methods = []
        if self.wavelengthexperimental:
            methods.append("EXP")
        if self.wavelengththeoretical:
            methods.append("THEO")
        return methods

    class Meta:
        db_table = u'transitions'

# This is copied from the VALD node.
class Sources(models.Model):
    id = models.CharField(max_length=7, primary_key=True, db_index=True)
    species = models.ForeignKey(Species, related_name='+', on_delete=models.CASCADE)
    bibtex = models.TextField(null=True)

    def XML(self):
        return BibTeX2XML(self.bibtex, self.id)

    class Meta:
        db_table = u'sources'
        def __unicode__(self):
            return u'%s'%self.id
