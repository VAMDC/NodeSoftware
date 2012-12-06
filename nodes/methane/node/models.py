# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from dictionaries import RETURNABLES

NODEID = RETURNABLES['NodeID']
source_prefix = 'B%s-' % NODEID
func_prefix = 'F%s-' % NODEID
env_prefix = 'E%s-' % NODEID
allenv = ('self','N2','O2','air','H2O','CO2','H2','He','Ar')                                       # all broadening environments
curenvid = (0,1,2,6)                                                                               # current environment ids e.g. 1,6 = N2,H2


class TransitionTypes(models.Model):
    typeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=90)
    class Meta:
        db_table = u'transition_types'

class Characterisation(models.Model):
    characid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    class Meta:
        db_table = u'characterisation'

    def getTransitionKind(self):
        if(self.characid == 2):
           return "Polarizability"
        else:
           return

    def getMultipole(self):
        if(self.characid == 1):
           return "E1"
        else:
           return

    def getUnit(self):
        result = self.name
        if(self.characid == 1):
           result = "1/cm2/atm"
        if(self.characid == 2):
           result = "undef"
        return result

class Sources(models.Model):
    sourceid = models.IntegerField(primary_key=True)
    ris = models.TextField()
    class Meta:
        db_table = u'sources'

    def extractChain(self,tokens,st):
        for token in tokens:
            if(token.startswith(st)): break

        result = token[5:]

        if(st == "TY"):
            result={
                "JOUR": "journal",
                "BOOK": "book",
               #"CHAP": "Book chapter",
               #"CONF": "Conference proceeding",
                "":""
            }[result]

        return result

    def author(self,tokens,st):
        a=[]
        for token in tokens:
           if(token.startswith(st)): a.append(token[5:])
        return a

    def extractRisVal(self,st):
        tokens = self.ris.split("|")
        result={
            "TY": self.extractChain(tokens,st),
            "T1": self.extractChain(tokens,st),
            "JO": self.extractChain(tokens,st),
            "VL": self.extractChain(tokens,st),
            "IS": self.extractChain(tokens,st),
            "SP": self.extractChain(tokens,st),
            "EP": self.extractChain(tokens,st),
            "PY": self.extractChain(tokens,st),
            "AU": self.author(tokens,st),
            "M1": self.extractChain(tokens,st),
            "ER": self.extractChain(tokens,st)
        }[st]

        return result

class SymmetryNames(models.Model):
    symnameid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=9)
    class Meta:
        db_table = u'symmetry_names'

class VibrationalLevels(models.Model):
    levelid = models.IntegerField(primary_key=True)
    nbmode = models.IntegerField()
    v1 = models.IntegerField(null=True, blank=True)
    v2 = models.IntegerField(null=True, blank=True)
    v3 = models.IntegerField(null=True, blank=True)
    v4 = models.IntegerField(null=True, blank=True)
    v5 = models.IntegerField(null=True, blank=True)
    v6 = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'vibrational_levels'

class PolyadDescriptions(models.Model):
    poldesid = models.IntegerField(primary_key=True)
    nblev = models.IntegerField()
    levelid1 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid1', blank=True, related_name='rn_levelid1')
    levelid2 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid2', blank=True, related_name='rn_levelid2')
    levelid3 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid3', blank=True, related_name='rn_levelid3')
    levelid4 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid4', blank=True, related_name='rn_levelid4')
    levelid5 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid5', blank=True, related_name='rn_levelid5')
    levelid6 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid6', blank=True, related_name='rn_levelid6')
    levelid7 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid7', blank=True, related_name='rn_levelid7')
    levelid8 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid8', blank=True, related_name='rn_levelid8')
    levelid9 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid9', blank=True, related_name='rn_levelid9')
    levelid10 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid10', blank=True, related_name='rn_levelid10')
    levelid11 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid11', blank=True, related_name='rn_levelid11')
    levelid12 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid12', blank=True, related_name='rn_levelid12')
    levelid13 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid13', blank=True, related_name='rn_levelid13')
    levelid14 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid14', blank=True, related_name='rn_levelid14')
    class Meta:
        db_table = u'polyad_descriptions'

