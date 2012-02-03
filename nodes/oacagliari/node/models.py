# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from decimal import *
import re

import dictionaries

from vamdctap.bibtextools import *
from vamdctap.generators import makeSourceRefs


#def returnXMLSource(SourcesIDs, NodeName):
#    SourceTypePrefix = u"B"
#    CompletePrefix = SourceTypePrefix + NodeName + u"-"
#    result = u""
#    for s in SourcesIDs:
#        result += u"<SourceRef>" + CompletePrefix + str(s) + u"</SourceRef>"
#    if len(result)>0: result += u"\n"
#    return result



class Author(object):
    def __init__(self, Name, Address):
        self.Name = Name
        self.Address = Address

class BibRef(object):
    # simple dummy object to define a Method 
    def __init__(self, SourceID, Category, SourceName, Year, Authors, Title):
        self.SourceID = SourceID
        self.Category = Category
        self.SourceName = SourceName
        self.Year = Year
        self.Authors = Authors
        self.Title = Title

class Method(object):
    # simple dummy object to define a Method 
    def __init__(self, mid, description, Sources):
        self.id = mid
        self.category = 'theory'
        self.description, tmpbib = description
        self.Sources = []
        for bib in tmpbib:
            if bib.bibtex:
                if not (bib in Sources):
                    self.Sources.append(bib)
        self.SourcesRef = [b.pk for b in self.Sources]
                    
        
class NormalMode(models.Model):
    def __init__(self, normalmode_id, frequency, intensity, sym_type, displacementvectors, electronicstate, elements, Methods, SourceRefs): 
        #electronicStateRef 
        self.pointgroupsymmetry = sym_type
        self.normalmodeidtype = normalmode_id #NormalModeIDType, defining unique identifier for this mode, to be referenced
        self.HarmonicFrequency = str(frequency * Decimal('29979.2458'))
        self.intensity = intensity
        self.electronicstate = electronicstate
        self.NormalModesMethod = Methods
        self.NormalModesSourceRef = SourceRefs
        if displacementvectors: 
            self.displacementvectors = eval(displacementvectors)
            self.displacementvectorsx = []
            self.displacementvectorsy = []
            self.displacementvectorsz = []
            self.displacementvectorselementref = []
            for index in range(len(elements)): #XXX
                self.displacementvectorselementref.append(elements[index])
                self.displacementvectorsx.append(self.displacementvectors[0 + index * 3 ])
                self.displacementvectorsy.append(self.displacementvectors[1 + index * 3 ])
                self.displacementvectorsz.append(self.displacementvectors[2 + index * 3 ])
        else:
            self.displacementvectors = None
    def returnXML(self, elements, method, RefSource, NodeName): 

        result = '<NormalMode id="V' + NodeName + "-" + str(self.normalmodeidtype) + '"'
        if self.pointgroupsymmetry:
            result += ' pointGroupSymmetry="' + self.pointgroupsymmetry + '"'
        if method:
            result += ' methodRef="M' + NodeName + "-" + str(method) + '"'
        result += '>\n'
        #result += returnXMLSource(RefSource, NodeName)
        result += '<HarmonicFrequency>\n'
        result += '<Value units="MHz">' + str(self.harmonicfrequency * Decimal('29979.2458')) + '</Value>\n'
        #result += '<Accuracy>1</Accuracy>\n'
        result += '</HarmonicFrequency>\n'
        result += '<Intensity>\n'
        result += '<Value units="km/mol">' + str(self.intensity) + '</Value>\n'
        result += '</Intensity>\n'
        if self.displacementvectors:
            result += '<DisplacementVectors units="1/cm">\n'
            for index in range(len(elements)): #XXX
                result += '<Vector ref="' + elements[index] + '"'
                result += ' x3="' + self.displacementvectors[0 + index * 3 ] + '"'
                result += ' y3="' + self.displacementvectors[1 + index * 3 ] + '"'
                result += ' z3="' + self.displacementvectors[2 + index * 3 ] + '"/>\n'
            result += '</DisplacementVectors>\n'
            
        result +="</NormalMode>\n"
        return result
        
