from django.db import models

class Usage(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return u'%s'%self.name

class KeyWord(models.Model):
    name = models.CharField(max_length=256)
    sdescr = models.TextField('Short description')
    ldescr = models.TextField('Long description')
    type = models.CharField('Type',max_length=1, choices=( ('s','String'),
                                                    ('i','Integer'),
                                                    ('f','Float'),
                                                    ('b','Boolean'),
                                                  ),
                            null=True,blank=True)
    constr = models.CharField('Constraint',max_length=256,null=True,blank=True)
    unit = models.CharField('Unit',max_length=256,null=True,blank=True)
    usage = models.ManyToManyField(Usage,null=True,blank=True)
    block = models.CharField('XSAMS block',max_length=2, choices=( \
                                                    ('at','Atoms'),
                                                    ('as','Atomic States'),
                                                    ('mo','Molecules'),
                                                    ('ms','Molecular States'),
                                                    ('mq','Molecular Quantum Numbers'),
                                                    ('ct','Collisional Transitions'),
                                                    ('rt','Radiative Transitions'),
                                                    ('nr','Non-Radiative Transitions'),
                                                    ('me','Methods'),
                                                    ('fu','Functions'),
                                                    ('en','Environments'),
                                                    ('so','Sources'),
                                                  ),
                            null=True,blank=True)
    datatype = models.BooleanField('DataType in XSAMS?',default=False)

    def list_usages(self):
        return ', '.join([u.name for u in self.usage.all()])

    def __unicode__(self):
        return u'%s'%self.name

    class Meta:
        ordering = ["name"]
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'