class MoleculeTypes(models.Model):
    moltypeid = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=30)
    nbmode = models.IntegerField()
    nbquantumnb = models.IntegerField()
    qname1 = models.CharField(max_length=12)
    status1 = models.IntegerField()
    qname2 = models.CharField(max_length=12)
    status2 = models.IntegerField()
    qname3 = models.CharField(max_length=12)
    status3 = models.IntegerField()
    qname4 = models.CharField(max_length=12)
    status4 = models.IntegerField()
    qname5 = models.CharField(max_length=12)
    status5 = models.IntegerField()
    qname6 = models.CharField(max_length=12)
    status6 = models.IntegerField()
    qname7 = models.CharField(max_length=12)
    status7 = models.IntegerField()
    qname8 = models.CharField(max_length=12)
    status8 = models.IntegerField()
    qname9 = models.CharField(max_length=12)
    status9 = models.IntegerField()
    qname10 = models.CharField(max_length=12)
    status10 = models.IntegerField()
    qname11 = models.CharField(max_length=12)
    status11 = models.IntegerField()
    qname12 = models.CharField(max_length=12)
    status12 = models.IntegerField()
    qname13 = models.CharField(max_length=12)
    status13 = models.IntegerField()
    qname14 = models.CharField(max_length=12)
    status14 = models.IntegerField()
    qname15 = models.CharField(max_length=12)
    status15 = models.IntegerField()
    qname16 = models.CharField(max_length=12)
    status16 = models.IntegerField()
    qname17 = models.CharField(max_length=12)
    status17 = models.IntegerField()
    qname18 = models.CharField(max_length=12)
    status18 = models.IntegerField()
    qname19 = models.CharField(max_length=12)
    status19 = models.IntegerField()
    qname20 = models.CharField(max_length=12)
    status20 = models.IntegerField()
    qname21 = models.CharField(max_length=12)
    status21 = models.IntegerField()
    class Meta:
        db_table = u'molecule_types'

class PolyadSchemes(models.Model):
    polschid = models.IntegerField(primary_key=True)
    moltypeid = models.ForeignKey(MoleculeTypes, db_column='moltypeid')
    nbsublev0 = models.IntegerField()
    poldesid0 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid0', blank=True, related_name='rn_poldesid0')
    nbsublev1 = models.IntegerField()
    poldesid1 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid1', blank=True, related_name='rn_poldesid1')
    nbsublev2 = models.IntegerField()
    poldesid2 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid2', blank=True, related_name='rn_poldesid2')
    nbsublev3 = models.IntegerField()
    poldesid3 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid3', blank=True, related_name='rn_poldesid3')
    nbsublev4 = models.IntegerField()
    poldesid4 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid4', blank=True, related_name='rn_poldesid4')
    nbsublev5 = models.IntegerField()
    poldesid5 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid5', blank=True, related_name='rn_poldesid5')
    nbsublev6 = models.IntegerField()
    poldesid6 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid6', blank=True, related_name='rn_poldesid6')
    nbsublev7 = models.IntegerField()
    poldesid7 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid7', blank=True, related_name='rn_poldesid7')
    nbsublev8 = models.IntegerField()
    poldesid8 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid8', blank=True, related_name='rn_poldesid8')
    nbsublev9 = models.IntegerField()
    poldesid9 = models.ForeignKey(PolyadDescriptions, null=True, db_column='poldesid9', blank=True, related_name='rn_poldesid9')
    class Meta:
        db_table = u'polyad_schemes'

class Polyads(models.Model):
    polyadid = models.IntegerField(primary_key=True)
    polschid = models.ForeignKey(PolyadSchemes, db_column='polschid')
    polyadnb = models.IntegerField()
    class Meta:
        db_table = u'polyads'

class MoleculesIsotopes(models.Model):
    isotopeid = models.IntegerField(primary_key=True)
    moltypeid = models.ForeignKey(MoleculeTypes, db_column='moltypeid')
    isotopename = models.CharField(max_length=30)
    inchi = models.CharField(max_length=120)
    inchikey = models.CharField(max_length=81)
    formtex = models.CharField(max_length=15)
    casregnum = models.CharField(max_length=15)
    eostateid = models.IntegerField()
    class Meta:
        db_table = u'molecules_isotopes'

