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

class Molecules( Model):
     id                    = IntegerField(primary_key=True, db_column='M_ID') 
     name                  = CharField(max_length=200, db_column='M_Name', blank=True)
     symbol                = CharField(max_length=250, db_column='M_Symbol', blank=True)
     cas                   = CharField(max_length= 20, db_column='M_CAS', blank=True)
     stoichiometricformula = CharField(max_length=200, db_column='M_StoichiometricFormula', blank=True)
     structuralformula     = CharField(max_length=200, db_column='M_StructuralFormula', blank=True)
     trivialname           = CharField(max_length=200, db_column='M_TrivialName', blank=True)
     numberofatoms         = CharField(max_length= 20, db_column='M_NumberOfAtoms', blank=True)
     formalcharge          = CharField(max_length=  5, db_column='M_FormalCharge', blank=True)
     comment               = TextField(db_column='M_Comment', blank=True)
     class Meta:
       db_table = u'Molecules'
       

class Species( Model):
     id                    = IntegerField(primary_key=True, db_column='E_ID')
     molecule              = ForeignKey(Molecules, db_column='E_M_ID')
     speciestag            = IntegerField(db_column='E_TAG')
     name                  = CharField(max_length=200, db_column='E_Name')
     isotopolog            = CharField(max_length=100, db_column='E_Isotopomer')
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
     class Meta:
       db_table = u'Entries'
     
     def getMassNumber(self):
          tag = str(self.speciestag)
          return tag[:-3] #self.speciestag[:-3]

     def _get_cml(self):
          cursor = connection.cursor()
#          cursor.execute("SELECT F_GetCML(%s) as cml FROM Entries WHERE id=%s", [settings.SECRET_KEY, self.id])
          cursor.execute("SELECT F_GetCML(%s) as cml ", [self.id])
          return cursor.fetchone()[0]
     
     cml = property(_get_cml)

class Datasets( Model):
     id                    = IntegerField(primary_key=True, db_column='DAT_ID')
     species               = ForeignKey(Species, db_column='DAT_E_ID')
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


       
class States( Model):
     id                    = IntegerField(primary_key=True, db_column='EGY_ID')
     species               = ForeignKey(Species, db_column='EGY_E_ID')
     speciestag            = IntegerField(db_column='EGY_E_Tag')
     dataset               = ForeignKey(Datasets, db_column='EGY_DAT_ID')
     energy                = FloatField(null=True, db_column='EGY_Energy')
     uncertainty           = FloatField(null=True, db_column='EGY_Uncertainty')
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

     def qns_xml(self):
	"""Yield the XML for the state quantum numbers"""
        qns = MolecularQuantumNumbers.objects.filter(state=self.id)
        case = qns[0].case     
        caseNS = 'http://vamdc.org/xml/xsams/0.2/cases/%s' % case
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

     XML = qns_xml



class TransitionsCalc( Model):
     id                    = IntegerField(primary_key=True, db_column='P_ID')
     species               = ForeignKey(Species, db_column='P_E_ID')
     speciestag            = IntegerField(db_column='P_E_Tag')
     frequency             =  FloatField(null=True, db_column='P_Frequency')
     frequencyexp          =  FloatField(null=True, db_column='P_Frequency_Exp')
     intensity             =  FloatField(null=True, db_column='P_Intensity')
     einsteina             =  FloatField(null=True, db_column='P_EinsteinA')
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
     dummy                 = CharField(db_column ='P_Dummy')
     unit                  = CharField(max_length=200, db_column='P_Unit')
     degreeoffreedom       = IntegerField(db_column='P_Degree_Of_Freedom')
     upperstatedegeneracy  = IntegerField(db_column='P_Upper_State_Degeneracy')
     originid              = IntegerField(db_column='P_Origin_Id')
     hfsflag               = IntegerField(db_column='P_HFS')
     userid                = IntegerField(db_column='P_U_ID')
     dataset               = ForeignKey(Datasets, related_name='isinitialstate', db_column='P_DAT_ID')
     qualityflag           = IntegerField(db_column='P_Quality')
     archiveflag           = IntegerField(db_column='P_Archive')
     timestamp             = DateTimeField(db_column='P_TIMESTAMP')
     upperstateref =  ForeignKey(States, related_name='upperstate',
                                db_column='P_Up_EGY_ID')
     lowerstateref =  ForeignKey(States, related_name='lowerstate',
                                db_column='P_Low_EGY_ID')

     def __unicode__(self):
        return u'ID:%s Tag:%s Freq: %s'%(self.id,self.speciestag,self.frequency)
     class Meta:
        db_table = u'Predictions'
        
        