class MolecularChemicalSpecies():
    def __init__(self, moleculestructure, MoleculeStructureMethod, MoleculeStructureSourceRef, normalmodes, NormalModesMethod, NormalModesSourceRef):
        #self.moleculestructure = moleculestructure.replace("<molecule>", '<cml xmlns="http://www.xml-cml.org/schema" xsi:schemaLocation="http://www.xml-cml.org/schema ../../schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">').replace("</molecule>", "</cml>")
        self.moleculestructure = moleculestructure
        self.MoleculeStructureMethod = MoleculeStructureMethod
        #self.normalmodes = returnXMLSource(NormalModesSourceRef, NodeName) + normalmodes
        #self.normalmodes = normalmodes
        #self.NormalModesMethod = NormalModesMethod
        #self.NormalModesSourceRef = NormalModesSourceRef
        self.MoleculeStructureSourceRef = MoleculeStructureSourceRef
        
    def CML(self):
        return self.moleculestructure.replace("<molecule>", "").replace("</molecule>", "").replace("atom ", "cml:atom ").replace("atomA", "cml:atomA").replace("bond", "cml:bond")


class Bibliography(models.Model):
    bib_id = models.AutoField(primary_key=True)
    #type = models.ForeignKey(Reftype)
    #series = models.ForeignKey(PublicationSeries)
    #authors = models.ManyToManyField(Authors) # , through = "AuthorGroups"
    #editors = models.ManyToManyField(Editors) # , through = "EditorsGroups"
    #publisher = models.ForeignKey(Publishers)
    #title = models.TextField(blank=True)
    #volume = models.IntegerField(null=True, blank=True)
    #doi = models.TextField(blank=True)
    #page_begin = models.CharField(max_length = 45, blank=True)
    #page_end = models.CharField(max_length = 45,blank=True)
    #uri = models.TextField(blank=True)
    #city = models.CharField(max_length = 45, blank=True)
    #version = models.CharField(max_length = 45, blank=True)
    #source_name = models.TextField(blank=True)
    #date = models.DateField(null=True, blank=True)
    #reference = models.TextField(blank=True)
    bibtex = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'bibliography'
    def __unicode__(self):
        return self.title + str(self.authors.all())
    def XML(self):
        """
        This function replace the source ID with the database ID Bibliography record
        and return the hard XML code by the function BibTeX2XML
        """
        try: NODEID = dictionaries.RETURNABLES['NodeID']
        except: NODEID = 'PleaseFillTheNodeID'
        if self.bibtex:
            r = r"sourceID=\"B"+ NODEID + r"-.*\""
            newidvalue = u'sourceID="B'+ NODEID + u"-" + str(self.bib_id) + u'"'
            result = re.sub(r, newidvalue,  BibTeX2XML( self.bibtex ))
            return unicode(result)
    #def XML(self):
    #    """
    #    This function return the hard XML code by the function BibTeX2XML
    #    """
    #    if self.bibtex:
    #        return BibTeX2XML( self.bibtex )
    def bibtextoref(self):
        if self.bibtex:
            from pybtex.database.input import bibtex
            parser = bibtex.Parser()
            bib_data = parser.parse_stream(self.bibtex)
            if "title" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_title = bib_data.entries[bib_data.entries.keys(0)].fields['title']
            else:
                tmp_title = None
            if "pages" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_page_begin, tmp_page_end  = re.split(r"[,-]", bib_data.entries[bib_data.entries.keys(0)].fields['pages'])
            if "volume" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_volume = bib_data.entries[bib_data.entries.keys(0)].fields['volume']
            if "doi" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_doi = bib_data.entries[bib_data.entries.keys(0)].fields['doi']
            return BibRef(self.bib_id, "book", "SourceName", "2011", [Author("Author01", None), Author("Author02", None)], tmp_title)



#class AuthGroup(models.Model):
#    id = models.IntegerField(primary_key=True)
#    name = models.CharField(unique=True, max_length=240)
#    class Meta:
#        db_table = u'auth_group'

#class AuthGroupPermissions(models.Model):
#    id = models.IntegerField(primary_key=True)
#    group_id = models.IntegerField()
#    permission_id = models.IntegerField()
#    class Meta:
#        db_table = u'auth_group_permissions'