class VibrationalSublevels(models.Model):
    sublevid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
    qvalue1 = models.IntegerField()
    qvalue2 = models.IntegerField()
    qvalue3 = models.IntegerField()
    qvalue4 = models.IntegerField()
    qvalue5 = models.IntegerField()
    qvalue6 = models.IntegerField()
    qvalue7 = models.IntegerField()
    qvalue8 = models.IntegerField()
    qvalue9 = models.IntegerField()
    qvalue10 = models.IntegerField()
    qvalue11 = models.IntegerField()
    qvalue12 = models.IntegerField()
    qvalue13 = models.IntegerField()
    qvalue14 = models.IntegerField()
    qvalue15 = models.IntegerField()
    qvalue16 = models.IntegerField()
    qvalue17 = models.IntegerField()
    qvalue18 = models.IntegerField()
    qvalue19 = models.IntegerField()
    qvalue20 = models.IntegerField()
    qvalue21 = models.IntegerField()
    class Meta:
        db_table = u'vibrational_sublevels'

    def getQNviMode(self):
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            return [1,2,3,4]
        else:
            # XY3Z
            return [1,2,3,4,5,6]

    def getQNvi(self):
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            return [self.qvalue3,self.qvalue7,self.qvalue11,self.qvalue16]
        else:
            # XY3Z
            return [self.qvalue3,self.qvalue6,self.qvalue9,self.qvalue12,self.qvalue15,self.qvalue19]

    def getQNliMode(self):
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            return [1,2,3,4]
        else:
            # XY3Z
            return [1,2,3,4,5,6]

    def getQNli(self):
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            return [self.qvalue4,self.qvalue8,self.qvalue12,self.qvalue17]
        else:
            # XY3Z
            return [self.qvalue4,self.qvalue7,self.qvalue10,self.qvalue13,self.qvalue16,self.qvalue20]

    def getQNrName(self):
        res = ["nv"]
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            res += ["n1","n2","n3","n4"]
        else:
            # XY3Z
            pass
        return res

    def getQNr(self):
        res = [self.qvalue2]
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            res += [self.qvalue5,self.qvalue9,self.qvalue13,self.qvalue18]
        else:
            # XY3Z
            pass
        return res

    def getQNsymName(self):
        res = ["Cv"]
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            res += ["C1","C2","C3","C23","C4"]
        else:
            # XY3Z
            res += ["C1","C2","C3","C4","C5","C45","C6"]
        return res

    def getQNsym(self):
        # Cv
        vssymid = self.qvalue1
        s = SymmetryNames.objects.get(symnameid = vssymid)
        res = [s.name]
        if( self.isotopeid.moltypeid.description == 'XY4' ):
            # XY4
            vssymid = self.qvalue6
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue10
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue14
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue15
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue19
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
        else:
            # XY3Z
            vssymid = self.qvalue5
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue8
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue11
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue14
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue17
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue18
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
            vssymid = self.qvalue21
            s = SymmetryNames.objects.get(symnameid = vssymid)
            res.append(s.name)
        return res

class ScalarNumbers(models.Model):
    scalarid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
    polyadid = models.ForeignKey(Polyads, db_column='polyadid')
    beta = models.FloatField()
    gamma = models.FloatField()
    pi = models.FloatField()
    class Meta:
        db_table = u'scalar_numbers'

