from django.db.models import *

class Species(Model):
    id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    name = CharField(max_length=10, db_index=True)

class State(Model):
    id = CharField(max_length=255, primary_key=True, db_index=True)
    species = ForeignKey(Species)
    energy = DecimalField(max_digits=16, decimal_places=5,null=True,blank=True, db_index=True)