#class AuthMessage(models.Model):
#    id = models.IntegerField(primary_key=True)
#    user_id = models.IntegerField()
#    message = models.TextField()
#    class Meta:
#        db_table = u'auth_message'

#class AuthPermission(models.Model):
#    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=150)
#    content_type_id = models.IntegerField()
#    codename = models.CharField(unique=True, max_length=255)
#    class Meta:
#        db_table = u'auth_permission'

#class AuthUser(models.Model):
#    id = models.IntegerField(primary_key=True)
#    username = models.CharField(unique=True, max_length=90)
#    first_name = models.CharField(max_length=90)
#    last_name = models.CharField(max_length=90)
#    email = models.CharField(max_length=225)
#    password = models.CharField(max_length=384)
#    is_staff = models.IntegerField()
#    is_active = models.IntegerField()
#    is_superuser = models.IntegerField()
#    last_login = models.DateTimeField()
#    date_joined = models.DateTimeField()
#    class Meta:
#        db_table = u'auth_user'

#class AuthUserGroups(models.Model):
#    id = models.IntegerField(primary_key=True)
#    user_id = models.IntegerField()
#    group_id = models.IntegerField()
#    class Meta:
#        db_table = u'auth_user_groups'

#class AuthUserUserPermissions(models.Model):
#    id = models.IntegerField(primary_key=True)
#    user_id = models.IntegerField()
#    permission_id = models.IntegerField()
#    class Meta:
#        db_table = u'auth_user_user_permissions'

#class Authors(models.Model):
#    author_id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=600, blank=True)
#    email = models.CharField(max_length=600, blank=True)
#    address = models.TextField(blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'authors'

class BasisSets(models.Model):
    basisset_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 45, blank=True, null=True,)
    description = models.TextField(blank=True, null=True,)
    bibliographies = models.ManyToManyField(Bibliography)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'basissets'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        else:
            returnstring += "NO NAME"
        if self.description:
            returnstring += " - " + self.description
        return returnstring



#class Bibliography(models.Model):
#    bib_id = models.IntegerField(primary_key=True)
#    type = models.ForeignKey("Reftype")
#    series = models.ForeignKey("PublicationSeries")
#    publisher = models.ForeignKey("Publishers")
#    title = models.TextField(blank=True)
#    volume = models.IntegerField(null=True, blank=True)
#    doi = models.TextField(blank=True)
#    page_begin = models.CharField(max_length=135, blank=True)
#    page_end = models.CharField(max_length=135, blank=True)
#    uri = models.TextField(blank=True)
#    city = models.CharField(max_length=135, blank=True)
#    version = models.CharField(max_length=135, blank=True)
#    source_name = models.TextField(blank=True)
#    date = models.DateField(null=True, blank=True)
#    reference = models.TextField(blank=True)
#    bibtex = models.TextField(blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'bibliography'

#class BasisSetsBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    basissets = models.ForeignKey("BasisSets")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'basissets_bibliographies'

#class BibliographyAuthors(models.Model):
#    id = models.IntegerField(primary_key=True)
#    authors = models.ForeignKey("Authors")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'bibliography_authors'

#class BibliographyEditors(models.Model):
#    id = models.IntegerField(primary_key=True)
#    bibliography = models.ForeignKey("Bibliography")
#    editors = models.ForeignKey("Editors")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'bibliography_editors'

