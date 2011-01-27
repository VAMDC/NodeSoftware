from django.db import models

class Usage(models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return u'%s'%self.name

class KeyWord(models.Model):
    name = models.CharField(max_length=256)
    sdescr = models.TextField('Short description')
    ldescr = models.TextField('Long description')
    type = models.CharField('Data type',max_length=1, choices=( ('s','String'),
                                                    ('i','Integer'),
                                                    ('f','Float'),
                                                    ('b','Boolean'),
                                                  ),
                            null=True,blank=True)
    constr = models.CharField('Constraint',max_length=256,null=True,blank=True)
    unit = models.CharField('Unit',max_length=256,null=True,blank=True)
    usage = models.ManyToManyField(Usage,null=True,blank=True)
    block = models.CharField('XSAMS block',max_length=2, choices=( \
                                                    ('so','Sources'),
                                                    ('as','Atomic States'),
                                                    ('ms','Molecular States'),
                                                    ('mq','Molecular Quantum Numbers'),
                                                    ('ct','Collisional Transitions'),
                                                    ('rt','Radiative Transitions'),
                                                    ('me','Methods'),
                                                    ('mo','Molecules'),
                                                    ('at','Atoms'),
                                                    ('sp','Species'),
                                                  ),
                            null=True,blank=True)


    def __unicode__(self):
        return u'%s'%self.name

    class Meta:
        ordering = ["name"]
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'

