# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

#class Collisions(models.Model):
    #idcollision = models.IntegerField(primary_key=True, db_column='idCollision') # Field name made lowercase.
    #title = models.TextField()
    #idelementof = models.IntegerField(db_column='idElementOf') # Field name made lowercase.
    #idelementwith = models.IntegerField(db_column='idElementWith') # Field name made lowercase.
    #comment = models.TextField(blank=True)
    #idrefgroup = models.IntegerField(db_column='idRefGroup') # Field name made lowercase.
    #labellingtableof = models.IntegerField(db_column='labellingTableOf') # Field name made lowercase.
    #labellingtablewith = models.IntegerField(db_column='labellingTableWith') # Field name made lowercase.
    #reducedmassvalue = models.FloatField(null=True, db_column='reducedMassValue', blank=True) # Field name made lowercase.
    #reducedmassunit = models.IntegerField(null=True, db_column='reducedMassUnit', blank=True) # Field name made lowercase.
    #reducedmassidrefgroup = models.IntegerField(db_column='reducedMassIdRefGroup') # Field name made lowercase.
    #pescomment = models.TextField(db_column='pesComment', blank=True) # Field name made lowercase.
    #pesidrefgroup = models.IntegerField(db_column='pesIdRefGroup') # Field name made lowercase.
    #methodcomment = models.TextField(db_column='methodComment', blank=True) # Field name made lowercase.
    #methodidrefgroup = models.IntegerField(db_column='methodIdRefGroup') # Field name made lowercase.
    #rangeofenergy = models.TextField(db_column='rangeOfEnergy', blank=True) # Field name made lowercase.
    #idcrosssection = models.IntegerField(db_column='idCrossSection') # Field name made lowercase.
    #basisset = models.TextField(db_column='basisSet', blank=True) # Field name made lowercase.
    #fittitle = models.TextField(db_column='fitTitle', blank=True) # Field name made lowercase.
    #fittext = models.TextField(db_column='fitText', blank=True) # Field name made lowercase.
    #idfitequation = models.IntegerField(null=True, db_column='idFitEquation', blank=True) # Field name made lowercase.
    #precis = models.TextField(blank=True)
    #recommended = models.CharField(max_length=9)
    #year = models.IntegerField()
    #idcontributor = models.IntegerField(db_column='idContributor') # Field name made lowercase.
    #creationdate = models.DateField(db_column='creationDate') # Field name made lowercase.
    #modificationdate = models.DateField(db_column='modificationDate') # Field name made lowercase.
    #isvisible = models.IntegerField(db_column='isVisible') # Field name made lowercase.
    #class Meta:
        #db_table = u'Collisions'

#class CollisionsProcessus(models.Model):
    #idcollision = models.IntegerField(primary_key=True, db_column='idCollision') # Field name made lowercase.
    #idprocessus = models.IntegerField(primary_key=True, db_column='idProcessus') # Field name made lowercase.
    #class Meta:
        #db_table = u'Collisions_Processus'

#class CollisionsScientists(models.Model):
    #idcollision = models.IntegerField(primary_key=True, db_column='idCollision') # Field name made lowercase.
    #idscientist = models.IntegerField(primary_key=True, db_column='idScientist') # Field name made lowercase.
    #rank = models.IntegerField()
    #class Meta:
        #db_table = u'Collisions_Scientists'

#class Contributors(models.Model):
    #idcontributor = models.IntegerField(primary_key=True, db_column='idContributor') # Field name made lowercase.
    #firstname = models.CharField(max_length=90, db_column='firstName') # Field name made lowercase.
    #lastname = models.CharField(max_length=90, db_column='lastName') # Field name made lowercase.
    #mail = models.CharField(max_length=90)
    #class Meta:
        #db_table = u'Contributors'

#class Couplings(models.Model):
    #idcoupling = models.IntegerField(primary_key=True, db_column='idCoupling') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=90)
    #class Meta:
        #db_table = u'Couplings'

#class Elementtypes(models.Model):
    #idelementtype = models.IntegerField(primary_key=True, db_column='idElementType') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=90)
    #class Meta:
        #db_table = u'ElementTypes'

