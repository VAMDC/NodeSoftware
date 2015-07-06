# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from django.db.models import *
#from vamdctap.bibtextools import *
from latex2html import *

FILTER_DICT={}
# References which will always be returned
DATABASE_REFERENCES = [1921]


def formatstring(value, format, noneformat):
     if value is not None:
          return format % value
     else:
          return noneformat % ""


def formatqn(value):
    if value == None:
        return ''
    elif value > 99 and value < 360:
        return chr(55+value/10)+ "%01d" % ( value % 10)
    elif value < -9 and value > -260:
        return chr(95-(value-1)/10)+ "%01d" % -( value % -10)
    else:
        return str(value)


def format_degeneracy(value):
     if value == None:
          return ''
     elif value>999 and value < 3600:
          return chr(55+value/100) + "%02d" % (value % 100)
     else:
          return str(value)


     
class Molecules( Model):
     """
     The Molecules class contains general information of the species. It is on top of
     the species class and collects data which is general for all isotopologs of a molecule.
     """
     id                    = IntegerField(primary_key=True, db_column='M_ID') 
     name                  = CharField(max_length=200, db_column='M_Name', blank=True)
     symbol                = CharField(max_length=250, db_column='M_Symbol', blank=True)
     cas                   = CharField(max_length= 20, db_column='M_CAS', blank=True)
     stoichiometricformula = CharField(max_length=200, db_column='M_StoichiometricFormula', blank=True)
     structuralformula     = CharField(max_length=200, db_column='M_StructuralFormula', blank=True)
     trivialname           = CharField(max_length=200, db_column='M_TrivialName', blank=True)
     numberofatoms         = CharField(max_length= 20, db_column='M_NumberOfAtoms', blank=True)
     elementsymbol         = CharField(max_length=  3, db_column='M_ElementSymbol', blank=True)
     formalcharge          = IntegerField(db_column='M_FormalCharge', blank=True)
#     formalcharge          = CharField(max_length=  5, db_column='M_FormalCharge', blank=True)
     comment               = TextField(db_column='M_Comment', blank=True)
     class Meta:
       db_table = u'Molecules'
       

class DictAtoms( Model):
     """
     This table contains a list of atoms and some of their properties.
     """
     id                    = IntegerField(primary_key=True, db_column='DA_ID') 
     name                  = CharField(max_length=50, db_column='DA_Name', blank=True)
     symbol                = CharField(max_length=10, db_column='DA_Symbol', blank=True)
     element               = CharField(max_length=10, db_column='DA_Element', blank=True)
     massnumber            = IntegerField(db_column='DA_MassNumber', blank=True)
     mass                  = FloatField(db_column='DA_Mass', blank=True)
     abundance             = FloatField(db_column='DA_Abundance', blank=True)
     mostabundant          = IntegerField(db_column='DA_MostAbundant', blank=True)
     massreference         = IntegerField(db_column='DA_MassReference', blank=True)
     nuclearcharge         = IntegerField(db_column='DA_NuclearCharge', blank=True)
     class Meta:
       db_table = u'Dict_Atoms'
       

class Species( Model):
     """
     The species class contains information about a species-entry. One isotopolog might have
     more than one entry. These could be different electronic or vibrational states or simply
     archived entries related to outdated versions of the specie (outdated versions are kept and
     not deleted).
     """
     id                    = IntegerField(primary_key=True, db_column='E_ID')
     molecule              = ForeignKey(Molecules, db_column='E_M_ID')
     atom                  = ForeignKey(DictAtoms, db_column='E_DA_ID')
     speciestag            = IntegerField(db_column='E_TAG')
     name                  = CharField(max_length=200, db_column='E_Name')
     isotopolog            = CharField(max_length=100, db_column='E_Isotopomer')
     massnumber            = IntegerField(db_column='E_MassNumber')
     state                 = CharField(max_length=200, db_column='E_States')
     linearsymasym         = CharField(max_length= 20, db_column='E_LinearSymAsym')
     shell                 = CharField(max_length= 20, db_column='E_Shell')
     inchi                 = CharField(max_length=200, db_column='E_Inchi')
     inchikey              = CharField(max_length=100, db_column='E_InchiKey')
     origin                = IntegerField(db_column='E_Origin')
     contributor           = CharField(max_length=200, db_column='E_Contributor')
     version               = CharField(max_length=  5, db_column='E_Version')
     dateofentry           = DateField(db_column='E_DateOfEntry')
     comment               = TextField(db_column='E_Comment')
     archiveflag           = IntegerField(db_column='E_Archive')
     dateactivated         = DateField(db_column='E_DateActivated')
     datearchived          = DateField(db_column='E_DateArchived')
     changedate            = DateTimeField(db_column='E_ChangeDate')
     class Meta:
       db_table = u'Entries'
     
     #def getMassNumber(self):
     #     tag = str(self.speciestag)
     #     return tag[:-3] #self.speciestag[:-3]

     def CML(self):
          """
          Return the CML version of the molecular structure.
          Use the database function F_GetCML to get the string
          """
          cursor = connection.cursor()
          cursor.execute("SELECT F_GetCML4XSAMS(%s) as cml ", [self.id])
          return cursor.fetchone()[0]
     
     def get_shortcomment(self):
          return "%6s- v%2s:%s; %s" % (self.speciestag, self.version, self.isotopolog, self.state)


     cmlstring = property(CML)
     #massnumber = property(getMassNumber)
     shortcomment = property(get_shortcomment)
          

     def state_html(self):
          return latex2html(self.state)



class Datasets( Model):
     """
     This class contains the datasets for each specie. A dataset is a header for
     either calculated transitions, experimental transitions or states.
     """
     id                    = IntegerField(primary_key=True, db_column='DAT_ID')
     specie                = ForeignKey(Species, db_column='DAT_E_ID')
     userid                = IntegerField(db_column='DAT_U_ID')
     fileid                = IntegerField(db_column='DAT_FIL_ID') 
     speciestag            = IntegerField(db_column='DAT_E_Tag')
     qntag                 = IntegerField(db_column='DAT_QN_Tag') 
     comment               = TextField(db_column='DAT_Comment') 
     name                  = CharField(max_length=100, db_column='DAT_Name')
     type                  = CharField(max_length= 10, db_column='DAT_Type') 
     public                = IntegerField(db_column='DAT_Public') 
     archiveflag           = IntegerField(db_column='DAT_Archive') 
     hfsflag               = IntegerField(db_column='DAT_HFS') 
     createdate            = DateField(db_column='DAT_Createdate')
     activateddate         = DateField(db_column='DAT_Date_Activated')
     archvieddate          = DateField(db_column='DAT_Date_Archived')
     class Meta:
       db_table = u'Datasets'

