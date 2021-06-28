
from django.db import models

class Job(models.Model):
    id        = models.CharField(max_length=37, primary_key=True)
    phase     = models.CharField(max_length=16)
    query     = models.CharField(max_length=1024)
    submitted = models.DateTimeField(auto_now_add=True)
    expiry    = models.DateTimeField()
    file      = models.CharField(max_length=1024)
    
    class Meta:
       db_table = 'jobs'



    