#class Elements(models.Model):
    #idelement = models.IntegerField(primary_key=True, db_column='idElement') # Field name made lowercase.
    #designation = models.CharField(max_length=60, blank=True)
    #stoichiometricformula = models.CharField(max_length=150, db_column='stoichiometricFormula', blank=True) # Field name made lowercase.
    #latex = models.CharField(max_length=60, blank=True)
    #molecularmass = models.FloatField(db_column='molecularMass') # Field name made lowercase.
    #molecularconstant = models.FloatField(db_column='molecularConstant') # Field name made lowercase.
    #typeofmolecule = models.CharField(max_length=51, db_column='typeOfMolecule', blank=True) # Field name made lowercase.
    #idelementtype = models.IntegerField(db_column='idElementType') # Field name made lowercase.
    #class Meta:
        #db_table = u'Elements'

class Energytables(models.Model):
    idenergytable = models.IntegerField(primary_key=True, db_column='idEnergyTable') # Field name made lowercase.
    symmelement = models.ForeignKey()
    #idsymmetricelement = models.IntegerField(db_column='idSymmetricElement') # Field name made lowercase.
    #title = models.TextField()
    #idrefgroup = models.IntegerField(db_column='idRefGroup') # Field name made lowercase.
    #comment = models.TextField(blank=True)
    #isvisible = models.IntegerField(db_column='isVisible') # Field name made lowercase.
    #energyunit = models.IntegerField(db_column='energyUnit') # Field name made lowercase.
    #energyorigin = models.CharField(max_length=300, db_column='energyOrigin', blank=True) # Field name made lowercase.
    #termsymbol = models.CharField(max_length=300, db_column='termSymbol', blank=True) # Field name made lowercase.
    #electroniccomponentdescription = models.CharField(max_length=300, db_column='electronicComponentDescription') # Field name made lowercase.
    #vibrationalcomponentdescription = models.CharField(max_length=300, db_column='vibrationalComponentDescription') # Field name made lowercase.
    #totalspinmomentums = models.FloatField(db_column='totalSpinMomentumS') # Field name made lowercase.
    #totalmolecularprojectionl = models.FloatField(db_column='totalMolecularProjectionL') # Field name made lowercase.
    #idcoupling = models.IntegerField(db_column='idCoupling') # Field name made lowercase.
    #exp = models.CharField(max_length=9)
    #creationdate = models.DateField(db_column='creationDate') # Field name made lowercase.
    #modificationdate = models.DateField(db_column='modificationDate') # Field name made lowercase.
    #class Meta:
        #db_table = u'EnergyTables'

#class EnergytablesLevels(models.Model):
    #idlevel = models.IntegerField(primary_key=True, db_column='idLevel') # Field name made lowercase.
    #idenergytable = models.IntegerField(unique=True, db_column='idEnergyTable') # Field name made lowercase.
    #level = models.IntegerField(unique=True)
    #energy = models.FloatField(null=True, blank=True)
    #class Meta:
        #db_table = u'EnergyTables_Levels'

#class EnergytablesLevelsQuantumnumbers(models.Model):
    #idlevel = models.IntegerField(primary_key=True, db_column='idLevel') # Field name made lowercase.
    #idquantumnumber = models.IntegerField(primary_key=True, db_column='idQuantumNumber') # Field name made lowercase.
    #value = models.FloatField()
    #class Meta:
        #db_table = u'EnergyTables_Levels_QuantumNumbers'

#class EnergytablesProcessus(models.Model):
    #idenergytable = models.IntegerField(primary_key=True, db_column='idEnergyTable') # Field name made lowercase.
    #idprocessus = models.IntegerField(primary_key=True, db_column='idProcessus') # Field name made lowercase.
    #class Meta:
        #db_table = u'EnergyTables_Processus'

#class EnergytablesQuantumnumbers(models.Model):
    #idenergytable = models.IntegerField(primary_key=True, db_column='idEnergyTable') # Field name made lowercase.
    #idquantumnumber = models.IntegerField(primary_key=True, db_column='idQuantumNumber') # Field name made lowercase.
    #position = models.IntegerField()
    #class Meta:
        #db_table = u'EnergyTables_QuantumNumbers'