class NuclearSpinIsomers(Model):
     """
     This class contains informations on nuclear spin isomers.
     """
     id     = IntegerField(primary_key=True, db_column='NSI_ID')
     specie = ForeignKey(Species, db_column='NSI_E_ID')
     name   = CharField(max_length=45, db_column='NSI_Name')
     lowestrovibsym = CharField(max_length=45, db_column='NSI_LowestRoVibSym')
     symmetrygroup  = CharField(max_length=45, db_column='NSI_SymmetryGroup')
     #lowestrovibstate = ForeignKey(States, db_column='NSI_LowestRoVib_EGY_ID')
     lowestrovibstate = IntegerField(db_column='NSI_LowestRoVib_EGY_ID')
     class Meta:
          db_table = u'NuclearSpinIsomers'

     def lowestrovibstateid(self):
          return '%s-origin-%s' % (self.lowestrovibstate, self.specie_id)

     
class States( Model):
     """
     This class contains the states of each specie.
     """
     id                    = IntegerField(primary_key=True, db_column='EGY_ID')
     specie                = ForeignKey(Species, db_column='EGY_E_ID')
     speciestag            = IntegerField(db_column='EGY_E_Tag')
     dataset               = ForeignKey(Datasets, db_column='EGY_DAT_ID')
     energy                = FloatField(null=True, db_column='EGY_Energy')
     uncertainty           = FloatField(null=True, db_column='EGY_Uncertainty')
     energyorigin          = IntegerField(db_column='EGY_EnergyOrigin_EGY_ID')
     mixingcoeff           = FloatField(null=True, db_column='EGY_PMIX')
     block                 = IntegerField(db_column='EGY_IBLK')
     index                 = IntegerField(db_column='EGY_INDX') 
     degeneracy            = IntegerField(db_column='EGY_IDGN') 
     nuclearstatisticalweight = IntegerField(db_column='EGY_NuclearStatisticalWeight')
     nsi                   = ForeignKey(NuclearSpinIsomers, db_column='EGY_NSI_ID')
     nuclearspinisomer     = CharField(max_length=10, db_column='EGY_NuclearSpinIsomer')
     nuclearspinisomersym  = CharField(max_length=45, db_column='EGY_NuclearSpinIsomerSym')
     nsioriginid           = IntegerField(db_column='EGY_NSI_LowestEnergy_EGY_ID')
     msgroup               = CharField(max_length=45, db_column='EGY_MS_Group')
     qntag                 = IntegerField(db_column='EGY_QN_Tag') 
     qn1                   = IntegerField(db_column='EGY_QN1')
     qn2                   = IntegerField(db_column='EGY_QN2') 
     qn3                   = IntegerField(db_column='EGY_QN3') 
     qn4                   = IntegerField(db_column='EGY_QN4') 
     qn5                   = IntegerField(db_column='EGY_QN5') 
     qn6                   = IntegerField(db_column='EGY_QN6') 
     user                  = CharField(max_length=40, db_column='EGY_User')      # obsolete
     timestamp             = IntegerField(db_column='EGY_TIMESTAMP')

     
     class Meta:
       db_table = u'Energies'
       ordering = ['energy']
       
     def origin(self):
          return '%s-origin-%s' % (self.energyorigin, self.specie_id)

     def nsiname(self):
          if self.nsi_id:
               return self.nsi.name
          else:
               return None

     def auxillary(self):
          try:
               if self.aux:
                    return 'true'
               else:
                    return ''
          except AttributeError:
               return ''

     def nsiorigin(self):
          return '%s-origin-%s' % (self.nsioriginid, self.specie_id)

     def qns_xml(self):
	"""Yield the XML for the state quantum numbers"""
        # remove "-origin" in order to retrieve also qns for state-origins
        try:
             #sid = self.id.replace('-origin-%s' % self.specie_id,'')
             sid = self.id.split('-')[0]
        except:
             sid = self.id
             
        qns = MolecularQuantumNumbers.objects.filter(state=sid)
        case = qns[0].case     
        caseNS = 'http://vamdc.org/xml/xsams/1.0/cases/%s' % case
        caseNSloc = '../../cases/%s.xsd' % case
        xml = []
        xml.append('<Case xsi:type="%s:Case" caseID="%s"'\
                   ' xmlns:%s="%s" xsi:schemaLocation="%s %s">'\
                  % (case, case, case, caseNS, caseNS, caseNSloc))
        xml.append('<%s:QNs>\n' % case)

        for qn in qns:
           if qn.attribute:
               # put quotes around the value of the attribute
               attr_name, attr_val = qn.attribute.split('=')
               qn.attribute = ' %s="%s"' % (attr_name, attr_val)
           else:
              qn.attribute = ''

           if qn.spinref:
               # add spinRef to attribute if it exists
               qn.attribute += ' nuclearSpinRef="%s"' % qn.spinref

           xml.append('<%s:%s%s>%s</%s:%s>\n' % (case, qn.label, qn.attribute , qn.value, case, qn.label) )
        xml.append('</%s:QNs>\n' % case)
        xml.append('</Case>\n')
        return ''.join(xml)

     # associate qns_xml with the XML attribute of the States class
     # so that generators.py checkXML() works:

     def get_qns_xml(self):
          """
          Yield the XML for state quantum numbers, generated from the filter-table
          """

          try:
               qns = FILTER_DICT[self.specie_id][self.qntag]
          except:
               if not FILTER_DICT.has_key(self.specie_id):
                    FILTER_DICT[self.specie_id]={}
               if not FILTER_DICT[self.specie_id].has_key(self.qntag):
                        
                    where = Q(specie = self.specie) & Q(qntag = self.qntag) # & ( Q(qn1=self.qn1) | Q(qn1__isnull=True)) & ( Q(qn2=self.qn1) | Q(qn2__isnull=True)) & ( Q(qn3=self.qn1) | Q(qn3__isnull=True)) & ( Q(qn4=self.qn1) | Q(qn4__isnull=True)) & ( Q(qn5=self.qn1) | Q(qn5__isnull=True)) & ( Q(qn6=self.qn1) | Q(qn6__isnull=True))                       
                    qns = QuantumNumbersFilter.objects.filter(where) #specie = self.specie, qntag = self.qntag)
                    FILTER_DICT[self.specie_id][self.qntag]=qns
          
          case = qns[0].case     
          caseNS = 'http://vamdc.org/xml/xsams/1.0/cases/%s' % case
          caseNSloc = '../../cases/%s.xsd' % case
          xml = []
          xml.append('<Case xsi:type="%s:Case" caseID="%s"'\
                     ' xmlns:%s="%s" xsi:schemaLocation="%s %s">'\
                     % (case, case, case, caseNS, caseNS, caseNSloc))
          xml.append('<%s:QNs>\n' % case)

          
          for qn in qns:
