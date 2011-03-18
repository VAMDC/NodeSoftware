from django.db.models import *
from vamdctap.bibtextools import *

class ScientificNotationField(CharField):
    """
    This field preserves scientific notation for storing very big or small numbers.
    """    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 25
        super(ScientificNotationField, self).__init__(*args, **kwargs)
    def to_python(self, value):
        if value == None: 
            return None
        return float('%e' % float(value))
  
class Species(Model):
    id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    name = CharField(max_length=10, db_index=True)
    ion = PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    mass = DecimalField(max_digits=8, decimal_places=5) 
    massno = PositiveSmallIntegerField(null=True, blank=True)
    ionen_ev = DecimalField(max_digits=7, decimal_places=3)
    ionen_cm1 = DecimalField(max_digits=14, decimal_places=3)
    atomic = PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    isotope = PositiveSmallIntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.name)
    class Meta:
        db_table = u'species'

class Reference(Model):
    id = CharField(max_length=64, primary_key=True, db_index=True)
    bibtex = TextField(null=True)

    def XML(self):
        return BibTeX2XML( self.bibtex )

    class Meta:
        db_table = u'refs'
    def __unicode__(self):
        return u'%s'%self.id

class State(Model):
    id = CharField(max_length=255, primary_key=True, db_index=True)
    species = ForeignKey(Species) 

    energy = DecimalField(max_digits=16, decimal_places=5,null=True,blank=True, db_index=True) 
    config = CharField(max_length=46, null=True, blank=True)
    lande = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    coupling = CharField(max_length=2, null=True,blank=True)
    term = CharField(max_length=56, null=True,blank=True)
    j = DecimalField(max_digits=3, decimal_places=1,db_column=u'J', null=True,blank=True)
    l = DecimalField(max_digits=3, decimal_places=1,db_column=u'L', null=True,blank=True)
    s = DecimalField(max_digits=3, decimal_places=1,db_column=u'S', null=True,blank=True)
    p = DecimalField(max_digits=3, decimal_places=1,db_column=u'P', null=True,blank=True)
    j1 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J1', null=True,blank=True)
    j2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J2', null=True,blank=True)
    k = DecimalField(max_digits=3, decimal_places=1,db_column=u'K', null=True,blank=True)
    s2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'S2', null=True,blank=True)
    jc = DecimalField(max_digits=3, decimal_places=1,db_column=u'Jc', null=True,blank=True)
    f_hfs = DecimalField(max_digits=3, decimal_places=1,db_column=u'f_hfs', null=True,blank=True) #

    #hyperfine structure
    hfs_a = DecimalField(max_digits=16, decimal_places=5, db_column=u'hfs_a', null=True,blank=True)
    hfs_b = DecimalField(max_digits=16, decimal_places=5, db_column=u'hfs_b', null=True,blank=True)        
    hfs_accur = DecimalField(max_digits=16, decimal_places=5, db_column=u'hfs_accur', null=True,blank=True)        
  
    hfs_ref = ForeignKey(Reference, related_name='ishfsref_state', null=True)

    # half-time
    tau_exp = ScientificNotationField(db_column=u'tau_exp',null=True,blank=True)
    #tau_exp = DecimalField(max_digits=8, decimal_places=4,db_column=u'tau_exp', null=True,blank=True)
    tau_calc = ScientificNotationField(db_column=u'tau_calc',null=True,blank=True)
    #tau_calc = DecimalField(max_digits=8, decimal_places=4,db_column=u'tau_calc', null=True,blank=True)
    tau_accur = ScientificNotationField(db_column=u'tau_accur',null=True,blank=True)
    #tau_accur = DecimalField(max_digits=8, decimal_places=4,db_column=u'tau_accur', null=True,blank=True)
    tau_exp_ref = ForeignKey(Reference, related_name='istau_exp_state', null=True)
    tau_calc_ref = ForeignKey(Reference, related_name='istau_calc_state',null=True)
    energy_ref = ForeignKey(Reference, related_name='isenergyref_state', null=True)
    lande_ref = ForeignKey(Reference, related_name='islanderef_state', null=True)
    level_ref = ForeignKey(Reference, related_name='islevelref_state', null=True)

    def get_best_tau(self):
        if self.tau_exp:
            return self.tau_exp
        else:
            return self.tau_calc
    def get_tau_ref(self):
        if self.tau_exp:
            return "LifetimeEXP"
        else:
            return "LifetimeTHEO"
        

    
    def __unicode__(self):
        return u'ID:%s Eng:%s'%(self.id,self.energy)
    class Meta:
        db_table = u'states'

class Transition(Model):
    id = AutoField(primary_key=True)
    upstate = ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True)
    lostate = ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True)
    
    vacwave = DecimalField(max_digits=20, decimal_places=8, db_index=True, null=True)     
    wavenum = DecimalField(max_digits=20, decimal_places=8, db_index=True, null=True) #
    airwave = DecimalField(max_digits=20, decimal_places=8, db_index=True, null=True) 
    species = ForeignKey(Species,db_column='species')
    loggf = DecimalField(max_digits=8, decimal_places=3,null=True,blank=True)
    loggf_method = CharField(max_length=4, null=True, blank=True) # "obs" / "calc"
    landeff = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammarad = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammastark = DecimalField(max_digits=7, decimal_places=3,null=True,blank=True)     
    gammawaals = DecimalField(max_digits=6, decimal_places=3,null=True,blank=True)    

    wave_accur = DecimalField(max_digits = 9, decimal_places=4,db_column=u'wave_accur', null=True,blank=True)        
    loggf_accur = DecimalField(max_digits = 9, decimal_places=4,db_column=u'loggf_accur', null=True,blank=True)        
    comment = CharField(max_length=128, null=True,blank=True)

    transition_ref = ForeignKey(Reference, null=True)
    wave_ref = ForeignKey(Reference, related_name='iswaveref_trans',null=True)
    loggf_ref = ForeignKey(Reference, related_name='isloggf_ref_trans',null=True)
    lande_ref = ForeignKey(Reference, related_name='islanderef_trans',null=True)
    gammarad_ref = ForeignKey(Reference, related_name='isgammaradref_trans',null=True)
    gammastark_ref = ForeignKey(Reference, related_name='isgammastarkref_trans',null=True)
    waals_ref = ForeignKey(Reference, related_name='iswaalsref_trans',null=True)
        
    def __unicode__(self):
        return u'ID:%s Wavel: %s'%(self.id,self.vacwave)
    class Meta:
        db_table = u'transitions'
