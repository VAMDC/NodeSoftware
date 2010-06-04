# -*- coding: utf-8 -*-

from django.db import models

###################################
# References
###################################
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
    def _get_fullname(self):
        return self.firstname + ' ' + self.surname
    fullname = property(_get_fullname)

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

class RefsGroups(models.Model):
    idrefgroup = models.IntegerField(primary_key=True, db_column='idRefGroup') # Field name made lowercase.
    #idref = models.IntegerField(primary_key=True, db_column='idRef') # Field name made lowercase.
    article = models.ForeignKey(RefsArticles, db_column='idRef')
    issource = models.IntegerField(db_column='isSource') # Field name made lowercase.
    class Meta:
        db_table = u'Refs_Groups'
    def __unicode__(self):
        return self.idrefgroup
        
###################################
# End of references
###################################
        
###################################
# Elements
###################################

class Elements(models.Model):
    idelement = models.IntegerField(primary_key=True, db_column='idElement') # Field name made lowercase.
    designation = models.CharField(max_length=60, blank=True)
    stoichiometricformula = models.CharField(max_length=150, db_column='stoichiometricFormula', blank=True) # Field name made lowercase.
    latex = models.CharField(max_length=60, blank=True)
    molecularmass = models.FloatField(db_column='molecularMass') # Field name made lowercase.
    molecularconstant = models.FloatField(db_column='molecularConstant') # Field name made lowercase.
    typeofmolecule = models.CharField(max_length=51, db_column='typeOfMolecule', blank=True) # Field name made lowercase.
    idelementtype = models.IntegerField(db_column='idElementType') # Field name made lowercase.
    class Meta:
        db_table = u'Elements'
        
class Symmetries(models.Model):
    idsymmetry = models.IntegerField(primary_key=True, db_column='idSymmetry') # Field name made lowercase.
    designation = models.CharField(unique=True, max_length=60)
    class Meta:
        db_table = u'Symmetries'
        
class Symmetricelements(models.Model):
    idsymmel = models.IntegerField(primary_key=True, db_column='idSymmetricElement') # Field name made lowercase.
    element = models.ForeignKey(Elements, db_column='idElement')
    #idelement = models.IntegerField(unique=True, db_column='idElement') # Field name made lowercase.
    symmetry = models.ForeignKey(Symmetries, db_column='idSymmetry')
    #idsymmetry = models.IntegerField(unique=True, db_column='idSymmetry') # Field name made lowercase.
    class Meta:
        db_table = u'SymmetricElements'
        
###################################
# End of elements
###################################

###################################
# Energy tables
###################################
class ETables(models.Model):
    idenergytable = models.IntegerField(primary_key=True, db_column='idEnergyTable') # Field name made lowercase.
    symmelement = models.ForeignKey(Symmetricelements,db_column='idSymmetricElement')
    #idsymmetricelement = models.IntegerField(db_column='idSymmetricElement') # Field name made lowercase.
    title = models.TextField()
    idrefgroup = models.IntegerField(db_column='idRefGroup') # Field name made lowercase.
    comment = models.TextField(blank=True)
    isvisible = models.IntegerField(db_column='isVisible') # Field name made lowercase.
    energyunit = models.IntegerField(db_column='energyUnit') # Field name made lowercase.
    energyorigin = models.CharField(max_length=300, db_column='energyOrigin', blank=True) # Field name made lowercase.
    termsymbol = models.CharField(max_length=300, db_column='termSymbol', blank=True) # Field name made lowercase.
    electroniccomponentdescription = models.CharField(max_length=300, db_column='electronicComponentDescription') # Field name made lowercase.
    vibrationalcomponentdescription = models.CharField(max_length=300, db_column='vibrationalComponentDescription') # Field name made lowercase.
    totalspinmomentums = models.FloatField(db_column='totalSpinMomentumS') # Field name made lowercase.
    totalmolecularprojectionl = models.FloatField(db_column='totalMolecularProjectionL') # Field name made lowercase.
    idcoupling = models.IntegerField(db_column='idCoupling') # Field name made lowercase.
    exp = models.CharField(max_length=9)
    #creationdate = models.DateField(db_column='creationDate') # Field name made lowercase.
    #modificationdate = models.DateField(db_column='modificationDate') # Field name made lowercase.
    class Meta:
        db_table = u'EnergyTables'

class QNums(models.Model):
    idquantumnumber = models.IntegerField(primary_key=True, db_column='idQuantumNumber') # Field name made lowercase.
    designation = models.CharField(unique=True, max_length=60, blank=True)
    comment = models.TextField(blank=True)
    class Meta:
        db_table = u'QuantumNumbers'

class ELevels(models.Model):
    idlevel = models.IntegerField(primary_key=True, db_column='idLevel') # Field name made lowercase.
    etable = models.ForeignKey(ETables,db_column='idEnergyTable',related_name='levels')
    level = models.IntegerField(unique=True)
    energy = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'EnergyTables_Levels'

class EtLQNums(models.Model):
    level = models.ForeignKey(ELevels,db_column='idLevel', related_name='qnums')
    qnum = models.ForeignKey(QNums,db_column='idQuantumNumber', related_name='level')
    value = models.FloatField()
    class Meta:
       db_table = u'EnergyTables_Levels_QuantumNumbers'





###################################
# End of Energy tables
###################################
