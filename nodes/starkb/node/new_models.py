# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class TArticles(models.Model):
    id_article = models.IntegerField(primary_key=True)
    authors = models.TextField()
    publication_year = models.DecimalField(max_digits=5, decimal_places=0)
    id_journal = models.ForeignKey(TJournals, db_column='id_journal')
    volume = models.IntegerField()
    pages = models.CharField(max_length=120)
    title = models.TextField()
    method = models.CharField(max_length=30)
    ads_reference = models.TextField(blank=True)
    doi_reference = models.TextField(blank=True)
    other_reference = models.TextField(blank=True)
    class Meta:
        db_table = u't_articles'

class TArticlesDatasets(models.Model):
    id_article = models.ForeignKey(TArticles, db_column='id_article')
    id_dataset = models.ForeignKey(TDatasets, db_column='id_dataset')
    class Meta:
        db_table = u't_articles_datasets'

class TColliders(models.Model):
    id_collider = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=36)
    ionization = models.CharField(unique=True, max_length=15)
    ionization_decimal = models.IntegerField()
    class Meta:
        db_table = u't_colliders'

class TDatasets(models.Model):
    id_dataset = models.IntegerField(primary_key=True)
    id_target = models.ForeignKey(TTargets, db_column='id_target')
    has_proton = models.IntegerField()
    filename = models.TextField()
    creation_date = models.DateField()
    description = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = u't_datasets'

class TDatasetsColliders(models.Model):
    id_dataset = models.ForeignKey(TDatasets, db_column='id_dataset')
    id_collider = models.ForeignKey(TColliders, db_column='id_collider')
    class Meta:
        db_table = u't_datasets_colliders'

class TJournals(models.Model):
    id_journal = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=225)
    class Meta:
        db_table = u't_journals'

class TLevels(models.Model):
    id_level = models.IntegerField(primary_key=True)
    id_dataset = models.ForeignKey(TDatasets, db_column='id_dataset')
    config = models.CharField(unique=True, max_length=60)
    term = models.CharField(unique=True, max_length=36)
    j = models.CharField(unique=True, max_length=15, blank=True)
    class Meta:
        db_table = u't_levels'

class TTargets(models.Model):
    id_target = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=15)
    ionization = models.CharField(unique=True, max_length=18)
    ionization_decimal = models.IntegerField()
    class Meta:
        db_table = u't_targets'

class TTemperatures(models.Model):
    id_temperature = models.IntegerField(primary_key=True)
    id_transitiondata = models.ForeignKey(TTransitiondata, db_column='id_transitiondata')
    temperature = models.IntegerField(unique=True)
    a = models.FloatField(null=True, blank=True)
    n_we = models.CharField(max_length=24)
    we = models.FloatField(null=True, blank=True)
    n_de = models.CharField(max_length=24)
    de = models.FloatField(null=True, blank=True)
    n_wp = models.CharField(max_length=24, blank=True)
    wp = models.FloatField(null=True, blank=True)
    n_dp = models.CharField(max_length=24, blank=True)
    dp = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u't_temperatures'

class TTemperaturesColliders(models.Model):
    id_temperature = models.ForeignKey(TTemperatures, db_column='id_temperature')
    id_collider = models.ForeignKey(TColliders, db_column='id_collider')
    n_w = models.CharField(max_length=24, blank=True)
    w = models.FloatField(null=True, blank=True)
    n_d = models.CharField(max_length=24, blank=True)
    d = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u't_temperatures_colliders'

class TTransitiondata(models.Model):
    id_transitiondata = models.IntegerField(primary_key=True)
    id_transition = models.ForeignKey(TTransitions, db_column='id_transition')
    density = models.FloatField(unique=True)
    c = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u't_transitiondata'

class TTransitions(models.Model):
    id_transition = models.IntegerField(primary_key=True)
    id_dataset = models.ForeignKey(TDatasets, db_column='id_dataset')
    lower_level = models.ForeignKey(TLevels, db_column='lower_level')
    upper_level = models.ForeignKey(TLevels, db_column='upper_level')
    multiplet = models.CharField(max_length=24, blank=True)
    wavelength = models.FloatField()
    class Meta:
        db_table = u't_transitions'

class VTransitions(models.Model):
    id_transition = models.IntegerField()
    id_dataset = models.IntegerField()
    lower_config = models.CharField(max_length=60)
    lower_term = models.CharField(max_length=36)
    lower_j = models.CharField(max_length=15, blank=True)
    upper_config = models.CharField(max_length=60)
    upper_term = models.CharField(max_length=36)
    upper_j = models.CharField(max_length=15, blank=True)
    multiplet = models.CharField(max_length=24, blank=True)
    wavelength = models.FloatField()
    class Meta:
        db_table = u'v_transitions'