##               #if qn.label == 'L':
##               #     self.L = qn.valuefloat
##               #elif qn.label == 'S':
##               #     self.S = qn.valuefloat
               if qn.columnvalue:
                    exec 'value = self.qn%s' % qn.columnvalue
                    if qn.columnvaluefunc == 'half':
                         value -= 0.5
                         
               elif qn.valuefloat is not None:
                    value = qn.valuefloat
               elif qn.valuestring:
                    value = qn.valuestring
                    
##               exec 'self.%s = %s' % (qn.label, value)
##          return self.J
               if qn.attribute:
                    # put quotes around the value of the attribute
                    attr_name, attr_val = qn.attribute.split('=')
                    qn.attribute = ' %s="%s"' % (attr_name, attr_val)
               else:
                    qn.attribute = ''
                    
               if qn.spinref:
                    # add spinRef to attribute if it exists
                    qn.attribute += ' nuclearSpinRef="%s"' % qn.spinref
               
               xml.append('<%s:%s%s>%s</%s:%s>\n' % (case, qn.label, qn.attribute , value, case, qn.label) )
          xml.append('</%s:QNs>\n' % case)
          xml.append('</Case>\n')
          return ''.join(xml)

     XML = qns_xml


     def qns_dict(self):
          """ Yield the quantum numbers as a dictionary """
          qns = MolecularQuantumNumbers.objects.filter(state=self.id)
          dictqns = {}
          
          for qn in qns:
#               if qn.attribute:
#                    # put quotes around the value of the attribute
#                    attr_name, attr_val = qn.attribute.split('=')
#                    qn.attribute = ' %s="%s"' % (attr_name, attr_val)
#               else:
#                    qn.attribute = ''
#                    
#               if qn.spinref:
#                    # add spinRef to attribute if it exists
#                    qn.attribute += ' nuclearSpinRef="%s"' % qn.spinref

               dictqns.update({qn.label : qn.value})
          return dictqns

##     def attach_atomic_qn(self):
##          """
##          Attaches atomic states
##          """

##          qns = QuantumNumbersFilter.objects.filter(specie = self.specie)
          
##          for qn in qns:
##               #if qn.label == 'L':
##               #     self.L = qn.valuefloat
##               #elif qn.label == 'S':
##               #     self.S = qn.valuefloat
##               if qn.columnvalue:
##                    exec 'value = self.qn%s' % qn.columnvalue
##                    if qn.columnvaluefunc == 'half':
##                         value -= 0.5
                         
##               elif qn.valuefloat:
##                    value = qn.valuefloat
##               elif qn.valuestring:
##                    value = qn.valuestring
                    
##               exec 'self.%s = %s' % (qn.label, value)
##          return self.J

class AtomStates( Model):
     """
     This class contains the states of each specie.
     """
     id                    = IntegerField(primary_key=True, db_column='EGY_ID')
     specie                = ForeignKey(Species, db_column='EGY_E_ID')
     speciestag            = IntegerField(db_column='EGY_E_Tag')
     dataset               = ForeignKey(Datasets, db_column='EGY_DAT_ID')
     energy                = FloatField(null=True, db_column='EGY_Energy')
     uncertainty           = FloatField(null=True, db_column='EGY_Uncertainty')
     energyorigin          = IntegerField(db_column='EGY_EnergyOrigin_EGY_ID')
     mixingcoeff           = FloatField(null=True, db_column='EGY_PMIX')
     block                 = IntegerField(db_column='EGY_IBLK')
     index                 = IntegerField(db_column='EGY_INDX') 
     degeneracy            = IntegerField(db_column='EGY_IDGN') 
     nuclearstatisticalweight = IntegerField(db_column='EGY_NuclearStatisticalWeight')
     nuclearspinisomer     = CharField(max_length=10, db_column='EGY_NuclearSpinIsomer')
     qntag                 = IntegerField(db_column='EGY_QN_Tag') 
     qn1                   = IntegerField(db_column='EGY_QN1')
     qn2                   = IntegerField(db_column='EGY_QN2') 
     qn3                   = IntegerField(db_column='EGY_QN3') 
     qn4                   = IntegerField(db_column='EGY_QN4') 
     qn5                   = IntegerField(db_column='EGY_QN5') 
     qn6                   = IntegerField(db_column='EGY_QN6') 
     user                  = CharField(max_length=40, db_column='EGY_User')      # obsolete
     timestamp             = IntegerField(db_column='EGY_TIMESTAMP')
     class Meta:
       db_table = u'Energies'

     def get_Components(self):
          """This is required in order to supply a Components property
          for the makeAtomsComponents tagmaker."""
          self.attach_atomic_qn()
          return self
     Components = property(get_Components)
    
     def attach_atomic_qn(self):
          """
          Attaches atomic states
          """

          qns = QuantumNumbersFilter.objects.filter(specie = self.specie)
          self.F = None 
          for qn in qns:
               #if qn.label == 'L':
               #     self.L = qn.valuefloat
               #elif qn.label == 'S':
               #     self.S = qn.valuefloat
               if qn.columnvalue:
                    exec 'value = self.qn%s' % qn.columnvalue
                    if qn.columnvaluefunc == 'half':
                         value -= 0.5
                         
               elif qn.valuefloat:
                    value = qn.valuefloat
               elif qn.valuestring:
                    value = qn.valuestring

               # convert floats to integer for some QNs
               if qn.label in ['L']:
                    value = int(value)
                    
               exec 'self.%s = %s' % (qn.label, value)
          return self.J

     def auxillary(self):
          try:
               if self.aux:
                    return 'True'
               else:
                    return ''
          except AttributeError:
               return ''
          