class CalculationGroups(models.Model):
    calcgroup_id = models.AutoField(primary_key=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'calculationgroups'

class ChemistryCodes(models.Model):
    code_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, null = True, blank=True)
    version = models.CharField(max_length = 45, null = True, blank=True)
    description = models.TextField( null = True, blank=True)
    bibliographies = models.ManyToManyField(Bibliography)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(blank=True, null = True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'chemistrycodes'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        return self.name + " - " + self.version

class Calculations(models.Model):
    calc_id = models.AutoField(primary_key=True)
    code = models.ForeignKey(ChemistryCodes)
    input = models.TextField(blank=True) 
    input_md5 = models.CharField(max_length = 45, blank=True)
    output = models.TextField(blank=True)
    output_md5 = models.CharField(max_length = 45, blank=True)
    other_output = models.TextField(blank=True)
    other_output_md5 = models.CharField(max_length = 45, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'calculations'
                
    def __unicode__(self):
        stringreturn = ""
        if self.time_stamp:
            stringreturn += "Entry date: " + self.time_stamp + "\n"
        if self.qual_index:
            stringreturn += "Quality index: " + self.qual_index + "\n"
        if self.code:
            stringreturn += "code: " + str(self.code) + "\n"
        if self.input_md5:
            stringreturn += "Input File md5: " + self.input_md5 + "\n"
        if self.output_md5:
            stringreturn += "Output File md5: " + self.output_md5 + "\n"
        if self.other_output_md5:
            stringreturn += "Other Output File md5: " + self.other_output_md5 + "\n"
        if len(stringreturn) > 0:
            return stringreturn
        else:
            return "No Data"

class CalculationLists(models.Model):
    calc_list_id = models.AutoField(primary_key=True)
    calcgroup = models.ForeignKey(CalculationGroups)
    calc = models.ForeignKey(Calculations)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'calculationlists'



#class ChemistryCodesBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    chemistrycodes = models.ForeignKey("ChemistryCodes")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'chemistry_codes_bibliographies'

#class DdResonances(models.Model):
#    dd_id = models.IntegerField(primary_key=True)
#    vibanalisys = models.ForeignKey("VibrationalAnalyses")
#    vib_id1 = models.ForeignKey("TabulatedVibrations", db_column='vib_id1', related_name = "vib_1")
#    vib_id2 = models.ForeignKey("TabulatedVibrations", db_column='vib_id2', related_name = "vib_2")
#    k = models.FloatField(null=True, blank=True)
#    class Meta:
#        db_table = u'dd_resonances'

#class DipoleMoments(models.Model):
#    dip_id = models.IntegerField(primary_key=True)
#    state = models.ForeignKey("ElectronicStates")
#    calc_group = models.ForeignKey("CalculationGroups")
#    mu_x = models.FloatField()
#    mu_y = models.FloatField()
#    mu_z = models.FloatField()
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'dipole_moments'

#class DipoleMomentsBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    dipole_moments = models.ForeignKey("DipoleMoments")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'dipole_moments_bibliographies'

#class DjangoAdminLog(models.Model):
#    id = models.IntegerField(primary_key=True)
#    action_time = models.DateTimeField()
#    user_id = models.IntegerField()
#    content_type_id = models.IntegerField(null=True, blank=True)
#    object_id = models.TextField(blank=True)
#    object_repr = models.CharField(max_length=600)
#    action_flag = models.IntegerField()
#    change_message = models.TextField()
#    class Meta:
#        db_table = u'django_admin_log'

#class DjangoContentType(models.Model):
#    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=300)
#    app_label = models.CharField(unique=True, max_length=255)
#    model = models.CharField(unique=True, max_length=255)
#    class Meta:
#        db_table = u'django_content_type'

#class DjangoSession(models.Model):
#    session_key = models.CharField(max_length=120, primary_key=True)
#    session_data = models.TextField()
#    expire_date = models.DateTimeField()
#    class Meta:
#        db_table = u'django_session'

#class DjangoSite(models.Model):
#    id = models.IntegerField(primary_key=True)
#    domain = models.CharField(max_length=300)
#    name = models.CharField(max_length=150)
#    class Meta:
#        db_table = u'django_site'

#class Editors(models.Model):
#    editor_id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=600, blank=True)
#    address = models.TextField(blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'editors'



#class ElectronicStatesBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    electronic_states = models.ForeignKey("ElectronicStates")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'electronic_states_bibliographies'

#class ElectronicTransitions(models.Model):
#    transition_id = models.IntegerField(primary_key=True)
#    low_state = models.ForeignKey("ElectronicStates", related_name = "state_1")
#    up_state = models.ForeignKey("ElectronicStates", related_name = "state_2")
#    calc_group = models.ForeignKey(CalculationGroups)
#    energy = models.FloatField(null=True, blank=True)
#    osc_strenght = models.FloatField(null=True, blank=True)
#    mu_x = models.FloatField(null=True, blank=True)
#    mu_y = models.FloatField(null=True, blank=True)
#    mu_z = models.FloatField(null=True, blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'electronic_transitions'

#class ElectronicTransitionsBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    electronictransitions = models.ForeignKey("ElectronicTransitions")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'electronic_transitions_bibliographies'

class Elements(models.Model): 
    element_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, blank=True)
    symbol = models.CharField(max_length = 45, blank=True)
    atomic_number = models.IntegerField(null=True, blank=True)
    atomic_mass = models.IntegerField(null=True, blank=True)
    element_group = models.CharField(max_length = 45, blank=True)
    standard_atomic_weight = models.FloatField(null=True, blank=True)
    isotope_of = models.ForeignKey("self", null=True, blank=True)
    class Meta:
        db_table = u'elements'
    def __unicode__(self):
        return self.name + "(" + self.symbol + ", " + str(self.atomic_number) +  ", " + str(self.atomic_mass) + ")"
    def electron_number(self):
        return self.atomic_number





#class FermiResonances(models.Model):
#    fermi_id = models.IntegerField(primary_key=True)
#    vib_analisys = models.ForeignKey("VibrationalAnalyses")
#    vib_id1 = models.ForeignKey("TabulatedVibrations", db_column='vib_id1', related_name = "vib_3")
#    vib_id2 = models.ForeignKey("TabulatedVibrations", db_column='vib_id2', related_name = "vib_4")
#    vib_id3 = models.ForeignKey("TabulatedVibrations", db_column='vib_id3', related_name = "vib_5")
#    fi = models.FloatField(null=True, blank=True)
#    class Meta:
#        db_table = u'fermi_resonances'

class Geometries(models.Model):
    geom_id = models.AutoField(primary_key=True)
    geometry = models.TextField(blank=True)
    geometry_md5 = models.CharField(max_length = 45, blank=True)
    sym_group = models.TextField(blank=True)
    sym_elements = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'geometries'
    def __unicode__(self):
        return str(self.geometry)
    def returncmlstructure(self, SourceRefIDs):
        #this function return the geometry stored in self.geometry (cml format)
        #return returnXMLSource(SourceRefIDs, NodeName) + self.geometry 
        return makeSourceRefs(SourceRefIDs) + self.geometry 
    def returnelementslist(self):
        #this function return the list of elements
        result = []
        atoms = re.findall('id=".*" element', self.geometry)
        for row in atoms:
            s = row.split('"')
            result.append(s[1])
            #result.append(s[3] + s[1].replace("a", None))
        return result


#class IonisationEnergies(models.Model):
#    ion_id = models.IntegerField(primary_key=True)
#    start_state = models.ForeignKey("ElectronicStates", related_name = "state_3")
#    ion_state = models.ForeignKey("ElectronicStates", related_name = "state_4")
#    iontype = models.ForeignKey("IonisationTypes")
#    energy = models.FloatField(null=True, blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'ionisation_energies'

#class IonisationEnergiesBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    ionisation_energies = models.ForeignKey("IonisationEnergies")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'ionisation_energies_bibliographies'

#class IonisationTypes(models.Model):
#    iontype_id = models.IntegerField(primary_key=True)
#    description = models.TextField(blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'ionisation_types'

class MolecularSpecies(models.Model):
    species_id = models.AutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    formula = models.TextField(null=True, blank=True)
    inchi = models.TextField(null=True, blank=True)
    inchikey = models.CharField(max_length = 45, blank=True)
    aromatic_cycles = models.IntegerField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    isotopologue_of = models.ForeignKey("self", blank=True, null=True)
    
    def _get_molweight(self): return self.molweight()
    def _set_molweight(self, value): pass
    totalmolweight = property(_get_molweight,_set_molweight)

    class Meta:
        db_table = u'molecularspecies'
    def __unicode__(self):
        return_string = ""
        if self.name:
            return_string += "name: " + self.name + ";"
        if self.formula:
            return_string += "formula: " + self.formula + ";"
        #if self.inchi:
        #    return_string += "inchi: " + self.inchi + ";"
        if self.inchikey:
            return_string += "inchikey: " + self.inchikey + ";"
        #if self.aromatic_cycles:
        #    return_string += "aromatic_cycles: " + self.aromatic_cycles + ";"
        #if self.charge:
        #    return_string += "charge: " + self.charge + ";"
        if len(return_string)>0:
            return_string = return_string[:-1]
        return return_string
    def atoms(self):
        result = []
        for element in self.elementspecies_set.all():
            result.append(element)
        return result
    def electrons_number(self):
        electrons = 0
        for tmp_atom in self.atoms():
            electrons += tmp_atom.electron_number()
        electrons += self.charge
        return electrons
    def molweight(self):
        weight = 0
        if self.species_id:
            elements_species = ElementSpecies.objects.filter(species = self)
            for e in elements_species:
                weight += e.element.standard_atomic_weight
        return weight
        
        
class ElementSpecies(models.Model):
    elemspecies_id = models.AutoField(primary_key=True)
    element = models.ForeignKey(Elements)
    species = models.ForeignKey(MolecularSpecies)
    number = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'elementspecies'

#class Polarisabilities(models.Model):
#    pol_id = models.IntegerField(primary_key=True)
#    state = models.ForeignKey("ElectronicStates")
#    calc_group = models.ForeignKey("CalculationGroups")
#    low_freq_lim = models.FloatField(null=True, blank=True)
#    up_freq_lim = models.FloatField(null=True, blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'polarisabilities'

#class PolarisabilitiesBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    polarisabilities = models.ForeignKey("Polarisabilities")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'polarisabilities_bibliographies'

#class PublicationSeries(models.Model):
#    series_id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=600, blank=True)
#    shortname = models.CharField(max_length=600, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'publication_series'

#class Publishers(models.Model):
#    publisher_id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=600, blank=True)
#    address = models.TextField(blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'publishers'

#class Reftype(models.Model):
#    type_id = models.IntegerField(primary_key=True)
#    description = models.CharField(max_length=600, blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'reftype'




#class RotationalConstantsBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    rotational_constants = models.ForeignKey("RotationalConstants")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'rotational_constants_bibliographies'

#class TabulatedChis(models.Model):
#    chiid = models.IntegerField(primary_key=True)
#    vibanalisys = models.ForeignKey("VibrationalAnalyses")
#    vib_id1 = models.ForeignKey("TabulatedVibrations", db_column='vib_id1', related_name = "vib_8")
#    vib_id2 = models.ForeignKey("TabulatedVibrations", db_column='vib_id2', related_name = "vib_9")
#    chi = models.FloatField(null=True, blank=True)
#    class Meta:
#        db_table = u'tabulated_chis'

#class TabulatedPolarisabilities(models.Model):
#    poltable_id = models.IntegerField(primary_key=True)
#    pol = models.ForeignKey("Polarisabilities")
#    frequency = models.FloatField()
#    re_alpha_xx = models.FloatField(null=True, blank=True)
#    im_alpha_xx = models.FloatField(null=True, blank=True)
#    re_alpha_yy = models.FloatField(null=True, blank=True)
#    im_alpha_yy = models.FloatField(null=True, blank=True)
#    re_alpha_zz = models.FloatField(null=True, blank=True)
#    im_alpha_zz = models.FloatField(null=True, blank=True)
#    re_alpha_xy = models.FloatField(null=True, blank=True)
#    im_alpha_xy = models.FloatField(null=True, blank=True)
#    re_alpha_xz = models.FloatField(null=True, blank=True)
#    im_alpha_xz = models.FloatField(null=True, blank=True)
#    re_alpha_yz = models.FloatField(null=True, blank=True)
#    im_alpha_yz = models.FloatField(null=True, blank=True)
#    class Meta:
#        db_table = u'tabulated_polarisabilities'


        
class TheoryLevels(models.Model):
    thlevel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 45, blank=True)
    description = models.TextField(blank=True)
    bibliographies = models.ManyToManyField(Bibliography)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    xc_name = models.TextField(blank=True)
    xc_description = models.TextField(blank=True)
    comments = models.TextField(blank=True, null=True)
    class Meta:
        db_table = u'theorylevels'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        else:
            returnstring += "NO NAME"
        if self.description:
            returnstring += " - " + self.description
        return returnstring

    #def fullprint(self):
    #    print "th_level_id:" + str(self.th_level_id) + "name:" + str(self.name) + "description:" + str(self.description) + "time_stamp:" + str(self.time_stamp) + "qual_index:"  + str(self.qual_index) + "comments:" + str(self.comments)