#class Fitequations(models.Model):
    #idfitequation = models.IntegerField(primary_key=True, db_column='idFitEquation') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=150)
    #description = models.TextField()
    #processing = models.CharField(max_length=21)
    #class Meta:
        #db_table = u'FitEquations'

#class Fitlevels(models.Model):
    #idfitlevel = models.IntegerField(primary_key=True, db_column='idFitLevel') # Field name made lowercase.
    #idcollision = models.IntegerField(db_column='idCollision') # Field name made lowercase.
    #initiallevelof = models.IntegerField(db_column='initialLevelOf') # Field name made lowercase.
    #finallevelof = models.IntegerField(db_column='finalLevelOf') # Field name made lowercase.
    #initiallevelwith = models.IntegerField(db_column='initialLevelWith') # Field name made lowercase.
    #finallevelwith = models.IntegerField(db_column='finalLevelWith') # Field name made lowercase.
    #class Meta:
        #db_table = u'FitLevels'

#class Fitvalues(models.Model):
    #idfitlevel = models.IntegerField(primary_key=True, db_column='idFitLevel') # Field name made lowercase.
    #coefficient = models.CharField(max_length=45, primary_key=True)
    #value = models.FloatField(primary_key=True)
    #position = models.IntegerField()
    #class Meta:
        #db_table = u'FitValues'

#class Foreignvalues(models.Model):
    #idforeignvaluesset = models.IntegerField(primary_key=True, db_column='idForeignValuesSet') # Field name made lowercase.
    #initiallevelof = models.IntegerField(primary_key=True, db_column='initialLevelOf') # Field name made lowercase.
    #finallevelof = models.IntegerField(primary_key=True, db_column='finalLevelOf') # Field name made lowercase.
    #frequency = models.DecimalField(max_digits=14, decimal_places=4)
    #einsteincoefficient = models.FloatField(db_column='einsteinCoefficient') # Field name made lowercase.
    #gup = models.IntegerField(db_column='gUp') # Field name made lowercase.
    #uncertainty = models.DecimalField(max_digits=9, decimal_places=4)
    #class Meta:
        #db_table = u'ForeignValues'

#class Foreignvaluessets(models.Model):
    #idforeignvaluesset = models.IntegerField(primary_key=True, db_column='idForeignValuesSet') # Field name made lowercase.
    #idcollision = models.IntegerField(unique=True, db_column='idCollision') # Field name made lowercase.
    #creationdate = models.DateField(unique=True, db_column='creationDate') # Field name made lowercase.
    #idspectrodatabase = models.IntegerField(db_column='idSpectroDatabase') # Field name made lowercase.
    #idchemicalelementspectro = models.IntegerField(db_column='idChemicalElementSpectro') # Field name made lowercase.
    #filename = models.CharField(max_length=150, db_column='fileName') # Field name made lowercase.
    #infosurl = models.CharField(max_length=300, db_column='infosUrl') # Field name made lowercase.
    #version = models.CharField(max_length=9)
    #dateofentry = models.CharField(max_length=45, db_column='dateOfEntry') # Field name made lowercase.
    #class Meta:
        #db_table = u'ForeignValuesSets'

#class HyperfineQnums(models.Model):
    #idrecord = models.IntegerField(primary_key=True, db_column='idRecord') # Field name made lowercase.
    #idenergytable = models.IntegerField(null=True, db_column='idEnergyTable', blank=True) # Field name made lowercase.
    #idmolnucleus = models.IntegerField(null=True, db_column='idMolNucleus', blank=True) # Field name made lowercase.
    #idqnumber = models.IntegerField(null=True, db_column='idQNumber', blank=True) # Field name made lowercase.
    #idrefqnumber = models.IntegerField(null=True, db_column='idRefQNumber', blank=True) # Field name made lowercase.
    #class Meta:
        #db_table = u'Hyperfine_QNums'

#class Matchedenergytables(models.Model):
    #idmatchedenergytable = models.IntegerField(primary_key=True, db_column='idMatchedEnergyTable') # Field name made lowercase.
    #idenergytable = models.IntegerField(db_column='idEnergyTable') # Field name made lowercase.
    #creationdate = models.DateField(db_column='creationDate') # Field name made lowercase.
    #idspectrodatabase = models.IntegerField(db_column='idSpectroDatabase') # Field name made lowercase.
    #version = models.CharField(max_length=9)
    #class Meta:
        #db_table = u'MatchedEnergyTables'