class TransitionsCalc( Model):
     """
     This class contains the calculated transition frequencies (mysql-table Predictions).
     """
     id                    = IntegerField(primary_key=True, db_column='P_ID')
     specie                = ForeignKey(Species, db_column='P_E_ID')
     speciestag            = IntegerField(db_column='P_E_Tag')
     frequency             =  FloatField(null=True, db_column='P_Frequency')
     frequencyexp          =  FloatField(null=True, db_column='P_Frequency_Exp')
     intensity             =  FloatField(null=True, db_column='P_Intensity')
     einsteina             =  FloatField(null=True, db_column='P_EinsteinA')
     smu2                  =  FloatField(null=True, db_column='P_Smu2')
     uncertainty           =  FloatField(null=True, db_column='P_Uncertainty')
     energylower           =  FloatField(null=True, db_column='P_Energy_Lower')
     energyupper           =  FloatField(null=True, db_column='P_Energy_Upper')
     qntag                 = IntegerField(db_column='P_QN_TAG')
     qnup1                 = IntegerField(db_column='P_QN_Up_1')
     qnup2                 = IntegerField(db_column='P_QN_Up_2')
     qnup3                 = IntegerField(db_column='P_QN_Up_3')
     qnup4                 = IntegerField(db_column='P_QN_Up_4')
     qnup5                 = IntegerField(db_column='P_QN_Up_5')
     qnup6                 = IntegerField(db_column='P_QN_Up_6')
     qnlow1                = IntegerField(db_column='P_QN_Low_1')
     qnlow2                = IntegerField(db_column='P_QN_Low_2')
     qnlow3                = IntegerField(db_column='P_QN_Low_3')
     qnlow4                = IntegerField(db_column='P_QN_Low_4')
     qnlow5                = IntegerField(db_column='P_QN_Low_5')
     qnlow6                = IntegerField(db_column='P_QN_Low_6')
     dummy                 = CharField(max_length=20, db_column ='P_Dummy')
     unit                  = CharField(max_length=200, db_column='P_Unit')
     degreeoffreedom       = IntegerField(db_column='P_Degree_Of_Freedom')
     upperstatedegeneracy  = IntegerField(db_column='P_Upper_State_Degeneracy')
     originid              = IntegerField(db_column='P_Origin_Id')
     hfsflag               = IntegerField(db_column='P_HFS')
     userid                = IntegerField(db_column='P_U_ID')
     dataset               = ForeignKey(Datasets, db_column='P_DAT_ID')
     qualityflag           = IntegerField(db_column='P_Quality')
     archiveflag           = IntegerField(db_column='P_Archive')
     timestamp             = DateTimeField(db_column='P_TIMESTAMP')
     upperstateref =  ForeignKey(States, related_name='upperstate',
                                 db_column='P_Up_EGY_ID')
     lowerstateref =  ForeignKey(States, related_name='lowerstate',
                                 db_column='P_Low_EGY_ID')
     
     upstate =  ForeignKey(States, related_name='upperstate',
                           db_column='P_Up_EGY_ID')
     lostate =  ForeignKey(States, related_name='lowerstate',
                           db_column='P_Low_EGY_ID')
     #frequencyArray        
     
     def __unicode__(self):
          return u'ID:%s Tag:%s Freq: %s'%(self.id,self.speciestag,self.frequency)

     def specieid(self):
          return '%s-hyp%s' % (self.specie_id,self.hfsflag)

     def process_class(self):
          pclass=['rota']
          if self.hfsflag>0:
               pclass.append('hyp%d' % self.hfsflag)
          return pclass
     
     def attach_evaluation(self):
          """
          """
          self.qualities=[]
          self.recommendations=[]
          self.evalrefs=[]
          evals = self.evaluation_set.all()
          for i in evals:
               self.qualities.append(i.quality)
               self.recommendations.append(i.recommended)
               self.evalrefs.append(i.source_id)
          return self.qualities
     
     def attach_exp_frequencies(self):
         """
         Create lists of frequencies, units, sources, ... for each transition.
         The calculated frequency is given anyway followed by experimental
         frequencies (db-table: Frequencies). In addition a unique list of
         methods for the experimental data is created and returned.

         Returns:
         - modified transitions (frequencies, ... attached as lists)
         - methods for experimental data

         """
         
         # Attach the calculated frequency first
         self.frequencies=[self.frequency]
         self.units=[self.unit]
         self.uncertainties=[self.uncertainty]
         self.refs=[""]
         self.methods=[self.dataset_id]
         self.evaluations=[self.attach_evaluation()]
         self.recommendations=[self.recommendations]
         self.evalrefs=[self.evalrefs]

         exptranss = TransitionsExp.objects.filter(specie=self.specie,
                                                   dataset__archiveflag=0,
                                                   qnup1=self.qnup1,
                                                   qnlow1=self.qnlow1,
                                                   qnup2=self.qnup2,
                                                   qnlow2=self.qnlow2,
                                                   qnup3=self.qnup3,
                                                   qnlow3=self.qnlow3,
                                                   qnup4=self.qnup4,
                                                   qnlow4=self.qnlow4,
                                                   qnup5=self.qnup5,
                                                   qnlow5=self.qnlow5,
                                                   qnup6=self.qnup6,
                                                   qnlow6=self.qnlow6)

         for exptrans in exptranss:
              self.frequencies.append(exptrans.frequency)
              self.units.append(exptrans.unit)
              self.uncertainties.append(exptrans.uncertainty)
              self.evaluations.append(exptrans.attach_evaluation())
              self.recommendations.append(exptrans.recommendations)
              self.evalrefs.append(exptrans.evalrefs)
              # get sources
              s= exptrans.sources.all().values_list('source',flat=True)
              self.refs.append(s)

              #if s.count()>0:
              #     method = "EXP" + "-".join(str(source) for source in s)
              #     self.methods.append(method)
              self.methods.append(exptrans.dataset_id)

         return self.frequencies

     def spfitstr(self):
          if self.frequencyexp:
               frequency = self.frequencyexp
               speciestag = -self.speciestag
          else:
               frequency = self.frequency
               speciestag = self.speciestag

          egy_lower = formatstring(self.energylower,'%10.4lf','%10s')
          if egy_lower=='   -0.0000':
               egy_lower = '    0.0000'
               
          return '%s%s%s%s%s%3s%s%s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s'\
                 % (formatstring(frequency,'%13.4lf','%13s'),
                    formatstring(self.uncertainty,'%8.4lf','%8s'),
                    formatstring(self.intensity,'%8.4lf','%8s'),
                    formatstring(self.degreeoffreedom,'%2d','%s'),
                    egy_lower,
                    format_degeneracy(self.upperstatedegeneracy),
                    formatstring(speciestag,'%7d','%7s'),
                    formatstring(self.qntag,'%4d','%4s'),
                    formatqn(self.qnup1),
                    formatqn(self.qnup2),
                    formatqn(self.qnup3),
                    formatqn(self.qnup4),
                    formatqn(self.qnup5),
                    formatqn(self.qnup6),
                    formatqn(self.qnlow1),
                    formatqn(self.qnlow2),
                    formatqn(self.qnlow3),
                    formatqn(self.qnlow4),
                    formatqn(self.qnlow5),
                    formatqn(self.qnlow6))

##     def get_exp_transitions(self):
##          exptranss = TransitionsExp.objects.filter(species=self.species,
##                                                    qnup1=self.qnup1,
##                                                    qnlow1=self.qnlow1,
##                                                    qnup2=self.qnup2,
##                                                    qnlow2=self.qnlow2,
##                                                    qnup3=self.qnup3,
##                                                    qnlow4=self.qnlow4,
##                                                    qnup5=self.qnup5,
##                                                    qnlow6=self.qnlow6)
##          freqs=[self.frequency]
##          for trans in exptranss:
##               freqs.append(trans.frequency)

