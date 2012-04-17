# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

import logging
log=logging.getLogger('vamdc.node.model')

class Sources(models.Model):
    SourceID = models.IntegerField(primary_key=True)
    SourceCategory = models.CharField(max_length=64)
    SourceAuthorName = models.TextField(blank=True)
    SourceTitle = models.TextField(blank=True)
    SourceName = models.CharField(max_length=255)
    SourceYear = models.IntegerField()
    SourceVolume = models.CharField(max_length=10)
    SourcePageBegin = models.IntegerField()
    SourcePageEnd = models.IntegerField()
    SourceURI = models.TextField(blank=True)
    class Meta:
        db_table = u'sources'

    def authorlist(self):
        aut_list = self.SourceAuthorName.split(",")
        return aut_list

class Bands(models.Model):
    mol_id = models.IntegerField()
    mi_id = models.IntegerField()
    vlup = models.IntegerField(db_column='VLup') 
    sup = models.CharField(max_length=12, db_column='Sup') 
    vllow = models.IntegerField(db_column='VLlow') 
    slow = models.CharField(max_length=12, db_column='Slow') 
    num_lines = models.IntegerField(null=True, blank=True)
    wnmin = models.FloatField(null=True, db_column='WNmin', blank=True) 
    wnmax = models.FloatField(null=True, db_column='WNmax', blank=True) 
    vsum = models.FloatField(null=True, db_column='Vsum', blank=True) 
    vmin = models.FloatField(null=True, db_column='Vmin', blank=True) 
    vmax = models.FloatField(null=True, db_column='Vmax', blank=True) 
    jmax = models.IntegerField(null=True, db_column='Jmax', blank=True) 
    class Meta:
        db_table = u'bands'

class Isotopes(models.Model):
    mol_id = models.IntegerField(primary_key=True)
    mi_id = models.IntegerField()
    inchi = models.CharField(max_length=75, db_column='InChi') 
    inchikey = models.CharField(max_length=75, db_column='InChiKey') 
    nnn = models.CharField(max_length=6)
    formula = models.CharField(max_length=189)
    mass = models.FloatField()
    abundance = models.FloatField()
    a = models.FloatField(db_column='A') 
    b = models.FloatField(db_column='B') 
    c = models.FloatField(db_column='C') 
    w1 = models.FloatField(null=True, blank=True)
    w2 = models.FloatField(null=True, blank=True)
    w3 = models.FloatField(null=True, blank=True)
    ref_mass = models.IntegerField(null=True, blank=True)
    ref_abundance = models.IntegerField(null=True, blank=True)
    ref_abc = models.IntegerField(db_column='ref_ABC', null=True, blank=True) 
    ref_w = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'isotopes'
        unique_together = ('mol_id','mi_id')

class Molecules(models.Model):
    mol_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=189)
    formula = models.CharField(max_length=189)
    class Meta:
        db_table = u'mols'

class ResGroups(models.Model):
    mol_id = models.IntegerField(primary_key=True)
    mi_id = models.IntegerField()
    rg_id = models.IntegerField()
    rg_name = models.CharField(max_length=300, blank=True)
    remin = models.FloatField(null=True, db_column='REmin', blank=True) 
    remax = models.FloatField(null=True, db_column='REmax', blank=True) 
    jmax = models.IntegerField(null=True, db_column='Jmax', blank=True) 
    file_rot = models.TextField(blank=True)
    file_par = models.TextField(blank=True)
    class Meta:
        db_table = u'res_groups'
        unique_together = ('mol_id','mi_id','rg_id')

class PartFun(models.Model):
    mol_id = models.IntegerField(primary_key=True)
    mi_id = models.IntegerField()
    Z0 = models.FloatField(null=True, blank=True) 
    Tmin = models.FloatField(null=True, blank=True) 
    Tmax = models.FloatField(null=True, blank=True) 
    ref_Z0 = models.IntegerField()
    class Meta:
        db_table = u'partfun'
        unique_together = ('mol_id','mi_id')

class StatSum(models.Model):
    mol_id = models.IntegerField(primary_key=True)
    mi_id = models.IntegerField()
    q_ind = models.IntegerField()
    value = models.FloatField(null=True, blank=True) 
    class Meta:
        db_table = u'statsum'
        unique_together = ('mol_id','mi_id','q_ind')