class TransitionsExp( Model):
     id                    = IntegerField(primary_key=True, db_column='F_ID')
     species               = ForeignKey(Species, db_column='F_E_ID')
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
     class Meta:
       db_table = u'Frequencies'
       
                
                
#class Molecules( Model):
     #speciesid   =  IntegerField(primary_key=True, db_column='I_ID')
     #inchi       =  CharField(max_length=200, db_column='I_Inchi', blank=True)
     #inchikey    =  CharField(max_length=100, db_column='I_Inchikey', blank=True)
     #name        =  CharField(max_length=100, db_column='I_Name', blank=True)
     #htmlname    =  CharField(max_length=200, db_column='I_HtmlName', blank=True)
     #latexname   =  CharField(max_length=100, db_column='I_LatexName', blank=True)
     #stoichiometricformula =  CharField(max_length=200, db_column='I_StoichiometricFormula', blank=True)
     #trivialname =  CharField(max_length=200, db_column='I_TrivialName', blank=True)
     #class Meta:
         #db_table = u'Isotopologs'


class StatesMolecules( Model):
    resource =  CharField(max_length=12, db_column='Resource') # Field name made lowercase.
    stateid =  IntegerField(primary_key=True, db_column='StateID') # Field name made lowercase.
    speciesid =  ForeignKey(Molecules, db_column='E_ID')
    moleculeid =  ForeignKey(Molecules, db_column='MoleculeID') # Field name made lowercase.
    chemicalname =  CharField(max_length=600, db_column='ChemicalName', blank=True) # Field name made lowercase.
    molecularchemicalspecies =  CharField(max_length=600, db_column='MolecularChemicalSpecies') # Field name made lowercase.
    isotopomer =  CharField(max_length=300, db_column='Isotopomer', blank=True) # Field name made lowercase.
    stateenergyvalue =  FloatField(null=True, db_column='StateEnergyValue', blank=True) # Field name made lowercase.
    stateenergyunit =  CharField(max_length=12, db_column='StateEnergyUnit') # Field name made lowercase.
    stateenergyaccuracy =  FloatField(null=True, db_column='StateEnergyAccuracy', blank=True) # Field name made lowercase.
    mixingcoefficient =  FloatField(null=True, db_column='MixingCoefficient', blank=True) # Field name made lowercase.
    statenuclearstatisticalweight =  IntegerField(null=True, db_column='StateNuclearStatisticalWeight', blank=True) # Field name made lowercase.
    qn_rotstate =  CharField(max_length=1500, db_column='QN_RotState', blank=True) # Field name made lowercase.
    qn_vibstate =  CharField(max_length=1500, db_column='QN_VibState', blank=True) # Field name made lowercase.
    qn_elecstate =  CharField(max_length=300, db_column='QN_ElecState', blank=True) # Field name made lowercase.
    qn_string =  CharField(max_length=1500, db_column='QN_String', blank=True) # Field name made lowercase.
    egy_qn_tag =  IntegerField(null=True, db_column='EGY_QN_Tag', blank=True) # Field name made lowercase.
    egy_qn1 =  IntegerField(null=True, db_column='EGY_QN1', blank=True) # Field name made lowercase.
    egy_qn2 =  IntegerField(null=True, db_column='EGY_QN2', blank=True) # Field name made lowercase.
    egy_qn3 =  IntegerField(null=True, db_column='EGY_QN3', blank=True) # Field name made lowercase.
    egy_qn4 =  IntegerField(null=True, db_column='EGY_QN4', blank=True) # Field name made lowercase.
    egy_qn5 =  IntegerField(null=True, db_column='EGY_QN5', blank=True) # Field name made lowercase.
    egy_qn6 =  IntegerField(null=True, db_column='EGY_QN6', blank=True) # Field name made lowercase.
    e_id =  IntegerField(db_column='E_ID') # Field name made lowercase.
    egy_dat_id =  IntegerField(null=True, db_column='EGY_DAT_ID', blank=True) # Field name made lowercase.
    e_tag =  IntegerField(db_column='E_Tag') # Field name made lowercase.
    class Meta:
        db_table = u'StatesMolecules'
    

    #def qns_xml(self):
        #"""Yield the XML for the state quantum numbers"""
        #qns = MolecularQuantumNumbers.objects.filter(statesmolecules=self.stateid)
        #case = qns[0].case     
        #caseNS = 'http://vamdc.org/xml/xsams/0.2/cases/%s' % case
        #caseNSloc = '../../cases/%s.xsd' % case
        #xml = []
        #xml.append('<Case xsi:type="%s:Case" caseID="%s"'\
                   #' xmlns:%s="%s" xsi:schemaLocation="%s %s">'\
                  #% (case, case, case, caseNS, caseNS, caseNSloc))
        #xml.append('<%s:QNs>\n' % case)

        #for qn in qns:
           #if qn.attribute:
               ## put quotes around the value of the attribute
               #attr_name, attr_val = qn.attribute.split('=')
               #qn.attribute = ' %s="%s"' % (attr_name, attr_val)
           #else:
              #qn.attribute = ''

           #if qn.spinref:
               ## add spinRef to attribute if it exists
               #qn.attribute += ' nuclearSpinRef="%s"' % qn.spinref

           #xml.append('<%s%s>%s</%s>\n' % (qn.label, qn.attribute , qn.value, qn.label) )
        #xml.append('</%s:QNs>\n' % case)
        #xml.append('</Case>\n')
        #return ''.join(xml)

    ## associate qns_xml with the XML attribute of the States class
    ## so that generators.py checkXML() works:

    #XML = qns_xml