class MolecularStates(models.Model):
    stateid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
    polyadid = models.ForeignKey(Polyads, db_column='polyadid')
    position = models.FloatField()
    j = models.IntegerField()
    symname = models.CharField(max_length=3)
    alpha = models.IntegerField()
    weight = models.IntegerField()
    nbcoefn0 = models.IntegerField()
    sublevid1 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid1', blank=True, related_name='rn_sublevid1')
    coefficient1 = models.FloatField(null=True, blank=True)
    sublevid2 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid2', blank=True, related_name='rn_sublevid2')
    coefficient2 = models.FloatField(null=True, blank=True)
    sublevid3 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid3', blank=True, related_name='rn_sublevid3')
    coefficient3 = models.FloatField(null=True, blank=True)
    sublevid4 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid4', blank=True, related_name='rn_sublevid4')
    coefficient4 = models.FloatField(null=True, blank=True)
    sublevid5 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid5', blank=True, related_name='rn_sublevid5')
    coefficient5 = models.FloatField(null=True, blank=True)
    sublevid6 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid6', blank=True, related_name='rn_sublevid6')
    coefficient6 = models.FloatField(null=True, blank=True)
    sublevid7 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid7', blank=True, related_name='rn_sublevid7')
    coefficient7 = models.FloatField(null=True, blank=True)
    sublevid8 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid8', blank=True, related_name='rn_sublevid8')
    coefficient8 = models.FloatField(null=True, blank=True)
    sublevid9 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid9', blank=True, related_name='rn_sublevid9')
    coefficient9 = models.FloatField(null=True, blank=True)
    sublevid10 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid10', blank=True, related_name='rn_sublevid10')
    coefficient10 = models.FloatField(null=True, blank=True)
    sublevid11 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid11', blank=True, related_name='rn_sublevid11')
    coefficient11 = models.FloatField(null=True, blank=True)
    sublevid12 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid12', blank=True, related_name='rn_sublevid12')
    coefficient12 = models.FloatField(null=True, blank=True)
    sublevid13 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid13', blank=True, related_name='rn_sublevid13')
    coefficient13 = models.FloatField(null=True, blank=True)
    sublevid14 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid14', blank=True, related_name='rn_sublevid14')
    coefficient14 = models.FloatField(null=True, blank=True)
    sublevid15 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid15', blank=True, related_name='rn_sublevid15')
    coefficient15 = models.FloatField(null=True, blank=True)
    sublevid16 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid16', blank=True, related_name='rn_sublevid16')
    coefficient16 = models.FloatField(null=True, blank=True)
    sublevid17 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid17', blank=True, related_name='rn_sublevid17')
    coefficient17 = models.FloatField(null=True, blank=True)
    sublevid18 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid18', blank=True, related_name='rn_sublevid18')
    coefficient18 = models.FloatField(null=True, blank=True)
    sublevid19 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid19', blank=True, related_name='rn_sublevid19')
    coefficient19 = models.FloatField(null=True, blank=True)
    sublevid20 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid20', blank=True, related_name='rn_sublevid20')
    coefficient20 = models.FloatField(null=True, blank=True)
    sublevid21 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid21', blank=True, related_name='rn_sublevid21')
    coefficient21 = models.FloatField(null=True, blank=True)
    sublevid22 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid22', blank=True, related_name='rn_sublevid22')
    coefficient22 = models.FloatField(null=True, blank=True)
    sublevid23 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid23', blank=True, related_name='rn_sublevid23')
    coefficient23 = models.FloatField(null=True, blank=True)
    sublevid24 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid24', blank=True, related_name='rn_sublevid24')
    coefficient24 = models.FloatField(null=True, blank=True)
    sublevid25 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid25', blank=True, related_name='rn_sublevid25')
    coefficient25 = models.FloatField(null=True, blank=True)
    sublevid26 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid26', blank=True, related_name='rn_sublevid26')
    coefficient26 = models.FloatField(null=True, blank=True)
    sublevid27 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid27', blank=True, related_name='rn_sublevid27')
    coefficient27 = models.FloatField(null=True, blank=True)
    sublevid28 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid28', blank=True, related_name='rn_sublevid28')
    coefficient28 = models.FloatField(null=True, blank=True)
    sublevid29 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid29', blank=True, related_name='rn_sublevid29')
    coefficient29 = models.FloatField(null=True, blank=True)
    sublevid30 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid30', blank=True, related_name='rn_sublevid30')
    coefficient30 = models.FloatField(null=True, blank=True)
    sublevid31 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid31', blank=True, related_name='rn_sublevid31')
    coefficient31 = models.FloatField(null=True, blank=True)
    sublevid32 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid32', blank=True, related_name='rn_sublevid32')
    coefficient32 = models.FloatField(null=True, blank=True)
    sublevid33 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid33', blank=True, related_name='rn_sublevid33')
    coefficient33 = models.FloatField(null=True, blank=True)
    sublevid34 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid34', blank=True, related_name='rn_sublevid34')
    coefficient34 = models.FloatField(null=True, blank=True)
    sublevid35 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid35', blank=True, related_name='rn_sublevid35')
    coefficient35 = models.FloatField(null=True, blank=True)
    sublevid36 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid36', blank=True, related_name='rn_sublevid36')
    coefficient36 = models.FloatField(null=True, blank=True)
    sublevid37 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid37', blank=True, related_name='rn_sublevid37')
    coefficient37 = models.FloatField(null=True, blank=True)
    sublevid38 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid38', blank=True, related_name='rn_sublevid38')
    coefficient38 = models.FloatField(null=True, blank=True)
    sublevid39 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid39', blank=True, related_name='rn_sublevid39')
    coefficient39 = models.FloatField(null=True, blank=True)
    sublevid40 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid40', blank=True, related_name='rn_sublevid40')
    coefficient40 = models.FloatField(null=True, blank=True)
    sublevid41 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid41', blank=True, related_name='rn_sublevid41')
    coefficient41 = models.FloatField(null=True, blank=True)
    sublevid42 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid42', blank=True, related_name='rn_sublevid42')
    coefficient42 = models.FloatField(null=True, blank=True)
    sublevid43 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid43', blank=True, related_name='rn_sublevid43')
    coefficient43 = models.FloatField(null=True, blank=True)
    sublevid44 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid44', blank=True, related_name='rn_sublevid44')
    coefficient44 = models.FloatField(null=True, blank=True)
    sublevid45 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid45', blank=True, related_name='rn_sublevid45')
    coefficient45 = models.FloatField(null=True, blank=True)
    sublevid46 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid46', blank=True, related_name='rn_sublevid46')
    coefficient46 = models.FloatField(null=True, blank=True)
    sublevid47 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid47', blank=True, related_name='rn_sublevid47')
    coefficient47 = models.FloatField(null=True, blank=True)
    sublevid48 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid48', blank=True, related_name='rn_sublevid48')
    coefficient48 = models.FloatField(null=True, blank=True)
    sublevid49 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid49', blank=True, related_name='rn_sublevid49')
    coefficient49 = models.FloatField(null=True, blank=True)
    sublevid50 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid50', blank=True, related_name='rn_sublevid50')
    coefficient50 = models.FloatField(null=True, blank=True)
    sublevid51 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid51', blank=True, related_name='rn_sublevid51')
    coefficient51 = models.FloatField(null=True, blank=True)
    sublevid52 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid52', blank=True, related_name='rn_sublevid52')
    coefficient52 = models.FloatField(null=True, blank=True)
    sublevid53 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid53', blank=True, related_name='rn_sublevid53')
    coefficient53 = models.FloatField(null=True, blank=True)
    sublevid54 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid54', blank=True, related_name='rn_sublevid54')
    coefficient54 = models.FloatField(null=True, blank=True)
    sublevid55 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid55', blank=True, related_name='rn_sublevid55')
    coefficient55 = models.FloatField(null=True, blank=True)
    sublevid56 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid56', blank=True, related_name='rn_sublevid56')
    coefficient56 = models.FloatField(null=True, blank=True)
    sublevid57 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid57', blank=True, related_name='rn_sublevid57')
    coefficient57 = models.FloatField(null=True, blank=True)
    sublevid58 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid58', blank=True, related_name='rn_sublevid58')
    coefficient58 = models.FloatField(null=True, blank=True)
    sublevid59 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid59', blank=True, related_name='rn_sublevid59')
    coefficient59 = models.FloatField(null=True, blank=True)
    sublevid60 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid60', blank=True, related_name='rn_sublevid60')
    coefficient60 = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'molecular_states'

    def PnPsn(self):
        return "P%s PS%s" % (self.polyadid.polyadnb,self.polyadid.polschid_id)

    Expansions = [1]

    def getBSID(self):
        return ( self.sublevid1_id,  self.sublevid2_id,  self.sublevid3_id,  self.sublevid4_id,  self.sublevid5_id,  self.sublevid6_id,
                 self.sublevid7_id,  self.sublevid8_id,  self.sublevid9_id,  self.sublevid10_id, self.sublevid11_id, self.sublevid12_id,
                 self.sublevid13_id, self.sublevid14_id, self.sublevid15_id, self.sublevid16_id, self.sublevid17_id, self.sublevid18_id,
                 self.sublevid19_id, self.sublevid20_id, self.sublevid21_id, self.sublevid22_id, self.sublevid23_id, self.sublevid24_id,
                 self.sublevid25_id, self.sublevid26_id, self.sublevid27_id, self.sublevid28_id, self.sublevid29_id, self.sublevid30_id,
                 self.sublevid31_id, self.sublevid32_id, self.sublevid33_id, self.sublevid34_id, self.sublevid35_id, self.sublevid36_id,
                 self.sublevid37_id, self.sublevid38_id, self.sublevid39_id, self.sublevid40_id, self.sublevid41_id, self.sublevid42_id,
                 self.sublevid43_id, self.sublevid44_id, self.sublevid45_id, self.sublevid46_id, self.sublevid47_id, self.sublevid48_id,
                 self.sublevid49_id, self.sublevid50_id, self.sublevid51_id, self.sublevid52_id, self.sublevid53_id, self.sublevid54_id,
                 self.sublevid55_id, self.sublevid56_id, self.sublevid57_id, self.sublevid58_id, self.sublevid59_id, self.sublevid60_id ) [:self.nbcoefn0]

    def getCoef(self):
        return ( self.coefficient1,  self.coefficient2,  self.coefficient3,  self.coefficient4,  self.coefficient5,  self.coefficient6,
                 self.coefficient7,  self.coefficient8,  self.coefficient9,  self.coefficient10, self.coefficient11, self.coefficient12,
                 self.coefficient13, self.coefficient14, self.coefficient15, self.coefficient16, self.coefficient17, self.coefficient18,
                 self.coefficient19, self.coefficient20, self.coefficient21, self.coefficient22, self.coefficient23, self.coefficient24,
                 self.coefficient25, self.coefficient26, self.coefficient27, self.coefficient28, self.coefficient29, self.coefficient30,
                 self.coefficient31, self.coefficient32, self.coefficient33, self.coefficient34, self.coefficient35, self.coefficient36,
                 self.coefficient37, self.coefficient38, self.coefficient39, self.coefficient40, self.coefficient41, self.coefficient42,
                 self.coefficient43, self.coefficient44, self.coefficient45, self.coefficient46, self.coefficient47, self.coefficient48,
                 self.coefficient49, self.coefficient50, self.coefficient51, self.coefficient52, self.coefficient53, self.coefficient54,
                 self.coefficient55, self.coefficient56, self.coefficient57, self.coefficient58, self.coefficient59, self.coefficient60 ) [:self.nbcoefn0]