class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    thlevel = models.ForeignKey(TheoryLevels)
    calc = models.ForeignKey(Calculations)
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'tasks'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        else:
            returnstring += "NO NAME"
        if self.description:
            returnstring += " - " + self.description
        return returnstring
    def usedbasissets(self):
        bs_list_id = []
        for bs in self.elementspeciesbasisset_set.all():
            if bs.basisset in bs_list_id:
                pass
            else:
                bs_list_id.append(bs.basisset)
        return bs_list_id
    def returnmethoddescriptionandbib(self):
        methoddescription = ""
        bibliographies = []
        #Chemistry code
        methoddescription += "implementation: " + self.calc.code.name + " " + self.calc.code.version + "\n"
        for bib in self.calc.code.bibliographies.all():
            if not (bib in bibliographies):
                bibliographies.append(bib)
        #Theory level
        methoddescription += "theory: " + self.thlevel.description + "\n"
        if self.thlevel.xc_name:
            methoddescription += "xc: " + self.thlevel.xc_description + "\n"
        for bib in self.thlevel.bibliographies.all():
            if not (bib in bibliographies):
                bibliographies.append(bib)
        #Basis sets
        bslist = self.usedbasissets()
        if len(bslist) > 0:
            methoddescription += "basis sets: "
            for bs in bslist:
                methoddescription += bs.name + ", "
                for bib in bs.bibliographies.all():
                    if not (bib in bibliographies):
                        bibliographies.append(bib)
            methoddescription = methoddescription[:-2] + "\n"
        return methoddescription, bibliographies
    
