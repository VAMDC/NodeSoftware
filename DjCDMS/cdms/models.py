# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class StatesMolecules(models.Model):
    resource = models.CharField(max_length=12, db_column='Resource') # Field name made lowercase.
    stateid = models.IntegerField(primary_key=True, db_column='StateID') # Field name made lowercase.
    moleculeid = models.IntegerField(db_column='MoleculeID') # Field name made lowercase.
    chemicalname = models.CharField(max_length=600, db_column='ChemicalName', blank=True) # Field name made lowercase.
    molecularchemicalspecies = models.CharField(max_length=600, db_column='MolecularChemicalSpecies') # Field name made lowercase.
    isotopomer = models.CharField(max_length=300, db_column='Isotopomer', blank=True) # Field name made lowercase.
    stateenergyvalue = models.FloatField(null=True, db_column='StateEnergyValue', blank=True) # Field name made lowercase.
    stateenergyunit = models.CharField(max_length=12, db_column='StateEnergyUnit') # Field name made lowercase.
    stateenergyaccuracy = models.FloatField(null=True, db_column='StateEnergyAccuracy', blank=True) # Field name made lowercase.
    mixingcoefficient = models.FloatField(null=True, db_column='MixingCoefficient', blank=True) # Field name made lowercase.
    statenuclearstatisticalweight = models.IntegerField(null=True, db_column='StateNuclearStatisticalWeight', blank=True) # Field name made lowercase.
    qn_rotstate = models.CharField(max_length=1500, db_column='QN_RotState', blank=True) # Field name made lowercase.
    qn_vibstate = models.CharField(max_length=1500, db_column='QN_VibState', blank=True) # Field name made lowercase.
    qn_elecstate = models.CharField(max_length=300, db_column='QN_ElecState', blank=True) # Field name made lowercase.
    qn_string = models.CharField(max_length=1500, db_column='QN_String', blank=True) # Field name made lowercase.
    egy_qn_tag = models.IntegerField(null=True, db_column='EGY_QN_Tag', blank=True) # Field name made lowercase.
    egy_qn1 = models.IntegerField(null=True, db_column='EGY_QN1', blank=True) # Field name made lowercase.
    egy_qn2 = models.IntegerField(null=True, db_column='EGY_QN2', blank=True) # Field name made lowercase.
    egy_qn3 = models.IntegerField(null=True, db_column='EGY_QN3', blank=True) # Field name made lowercase.
    egy_qn4 = models.IntegerField(null=True, db_column='EGY_QN4', blank=True) # Field name made lowercase.
    egy_qn5 = models.IntegerField(null=True, db_column='EGY_QN5', blank=True) # Field name made lowercase.
    egy_qn6 = models.IntegerField(null=True, db_column='EGY_QN6', blank=True) # Field name made lowercase.
    e_id = models.IntegerField(db_column='E_ID') # Field name made lowercase.
    egy_dat_id = models.IntegerField(null=True, db_column='EGY_DAT_ID', blank=True) # Field name made lowercase.
    e_tag = models.IntegerField(db_column='E_Tag') # Field name made lowercase.
    class Meta:
        db_table = u'StatesMolecules'
    