class Transitions(models.Model):
    transitionid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
    inchikey = models.CharField(max_length=81)
    typeid = models.ForeignKey(TransitionTypes, db_column='typeid')
    characid = models.ForeignKey(Characterisation, db_column='characid')
    lowstateid = models.ForeignKey(MolecularStates, db_column='lowstateid', related_name='rn_lowstateid')
    upstateid = models.ForeignKey(MolecularStates, db_column='upstateid', related_name='rn_upstateid')
    wavenumber = models.FloatField()
    wavenumber_prec = models.FloatField()
    wavenumber_residual = models.FloatField()
    wavenumber_sourceid = models.ForeignKey(Sources, null=True, db_column='wavenumber_sourceid', blank=True, related_name='rn_wavenumber_sourceid')
    intensity = models.FloatField()
    inthitran = models.FloatField(db_column='intHITRAN') # Field name made lowercase.
    intensity_prec = models.FloatField()
    intensity_residual = models.FloatField()
    intensity_sourceid = models.ForeignKey(Sources, null=True, db_column='intensity_sourceid', blank=True, related_name='rn_intensity_sourceid')
    einstein = models.FloatField()
    gamma1 = models.FloatField()
    gamma1_prec = models.FloatField()
    gamma1_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma1_sourceid', blank=True, related_name='rn_gamma1_sourceid')
    delta1 = models.FloatField()
    delta1_prec = models.FloatField()
    delta1_sourceid = models.ForeignKey(Sources, null=True, db_column='delta1_sourceid', blank=True, related_name='rn_delta1_sourceid')
    nexp1 = models.FloatField()
    nexp1_prec = models.FloatField()
    nexp1_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp1_sourceid', blank=True, related_name='rn_nexp1_sourceid')
    gamma2 = models.FloatField()
    gamma2_prec = models.FloatField()
    gamma2_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma2_sourceid', blank=True, related_name='rn_gamma2_sourceid')
    delta2 = models.FloatField()
    delta2_prec = models.FloatField()
    delta2_sourceid = models.ForeignKey(Sources, null=True, db_column='delta2_sourceid', blank=True, related_name='rn_delta2_sourceid')
    nexp2 = models.FloatField()
    nexp2_prec = models.FloatField()
    nexp2_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp2_sourceid', blank=True, related_name='rn_nexp2_sourceid')
    gamma3 = models.FloatField()
    gamma3_prec = models.FloatField()
    gamma3_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma3_sourceid', blank=True, related_name='rn_gamma3_sourceid')
    delta3 = models.FloatField()
    delta3_prec = models.FloatField()
    delta3_sourceid = models.ForeignKey(Sources, null=True, db_column='delta3_sourceid', blank=True, related_name='rn_delta3_sourceid')
    nexp3 = models.FloatField()
    nexp3_prec = models.FloatField()
    nexp3_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp3_sourceid', blank=True, related_name='rn_nexp3_sourceid')
    gamma4 = models.FloatField()
    gamma4_prec = models.FloatField()
    gamma4_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma4_sourceid', blank=True, related_name='rn_gamma4_sourceid')
    delta4 = models.FloatField()
    delta4_prec = models.FloatField()
    delta4_sourceid = models.ForeignKey(Sources, null=True, db_column='delta4_sourceid', blank=True, related_name='rn_delta4_sourceid')
    nexp4 = models.FloatField()
    nexp4_prec = models.FloatField()
    nexp4_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp4_sourceid', blank=True, related_name='rn_nexp4_sourceid')
    gamma5 = models.FloatField()
    gamma5_prec = models.FloatField()
    gamma5_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma5_sourceid', blank=True, related_name='rn_gamma5_sourceid')
    delta5 = models.FloatField()
    delta5_prec = models.FloatField()
    delta5_sourceid = models.ForeignKey(Sources, null=True, db_column='delta5_sourceid', blank=True, related_name='rn_delta5_sourceid')
    nexp5 = models.FloatField()
    nexp5_prec = models.FloatField()
    nexp5_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp5_sourceid', blank=True, related_name='rn_nexp5_sourceid')
    gamma6 = models.FloatField()
    gamma6_prec = models.FloatField()
    gamma6_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma6_sourceid', blank=True, related_name='rn_gamma6_sourceid')
    delta6 = models.FloatField()
    delta6_prec = models.FloatField()
    delta6_sourceid = models.ForeignKey(Sources, null=True, db_column='delta6_sourceid', blank=True, related_name='rn_delta6_sourceid')
    nexp6 = models.FloatField()
    nexp6_prec = models.FloatField()
    nexp6_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp6_sourceid', blank=True, related_name='rn_nexp6_sourceid')
    gamma7 = models.FloatField()
    gamma7_prec = models.FloatField()
    gamma7_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma7_sourceid', blank=True, related_name='rn_gamma7_sourceid')
    delta7 = models.FloatField()
    delta7_prec = models.FloatField()
    delta7_sourceid = models.ForeignKey(Sources, null=True, db_column='delta7_sourceid', blank=True, related_name='rn_delta7_sourceid')
    nexp7 = models.FloatField()
    nexp7_prec = models.FloatField()
    nexp7_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp7_sourceid', blank=True, related_name='rn_nexp7_sourceid')
    gamma8 = models.FloatField()
    gamma8_prec = models.FloatField()
    gamma8_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma8_sourceid', blank=True, related_name='rn_gamma8_sourceid')
    delta8 = models.FloatField()
    delta8_prec = models.FloatField()
    delta8_sourceid = models.ForeignKey(Sources, null=True, db_column='delta8_sourceid', blank=True, related_name='rn_delta8_sourceid')
    nexp8 = models.FloatField()
    nexp8_prec = models.FloatField()
    nexp8_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp8_sourceid', blank=True, related_name='rn_nexp8_sourceid')
    gamma9 = models.FloatField()
    gamma9_prec = models.FloatField()
    gamma9_sourceid = models.ForeignKey(Sources, null=True, db_column='gamma9_sourceid', blank=True, related_name='rn_gamma9_sourceid')
    delta9 = models.FloatField()
    delta9_prec = models.FloatField()
    delta9_sourceid = models.ForeignKey(Sources, null=True, db_column='delta9_sourceid', blank=True, related_name='rn_delta9_sourceid')
    nexp9 = models.FloatField()
    nexp9_prec = models.FloatField()
    nexp9_sourceid = models.ForeignKey(Sources, null=True, db_column='nexp9_sourceid', blank=True, related_name='rn_nexp9_sourceid')
    class Meta:
        db_table = u'transitions'

