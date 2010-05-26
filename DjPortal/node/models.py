from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

def allownull__init__(self,*args,**kwargs):
    super(type(self), self).__init__(self,*args, **kwargs) 
    self.null=True
    self.blank=True
   
    
    
class CharFieldN(models.CharField):
    __init__=allownull__init__

class FloatFieldN(models.FloatField):
    __init__=allownull__init__

class IntegerFieldN(models.IntegerField):
    __init__=allownull__init__

#################################################################

class Source(models.Model):
    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
    sourceID=models.CharField(max_length=64,primary_key=True)
    #Category=
    #Year=
    #SourceName=
    #Volume=
    #PageBegin=
    
class Author(models.Model):
    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
    Source=models.ForeignKey(Source,related_name='Authors')
    Name=models.CharField(max_length=64)

################################################################

class Method(models.Model):
    class Meta:
        verbose_name = _('Method')
        verbose_name_plural = _('Methods')
    methodID=models.CharField(max_length=64,primary_key=True)
    #Category=
    #Description=
 

################################################################

class AtomicState(models.Model):
    class Meta:
        verbose_name = _('AtomicState')
        verbose_name_plural = _('AtomicStates')
    stateID=models.CharField(max_length=64,primary_key=True)
    Description=models.CharField(max_length=64)
    

class Isotope(models.Model):
    class Meta:
        verbose_name = _('Isotope')
        verbose_name_plural = _('Isotopes')
    
class Atom(models.Model):
    class Meta:
        verbose_name = _('Atom')
        verbose_name_plural = _('Atoms')
    AtomicState=models.ForeignKey(AtomicState)

################################################################

class MolecularState(models.Model):
    class Meta:
        verbose_name = _('Molecule')
        verbose_name_plural = _('Molecules')
    
class Molecule(models.Model):
    class Meta:
        verbose_name = _('Molecule')
        verbose_name_plural = _('Molecules')
    MolecularState=models.ForeignKey(MolecularState)

class Particle(models.Model):
    class Meta:
        verbose_name = _('Particle')
        verbose_name_plural = _('Particle')

###############################################################

class Process(models.Model):
    class Meta:
        verbose_name = _('Process')
        verbose_name_plural = _('Processes')