class Transitions(models.Model):
    mol_id = models.IntegerField(primary_key=True)
    mi_id = models.IntegerField()
    inchi = models.CharField(max_length=75, db_column='InChi') 
    inchikey = models.CharField(max_length=75, db_column='InChiKey') 
    nnn = models.CharField(max_length=6)
    vlup = models.IntegerField(db_column='VLup') 
    sup = models.CharField(max_length=12, db_column='Sup') 
    vllow = models.IntegerField(db_column='VLlow') 
    slow = models.CharField(max_length=12, db_column='Slow') 
    jup = models.IntegerField(db_column='Jup') 
    kaup = models.IntegerField(db_column='KAup') 
    kcup = models.IntegerField(db_column='KCup') 
    jlow = models.IntegerField(db_column='Jlow') 
    kalow = models.IntegerField(db_column='KAlow') 
    kclow = models.IntegerField(db_column='KClow') 
    state_up = models.CharField(max_length=25) 
    state_low = models.CharField(max_length=25) 
    wn = models.FloatField(db_column='WN') 
    sqr = models.FloatField(null=True, db_column='SqR', blank=True) 
    elow = models.FloatField(null=True, db_column='Elow', blank=True) 
    s = models.FloatField(null=True, db_column='S', blank=True)
    ae = models.FloatField(null=True, db_column='Aein', blank=True)
    hwhma = models.FloatField(null=True, db_column='HWHMa', blank=True) 
    hwhms = models.FloatField(null=True, db_column='HWHMs', blank=True) 
    tc = models.FloatField(null=True, db_column='Tc', blank=True) 
    dwn = models.FloatField(null=True, db_column='Dwn', blank=True) 
    dint = models.FloatField(null=True, db_column='Dint', blank=True) 
    dha = models.FloatField(null=True, db_column='Dha', blank=True) 
    dhs = models.FloatField(null=True, db_column='Dhs', blank=True) 
    ref_wn = models.IntegerField(null=True, blank=True)
    ref_s = models.IntegerField(null=True, blank=True)
    ref_e = models.IntegerField(null=True, blank=True)
    mol_name = models.CharField(max_length=12) 
    mol_formula = models.CharField(max_length=12) 
    charge = models.IntegerField() 
    class Meta:
        db_table = u'transitions_vlg'
        unique_together = ('mol_id','mi_id','vlup','sup','vllow','slow','jup','kaup','kcup','jlow','kalow','kclow')

    def getTranId(self):
        return str(self.mol_id) + '-' + str(self.mi_id) + '-' + str(self.vlup) + '-' + self.sup + '-' + str(self.jup) + '-' + str(self.kaup) + '-' + str(self.kcup) + '-' + str(self.vllow) + '-' + self.slow + '-' + str(self.jlow) + '-' + str(self.kalow) + '-' + str(self.kclow)

    def getStateRefUp(self):
        return str(self.mol_id) + '-' + str(self.mi_id) + '-' + str(self.vlup) + '-' + self.sup

    def getStateRefLow(self):
        return str(self.mol_id) + '-' + str(self.mi_id) + '-' + str(self.vllow) + '-' + self.slow

    def XML_Broadening(self):
        """
        Build and return the XML for the air- and self-broadening parameters
        gamma_air, n_air, and gamma_self.

        """

        broadening_xml = []
        if 'hwhma' in self.__dict__:
            lineshape_xml = []
            lineshape_xml.append('      <Lineshape name="Lorentzian">\n'\
                   '      <Comments>The temperature-dependent pressure'\
                   ' broadening Lorentzian lineshape</Comments>\n'\
                   '      <LineshapeParameter name="gammaL">\n'\
                   '        <FitParameters functionRef="FGSMA-SMPO-gammaL">\n'\
                   '          <FitArgument name="T" units="K" />\n'\
                   '          <FitArgument name="P" units="atm" />\n'\
                   '          <FitParameter name="hwhm">\n')
            lineshape_xml.append('            <Value units="1/cm">%s</Value>\n'
                                 % self.hwhma)
            if self.dha is not None:
                lineshape_xml.append('            <Accuracy type="statistical" relative="true"'
                     '>%s</Accuracy>\n' % str(self.dha/self.hwhma))
            lineshape_xml.append('          </FitParameter>\n')
            if 'tc' in self.__dict__:
                lineshape_xml.append('          <FitParameter name="tc">\n')
                lineshape_xml.append('            <Value units="unitless">%s'
                                     '</Value>\n' % self.tc)
                lineshape_xml.append('          </FitParameter>\n')
            lineshape_xml.append('        </FitParameters>\n'\
                                 '      </LineshapeParameter>\n</Lineshape>\n')
            broadening_xml.append('    <Broadening'
                ' envRef="EGSMA-SMPO-BRDair" name="pressure">\n'
                '%s    </Broadening>\n' % ''.join(lineshape_xml))
        if 'hwhms' in self.__dict__:
            lineshape_xml = []
            lineshape_xml.append('      <Lineshape name="Lorentzian">\n'\
                           '        <LineshapeParameter name="gammaL">\n')
            lineshape_xml.append('          <Value units="1/cm">%s</Value>\n'
                      % self.hwhms)
            if self.dhs is not None:
                lineshape_xml.append('          <Accuracy type="statistical" relative="true">'\
                    '%s</Accuracy>\n' % str(self.dhs/self.hwhms))
            lineshape_xml.append('        </LineshapeParameter>\n'\
                                 '      </Lineshape>\n')
            broadening_xml.append('    <Broadening'\
                ' envRef="EGSMA-SMPO-BRDself" name="pressure">\n'\
                '%s    </Broadening>\n' % ''.join(lineshape_xml))
        return '    %s\n' % ''.join(broadening_xml)

