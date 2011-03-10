from django.db import models

# write your models here
# or autogenerate with inspectdb

# example models
class Species(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=3)
    ion = models.IntegerField()
    mass = models.DecimalField(max_digits=7, decimal_places=2)
    class Meta:
        db_table = u'species'   # if you want the table to be
				# named differently than the model

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    species = models.ForeignKey(Species)
    energy = models.DecimalField(max_digits=17, decimal_places=4)

class Transition(models.Model):
    id = models.IntegerField(primary_key=True)
    species = models.ForeignKey(Species)
    upper_state = models.ForeignKey(State, related_name='transup')
    lower_state = models.ForeignKey(State, related_name='translo')
    wavelength = FloatField()
