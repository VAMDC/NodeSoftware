from django.db import models
from django.utils.translation import ugettext_lazy as _

# def myvalidate(value):
#     print "myvalidate=%s" % value
#     return 

# class IntegerForeignKey(models.ForeignKey):
#     """
#     This custom field also accepts an integer value, if it
#     is given; this integer is assumed to match the pk value
#     of an existing reference. The use of this is an improved speed
#     during load but means less erro checking.    
#     """       

#     # def __init__(self, *args, **kwargs):
#     #     print "in __init__"
#     #     super(IntegerForeignKey, self).__init__(*args, **kwargs)
        
#     # def validate(self, value, model_instance):
#     #     """
#     #     Run a different validation
#     #     """        
#     #     print "validate"
#     #     print value
#     #     if isinstance(value, int):
#     #         # this is not a django object but an integer, so we assume this
#     #         # is in fact the pk of the object we are referencing. We don't error
#     #         # check this!
#     #         return True 
#     #         print self.field.attname            
#     #         setattr(instance, self.field.attname, value)
#     #     else:
#     #         # normal operation; this will raise a ValueError for all other
#     #         # problems
#     #         super(IntegerForeignKey, self).__validate__(instance, value)

#     # def get_attname(self):
#     #     print "get_attname"
#     #     return super(IntegerForeignKey, self).get_attname()

#     # def get_validator_unique_lookup_type(self):
#     #     print " get_validator_unique_lookup_type"
#     #     return super(IntegerForeignKey, self).get_validator_unique_lookup_type()

#     # def get_db_prep_save(self, value, connection):   
#     #     print "get_db_prep_save"
#     #     super(IntegerForeignKey, self).get_db_prep_save(value, connection)

#     # def formfield(self, **kwargs):
#     #     print "formfield"
#     #     return super(IntegerForeignKey, self).formfield(**kwargs)
        
#     # def db_type(self, connection):
#     #     print "db_type"
#     #     return super(IntegerForeignKey, self).db_type(connection)
        
#     __metaclass__ = models.SubfieldBase
    
#     def __init__(self, *args, **kwargs):
#         print "In creation!"
#         super(IntegerForeignKey, self).__init__(*args, **kwargs)
        
#     def __set__(self, instance, value):
#         """
#         Custom set operation when assigning to the field. 
#         """
#         print "test"
#         print instance, value
#         if isinstance(value, int):
#             # this is not a django object but an integer, so we assume this
#             # is in fact the pk of the object we are referencing. We don't error
#             # check this!
#             print self.field.attname            
#             setattr(instance, self.field.attname, value)
#         else:
#             # normal operation; this will raise a ValueError for all other
#             # problems
#             super(IntegerForeignKey, self).__set__(instance, value)
        
#     def get_internal_type(self):
#         return "ForeignKey"

class Species(models.Model):
    name = models.CharField(max_length=10, db_index=True)
    ion = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    mass = models.DecimalField(max_digits=5, decimal_places=2) 
    massno = models.PositiveSmallIntegerField(null=True, blank=True)
    ionen = models.DecimalField(max_digits=7, decimal_places=3) 
    solariso = models.DecimalField(max_digits=5, decimal_places=4) 
    ncomp = models.PositiveSmallIntegerField(null=True, blank=True)
    atomic = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    isotope = models.PositiveSmallIntegerField(null=True, blank=True)
    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.name)
    class Meta:
        db_table = u'species'
        verbose_name = _('Species')
        verbose_name_plural = _('Species')

class Publication(models.Model):
    dbref = models.CharField(max_length=64, db_index=True, unique=True)
    bibref = models.CharField(max_length=25, db_index=True)
    author = models.CharField(max_length = 512, db_index=True, null=True, blank=True)
    bibtex = models.CharField(max_length = 512, db_index=True)
    class Meta:
        db_table = u'publications'
        verbose_name = _('Publication')
        verbose_name_plural = _('Publications')
    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.dbref)

class Source(models.Model):
    srcfile = models.CharField(max_length=128)
    srcfile_ref = models.CharField(max_length=128, null=True)
    speclo = models.ForeignKey(Species,related_name='islowerboundspecies_source',db_column='speclo',null=True)
    spechi = models.ForeignKey(Species,related_name='isupperboundspecies_source',db_column='spechi',null=True)
    #publication = models.ForeignKey(Publication,related_name='publication_set',null=True)
    publications = models.ManyToManyField(Publication, symmetrical=False, related_name='publications_set', null=True)
    listtype = models.PositiveSmallIntegerField(null=True,blank=True)
    r1 = models.PositiveSmallIntegerField(null=True, blank=True)
    r2 = models.PositiveSmallIntegerField(null=True, blank=True)
    r3 = models.PositiveSmallIntegerField(null=True, blank=True)
    r4 = models.PositiveSmallIntegerField(null=True, blank=True)
    r5 = models.PositiveSmallIntegerField(null=True, blank=True)
    r6 = models.PositiveSmallIntegerField(null=True, blank=True)
    r7 = models.PositiveSmallIntegerField(null=True, blank=True)
    r8 = models.PositiveSmallIntegerField(null=True, blank=True)
    r9 = models.PositiveSmallIntegerField(null=True, blank=True)
    srcdescr = models.CharField(max_length=128, blank=True, null=True)
    def __unicode__(self):
        return u'ID%s: %s'%(self.id,self.srcdescr)
        
    class Meta:
        db_table = u'sources'
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')