#class MatchedenergytablesLevels(models.Model):
    #idmatchedlevel = models.IntegerField(primary_key=True, db_column='idMatchedLevel') # Field name made lowercase.
    #idmatchedenergytable = models.IntegerField(db_column='idMatchedEnergyTable') # Field name made lowercase.
    #level = models.IntegerField()
    #energy = models.FloatField()
    #degeneracy = models.IntegerField()
    #class Meta:
        #db_table = u'MatchedEnergyTables_Levels'

#class MoleculeBonds(models.Model):
    #idbond = models.IntegerField(primary_key=True, db_column='idBond') # Field name made lowercase.
    #bondorder = models.CharField(max_length=3, db_column='bondOrder', blank=True) # Field name made lowercase.
    #added = models.DateField(null=True, blank=True)
    #expires = models.DateField(null=True, blank=True)
    #idsymmetricelement = models.IntegerField(null=True, db_column='idSymmetricElement', blank=True) # Field name made lowercase.
    #idenergytable = models.IntegerField(null=True, db_column='idEnergyTable', blank=True) # Field name made lowercase.
    #class Meta:
        #db_table = u'Molecule_Bonds'

#class MoleculeNuclei(models.Model):
    #idmolnucleus = models.IntegerField(primary_key=True, db_column='idMolNucleus') # Field name made lowercase.
    #idsymmetricelement = models.IntegerField(null=True, db_column='idSymmetricElement', blank=True) # Field name made lowercase.
    #idenergytable = models.IntegerField(null=True, db_column='idEnergyTable', blank=True) # Field name made lowercase.
    #idnucleus = models.IntegerField(null=True, db_column='idNucleus', blank=True) # Field name made lowercase.
    #hcount = models.IntegerField(null=True, db_column='HCount', blank=True) # Field name made lowercase.
    #count = models.IntegerField(null=True, db_column='Count', blank=True) # Field name made lowercase.
    #added = models.DateField(null=True, blank=True)
    #expires = models.DateField(null=True, blank=True)
    #class Meta:
        #db_table = u'Molecule_Nuclei'

#class Nuclei(models.Model):
    #idnucleus = models.IntegerField(primary_key=True, db_column='idNucleus') # Field name made lowercase.
    #z = models.IntegerField(null=True, db_column='Z', blank=True) # Field name made lowercase.
    #symbol = models.CharField(max_length=9, blank=True)
    #isotope = models.IntegerField(null=True, blank=True)
    #spin = models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True)
    #added = models.DateField(null=True, blank=True)
    #expires = models.DateField(null=True, blank=True)
    #class Meta:
        #db_table = u'Nuclei'

#class NucleiBonds(models.Model):
    #idrecord = models.IntegerField(primary_key=True, db_column='idRecord') # Field name made lowercase.
    #idmolnucleus = models.IntegerField(null=True, db_column='idMolNucleus', blank=True) # Field name made lowercase.
    #idbond = models.IntegerField(null=True, db_column='idBond', blank=True) # Field name made lowercase.
    #added = models.DateField(null=True, blank=True)
    #expires = models.DateField(null=True, blank=True)
    #class Meta:
        #db_table = u'Nuclei_Bonds'

#class Processus(models.Model):
    #idprocessus = models.IntegerField(primary_key=True, db_column='idProcessus') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=60)
    #class Meta:
        #db_table = u'Processus'

#class Quantumnumbers(models.Model):
    #idquantumnumber = models.IntegerField(primary_key=True, db_column='idQuantumNumber') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=60, blank=True)
    #comment = models.TextField(blank=True)
    #class Meta:
        #db_table = u'QuantumNumbers'