class Methods (Model):
    id = IntegerField(primary_key=True, db_column='ME_ID')
    ref = CharField(max_length=10, db_column='ME_Ref')
    functionref = IntegerField(db_column='ME_FunctionRef')
    category = CharField(max_length=30, db_column='ME_Category')
    description = CharField(max_length=500, db_column='ME_Description')
    class Meta:
        db_table = u'Methods'
    


class RadiativeTransitions(Model):

    resource =  CharField(max_length=12, db_column='Resource') # Field name made lowercase.
    radiativetransitionid =  IntegerField(primary_key=True, db_column='RadiativeTransitionID') # Field name made lowercase.
    moleculeid =  IntegerField(db_column='MoleculeID') # Field name made lowercase.
    speciesid =  ForeignKey(Molecules, db_column='E_ID')
    species = ForeignKey(Molecules, related_name='isspecies', db_column='E_ID', null=False)
    chemicalname =  CharField(max_length=600, db_column='ChemicalName', blank=True) # Field name made lowercase.
    molecularchemicalspecies =  CharField(max_length=600, db_column='MolecularChemicalSpecies') # Field name made lowercase.
    isotopomer =  CharField(max_length=300, db_column='Isotopomer', blank=True) # Field name made lowercase.
    energywavelength =  CharField(max_length=27, db_column='EnergyWavelength') # Field name made lowercase.
    wavelengthwavenumber =  CharField(max_length=33, db_column='WavelengthWavenumber') # Field name made lowercase.
    frequencyvalue =  FloatField(null=True, db_column='FrequencyValue', blank=True) # Field name made lowercase.
    frequencyunit =  CharField(max_length=9, db_column='FrequencyUnit') # Field name made lowercase.
    energywavelengthaccuracy =  FloatField(null=True, db_column='EnergyWavelengthAccuracy', blank=True) # Field name made lowercase.
    wavelengthvalue =  FloatField(null=True, db_column='WavelengthValue', blank=True) # Wavelength 
    wavelengthunit =  CharField(max_length=15, db_column='WavelengthUnit')
    multipole =  CharField(max_length=6, db_column='Multipole') # Field name made lowercase.
    log10weightedoscillatorstrengthvalue =  FloatField(null=True, db_column='Log10WeightedOscillatorStrengthValue', blank=True) # Field name made lowercase.
    log10weightedoscillatorstrengthunit =  CharField(max_length=24, db_column='Log10WeightedOscillatorStrengthUnit') # Field name made lowercase.
    einsteinA =  FloatField(null=True, db_column='EinsteinA', blank=True)
    lowerstateenergyvalue =  FloatField(null=True, db_column='LowerStateEnergyValue', blank=True) # Field name made lowercase.
    lowerstateenergyunit =  CharField(max_length=12, db_column='LowerStateEnergyUnit') # Field name made lowercase.
    upperstatenuclearstatisticalweight =  IntegerField(null=True, db_column='UpperStateNuclearStatisticalWeight', blank=True) # Field name made lowercase.
