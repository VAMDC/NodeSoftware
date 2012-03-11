# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Term:
    l = 0
    s = 0

class Component:
    Terms = Term();

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
    id = models.IntegerField(null=False, primary_key=True, blank=False)
    chiantiiontype = models.CharField(max_length=3, db_column='ChiantiIonType', blank=True)
    atomsymbol = models.CharField(max_length=6, db_column='AtomSymbol', blank=True)
    species = models.ForeignKey(Species, related_name='+', db_column='species')
    atomnuclearcharge = models.IntegerField(null=True, db_column='AtomNuclearCharge', blank=True)
    atomioncharge = models.IntegerField(null=True, db_column='AtomIonCharge', blank=True)
    atomstateconfigurationlabel = models.CharField(max_length=96, db_column='AtomStateConfigurationLabel', blank=True)
    atomstates = models.FloatField(null=True, db_column='AtomStateS', blank=True)
    atomstatel = models.IntegerField(null=True, db_column='AtomStateL', blank=True)
    atomstatetotalangmom = models.FloatField(null=True, db_column='AtomStateTotalAngMom', blank=True)
    energy = models.FloatField(null=True, db_column='AtomStateEnergy', blank=True)
    energyMethod = models.CharField(max_length=4, db_column='AtomStateEnergyMethod', null=False, blank='False')

    # Each state has one component and each component has one term, describing LS coupling.
    # The generator relies on direct access to the Components attribute of the state and the Terms
    # attribute of the component, using those specific names. The values of the attributes may be
    # either scalars or arrays (the generator is specifically coded to deal with either).
    Components = Component()
    Components.Terms.l = atomstatel
    Components.Terms.s = atomstates
    print Components.Terms.l

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


    class Meta:
        db_table = u'states'

class Transitions(models.Model):
    id = models.IntegerField(db_column='id', null=False, blank=False, primary_key=True)
    chiantiradtranstype = models.CharField(max_length=3, db_column='ChiantiRadTransType', blank=True)
    atomsymbol = models.CharField(max_length=24, db_column='AtomSymbol', blank=True)
    finalstateindex = models.ForeignKey(States, related_name='+', db_column='chiantiradtransfinalstateindex')
    initialstateindex = models.ForeignKey(States, related_name='+', db_column='chiantiradtransinitialstateindex')
    wavelengthexperimental = models.FloatField(null=True, db_column='wavelengthexperimental', blank=True)
    wavelengththeoretical = models.FloatField(null=True, db_column='wavelengththeoretical', blank=True)
    wavelength = models.FloatField(null=True, db_column='wavelength', blank=True)
    weightedoscillatorstrength = models.FloatField(null=True, db_column='RadTransProbabilityWeightedOscillatorStrength', blank=True)
    probabilitya = models.FloatField(null=True, db_column='RadTransProbabilityTransitionProbabilityA', blank=True)

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
