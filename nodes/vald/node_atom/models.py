from vald.node_common.models import *
#from ..node_common.models import *

class State(Model):
    id = IntegerField(primary_key=True, db_index=True)

    species = ForeignKey(Species, db_index=False)

    energy = DecimalField(max_digits=15, decimal_places=4,null=True, db_index=True)
    lande = DecimalField(max_digits=6, decimal_places=2,null=True)
    term_desc = CharField(max_length=86, null=True)

    energy_ref_id= RefCharField(max_length=7, null=True)
    lande_ref_id = RefCharField(max_length=7, null=True)
    level_ref_id = RefCharField(max_length=7, null=True)

    j = DecimalField(max_digits=3, decimal_places=1,db_column=u'J', null=True)
    l = PositiveSmallIntegerField(db_column=u'L', null=True)
    s = DecimalField(max_digits=3, decimal_places=1,db_column=u'S', null=True)
    p = DecimalField(max_digits=3, decimal_places=1,db_column=u'P', null=True)
    j1 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J1', null=True)
    j2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J2', null=True)
    k = DecimalField(max_digits=3, decimal_places=1,db_column=u'K', null=True)
    s2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'S2', null=True)
    jc = DecimalField(max_digits=3, decimal_places=1,db_column=u'Jc', null=True)
    sn = PositiveSmallIntegerField(db_column=u'Sn',null=True)
    n = PositiveSmallIntegerField(db_column=u'n',null=True)

    def jj(self):
        if None not in (self.j1, self.j2):
            return (self.j1, self.j2)
    def multiplicity(self):
        if self.s != None:
            return 2 * self.s + 1
    def __unicode__(self):
        return u'ID:%s Eng:%s'%(self.id,self.energy)

    def get_Components(self):
        """This is required in order to supply a Components property
        for the makeAtomsComponents tagmaker."""
        return self
    Components = property(get_Components)

    class Meta:
        db_table = u'states'


class Transition(Model):
    id = AutoField(primary_key=True)
    upstate = ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True, db_index=False)
    lostate = ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True, db_index=False)

    wave = DecimalField(max_digits=16, decimal_places=8, db_index=True)
    waveritz = DecimalField(max_digits=16, decimal_places=8, db_index=True)

    species = ForeignKey(Species, db_index=True)
    loggf = DecimalField(max_digits=8, decimal_places=3, null=True)
    einsteina = DecimalField(max_digits=20, decimal_places=3, db_index=True, null=True)
    gammarad = DecimalField(max_digits=6, decimal_places=2,null=True)
    gammastark = DecimalField(max_digits=7, decimal_places=3,null=True)
    gammawaals = DecimalField(max_digits=6, decimal_places=3,null=True)
    sigmawaals = PositiveSmallIntegerField(null=True)
    alphawaals = DecimalField(max_digits=6, decimal_places=3,null=True)

    # The accur tags are populated using the methods below
    accurflag = CharField(max_length=1, null=True) # VALD flag: N,E,C or P
    accur = DecimalField(max_digits=6, decimal_places=3, null=True)
    #comment = CharField(max_length=128, null=True)

    wave_ref_id = RefCharField(max_length=7, null=True)
    waveritz_ref_id = RefCharField(max_length=7, null=True)
    loggf_ref_id = RefCharField(max_length=7, null=True)
    gammarad_ref_id = RefCharField(max_length=7, null=True)
    gammastark_ref_id = RefCharField(max_length=7, null=True)
    waals_ref_id = RefCharField(max_length=7, null=True)

    wave_linelist = ForeignKey(LineList, related_name='iswavelinelist_trans', db_index=False) # needed for population
    #loggf_linelist = ForeignKey(LineList, related_name='isloggflinelist_trans', db_index=False)
    #gammarad_linelist = ForeignKey(LineList, related_name='isgammaradlinelist_trans', db_index=False)
    #gammastark_linelist = ForeignKey(LineList, related_name='isgammastarklinelist_trans', db_index=False)
    #waals_linelist = ForeignKey(LineList, related_name='iswaalslinelist_trans', db_index=False)

    transition_type = CharField(max_length=2, null=True)
    autoionized = NullBooleanField(default=False)

    # Method information. Since some xsams method categories are represented by more than one vald equivalent,
    # we need one field for restrictable's queries and returnable's queries respectively.
    # vald category mapping = {'exp':0, 'obs':1, 'emp':2, 'pred':3, 'calc':4, 'mix':5}
    # vald->xsams mapping = {0:'experiment', 1:'semiempirical', 2:'derived', 3:'theory',4:'semiempirical',5:'compilation'}
    # mapping between method_return and method_restrict = {0:0, 1:1, 2:2, 3:3, 4:1, 5:5} (i.e. xsams=semiempirical is represented in vald by both obs and calc (1 and 4)).

    method_return = PositiveSmallIntegerField(null=True, db_index=False) # this is the method category, populated in post-processing by parsing wave_linelist field
    method_restrict = PositiveSmallIntegerField(null=True, db_index=True) # this is the method category to restrict on, populated in post-processing.

    # helper extraction methods
    def get_waves(self):
        return self.wave, self.waveritz
    def get_wave_comments(self):
        return 'Vacuum wavelength from state energies (RITZ)','Vacuum wavelength from measurements (non-RITZ)'
    def get_wave_refs(self):
        return self.wave_ref_id, self.waveritz_ref_id
    def get_waals(self):
        if self.gammawaals: return self.gammawaals
        elif self.sigmawaals and self.alphawaals: return [self.sigmawaals, self.alphawaals]
        else: return ""
    def get_waals_name(self):
        if self.gammawaals: return "log(gamma)"
        elif self.sigmawaals and self.alphawaals: return ["log(gamma)", "alpha"]
        else: return ""
    def get_waals_units(self):
        if self.gammawaals: return "cm3/s"
        elif self.sigmawaals and self.alphawaals: return ["m", "unitless"]
        else: return ""
    def get_waals_function(self):
        if self.gammawaals: return "waals"
        elif self.sigmawaals and self.alphawaals: return "waals-barklem"
        else: return ""
    def get_accur_type(self):
        "retrieve the right AccurType type depending on the VALD accur flag"
        if self.accurflag in (u"N", u"E"): return u"estimated"
        elif self.accurflag == u'C': return u"arbitrary"
        elif self.accurflag == u'P': return u"systematic"
        else: return ""
    def get_accur_relative(self):
        "retrieve AccuracyRelative tag as true/false depending on VALD accur flag"
        return str(self.accurflag in (u"N", u"E", u"C")).lower() # returns true/false

# Don't calculate here, but directly using sql (kept here for reference)
#    def getEinsteinA(self):
#        "Calculate the einstein A"
#        return (0.667025e16 * 10**self.loggf) / ((2 * self.upstate.j + 1.0) * self.wave**2)

    def __unicode__(self):
        return u'ID:%s Wavel: %s' % (self.id, self.wave)
    class Meta:
        db_table = u'transitions'