#    initialstateref =  IntegerField(null=True, db_column='InitialStateRef', blank=True) # Field name made lowercase.
#    finalstateref =  IntegerField(null=True, db_column='FinalStateRef', blank=True) # Field name made lowercase.
    initialstateref =  ForeignKey(StatesMolecules, related_name='isinitialstate',
                                db_column='InitialStateRef', null=False)

    finalstateref   =  ForeignKey(StatesMolecules, related_name='isfinalstate',
                                db_column='FinalStateRef', null=False)

    freqmethodref  = ForeignKey(Methods, db_column='FrequencyMethodRef')

    caseqn =  IntegerField(null=True, db_column='CaseQN', blank=True) # Field name made lowercase.
    qn_up_1 =  IntegerField(null=True, db_column='QN_Up_1', blank=True) # Field name made lowercase.
    qn_up_2 =  IntegerField(null=True, db_column='QN_Up_2', blank=True) # Field name made lowercase.
    qn_up_3 =  IntegerField(null=True, db_column='QN_Up_3', blank=True) # Field name made lowercase.
    qn_up_4 =  IntegerField(null=True, db_column='QN_Up_4', blank=True) # Field name made lowercase.
    qn_up_5 =  IntegerField(null=True, db_column='QN_Up_5', blank=True) # Field name made lowercase.
    qn_up_6 =  IntegerField(null=True, db_column='QN_Up_6', blank=True) # Field name made lowercase.
    qn_low_1 =  IntegerField(null=True, db_column='QN_Low_1', blank=True) # Field name made lowercase.
    qn_low_2 =  IntegerField(null=True, db_column='QN_Low_2', blank=True) # Field name made lowercase.
    qn_low_3 =  IntegerField(null=True, db_column='QN_Low_3', blank=True) # Field name made lowercase.
    qn_low_4 =  IntegerField(null=True, db_column='QN_Low_4', blank=True) # Field name made lowercase.
    qn_low_5 =  IntegerField(null=True, db_column='QN_Low_5', blank=True) # Field name made lowercase.
    qn_low_6 =  IntegerField(null=True, db_column='QN_Low_6', blank=True) # Field name made lowercase.
    e_id =  IntegerField(db_column='E_ID') # Field name made lowercase.
    e_tag =  IntegerField(db_column='E_Tag') # Field name made lowercase.
    e_states =  CharField(max_length=600, db_column='E_States', blank=True) # Field name made lowercase.
    e_name =  CharField(max_length=600, db_column='E_Name') # Field name made lowercase.
#    def getRefs(self,which):
#        try:
#            id = eval('self.'+which+'_ref_id')
#            return refcache[id]
#        except:
#            return None

    def __unicode__(self):
        return u'ID:%s Freq: %s'%(self.radiativetransitionid,self.frequencyvalue)
    class Meta:
        db_table = u'RadiativeTransitions'




class MolecularQuantumNumbers( Model): 
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

class BondArray( Model):
    id = IntegerField(primary_key=True, db_column='BA_ID')
    inchikey = CharField(max_length=100, db_column='BA_InchiKey')
    atom1 = CharField(max_length=10, db_column='BA_AtomId1')
    atom2 = CharField(max_length=10, db_column='BA_AtomId2')
    order = CharField(max_length=10, db_column='BA_Order')
    eId   = ForeignKey(Molecules, db_column='BA_E_ID')

    class Meta:
        db_table = u'BondArray'
        
class AtomArray( Model):
    id =  IntegerField(primary_key=True, db_column='AA_ID')
    inchikey = CharField(max_length=100, db_column='AA_InchiKey')
    atomid = CharField(max_length=10, db_column='AA_AtomId')
    elementtype = CharField(max_length=5, db_column='AA_ElementType')
    isotopenumber = IntegerField( db_column='AA_IsotopeNumber')
    formalcharge = CharField(max_length=5, db_column='AA_FormalCharge')
    eId = ForeignKey(Molecules, db_column='AA_E_ID')    
    
    class Meta:
        db_table = u'AtomArray'



class Sources( Model):
    rId       =  IntegerField(primary_key=True, db_column='R_ID')
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

        
class SourcesIDRefs( Model):
    rlId  =  IntegerField(primary_key=True, db_column='RL_ID')
    rId   =  IntegerField(null=True, db_column='RL_R_ID')
    eId   =  IntegerField(null=True, db_column='RL_E_ID')
    datId =  IntegerField(null=True, db_column='RL_DAT_ID', blank=True)
    fId   =  IntegerField(null=True, db_column='RL_F_ID', blank=True)
    class Meta:
        db_table = u'ReferenceList'

    referenceid = ForeignKey(Sources, db_column='RL_R_ID')
#    stateReferenceId =  ForeignKey(StatesMolecules, related_name='isStateRefId',
#                                db_column='RL_E_ID', null=False)



class Partitionfunctions( Model):
    id  =  IntegerField(primary_key=True, db_column='PF_ID')
    mid =  IntegerField(db_column='PF_M_ID')
    eid =  ForeignKey(Molecules, db_column='PF_E_ID')
    temperature = FloatField(db_column='PF_Temperature')
    partitionfunc = FloatField(db_column='PF_Partitionfunction')
    comment = CharField(max_length=150, db_column='PF_Comment')
    
    class Meta:
        db_table = u'Partitionfunctions' 
                     
                                    


class Method:
    def __init__(self, id, speciesid, category, description, sourcesref):

        self.id = id
        self.speciesid = speciesid
        self.category = category
        self.description = description
        self.sourcesref = sourcesref
        
                                