class VibLevels(models.Model):
    mol_id = models.IntegerField(primary_key=True)
    mi_id = models.IntegerField()
    vs_id = models.IntegerField()
    src_id = models.IntegerField()
    rg_id = models.IntegerField()
    symm = models.CharField(max_length=12)
    polyad = models.CharField(max_length=30, blank=True)
    vl_num = models.IntegerField()
    vl_energy = models.FloatField(null=True, blank=True)
    ref_e = models.IntegerField(null=True, blank=True)
    vl_id_gqn = models.CharField(max_length=90, db_column='vl_id_GQN') 
    vl_eobs = models.FloatField(null=True, db_column='vl_Eobs', blank=True) 
    class Meta:
        db_table = u'vib_levels2'
        unique_together = ('mol_id','mi_id','symm','vl_num')

class Method(object):
    def __init__(self, id, category, description):
        self.id = id
        self.category = category
        self.description = description

class FunArg(object):
    def __init__(self, arg):
        self.name = arg[0]
        if len(arg)>1:
            self.units = arg[1]
        else:
            self.units = 'unitless'
        if len(arg)>2:
            self.low = arg[2]
        else:
            self.low = ''
        if len(arg)>3:
            self.up = arg[3]
        else:
            self.up = ''
        if len(arg)>4:
            self.descr = arg[4]
        else:
            self.descr = ''

class FunParm(object):
    def __init__(self, arg):
        self.name = arg[0]
        if len(arg)>1:
            self.units = arg[1]
        else:
            self.units = 'unitless'
        if len(arg)>2:
            self.descr = arg[2]
        else:
            self.descr = ''

class Function(object):
    def __init__(self, id, name, clang, expr, yname, yunits, descr='', ydescr='', args=[], parms=[]):
        self.id = id
        self.name = name
        self.clang = clang
        self.expr = expr
        self.yname = yname
        self.yunits = yunits
        self.descr = descr
        self.ydescr = ydescr
        if len(args)>0:
            self.Arguments = []
            for arg in args:
                self.Arguments.append(FunArg(arg))
        if len(parms)>0:
            self.Parameters = []
            for parm in parms:
                self.Parameters.append(FunParm(parm))

class EnvSpecie(object):
    def __init__(self, name, fraction):
        self.name = name
        self.fraction = fraction

class Environment(object):
    def __init__(self, id, temp, press, species=[]):
        self.id = id
        self.temperature = temp
        self.pressure = press
        if len(species)>0:
            self.Species = []
            for specie in species:
                self.Species.append(EnvSpecie(specie[0],specie[1]))
