from django.db import models

# Create your models here.

class Query(models.Model):
    qid=models.CharField(max_length=6,primary_key=True,db_index=True)
    datetime=models.DateTimeField(auto_now_add=True)
    query=models.CharField(max_length=512)