class ElectronicStates(models.Model):
    state_id = models.AutoField(primary_key=True)
    species = models.ForeignKey(MolecularSpecies)
    geom = models.ForeignKey(Geometries)
    task = models.ForeignKey(Tasks)
    bibliographies = models.ManyToManyField(Bibliography)
    total_energy = models.FloatField(null=True, blank=True)
    is_minimum = models.BooleanField(null=False)
    rel_energy = models.FloatField(null=True, blank=True)
    electronicstateenergy = models.ForeignKey("self", null=True, blank=True)
    symmetry = models.TextField(blank=True)
    multiplicity = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    #normalmodes = models.ManyToManyField(NormalMode)
    class Meta:
        db_table = u'electronicstates'
    def __unicode__(self):
        returnstring = ""
        if self.total_energy:
            returnstring += "Total Energy: " + str(self.total_energy) + "; "
        if self.multiplicity:
            returnstring += "Multiplicity: " + str(self.multiplicity)
        return returnstring
    
    
class RotationalConstants(models.Model):
    rot_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(ElectronicStates)
    a = models.FloatField(null=True, blank=True)
    b = models.FloatField(null=True, blank=True)
    c = models.FloatField(null=True, blank=True)
    wilson_dj = models.FloatField(null=True, blank=True)
    wilson_djk = models.FloatField(null=True, blank=True)
    wilson_dk = models.FloatField(null=True, blank=True)
    nielsen_dj = models.FloatField(null=True, blank=True)
    nielsen_djk = models.FloatField(null=True, blank=True)
    nielsen_dk = models.FloatField(null=True, blank=True)
    nielsen_d_j = models.FloatField(null=True, blank=True)
    nielsen_r5 = models.FloatField(null=True, blank=True)
    nielsen_r6 = models.FloatField(null=True, blank=True)
    bibliographies = models.ManyToManyField(Bibliography)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'rotationalconstants'

