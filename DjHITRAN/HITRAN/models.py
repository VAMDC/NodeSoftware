# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class AllStates(models.Model):
    molecid = models.IntegerField(null=True, db_column='molecID', blank=True) # Field name made lowercase.
    isoid = models.IntegerField(null=True, db_column='isoID', blank=True) # Field name made lowercase.
    stateid = models.CharField(max_length=192, primary_key=True, db_column='stateID') # Field name made lowercase.
    assigned = models.IntegerField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    energy_err = models.FloatField(null=True, blank=True)
    energy_flag = models.CharField(max_length=3, blank=True)
    g = models.IntegerField(null=True, blank=True)
    caseid = models.IntegerField(null=True, db_column='caseID', blank=True) # Field name made lowercase.
    elecstatelabel = models.CharField(max_length=3, db_column='ElecStateLabel', blank=True) # Field name made lowercase.
    qn1 = models.IntegerField(null=True, db_column='QN1', blank=True) # Field name made lowercase.
    qn2 = models.IntegerField(null=True, db_column='QN2', blank=True) # Field name made lowercase.
    qn3 = models.IntegerField(null=True, db_column='QN3', blank=True) # Field name made lowercase.
    qn4 = models.IntegerField(null=True, db_column='QN4', blank=True) # Field name made lowercase.
    qn5 = models.IntegerField(null=True, db_column='QN5', blank=True) # Field name made lowercase.
    qn6 = models.IntegerField(null=True, db_column='QN6', blank=True) # Field name made lowercase.
    qn7 = models.IntegerField(null=True, db_column='QN7', blank=True) # Field name made lowercase.
    qn8 = models.IntegerField(null=True, db_column='QN8', blank=True) # Field name made lowercase.
    qn9 = models.IntegerField(null=True, db_column='QN9', blank=True) # Field name made lowercase.
    qn10 = models.IntegerField(null=True, db_column='QN10', blank=True) # Field name made lowercase.
    sym1 = models.CharField(max_length=12, db_column='Sym1', blank=True) # Field name made lowercase.
    sym2 = models.CharField(max_length=12, db_column='Sym2', blank=True) # Field name made lowercase.
    sym3 = models.CharField(max_length=12, db_column='Sym3', blank=True) # Field name made lowercase.
    sym4 = models.CharField(max_length=12, db_column='Sym4', blank=True) # Field name made lowercase.
    sym5 = models.CharField(max_length=12, db_column='Sym5', blank=True) # Field name made lowercase.
    sym6 = models.CharField(max_length=12, db_column='Sym6', blank=True) # Field name made lowercase.
    sym7 = models.CharField(max_length=12, db_column='Sym7', blank=True) # Field name made lowercase.
    sym8 = models.CharField(max_length=12, db_column='Sym8', blank=True) # Field name made lowercase.
    sym9 = models.CharField(max_length=12, db_column='Sym9', blank=True) # Field name made lowercase.
    sym10 = models.CharField(max_length=12, db_column='Sym10', blank=True) # Field name made lowercase.
    sqn1 = models.IntegerField(null=True, db_column='sQN1', blank=True) # Field name made lowercase.
    sqn2 = models.IntegerField(null=True, db_column='sQN2', blank=True) # Field name made lowercase.
    sqn3 = models.IntegerField(null=True, db_column='sQN3', blank=True) # Field name made lowercase.
    sqn4 = models.IntegerField(null=True, db_column='sQN4', blank=True) # Field name made lowercase.
    sqn5 = models.IntegerField(null=True, db_column='sQN5', blank=True) # Field name made lowercase.
    timestamp = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'all_states'

class Refs(models.Model):
    sourceid = models.CharField(max_length=192, primary_key=True, db_column='sourceID') # Field name made lowercase.
    type = models.CharField(max_length=96, blank=True)
    author = models.TextField(blank=True)
    title = models.TextField(blank=True)
    journal = models.TextField(blank=True)
    volume = models.CharField(max_length=30, blank=True)
    pages = models.CharField(max_length=60, blank=True)
    year = models.TextField(blank=True) # This field type is a guess.
    institution = models.TextField(blank=True)
    note = models.TextField(blank=True)
    doi = models.CharField(max_length=192, blank=True)
    class Meta:
        db_table = u'refs'

class Trans(models.Model):
    molec_name = models.CharField(max_length=60)
    isoid = models.IntegerField(db_column='isoID') # Field name made lowercase.
    nu = models.FloatField()
    nu_err = models.FloatField(null=True, blank=True)
    nu_ref = models.CharField(max_length=93, blank=True)
    initialstateref = models.CharField(max_length=192, db_column='InitialStateRef', blank=True) # Field name made lowercase.
    finalstateref = models.CharField(max_length=192, db_column='FinalStateRef', blank=True) # Field name made lowercase.
    s = models.FloatField(null=True, db_column='S', blank=True) # Field name made lowercase.
    s_err = models.FloatField(null=True, db_column='S_err', blank=True) # Field name made lowercase.
    s_ref = models.CharField(max_length=90, db_column='S_ref', blank=True) # Field name made lowercase.
    a = models.FloatField(null=True, db_column='A', blank=True) # Field name made lowercase.
    a_err = models.FloatField(null=True, db_column='A_err', blank=True) # Field name made lowercase.
    a_ref = models.CharField(max_length=90, db_column='A_ref', blank=True) # Field name made lowercase.
    multipole = models.CharField(max_length=6, blank=True)
    g_air = models.FloatField(null=True, blank=True)
    g_air_err = models.FloatField(null=True, blank=True)
    g_air_ref = models.CharField(max_length=102, blank=True)
    g_self = models.FloatField(null=True, blank=True)
    g_self_err = models.FloatField(null=True, blank=True)
    g_self_ref = models.CharField(max_length=105, blank=True)
    n_air = models.FloatField(null=True, blank=True)
    n_air_err = models.FloatField(null=True, blank=True)
    n_air_ref = models.CharField(max_length=102, blank=True)
    delta_air = models.FloatField(null=True, blank=True)
    delta_air_err = models.FloatField(null=True, blank=True)
    delta_air_ref = models.CharField(max_length=120, blank=True)
    elower = models.FloatField(null=True, db_column='Elower', blank=True) # Field name made lowercase.
    gp = models.IntegerField(null=True, blank=True)
    gpp = models.IntegerField(null=True, blank=True)
    line_number = models.IntegerField(null=True, blank=True)
    timestamp = models.IntegerField(null=True, blank=True)
    ierr = models.CharField(max_length=18, db_column='Ierr', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'trans'

class Molecules(models.Model):
	molec_id = models.IntegerField(primary_key=True, null=False)
	molec_name = models.CharField(max_length=20, null=False)
	molec_name_html = models.CharField(max_length=128, null=False)
	molec_name_latex = models.CharField(max_length=128, null=False)
	stoichiometric_formula = models.CharField(max_length=40, null=False)
	chemical_names = models.CharField(max_length=256)
	case_id = models.IntegerField(null=False)
	class Meta:
        	db_table = u'molecules'
