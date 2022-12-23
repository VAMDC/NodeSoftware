"""
This module defines the database schema of the node.

Each model class defines a table in the database. The fields define the columns of this table.

"""

# library import
from django.db.models import *

# this is only need for converting bibtex -> xsams sources
# requrires package "pybtex"
#from vamdctap import bibtextools

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

    # defines some optional meta-options for viewing and storage
    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.name)
    class Meta:
        db_table = u'species'

class Reference(Model):
    id = CharField(max_length=64, primary_key=True, db_index=True)
    bibtex = TextField(null=True)

    def XML(self):
        """
        If a model has a method XML, this will be called automatically by the
        xml generator, bypassing the definition on right-hand-side of the RETURNABLES dictionary.
        It is the job of this method to return correct XML.
        Note that errors in this method will cause the call to fail silently!

        In this case we use the BibTex2XML helper to format the bibtex entry for return.
        """
        # commented out to not depend on pybtex package
        #return bibtextools.BibTeX2XML( self.bibtex )
        return ''

    class Meta:
        db_table = u'refs'
    def __unicode__(self):
        return u'%s'%self.id

class State(Model):
    id = CharField(max_length=255, primary_key=True, db_index=True)
    species = ForeignKey(Species, on_delete=CASCADE)

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

    # half-time
    tau_exp = DecimalField(max_digits=8, decimal_places=4,db_column=u'tau_exp', null=True,blank=True)
    tau_calc = DecimalField(max_digits=8, decimal_places=4,db_column=u'tau_calc', null=True,blank=True)
    tau_exp_ref = ForeignKey(Reference, related_name='istau_exp_state', null=True, on_delete=CASCADE)
    tau_calc_ref = ForeignKey(Reference, related_name='istau_calc_state',null=True, on_delete=CASCADE)
    energy_ref = ForeignKey(Reference, related_name='isenergyref_state', null=True, on_delete=CASCADE)
    lande_ref = ForeignKey(Reference, related_name='islanderef_state', null=True, on_delete=CASCADE)
    level_ref = ForeignKey(Reference, related_name='islevelref_state', null=True, on_delete=CASCADE)

    # Helper methods for accessing one of the fields. These are called from
    # the RETURNABLES dictionary

    def get_best_tau(self):
        "Give preference to the experimentally measured data"
        if self.tau_exp:
            return self.tau_exp
        else:
            return self.tau_calc

    def get_tau_ref(self):
        """
        Inform us which type of tau was returned. Note that these identifiers are
        the same as we made available in the 'Method' xsams category, as defined in queryfuncs.py.
        """
        if self.tau_exp:
            return "MtauEXP"
        else:
            return "MtauTHEO"

    # metadata
    def __unicode__(self):
        return u'ID:%s En:%s'%(self.id,self.energy)
    class Meta:
        db_table = u'states'

class Transition(Model):
    id = AutoField(primary_key=True)
    upstate = ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True, on_delete=CASCADE)
    lostate = ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True, on_delete=CASCADE)

    vacwave = DecimalField(max_digits=20, decimal_places=8, db_index=True, null=True)
    species = ForeignKey(Species,db_column='species', on_delete=CASCADE)
    loggf = DecimalField(max_digits=8, decimal_places=3,null=True,blank=True)
    landeff = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammarad = DecimalField(max_digits=6, decimal_places=2,null=True,blank=True)
    gammastark = DecimalField(max_digits=7, decimal_places=3,null=True,blank=True)
    gammawaals = DecimalField(max_digits=6, decimal_places=3,null=True,blank=True)

    wave_accur = DecimalField(max_digits = 9, decimal_places=4,db_column=u'wave_accur', null=True,blank=True)
    loggf_accur = DecimalField(max_digits = 9, decimal_places=4,db_column=u'loggf_accur', null=True,blank=True)
    comment = CharField(max_length=128, null=True,blank=True)

    wave_ref = ForeignKey(Reference, related_name='iswaveref_trans',null=True, on_delete=CASCADE)
    loggf_ref = ForeignKey(Reference, related_name='isloggf_ref_trans',null=True, on_delete=CASCADE)
    lande_ref = ForeignKey(Reference, related_name='islanderef_trans',null=True, on_delete=CASCADE)
    gammarad_ref = ForeignKey(Reference, related_name='isgammaradref_trans',null=True, on_delete=CASCADE)
    gammastark_ref = ForeignKey(Reference, related_name='isgammastarkref_trans',null=True, on_delete=CASCADE)
    waals_ref = ForeignKey(Reference, related_name='iswaalsref_trans',null=True, on_delete=CASCADE)

    def __unicode__(self):
        return u'ID:%s Wavel: %s'%(self.id,self.vacwave)
    class Meta:
        db_table = u'transitions'