##          self.frequencyArray = freqs
##          return freqs

##     frequencyarray = attach_exp_frequencies
     
#     def __init__(self):
#          attach_exp_frequencies()
#          self.frequenciess = 123,234
#          self.frequencyArray = [12345,2345]
#          
#     frequencyArray = get_exp_transitions() #[12345,23456]
        
     class Meta:
        db_table = u'Predictions'
        

class RadiativeTransitions( Model):
     """
     This class contains the calculated transition frequencies (mysql-table Predictions).
     """
     id                    = IntegerField(primary_key=True, db_column='RadiativeTransitionID')
     specie                = ForeignKey(Species, db_column='SpeciesID')
     speciestag            = IntegerField(db_column='SpeciesTag')
     frequency             =  FloatField(null=True, db_column='FrequencyValue')
     intensity             =  FloatField(null=True, db_column='IdealisedIntensity')
     einsteina             =  FloatField(null=True, db_column='EinsteinA')
     #smu2                  =  FloatField(null=True, db_column='P_Smu2')
     uncertainty           =  FloatField(null=True, db_column='EnergyWavelengthAccuracy')
     energylower           =  FloatField(null=True, db_column='LowerStateEnergyValue')
     #energyupper           =  FloatField(null=True, db_column='P_Energy_Upper')
     qntag                 = IntegerField(db_column='CaseQN')
     qnup1                 = IntegerField(db_column='QN_Up_1')
     qnup2                 = IntegerField(db_column='QN_Up_2')
     qnup3                 = IntegerField(db_column='QN_Up_3')
     qnup4                 = IntegerField(db_column='QN_Up_4')
     qnup5                 = IntegerField(db_column='QN_Up_5')
     qnup6                 = IntegerField(db_column='QN_Up_6')
     qnlow1                = IntegerField(db_column='QN_Low_1')
     qnlow2                = IntegerField(db_column='QN_Low_2')
     qnlow3                = IntegerField(db_column='QN_Low_3')
     qnlow4                = IntegerField(db_column='QN_Low_4')
     qnlow5                = IntegerField(db_column='QN_Low_5')
     qnlow6                = IntegerField(db_column='QN_Low_6')
     #dummy                 = CharField(max_length=20, db_column ='P_Dummy')
     unit                  = CharField(max_length=200, db_column='FrequencyUnit')
     degreeoffreedom       = IntegerField(db_column='Degree_Of_Freedom')
     upperstatedegeneracy  = IntegerField(db_column='UpperStateNuclearStatisticalWeight')
     originid              = IntegerField(db_column='Resource')
     hfsflag               = IntegerField(db_column='hfsflag')
     #userid                = IntegerField(db_column='P_U_ID')
     dataset               = ForeignKey(Datasets, db_column='DAT_ID')
     #qualityflag           = IntegerField(db_column='P_Quality')
     #archiveflag           = IntegerField(db_column='P_Archive')
     timestamp             = DateTimeField(db_column='Createdate')
     frequencies = CharField (db_column = 'FrequencyList')
     uncertainties = CharField (db_column = 'UncertaintyList')
     methods = CharField (db_column = 'MethodList')
     references = CharField (db_column = 'ReferenceList')
     frequencymethod = IntegerField(db_column = 'FrequencyMethodRef')
     processclass = CharField(max_length=100, db_column='ProcessClass')
     
     upperstateref =  ForeignKey(States, related_name='upperstate',
                                 db_column='UpperStateRef')
     lowerstateref =  ForeignKey(States, related_name='lowerstate',
                                 db_column='LowerStateRef')
     
     upstate =  ForeignKey(States, related_name='upperstate',
                           db_column='UpperStateRef')
     lostate =  ForeignKey(States, related_name='lowerstate',
                           db_column='LowerStateRef')
     #frequencyArray        
     
     def __unicode__(self):
          return u'ID:%s Tag:%s Freq: %s'%(self.id,self.speciestag,self.frequency)

     def specieid(self):
          return '%s-hyp%s' % (self.specie_id,self.hfsflag)

#     def process_class(self):
#          return eval(self.processclass)
     
     def spfitstr(self):
          if self.frequencymethod == 4:
               speciestag = -self.speciestag
          else:
               speciestag = self.speciestag

          egy_lower = formatstring(self.energylower,'%10.4lf','%10s')
          if egy_lower=='   -0.0000':
               egy_lower = '    0.0000'
               
          return '%s%s%s%s%s%3s%s%s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s'\
                 % (formatstring(self.frequency,'%13.4lf','%13s'),
                    formatstring(self.uncertainty,'%8.4lf','%8s'),
                    formatstring(self.intensity,'%8.4lf','%8s'),
                    formatstring(self.degreeoffreedom,'%2d','%s'),
                    egy_lower,
                    format_degeneracy(self.upperstatedegeneracy),
                    formatstring(speciestag,'%7d','%7s'),
                    formatstring(self.qntag,'%4d','%4s'),
                    formatqn(self.qnup1),
                    formatqn(self.qnup2),
                    formatqn(self.qnup3),
                    formatqn(self.qnup4),
                    formatqn(self.qnup5),
                    formatqn(self.qnup6),
                    formatqn(self.qnlow1),
                    formatqn(self.qnlow2),
                    formatqn(self.qnlow3),
                    formatqn(self.qnlow4),
                    formatqn(self.qnlow5),
                    formatqn(self.qnlow6))
     
        
     class Meta:
        db_table = u'RadiativeTransitions'
        
