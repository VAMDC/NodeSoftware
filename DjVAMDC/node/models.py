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



class Source(models.Model):
    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

class Method(models.Model):
    class Meta:
        verbose_name = _('Method')
        verbose_name_plural = _('Methods')

class State(models.Model):
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')

class Atom(models.Model):
    class Meta:
        verbose_name = _('Atom')
        verbose_name_plural = _('Atoms')

class Molecule(models.Model):
    class Meta:
        verbose_name = _('Molecule')
        verbose_name_plural = _('Molecules')

class Particle(models.Model):
    class Meta:
        verbose_name = _('Particle')
        verbose_name_plural = _('Particle')

class Process(models.Model):
    class Meta:
        verbose_name = _('Process')
        verbose_name_plural = _('Processes')
