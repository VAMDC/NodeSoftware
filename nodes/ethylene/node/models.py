# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

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

    def renameCharacterisation(self):
        result = self.name
        if(self.characid == 1):
           result = "E1"
        if(self.characid == 2):
           result = "P"

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
    v7 = models.IntegerField(null=True, blank=True)
    v8 = models.IntegerField(null=True, blank=True)
    v9 = models.IntegerField(null=True, blank=True)
    v10 = models.IntegerField(null=True, blank=True)
    v11 = models.IntegerField(null=True, blank=True)
    v12 = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'vibrational_levels'

class PolyadDescriptions(models.Model):
    poldesid = models.IntegerField(primary_key=True)
    nblev = models.IntegerField()
    levelid1 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid1', blank=True, related_name='rn_levelid1')
    levelid2 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid2', blank=True, related_name='rn_levelid2')
    levelid3 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid3', blank=True, related_name='rn_levelid3')
    levelid4 = models.ForeignKey(VibrationalLevels, null=True, db_column='levelid4', blank=True, related_name='rn_levelid4')
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
    qname22 = models.CharField(max_length=12)
    status22 = models.IntegerField()
    qname23 = models.CharField(max_length=12)
    status23 = models.IntegerField()
    qname24 = models.CharField(max_length=12)
    status24 = models.IntegerField()
    qname25 = models.CharField(max_length=12)
    status25 = models.IntegerField()
    qname26 = models.CharField(max_length=12)
    status26 = models.IntegerField()
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

class VibrationalSublevels(models.Model):
    sublevid = models.IntegerField(primary_key=True)
    moltypeid = models.ForeignKey(MoleculeTypes, db_column='moltypeid')
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
    qvalue22 = models.IntegerField()
    qvalue23 = models.IntegerField()
    qvalue24 = models.IntegerField()
    qvalue25 = models.IntegerField()
    qvalue26 = models.IntegerField()
    class Meta:
        db_table = u'vibrational_sublevels'

class MoleculesIsotopes(models.Model):
    isotopeid = models.IntegerField(primary_key=True)
    moltypeid = models.ForeignKey(MoleculeTypes, db_column='moltypeid')
    isotopename = models.CharField(max_length=30)
    inchi = models.CharField(max_length=120)
    inchikey = models.CharField(max_length=81)
    class Meta:
        db_table = u'molecules_isotopes'

class ScalarNumbers(models.Model):
    scalarid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
    polyadid = models.ForeignKey(Polyads, db_column='polyadid')
    beta = models.FloatField()
    gamma = models.FloatField()
    pi = models.FloatField()
    class Meta:
        db_table = u'scalar_numbers'

class VibrationalComponents(models.Model):
    vibcompid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
    polyadid = models.ForeignKey(Polyads, db_column='polyadid')
    sublevid1 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid1', blank=True, related_name='rn_sublevid1')
    coefficient1 = models.FloatField(null=True, blank=True)
    sublevid2 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid2', blank=True, related_name='rn_sublevid2')
    coefficient2 = models.FloatField(null=True, blank=True)
    sublevid3 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid3', blank=True, related_name='rn_sublevid3')
    coefficient3 = models.FloatField(null=True, blank=True)
    sublevid4 = models.ForeignKey(VibrationalSublevels, null=True, db_column='sublevid4', blank=True, related_name='rn_sublevid4')
    coefficient4 = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'vibrational_components'

class MolecularStates(models.Model):
    stateid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
    polyadid = models.ForeignKey(Polyads, db_column='polyadid')
    position = models.FloatField()
    j = models.IntegerField()
    symnameid = models.ForeignKey(SymmetryNames, db_column='symnameid')
    alpha = models.IntegerField()
    vibcompid = models.ForeignKey(VibrationalComponents, db_column='vibcompid')
    weight = models.IntegerField()
    class Meta:
        db_table = u'molecular_states'

    def PnJcn(self):
        return "P%s %s %s %s" % (self.polyadid.polyadnb,self.j,self.symnameid.name,self.alpha)

class Transitions(models.Model):
    transitionid = models.IntegerField(primary_key=True)
    isotopeid = models.ForeignKey(MoleculesIsotopes, db_column='isotopeid')
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