class RadiativeTransitionsT( Model):
     """
     This class contains the calculated transition frequencies (mysql-view RadiativeTransitionsT) 
     with temperature dependend intensities.
     """
     id                    = IntegerField(primary_key=True, db_column='RadiativeTransitionID')
     specie                = ForeignKey(Species, db_column='SpeciesID')
     speciestag            = IntegerField(db_column='SpeciesTag')
     frequency             =  FloatField(null=True, db_column='FrequencyValue')
     intensity             =  FloatField(null=True, db_column='IdealisedIntensityT')
     einsteina             =  FloatField(null=True, db_column='EinsteinA')
     #smu2                  =  FloatField(null=True, db_column='P_Smu2')
     uncertainty           =  FloatField(null=True, db_column='EnergyWavelengthAccuracy')
     energylower           =  FloatField(null=True, db_column='LowerStateEnergyValue')
     #energyupper           =  FloatField(null=True, db_column='P_Energy_Upper')
     qntag                 = IntegerField(db_column='CaseQN')
     qnup1                 = IntegerField(db_column='QN_Up_1')
     qnup2                 = IntegerField(db_column='QN_Up_2')
     qnup3                 = IntegerField(db_column='QN_Up_3')
     qnup4                 = IntegerField(db_column='QN_Up_4')
     qnup5                 = IntegerField(db_column='QN_Up_5')
     qnup6                 = IntegerField(db_column='QN_Up_6')
     qnlow1                = IntegerField(db_column='QN_Low_1')
     qnlow2                = IntegerField(db_column='QN_Low_2')
     qnlow3                = IntegerField(db_column='QN_Low_3')
     qnlow4                = IntegerField(db_column='QN_Low_4')
     qnlow5                = IntegerField(db_column='QN_Low_5')
     qnlow6                = IntegerField(db_column='QN_Low_6')
     #dummy                 = CharField(max_length=20, db_column ='P_Dummy')
     unit                  = CharField(max_length=200, db_column='FrequencyUnit')
     degreeoffreedom       = IntegerField(db_column='Degree_Of_Freedom')
     upperstatedegeneracy  = IntegerField(db_column='UpperStateNuclearStatisticalWeight')
     originid              = IntegerField(db_column='Resource')
     hfsflag               = IntegerField(db_column='hfsflag')
     #userid                = IntegerField(db_column='P_U_ID')
     dataset               = ForeignKey(Datasets, db_column='DAT_ID')
     #qualityflag           = IntegerField(db_column='P_Quality')
     #archiveflag           = IntegerField(db_column='P_Archive')
     timestamp             = DateTimeField(db_column='Createdate')
     temperature           = FloatField(db_column = 'Temperature')
     partitionfunc300      = FloatField(db_column = 'Partitionfunction300K')
     partitionfuncT        = FloatField(db_column = 'PartitionfunctionT')
     frequencies = CharField (db_column = 'FrequencyList')
     uncertainties = CharField (db_column = 'UncertaintyList')
     methods = CharField (db_column = 'MethodList')
     references = CharField (db_column = 'ReferenceList')
     frequencymethod = IntegerField(db_column = 'FrequencyMethodRef')
     processclass = CharField(max_length=100, db_column='ProcessClass')
     
     upperstateref =  ForeignKey(States, related_name='upperstate',
                                 db_column='UpperStateRef')
     lowerstateref =  ForeignKey(States, related_name='lowerstate',
                                 db_column='LowerStateRef')
     
     upstate =  ForeignKey(States, related_name='upperstate',
                           db_column='UpperStateRef')
     lostate =  ForeignKey(States, related_name='lowerstate',
                           db_column='LowerStateRef')
     #frequencyArray        
     
     def __unicode__(self):
          return u'ID:%s Tag:%s Freq: %s'%(self.id,self.speciestag,self.frequency)

     def specieid(self):
          return '%s-hyp%s' % (self.specie_id,self.hfsflag)

#     def process_class(self):
#          return eval(self.processclass)
     
     def spfitstr(self):
          if self.frequencymethod == 4:
               speciestag = -self.speciestag
          else:
               speciestag = self.speciestag

          egy_lower = formatstring(self.energylower,'%10.4lf','%10s')
          if egy_lower=='   -0.0000':
               egy_lower = '    0.0000'
               
          return '%s%s%s%s%s%3s%s%s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s%2s'\
                 % (formatstring(self.frequency,'%13.4lf','%13s'),
                    formatstring(self.uncertainty,'%8.4lf','%8s'),
                    formatstring(self.intensity,'%8.4lf','%8s'),
                    formatstring(self.degreeoffreedom,'%2d','%s'),
                    egy_lower,
                    format_degeneracy(self.upperstatedegeneracy),
                    formatstring(speciestag,'%7d','%7s'),
                    formatstring(self.qntag,'%4d','%4s'),
                    formatqn(self.qnup1),
                    formatqn(self.qnup2),
                    formatqn(self.qnup3),
                    formatqn(self.qnup4),
                    formatqn(self.qnup5),
                    formatqn(self.qnup6),
                    formatqn(self.qnlow1),
                    formatqn(self.qnlow2),
                    formatqn(self.qnlow3),
                    formatqn(self.qnlow4),
                    formatqn(self.qnlow5),
                    formatqn(self.qnlow6))
     
        
     class Meta:
        db_table = u'RadiativeTransitionsT'
 

class Sources( Model):
     """
     This class contains references 
     """
     id        =  IntegerField(primary_key=True, db_column='R_ID')
     authors   =  CharField(max_length=500, db_column='R_Authors', blank=True)
     category  =  CharField(max_length=100, db_column='R_Category', blank=True)
     name      =  CharField(max_length=200, db_column='R_SourceName', blank=True)
     year      =  IntegerField(null=True, db_column='R_Year', blank=True)
     vol       =  CharField(max_length=20, db_column='R_Volume', blank=True)
     doi       =  CharField(max_length=50, db_column='R_DOI', blank=True)
     pageBegin =  CharField(max_length=10, db_column='R_PageBegin', blank=True)
     pageEnd   =  CharField(max_length=10, db_column='R_PageEnd', blank=True)
     uri       =  CharField(max_length=100, db_column='R_URI', blank=True)
     publisher =  CharField(max_length=300, db_column='R_Publisher', blank=True)
     city      =  CharField(max_length=80, db_column='R_City', blank=True)
     editors   =  CharField(max_length=300, db_column='R_Editors', blank=True)
     productionDate =  DateField(max_length=12, db_column='R_ProductionDate', blank=True)
     version   =  CharField(max_length=20, db_column='R_Version', blank=True)
     url       =  CharField(max_length=200, db_column='R_URL', blank=True)
     comments  =  CharField(max_length=100, db_column='R_Comments', blank=True)
     class Meta:
          db_table = u'ReferenceBib'
          
     def getAuthorList(self):
          try:
               return [name.replace("{","").replace("}","") for name in self.authors.split("},{")]
          except:
               return none

#    referenceId =  ForeignKey(SourcesIDRefs, related_name='isRefId',
#                                db_column='rId', null=False)

class Parameter (Model):
     id = IntegerField(primary_key=True, db_column='PAR_ID')
     specie = ForeignKey(Species, db_column='PAR_E_ID')
     speciestag = IntegerField(db_column='PAR_M_TAG')
     parameter = CharField(max_length=100, db_column='PAR_PARAMETER')
     value = CharField(max_length=100, db_column='PAR_VALUE')
     unit = CharField(max_length=7, db_column='PAR_UNIT')
     type = CharField(max_length=30, db_column='PAR_Type')
     rId = ForeignKey(Sources, db_column='PAR_R_ID')
     class Meta:
          db_table = u'Parameter'

     def parameter_html(self):
          u_score = self.parameter.find('_')
          if u_score<0:
               return self.parameter
          else:
               return self.parameter.replace(self.parameter[u_score:u_score+2],'<sub>'+self.parameter[u_score+1:u_score+2]+'</sub>')