#class Ratecoefficients(models.Model):
    #idcollision = models.IntegerField(primary_key=True, db_column='idCollision') # Field name made lowercase.
    #temperature = models.FloatField(primary_key=True)
    #initiallevelof = models.IntegerField(primary_key=True, db_column='initialLevelOf') # Field name made lowercase.
    #finallevelof = models.IntegerField(primary_key=True, db_column='finalLevelOf') # Field name made lowercase.
    #initiallevelwith = models.IntegerField(primary_key=True, db_column='initialLevelWith') # Field name made lowercase.
    #finallevelwith = models.IntegerField(primary_key=True, db_column='finalLevelWith') # Field name made lowercase.
    #iseffectiverate = models.IntegerField(primary_key=True, db_column='isEffectiveRate') # Field name made lowercase.
    #data = models.FloatField()
    #class Meta:
        #db_table = u'RateCoefficients'

class RefsAdsnotes(models.Model):
    idadsnote = models.IntegerField(primary_key=True, db_column='idAdsnote') # Field name made lowercase.
    value = models.TextField(blank=True)
    class Meta:
        db_table = u'Refs_Adsnotes'

class RefsAuthors(models.Model):
    idauthor = models.IntegerField(primary_key=True, db_column='idAuthor') # Field name made lowercase.
    surname = models.CharField(unique=True, max_length=60, blank=True)
    firstname = models.CharField(unique=True, max_length=60, db_column='firstName', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Refs_Authors'

class ManyToManyFieldWithCustomColumns(models.ManyToManyField):
    def _get_m2m_column_name(self, related):
        return related.model._meta.pk.db_column
    def _get_m2m_reverse_name(self, related):
        return self.db_column

class RefsJournals(models.Model):
    idjournal = models.IntegerField(primary_key=True, db_column='idJournal') # Field name made lowercase.
    name = models.CharField(max_length=765, blank=True)
    smallname = models.CharField(unique=True, max_length=30, db_column='smallName', blank=True) # Field name made lowercase.
    category = models.CharField(max_length=63)
    class Meta:
        db_table = u'Refs_Journals'

class RefsArticles(models.Model):
    idarticle = models.IntegerField(primary_key=True, db_column='idArticle') # Field name made lowercase.
    title = models.TextField(blank=True)
    url = models.TextField(blank=True)
    adsnote = models.ForeignKey(RefsAdsnotes,db_column='idAdsNote')
    journal = models.ForeignKey(RefsJournals,db_column='idJournal')
    volume = models.CharField(max_length=30, blank=True)
    issue = models.CharField(max_length=30, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField()
    page = models.CharField(max_length=60, blank=True)
    linktodata = models.TextField(db_column='linkToData', blank=True) # Field name made lowercase.
    status = models.CharField(max_length=12)
    authors = ManyToManyFieldWithCustomColumns(RefsAuthors,db_column='idAuthor',related_name='authors',db_table=u'Refs_Articles_Authors')
    class Meta:
        db_table = u'Refs_Articles'
    def __unicode__(self):
        return self.title
        

class RefsArticlesAuthors(models.Model):
    id = models.IntegerField(primary_key=True)
    idarticle = models.IntegerField(unique=True, db_column='idArticle') # Field name made lowercase.
    idauthor = models.IntegerField(unique=True, db_column='idAuthor') # Field name made lowercase.
    class Meta:
        db_table = u'Refs_Articles_Authors'

#class RefsArticlesKeywords(models.Model):
    #idarticle = models.IntegerField(unique=True, db_column='idArticle') # Field name made lowercase.
    #idkeyword = models.IntegerField(unique=True, db_column='idKeyword') # Field name made lowercase.
    #class Meta:
        #db_table = u'Refs_Articles_Keywords'

class RefsGroups(models.Model):
    idrefgroup = models.IntegerField(primary_key=True, db_column='idRefGroup') # Field name made lowercase.
    #idref = models.IntegerField(primary_key=True, db_column='idRef') # Field name made lowercase.
    article = models.ForeignKey(RefsArticles, db_column='idRef')
    issource = models.IntegerField(db_column='isSource') # Field name made lowercase.
    class Meta:
        db_table = u'Refs_Groups'
    def __unicode__(self):
        return self.idrefgroup

#class RefsKeywords(models.Model):
    #idkeyword = models.IntegerField(primary_key=True, db_column='idKeyword') # Field name made lowercase.
    #idcategory = models.IntegerField(unique=True, db_column='idCategory') # Field name made lowercase.
    #value = models.CharField(unique=True, max_length=150, blank=True)
    #class Meta:
        #db_table = u'Refs_Keywords'

#class RefsKeywordsCategories(models.Model):
    #idcategory = models.IntegerField(primary_key=True, db_column='idCategory') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=90)
    #class Meta:
        #db_table = u'Refs_Keywords_Categories'

#class Scientists(models.Model):
    #idscientist = models.IntegerField(primary_key=True, db_column='idScientist') # Field name made lowercase.
    #firstname = models.CharField(max_length=60, db_column='firstName') # Field name made lowercase.
    #lastname = models.CharField(max_length=60, db_column='lastName') # Field name made lowercase.
    #class Meta:
        #db_table = u'Scientists'

#class Spectrodatabases(models.Model):
    #idspectrodatabase = models.IntegerField(primary_key=True, db_column='idSpectroDatabase') # Field name made lowercase.
    #name = models.CharField(unique=True, max_length=60)
    #class Meta:
        #db_table = u'SpectroDatabases'

#class StatusAvailables(models.Model):
    #idcollision = models.IntegerField(primary_key=True, db_column='idCollision') # Field name made lowercase.
    #date = models.DateField()
    #status = models.TextField()
    #class Meta:
        #db_table = u'Status_Availables'

#class StatusCurrentworks(models.Model):
    #idcurrentwork = models.IntegerField(primary_key=True, db_column='idCurrentWork') # Field name made lowercase.
    #idelementof = models.IntegerField(db_column='idElementOf') # Field name made lowercase.
    #idelementwith = models.IntegerField(db_column='idElementWith') # Field name made lowercase.
    #temperatures = models.TextField(blank=True)
    #group = models.TextField(blank=True)
    #groupdetails = models.TextField(db_column='groupDetails', blank=True) # Field name made lowercase.
    #details = models.TextField(blank=True)
    #class Meta:
        #db_table = u'Status_CurrentWorks'

#class StatusNeeds(models.Model):
    #idneed = models.IntegerField(primary_key=True, db_column='idNeed') # Field name made lowercase.
    #idelementof = models.IntegerField(db_column='idElementOf') # Field name made lowercase.
    #idelementwith = models.IntegerField(db_column='idElementWith') # Field name made lowercase.
    #region = models.TextField(blank=True)
    #regiondetails = models.TextField(db_column='regionDetails', blank=True) # Field name made lowercase.
    #temperatures = models.TextField(blank=True)
    #class Meta:
        #db_table = u'Status_Needs'

#class Symmetricelements(models.Model):
    #idsymmetricelement = models.IntegerField(primary_key=True, db_column='idSymmetricElement') # Field name made lowercase.
    #idelement = models.IntegerField(unique=True, db_column='idElement') # Field name made lowercase.
    #idsymmetry = models.IntegerField(unique=True, db_column='idSymmetry') # Field name made lowercase.
    #class Meta:
        #db_table = u'SymmetricElements'

#class Symmetries(models.Model):
    #idsymmetry = models.IntegerField(primary_key=True, db_column='idSymmetry') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=60)
    #class Meta:
        #db_table = u'Symmetries'

#class Units(models.Model):
    #idunit = models.IntegerField(primary_key=True, db_column='idUnit') # Field name made lowercase.
    #designation = models.CharField(unique=True, max_length=60)
    #latex = models.CharField(max_length=60)
    #class Meta:
        #db_table = u'Units'

#class Versions(models.Model):
    #idversion = models.IntegerField(primary_key=True, db_column='idVersion') # Field name made lowercase.
    #versionnumber = models.IntegerField(unique=True, db_column='versionNumber') # Field name made lowercase.
    #versiontype = models.CharField(unique=True, max_length=33, db_column='versionType') # Field name made lowercase.
    #idversionedelement = models.IntegerField(unique=True, db_column='idVersionedElement') # Field name made lowercase.
    #comment = models.TextField(blank=True)
    #creationdate = models.DateField(db_column='creationDate') # Field name made lowercase.
    #class Meta:
        #db_table = u'Versions'