class RadiativeTransitions(models.Model):
    resource = models.CharField(max_length=12, db_column='Resource') # Field name made lowercase.
    radiativetransitionid = models.IntegerField(primary_key=True, db_column='RadiativeTransitionID') # Field name made lowercase.
    moleculeid = models.IntegerField(db_column='MoleculeID') # Field name made lowercase.
    chemicalname = models.CharField(max_length=600, db_column='ChemicalName', blank=True) # Field name made lowercase.
    molecularchemicalspecies = models.CharField(max_length=600, db_column='MolecularChemicalSpecies') # Field name made lowercase.
    isotopomer = models.CharField(max_length=300, db_column='Isotopomer', blank=True) # Field name made lowercase.
    energywavelength = models.CharField(max_length=27, db_column='EnergyWavelength') # Field name made lowercase.
    wavelengthwavenumber = models.CharField(max_length=33, db_column='WavelengthWavenumber') # Field name made lowercase.
    frequencyvalue = models.FloatField(null=True, db_column='FrequencyValue', blank=True) # Field name made lowercase.
    frequencyunit = models.CharField(max_length=9, db_column='FrequencyUnit') # Field name made lowercase.
    energywavelengthaccuracy = models.FloatField(null=True, db_column='EnergyWavelengthAccuracy', blank=True) # Field name made lowercase.
    multipole = models.CharField(max_length=6, db_column='Multipole') # Field name made lowercase.
    log10weightedoscillatorstrengthvalue = models.FloatField(null=True, db_column='Log10WeightedOscillatorStrengthValue', blank=True) # Field name made lowercase.
    log10weightedoscillatorstrengthunit = models.CharField(max_length=24, db_column='Log10WeightedOscillatorStrengthUnit') # Field name made lowercase.
    lowerstateenergyvalue = models.FloatField(null=True, db_column='LowerStateEnergyValue', blank=True) # Field name made lowercase.
    lowerstateenergyunit = models.CharField(max_length=12, db_column='LowerStateEnergyUnit') # Field name made lowercase.
    upperstatenuclearstatisticalweight = models.IntegerField(null=True, db_column='UpperStateNuclearStatisticalWeight', blank=True) # Field name made lowercase.
    initialstateref = models.IntegerField(null=True, db_column='InitialStateRef', blank=True) # Field name made lowercase.
    finalstateref = models.IntegerField(null=True, db_column='FinalStateRef', blank=True) # Field name made lowercase.
    caseqn = models.IntegerField(null=True, db_column='CaseQN', blank=True) # Field name made lowercase.
    qn_up_1 = models.IntegerField(null=True, db_column='QN_Up_1', blank=True) # Field name made lowercase.
    qn_up_2 = models.IntegerField(null=True, db_column='QN_Up_2', blank=True) # Field name made lowercase.
    qn_up_3 = models.IntegerField(null=True, db_column='QN_Up_3', blank=True) # Field name made lowercase.
    qn_up_4 = models.IntegerField(null=True, db_column='QN_Up_4', blank=True) # Field name made lowercase.
    qn_up_5 = models.IntegerField(null=True, db_column='QN_Up_5', blank=True) # Field name made lowercase.
    qn_up_6 = models.IntegerField(null=True, db_column='QN_Up_6', blank=True) # Field name made lowercase.
    qn_low_1 = models.IntegerField(null=True, db_column='QN_Low_1', blank=True) # Field name made lowercase.
    qn_low_2 = models.IntegerField(null=True, db_column='QN_Low_2', blank=True) # Field name made lowercase.
    qn_low_3 = models.IntegerField(null=True, db_column='QN_Low_3', blank=True) # Field name made lowercase.
    qn_low_4 = models.IntegerField(null=True, db_column='QN_Low_4', blank=True) # Field name made lowercase.
    qn_low_5 = models.IntegerField(null=True, db_column='QN_Low_5', blank=True) # Field name made lowercase.
    qn_low_6 = models.IntegerField(null=True, db_column='QN_Low_6', blank=True) # Field name made lowercase.
    e_id = models.IntegerField(db_column='E_ID') # Field name made lowercase.
    e_tag = models.IntegerField(db_column='E_Tag') # Field name made lowercase.
    e_states = models.CharField(max_length=600, db_column='E_States', blank=True) # Field name made lowercase.
    e_name = models.CharField(max_length=600, db_column='E_Name') # Field name made lowercase.
    class Meta:
        db_table = u'RadiativeTransitions'

    initialstate = models.ForeignKey(StatesMolecules, related_name='isinitialstate',
                                db_column='InitialStateRef', null=False)

    finalstate   = models.ForeignKey(StatesMolecules, related_name='isfinalstate',
                                db_column='FinalStateRef', null=False)


class MolecularQuantumNumbers(models.Model): 

    stateid = models.IntegerField(primary_key=True, db_column='StateID')
    case = models.CharField(max_length=10, db_column='Case')
    label = models.CharField(max_length=50, db_column='Label')
    value = models.CharField(max_length=100, db_column='Value')
    spinref = models.CharField(max_length=100, db_column='SpinRef')
    attribute = models.CharField(max_length=100, db_column='Attribute')

    class Meta:
        db_table = 'V_MolQN'

    statesmolecules = models.ForeignKey(StatesMolecules, related_name='quantumnumbers', 
                            db_column='StateID')



class SourcesIDRefs(models.Model):
    rlId  = models.IntegerField(primary_key=True, db_column='RL_ID')
    rId   = models.IntegerField(null=True, db_column='RL_R_ID')
    eId   = models.IntegerField(null=True, db_column='RL_E_ID')
    datId = models.IntegerField(null=True, db_column='RL_DAT_ID', blank=True)
    fId   = models.IntegerField(null=True, db_column='RL_F_ID', blank=True)
    class Meta:
        db_table = u'ReferenceList'

    stateReferenceId = models.ForeignKey(StatesMolecules, related_name='isStateRefId',
                                db_column='eId', null=False)

class Sources(models.Model):
    rId       = models.IntegerField(primary_key=True, db_column='R_ID')
    authors   = models.CharField(max_length=500, db_column='R_Authors', blank=True)
    category  = models.CharField(max_length=100, db_column='R_Category', blank=True)
    name      = models.CharField(max_length=200, db_column='R_SourceName', blank=True)
    year      = models.IntegerField(null=True, db_column='R_Year', blank=True)
    vol       = models.CharField(max_length=20, db_column='R_Volume', blank=True)
    doi       = models.CharField(max_length=50, db_column='R_DOI', blank=True)
    pageBegin = models.CharField(max_length=10, db_column='R_PageBegin', blank=True)
    pageEnd   = models.CharField(max_length=10, db_column='R_PageEnd', blank=True)
    uri       = models.CharField(max_length=100, db_column='R_URI', blank=True)
    publisher = models.CharField(max_length=300, db_column='R_Publisher', blank=True)
    city      = models.CharField(max_length=80, db_column='R_City', blank=True)
    editors   = models.CharField(max_length=300, db_column='R_Editors', blank=True)
    productionDate = models.DateField(max_length=12, db_column='R_ProductionDate', blank=True)
    version   = models.CharField(max_length=20, db_column='R_Version', blank=True)
    comments  = models.CharField(max_length=100, db_column='R_Comments', blank=True)
    class Meta:
        db_table = u'ReferenceBib'

    referenceId = models.ForeignKey(SourcesIDRefs, related_name='isRefId',
                                db_column='rId', null=False)