#          else:
#               return self.parameter
          
          

        
class TransitionsExp( Model):
     """
     This class contains the experimental transition frequencies (mysql-table Frequencies).
     """
     id                    = IntegerField(primary_key=True, db_column='F_ID')
     specie                = ForeignKey(Species, db_column='F_E_ID')
     vid                   = IntegerField(db_column='F_V_ID') # obsolete
     frequency             = FloatField(null=True, db_column='F_Frequency')
     uncertainty           = FloatField(null=True, db_column='F_Error')
     weight                = FloatField(null=True, db_column='F_WT')
     unit                  = CharField(max_length=10, db_column='F_Unit')
     qnup1                 = IntegerField(db_column='F_QN_Up_1') 
     qnup2                 = IntegerField(db_column='F_QN_Up_2') 
     qnup3                 = IntegerField(db_column='F_QN_Up_3') 
     qnup4                 = IntegerField(db_column='F_QN_Up_4') 
     qnup5                 = IntegerField(db_column='F_QN_Up_5') 
     qnup6                 = IntegerField(db_column='F_QN_Up_6') 
     qnlow1                = IntegerField(db_column='F_QN_Low_1')
     qnlow2                = IntegerField(db_column='F_QN_Low_2') 
     qnlow3                = IntegerField(db_column='F_QN_Low_3') 
     qnlow4                = IntegerField(db_column='F_QN_Low_4') 
     qnlow5                = IntegerField(db_column='F_QN_Low_5') 
     qnlow6                = IntegerField(db_column='F_QN_Low_6')
     comment               = TextField(db_column='F_Comment')
     rating                = IntegerField(db_column='F_Rating')
     userid                = IntegerField(db_column='F_U_ID')
     papid                 = IntegerField(db_column='F_PAP_ID')  # obsolete
     dataset               = ForeignKey(Datasets, db_column='F_DAT_ID')
     timestamp             = DateTimeField(db_column='F_TIMESTAMP')
     sources               = ManyToManyField(Sources, through='SourcesIDRefs')
     class Meta:
       db_table = u'Frequencies'
       
     def spfitstr(self):
          """
          Renders the current transition in spfit's output format
          12I3, freeform: QN, FREQ, ERR, WT
          """
          qnupstr=""
          qnlowstr=""
          emptystr=""
          for qn in [self.qnup1,self.qnup2,self.qnup3,self.qnup4,self.qnup5,self.qnup6]:
               if qn is not None:
                    qnupstr+='%3d' % qn
               else:
                    emptystr += '   '
          for qn in [self.qnlow1,self.qnlow2,self.qnlow3,self.qnlow4,self.qnlow5,self.qnlow6]:
               if qn is not None:
                    qnlowstr+='%3d' % qn
               else:
                    emptystr += '   '
                
          return '%s'\
                 '%s %s %s  '\
                 '%s'\
                 % (qnupstr+qnlowstr+emptystr,
                    '%16.4lf' % self.frequency if self.frequency  else "",
                    '%10.4lf' % self.uncertainty if self.uncertainty  else "",
                    '%8.4lf' % self.weight if self.weight  else "",
                    self.comment)
     
     def __unicode__(self):
        return self.spfitstr()           
                
     def attach_evaluation(self):
          """
          """
          self.qualities=[]
          self.recommendations=[]
          self.evalrefs=[]
          evals = self.evaluation_set.all()
          for i in evals:
               self.qualities.append(i.quality)
               self.recommendations.append(i.recommended)
               self.evalrefs.append(i.source_id)
          return self.qualities

class SourcesIDRefs( Model):
     """
     This class maps references to classes: species, datasets, frequency
     """
     id  =  AutoField(primary_key=True, db_column='RL_ID')
     source =  ForeignKey(Sources, null=True, db_column='RL_R_ID')
     specie   =  ForeignKey(Species, null=True, db_column='RL_E_ID')
     dataset =  ForeignKey(Datasets, null=True, db_column='RL_DAT_ID', blank=True)
     transitionexp  =  ForeignKey(TransitionsExp, null=True, db_column='RL_F_ID', related_name='sources', blank=True)
     parameter  =  ForeignKey(Parameter, null=True, db_column='RL_F_ID', blank=True)
     class Meta:
          db_table = u'ReferenceList'

#     referenceid = ForeignKey(Sources, db_column='RL_R_ID')
#    stateReferenceId =  ForeignKey(StatesMolecules, related_name='isStateRefId',
#                                db_column='RL_E_ID', null=False)

     
class Methods (Model):
    id = IntegerField(primary_key=True, db_column='ME_ID')
    ref = CharField(max_length=10, db_column='ME_Ref')
    functionref = IntegerField(db_column='ME_FunctionRef')
    category = CharField(max_length=30, db_column='ME_Category')
    description = CharField(max_length=500, db_column='ME_Description')
    class Meta:
        db_table = u'Methods'
    

class MolecularQuantumNumbers( Model):
     """
     This class is based on the mysql-view 'V_MolstateQN' and contains
     the transformed quantum numbers of a state (spcat->XSAMS)
     """
     id = IntegerField(primary_key=True, db_column='Id')
     state =  ForeignKey(States, related_name='quantumnumbers', db_column='StateID')
#    stateid =  IntegerField(primary_key=True, db_column='StateID')
     case =  CharField(max_length=10, db_column='Case')
     label =  CharField(max_length=50, db_column='Label')
     value =  CharField(max_length=100, db_column='Value')
     spinref =  CharField(max_length=100, db_column='SpinRef')
     attribute =  CharField(max_length=100, db_column='Attribute')

     class Meta:
          db_table = 'V_MolstateQN'
          managed=False

