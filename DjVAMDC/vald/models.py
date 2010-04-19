from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

class Transition(models.Model):
    class Meta:
        verbose_name = _('Transition')
        verbose_name_plural = _('Transitions')


class State(models.Model):
    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')


class Source(models.Model):
    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

class Species(models.Model):
    class Meta:
        verbose_name = _('Species')
        verbose_name_plural = _('Species')