#class TheoryLevelsBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    theorylevels = models.ForeignKey("TheoryLevels")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.CharField(max_length=135, blank=True)
#    class Meta:
#        db_table = u'theory_levels_bibliographies'

#class VanDerWaals(models.Model):
#    van_der_waals_id = models.IntegerField(primary_key=True)
#    state_id_1 = models.ForeignKey("ElectronicStates", db_column='state_id_1', related_name = "state_9")
#    state_id_2 = models.ForeignKey("ElectronicStates", db_column='state_id_2', related_name = "state_10")
#    calc_group = models.ForeignKey("CalculationGroups")
#    effective_freq = models.FloatField(null=True, blank=True)
#    c6 = models.FloatField(null=True, blank=True)
#    k = models.FloatField(null=True, blank=True)
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'van_der_waals'

#class VanDerWallsBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    van_der_walls = models.ForeignKey("VanDerWaals")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'van_der_walls_bibliographies'

class VibrationalAnalysesAnarmonic(models.Model):
    vibanalysesanarmonic_id = models.AutoField(primary_key=True)
    polymode = models.TextField(blank=True)
    state = models.ForeignKey(ElectronicStates)
    task = models.ForeignKey(Tasks)
    bibliographies = models.ManyToManyField(Bibliography)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'vibrationalanalysesanarmonic'
            
            