class QuantumNumbersFilter(Model):
     """
     This table (StateQNXsams) is used to map spcat's QuantumNumbers
     to XSAMS Quantum numbers (case description)
     """
     id  = IntegerField(primary_key=True, db_column='SQN_ID')
     specie = ForeignKey(Species, db_column='SQN_E_ID')
     qntag = IntegerField(db_column='SQN_QN_Tag')
     qn1 = IntegerField(db_column='SQN_QN1')
     qn2 = IntegerField(db_column='SQN_QN2')
     qn3 = IntegerField(db_column='SQN_QN3')
     qn4 = IntegerField(db_column='SQN_QN4')
     qn5 = IntegerField(db_column='SQN_QN5')
     qn6 = IntegerField(db_column='SQN_QN6')
     case = CharField(max_length=20, db_column='SQN_Case')
     label = CharField(max_length=100, db_column='SQN_Label')
     slaplabel = CharField(max_length=100, db_column='SQN_SLAP_Label')
     valuefloat = FloatField(db_column='SQN_ValueFloat')
     valuestring = CharField(max_length=100, db_column='SQN_ValueString')
     columnvalue = IntegerField(db_column='SQN_ColumnValue')
     columnvaluefunc = CharField(max_length=10, db_column='SQN_ColumnValueFunction')
     spinref= CharField(max_length=10, db_column='SQN_SpinRef')
     attribute = CharField(max_length=20, db_column='SQN_Attribute')
     order = IntegerField(db_column='SQN_Order')
     comment = TextField(db_column='SQN_Comment')

     class Meta:
          db_table='StateQNXsams'
          

class BondArray( Model):
     """
     This class contains the bonds of each specie. One bond per object.
     atom1 and atom2 correspond to atomid of the AtomArray - class.
     """
     id = IntegerField(primary_key=True, db_column='BA_ID')
     inchikey = CharField(max_length=100, db_column='BA_InchiKey')
     atom1 = CharField(max_length=10, db_column='BA_AtomId1')
     atom2 = CharField(max_length=10, db_column='BA_AtomId2')
     order = CharField(max_length=10, db_column='BA_Order')
     specie = ForeignKey(Molecules, db_column='BA_E_ID')
     
     class Meta:
          db_table = u'BondArray'
        
class AtomArray( Model):
     """
     This class contains the atoms of each specie. One atom per object.
     atomid is used in BondArray to identify atoms.
     """
     id =  IntegerField(primary_key=True, db_column='AA_ID')
     inchikey = CharField(max_length=100, db_column='AA_InchiKey')
     atomid = CharField(max_length=10, db_column='AA_AtomId')
     elementtype = CharField(max_length=5, db_column='AA_ElementType')
     isotopenumber = IntegerField( db_column='AA_IsotopeNumber')
     formalcharge = CharField(max_length=5, db_column='AA_FormalCharge')
     specie = ForeignKey(Species, db_column='AA_E_ID')    
     
     class Meta:
          db_table = u'AtomArray'


class Evaluation(Model):
     """
     This class contains recommendations and evaluation information for specific
     transitions.
     One transition (ether experimental or calculated) is evaluated. The entity is
     specified in source.
     """
     id = IntegerField(primary_key=True, db_column='EVA_ID')
     specie = ForeignKey(Species, db_column='EVA_E_ID')
     exptransition = ForeignKey(TransitionsExp, db_column='EVA_F_ID')
     calctransition = ForeignKey(TransitionsCalc, db_column='EVA_P_ID')
     recommended = BooleanField( db_column='EVA_Recommended')
     quality = CharField(max_length=45, db_column='EVA_Quality')
     source = ForeignKey(Sources, db_column='EVA_R_ID')
     class Meta:
          db_table = u'Evaluation'

##class Partitionfunctions( Model):
##     """
##     This class contains partition function (mysql-table: Partitionfunctions) for each specie.
##     """
##     id  =  IntegerField(primary_key=True, db_column='PF_ID')
##     mid =  IntegerField(db_column='PF_M_ID')
##     eid =  ForeignKey(Molecules, db_column='PF_E_ID')
##     temperature = FloatField(db_column='PF_Temperature')
##     partitionfunc = FloatField(db_column='PF_Partitionfunction')
##     comment = CharField(max_length=150, db_column='PF_Comment')
    
##     class Meta:
##          db_table = u'Partitionfunctions' 
                     
class Partitionfunctions( Model):
     """
     This class contains partition function (mysql-table: Partitionfunctions) for each specie.
     """
     id  =  AutoField(primary_key=True, db_column='PF_ID')
     molecule =  ForeignKey(Molecules, db_column='PF_M_ID', blank=True, null = True)
     specie =  ForeignKey(Species, db_column='PF_E_ID')
     dataset =  ForeignKey(Datasets, db_column='PF_DAT_ID', blank=True, null = True)
     nsi =  ForeignKey(NuclearSpinIsomers, db_column='PF_NSI_ID', blank=True, null = True)
     temperature = FloatField(db_column='PF_Temperature')
     partitionfunc = FloatField(db_column='PF_Partitionfunction')
     state = CharField(max_length=100, db_column = 'PF_State')
     comment = CharField(max_length=150, db_column='PF_Comment')
    
     class Meta:
          db_table = u'Partitionfunctions' 
                     
                         
class PartitionfunctionsDetailed( Model):
     """
     This class contains partition function (mysql-table: Partitionfunctions) for each specie
     which have been calculated based on the state energy listing and include contributions
     from other vibrational states (other specie).
     """
     id  =  AutoField(primary_key=True, db_column='PFD_ID')
     specie =  ForeignKey(Species, db_column='PFD_E_ID')
     inchikey =  CharField(max_length=30, db_column='PFD_Inchikey', blank=True, null = True)
     state = CharField(max_length=100, db_column = 'PFD_State')
     loweststateenergy = FloatField(db_column='PFD_LowestStateEnergy')
     nsi =  ForeignKey(NuclearSpinIsomers, db_column='PFD_NSI', blank=True, null = True)
     temperature = FloatField(db_column='PFD_Temperature')
     partitionfunc = FloatField(db_column='PFD_Partitionfunction')
     comment = CharField(max_length=150, db_column='PFD_Comment')
     createdate = DateTimeField(db_column='PFD_Createdate')
     changedate = DateTimeField(db_column='PFD_Changedate')

     class Meta:
          db_table = u'PartitionFunctionsDetailed' 

     def __unicode__(self):
          return "%6d %20s %9.3lf %20.6lf" % (self.specie.id, self.state, self.temperature, self.partitionfunc)

class Method:
     """
     This class wraps the sources for each specie (like a header).
     """
     def __init__(self, id, speciesid, category, description, sourcesref):

        self.id = id
        self.speciesid = speciesid
        self.category = category
        self.description = description
        self.sourcesref = sourcesref
        

class Files (Model):
     id = IntegerField(primary_key=True, db_column='FIL_ID')
     specie = ForeignKey(Species, db_column='FIL_E_ID')
     name = CharField(max_length=50, db_column='FIL_Name')
     type = CharField(max_length=10, db_column='FIL_Type')
     asciifile = TextField(db_column='FIL_ASCIIFILE')
     comment = TextField(db_column='FIL_Comment')
     createdate = DateField(db_column='FIL_Createdate')
     class Meta:
          db_table = u'Files'
