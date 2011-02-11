from django.db import models

# write your models here
# or autogenerate with inspectdb

# example models
class Species(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    ion = models.IntegerField()
    mass = models.DecimalField(max_digits=7, decimal_places=2)
    massno = models.IntegerField()
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
    energy = models.DecimalField(max_digits=17, decimal_places=4)
    upperstate = models.ForeignKey(State,related_name='upper')
    lowerstate = models.ForeignKey(State,related_name='lower')
