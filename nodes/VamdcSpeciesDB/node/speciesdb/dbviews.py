from django.db import models

# These are database VIEWS, not tables
class SpeciesList(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=120) # Combination of inchikey and any inchi suffix
    mass = models.IntegerField(blank=False)
    name = models.TextField(blank=True)
    structural_formula = models.TextField(blank=True)
    stoichiometric_formula = models.TextField(blank=True)

    class Meta:
        db_table = u'vamdc_view_species_list'