class State(models.Model):
    charid = models.CharField(max_length=128, db_index=True,unique=True,null=False)
    species = models.ForeignKey(Species, db_column='species', db_index=True)#, validators=[myvalidate])    
    #species = models.PositiveSmallIntegerField()    
    energy = models.DecimalField(max_digits=15, decimal_places=4,null=True,blank=True, db_index=True) 
    lande = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    coupling = models.CharField(max_length=2, null=True,blank=True)
    term = models.CharField(max_length=56, null=True,blank=True)
    #energy_ref = models.ForeignKey(Source, db_index=True, related_name='isenergyref_state')
    #lande_ref = models.ForeignKey(Source, db_index=True, related_name='islanderef_state')
    #level_ref = models.ForeignKey(Source, db_index=True, related_name='islevelref_state')
    energy_ref = models.PositiveSmallIntegerField()
    lande_ref = models.PositiveSmallIntegerField()
    level_ref = models.PositiveSmallIntegerField()
    j = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'J', null=True,blank=True)
    l = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'L', null=True,blank=True)
    s = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'S', null=True,blank=True)
    p = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'P', null=True,blank=True)
    j1 = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'J1', null=True,blank=True)
    j2 = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'J2', null=True,blank=True)
    k = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'K', null=True,blank=True)
    s2 = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'S2', null=True,blank=True)
    jc = models.DecimalField(max_digits=3, decimal_places=1,db_column=u'Jc', null=True,blank=True)
    def __unicode__(self):
        return u'ID:%s Eng:%s'%(self.id,self.energy)

    class Meta:
        db_table = u'states'
        verbose_name = _('State')
        verbose_name_plural = _('States')

class Transition(models.Model):
    vacwave = models.DecimalField(max_digits=20, decimal_places=8) 
    airwave = models.DecimalField(max_digits=20, decimal_places=8) 
    species = models.ForeignKey(Species,db_column='species',related_name='isspecies_trans')
    #species = models.PositiveSmallIntegerField()
    loggf = models.DecimalField(max_digits=8, decimal_places=3,null=True,blank=True)
    landeff = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammarad = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammastark = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True) 
    gammawaals = models.DecimalField(max_digits=6, decimal_places=2,null=True,blank=True) 
    srctag = models.ForeignKey(Publication, db_column='publication', db_index=True, null=True)
    #acflag = models.CharField(max_length=1, blank=True,null=True)
    accur = models.CharField(max_length=11, blank=True,null=True)
    comment = models.CharField(max_length=128, null=True,blank=True)
    #wave_ref = models.ForeignKey(Source,db_column=u'wave_ref',related_name='iswaveref_trans')
    #loggf_ref = models.ForeignKey(Source,db_column=u'loggf_ref',related_name='isloggfref_trans')
    #lande_ref = models.ForeignKey(Source,db_column=u'lande_ref',related_name='islanderef_trans')
    #gammarad_ref = models.ForeignKey(Source,db_column=u'gammarad_ref',related_name='isgammaradref_trans')
    #gammastark_ref = models.ForeignKey(Source,db_column=u'gammastark_ref',related_name='isgammastarkref_trans')
    #gammawaals_ref = models.ForeignKey(Source,db_column=u'gammawaals_ref',related_name='isgammawaalsref_trans')
    wave_ref = models.PositiveSmallIntegerField()
    loggf_ref = models.PositiveSmallIntegerField()
    lande_ref = models.PositiveSmallIntegerField()
    gammarad_ref = models.PositiveSmallIntegerField()
    gammastark_ref = models.PositiveSmallIntegerField()
    gammawaals_ref = models.PositiveSmallIntegerField()

    upstate = models.ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True)
    lostate = models.ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True)
    upstateid = models.CharField(max_length=128,null=True)
    lostateid = models.CharField(max_length=128,null=True)
    
    def __unicode__(self):
        return u'ID:%s Wavel: %s'%(self.id,self.vacwave)
    class Meta:
        db_table = u'transitions'
        verbose_name = _('Transition')
        verbose_name_plural = _('Transitions')

# dynamically created models
            
class Query(models.Model):
    qid=models.CharField(max_length=6,primary_key=True,db_index=True)
    datetime=models.DateTimeField(auto_now_add=True)
    query=models.CharField(max_length=512)

class LogManager(models.Manager):
    """
    Handles log object searches
    """
    #def makeQID(self, length=6, chars=s.letters + s.digits):
    #    return ''.join([choice(chars) for i in xrange(length)])

    def create(self, request):
        """
        Create a query log based on a request
        """
        pass
    
class Log(models.Model):
    """
    Stores data of a query
    """
    qid = models.CharField(max_length=128)
    datetime = datetime=models.DateTimeField(auto_now_add=True)
    query = models.ForeignKey(Query, related_name='dbquery', db_column='query')
    request = models.TextField()

    objects = LogManager()