###
# thanks to hitran

    def XML_Broadening(self):
        """
        Build and return the XML for the various broadening environments
        gamma, delta, nexp

        """

        gamma = ( self.gamma1, self.gamma2, self.gamma3, self.gamma4, self.gamma5,
                  self.gamma6, self.gamma7, self.gamma8, self.gamma9 )
        gamma_prec = ( self.gamma1_prec, self.gamma2_prec, self.gamma3_prec, self.gamma4_prec, self.gamma5_prec,
                       self.gamma6_prec, self.gamma7_prec, self.gamma8_prec, self.gamma9_prec )
        gamma_sourceid = ( self.gamma1_sourceid, self.gamma2_sourceid, self.gamma3_sourceid, self.gamma4_sourceid, self.gamma5_sourceid,
                           self.gamma6_sourceid, self.gamma7_sourceid, self.gamma8_sourceid, self.gamma9_sourceid )
       #delta = ( self.delta1, self.delta2, self.delta3, self.delta4, self.delta5,
       #          self.delta6, self.delta7, self.delta8, self.delta9 )
       #delta_prec = ( self.delta1_prec, self.delta2_prec, self.delta3_prec, self.delta4_prec, self.delta5_prec,
       #               self.delta6_prec, self.delta7_prec, self.delta8_prec, self.delta9_prec )
       #delta_sourceid = ( self.delta1_sourceid, self.delta2_sourceid, self.delta3_sourceid, self.delta4_sourceid, self.delta5_sourceid,
       #                   self.delta6_sourceid, self.delta7_sourceid, self.delta8_sourceid, self.delta9_sourceid )
        nexp = ( self.nexp1, self.nexp2, self.nexp3, self.nexp4, self.nexp5,
                 self.nexp6, self.nexp7, self.nexp8, self.nexp9 )
        nexp_prec = ( self.nexp1_prec, self.nexp2_prec, self.nexp3_prec, self.nexp4_prec, self.nexp5_prec,
                      self.nexp6_prec, self.nexp7_prec, self.nexp8_prec, self.nexp9_prec )
        nexp_sourceid = ( self.nexp1_sourceid, self.nexp2_sourceid, self.nexp3_sourceid, self.nexp4_sourceid, self.nexp5_sourceid,
                          self.nexp6_sourceid, self.nexp7_sourceid, self.nexp8_sourceid, self.nexp9_sourceid )

        broadening_xml = []
        for idc in curenvid:
            lineshape_xml = []
            lineshape_xml.append('      <Lineshape name="Lorentzian">\n'\
                   '      <Comments>The temperature-dependent pressure'\
                   ' broadening Lorentzian lineshape</Comments>\n'\
                   '      <LineshapeParameter name="gammaL">\n'\
                   '        <FitParameters functionRef="%sgammaL">\n'\
                   '          <FitArgument name="T" units="K">\n'\
                   '          </FitArgument>\n'\
                   '          <FitParameter name="gammaL_ref">\n'
                   % func_prefix)
            if gamma_sourceid[idc]:
                lineshape_xml.append('           <SourceRef>%s%s</SourceRef>\n'
                                     % (source_prefix, gamma_sourceid[idc]))
            lineshape_xml.append('            <Value units="1/cm">%s</Value>\n'
                                 % gamma[idc])
            lineshape_xml.append('            <Accuracy type="statistical" relative="true"'
                                 '>%s</Accuracy>\n' % str(gamma_prec[idc]))
            lineshape_xml.append('          </FitParameter>\n')
            lineshape_xml.append('          <FitParameter name="n">\n')
            if nexp_sourceid[idc]:
                lineshape_xml.append('            <SourceRef>%s%s'
                                     '</SourceRef>\n' % (source_prefix, nexp_sourceid[idc]))
            lineshape_xml.append('            <Value units="unitless">%s'
                                 '</Value>\n' % nexp[idc])
            lineshape_xml.append('            <Accuracy type="statistical" relative="true"'
                                 '>%s</Accuracy>\n' % str(nexp_prec[idc]))
            lineshape_xml.append('          </FitParameter>\n')
            lineshape_xml.append('        </FitParameters>\n'\
                                 '      </LineshapeParameter>\n</Lineshape>\n')
            broadening_xml.append('    <Broadening'
                ' envRef="%sBroadening-%s" name="pressure">\n'
                '%s    </Broadening>\n' % (env_prefix, allenv[idc], ''.join(lineshape_xml)))
        return '    %s\n' % ''.join(broadening_xml)

#
###

###
# thanks to smpo

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
           #self.low = ''
            self.low = 0                                                                           # must be double
        if len(arg)>3:
            self.up = arg[3]
        else:
           #self.up = ''
            self.up = 0                                                                            # must be double
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
    def __init__(self, id, com, temp, press=(), species=[]):
        self.id = id
        self.comment = com
        self.temperature = temp
        self.pressure = press
        if len(species)>0:
            self.Species = []
            for specie in species:
                self.Species.append(EnvSpecie(specie[0],specie[1]))