class VibrationalAnalysesArmonic(models.Model):
    vibanalysisarmonic_id = models.AutoField(primary_key=True)
    state = models.ForeignKey(ElectronicStates)
    task = models.ForeignKey(Tasks)
    bibliographies = models.ManyToManyField(Bibliography)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'vibrationalanalysesarmonic'


class TabulatedVibrations(models.Model):
    vib_id = models.AutoField(primary_key=True) #Probably problem whit bigint
    vibrationalanalysesarmonic = models.ForeignKey(VibrationalAnalysesArmonic)
    sym_type = models.TextField(blank=True)
    frequency = models.FloatField(null=True, blank=True)
    ir_intensity = models.FloatField(null=True, blank=True)
    alpha_a = models.FloatField(null=True, blank=True)
    alpha_b = models.FloatField(null=True, blank=True)
    alpha_c = models.FloatField(null=True, blank=True)
    diff_mu_x = models.FloatField(null=True, blank=True)
    diff_mu_y = models.FloatField(null=True, blank=True)
    diff_mu_z = models.FloatField(null=True, blank=True)
    eigenvectors = models.TextField(blank=True)
    class Meta:
        db_table = u'tabulatedvibrations'
    def __unicode__(self):
        return_string = ""
        if self.sym_type:
            return_string += "sym_type: " + str(self.sym_type) + ";"
        if self.frequency:
            return_string += "frequency: " + str(self.frequency) + ";"
        if self.alpha_a:
            return_string += "alpha_a: " + str(self.alpha_a) + ";"
            return_string += "alpha_b: " + str(self.alpha_b) + ";"
            return_string += "alpha_c: " + str(self.alpha_c) + ";"
        if self.diff_mu_x:
            return_string += "diff_mu_x: " + str(self.diff_mu_x) + ";"
            return_string += "diff_mu_y: " + str(self.diff_mu_y) + ";"
            return_string += "diff_mu_z: " + str(self.diff_mu_z) + ";"
        if return_string:
            return return_string[:-1]
        else:
            return "Empty"


#class VibrationalAnalysisBibliographies(models.Model):
#    id = models.IntegerField(primary_key=True)
#    vibrationalalalysis = models.ForeignKey("VibrationalAnalyses")
#    bibliography = models.ForeignKey("Bibliography")
#    time_stamp = models.DateTimeField(null=True, blank=True)
#    qual_index = models.IntegerField(null=True, blank=True)
#    comments = models.TextField(blank=True)
#    class Meta:
#        db_table = u'vibrational_analysis_bibliographies'

class ElementSpeciesBasisSet(models.Model):
    elementspecies_basisset_id = models.AutoField(primary_key= True)
    basisset = models.ForeignKey(BasisSets)
    task = models.ForeignKey(Tasks)
    elementspecies = models.ForeignKey(ElementSpecies)
    
    class Meta:
        db_table = u'elementspecies_basisset'
