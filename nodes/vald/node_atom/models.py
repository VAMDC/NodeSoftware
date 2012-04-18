from vald.node_common.models import *
#from ..node_common.models import *

class State(Model):
    id = IntegerField(primary_key=True, db_index=True)

    species = ForeignKey(Species, db_index=False)

    energy = DecimalField(max_digits=15, decimal_places=4,null=True, db_index=True)
    lande = DecimalField(max_digits=6, decimal_places=2,null=True)
    #coupling = CharField(max_length=2, null=True)
    #term = CharField(max_length=56, null=True)

    energy_ref = ForeignKey(Reference, related_name='isenergyref_state', db_index=False)
    lande_ref = ForeignKey(Reference, related_name='islanderef_state', db_index=False)
    level_ref = ForeignKey(Reference, related_name='islevelref_state', db_index=False)

    #energy_linelist = ForeignKey(LineList, related_name='isenergylinelist_state', db_index=False)
    #lande_linelist = ForeignKey(LineList, related_name='islandelinelist_state', db_index=False)
    #level_linelist = ForeignKey(LineList, related_name='islevellinelist_state', db_index=False)

    j = DecimalField(max_digits=3, decimal_places=1,db_column=u'J', null=True)
    l = PositiveSmallIntegerField(db_column=u'L', null=True)
    s = DecimalField(max_digits=3, decimal_places=1,db_column=u'S', null=True)
    p = DecimalField(max_digits=3, decimal_places=1,db_column=u'P', null=True)
    j1 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J1', null=True)
    j2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J2', null=True)
    k = DecimalField(max_digits=3, decimal_places=1,db_column=u'K', null=True)
    s2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'S2', null=True)
    jc = DecimalField(max_digits=3, decimal_places=1,db_column=u'Jc', null=True)
    sn = PositiveSmallIntegerField(null=True)

    def j1j2(self):
        if self.j1 and self.j2:
            return (self.j1,self.j2)

    def __unicode__(self):
        return u'ID:%s Eng:%s'%(self.id,self.energy)
    class Meta:
        db_table = u'states'


class Transition(Model):
    id = AutoField(primary_key=True)
    upstate = ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True, db_index=False)
    lostate = ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True, db_index=False)

    wavevac = DecimalField(max_digits=20, decimal_places=8, db_index=True)
    waveair = DecimalField(max_digits=20, decimal_places=8, db_index=True)
    # wavevac (calculated from energies, has separated wavewac_ref (same as energies))
    # waveair + waveair_ref

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

    #srctag = ForeignKey(Reference, db_index=False)

    wavevac_ref = ForeignKey(Reference, related_name='iswavevacref_trans', db_index=False)
    waveair_ref = ForeignKey(Reference, related_name='iswaveairref_trans', db_index=False)
    # change above to waveair_ref?
    loggf_ref = ForeignKey(Reference, related_name='isloggfref_trans', db_index=False)
    gammarad_ref = ForeignKey(Reference, related_name='isgammaradref_trans', db_index=False)
    gammastark_ref = ForeignKey(Reference, related_name='isgammastarkref_trans', db_index=False)
    waals_ref = ForeignKey(Reference, related_name='iswaalsref_trans', db_index=False)

    wave_linelist = ForeignKey(LineList, related_name='iswavelinelist_trans', db_index=False) # needed for population
    #loggf_linelist = ForeignKey(LineList, related_name='isloggflinelist_trans', db_index=False)
    #gammarad_linelist = ForeignKey(LineList, related_name='isgammaradlinelist_trans', db_index=False)
    #gammastark_linelist = ForeignKey(LineList, related_name='isgammastarklinelist_trans', db_index=False)
    #waals_linelist = ForeignKey(LineList, related_name='iswaalslinelist_trans', db_index=False)

    transition_type = CharField(max_length=2, null=True)
    autoionized = NullBooleanField(default=False)

    # Method information. Since some xsams method categories are represented more than one vald equivalent,
    # we need one field for restrictable's queries and returnable's queries respectively.
    # vald category mapping = {'exp':0, 'obs':1, 'emp':2, 'pred':3, 'calc':4, 'mix':5}
    # vald->xsams mapping = {0:'experiment', 1:'semiempirical', 2:'derived', 3:'theory',4:'semiempirical',5:'compilation'}
    # mapping between method_return and method_restrict = {0:0, 1:1, 2:2, 3:3, 4:1, 5:5} (i.e. xsams=semiempirical is represented in vald by both obs and calc (1 and 4)).

    method_return = PositiveSmallIntegerField(null=True, db_index=False) # this is the method category, populated in post-processing by parsing wave_linelist field
    method_restrict = PositiveSmallIntegerField(null=True, db_index=True) # this is the method category to restrict on, populated in post-processing.

    def getWaals(self):
        if self.gammawaals: return self.gammawaals
        elif self.sigmawaals and self.alphawaals: return [self.sigmawaals,self.alphawaals]
        else: return ""

    def getAccurType(self):
        "retrieve the right AccurType type depending on the VALD accur flag"
        if self.accurflag in (u"N", u"E"): return u"estimated"
        elif self.accurflag == u'C': return u"arbitrary"
        elif self.accurflag == u'P': return u"systematic"
        else: return ""

    def getAccurRelative(self):
        "retrieve AccuracyRelative tag as true/false depending on VALD accur flag"
        return str(self.accurflag in (u"N", u"E", u"C")).lower() # returns true/false

# Don't calculate here, but directly using sql (kept here for reference)
#    def getEinsteinA(self):
#        "Calculate the einstein A"
#        return (0.667025e16 * 10**self.loggf) / ((2 * self.upstate.j + 1.0) * self.wave**2)

    def __unicode__(self):
        return u'ID:%s Wavel: %s'%(self.id,self.wave)
    class Meta:
        db_table = u'transitions'



