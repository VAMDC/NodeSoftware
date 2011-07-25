# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or
# field names.
#
# Also note: You'll have to insert the output of
# 'django-admin.py sqlcustom [appname]' into your database.

from django.db import models

import datetime, time

case_prefixes = {}
case_prefixes[1] = 'dcs'
case_prefixes[2] = 'hunda'
case_prefixes[3] = 'hundb'
case_prefixes[4] = 'ltcs'
case_prefixes[5] = 'nltcs'
case_prefixes[6] = 'stcs'
case_prefixes[7] = 'lpcs'
case_prefixes[8] = 'asymcs'
case_prefixes[9] = 'asymos'
case_prefixes[10] = 'sphcs'
case_prefixes[11] = 'sphos'
case_prefixes[12] = 'ltos'
case_prefixes[13] = 'lpos'
case_prefixes[14] = 'nltos'

class Molecules(models.Model):
    molecid = models.IntegerField(primary_key=True, null=False,
                                  db_column='molecID')
    inchikeystem = models.CharField(max_length=42, db_column='InChIKeyStem')
    molec_name = models.CharField(max_length=20, null=False,
                                  db_column='molec_name')
    molec_name_html = models.CharField(max_length=128, null=False,
                                       db_column='molec_name_html')
    molec_name_latex = models.CharField(max_length=128, null=False,
                                       db_column='molec_name_latex')
    stoichiometric_formula = models.CharField(max_length=40, null=False,
                                       db_column='stoichiometric_formula')
    chemical_names = models.CharField(max_length=256,
                                      db_column='chemical_names')
    class Meta:
            db_table = u'molecules'

class Isotopologues(models.Model):
    inchikey = models.CharField(primary_key=True, max_length=81,
                               db_column='InChIKey')
    inchi = models.CharField(max_length=384, db_column='InChI')
    molecid = models.IntegerField(null=False, db_column='molecID')
    isoid = models.IntegerField(db_column='isoID')
    iso_name = models.CharField(max_length=384, db_column='iso_name')
    iso_name_html = models.CharField(max_length=1536,
                                     db_column='iso_name_html')
    iso_name_latex = models.CharField(max_length=384,
                                      db_column='iso_name_latex')
    abundance = models.FloatField(null=True, blank=True, db_column='abundance')
    afgl_code = models.IntegerField(null=True, blank=True,
                                    db_column='AFGL_code')
    caseid = models.IntegerField(null=True, db_column='caseID')
    class Meta:
            db_table = u'isotopologues'

# This is a plumbing class to make the way my database stores molecule
# information play nicely with the generic generator code 
class Species:
   def __init__(self, molecid, isoid, inchikey, molec_name, iso_name,
                chemical_names, ordinary_formula, stoichiometric_formula):
        self.molecid = molecid
        self.isoid = isoid
        self.inchikey = inchikey
        self.molec_name = molec_name
        self.iso_name = iso_name
        self.chemical_names = chemical_names
        self.ordinary_formula = ordinary_formula
        self.stoichiometric_formula = stoichiometric_formula
        self.States = None

   def __getitem__(self, name):
        return self.__dict__[name]

class States(models.Model):
    id = models.IntegerField(primary_key=True, db_column='id')
    molecid = models.IntegerField(null=True, db_column='molecID', blank=True)
    isoid = models.IntegerField(null=True, db_column='isoID', blank=True)
    # XXX why does django multiply my VARCHAR lengths by 3???
    inchikey = models.CharField(max_length=81, db_column='InChIKey')
    assigned = models.IntegerField(null=True, db_column='assigned', blank=True)
    energy = models.FloatField(null=True, db_column='energy', blank=True)
    energy_err = models.FloatField(null=True, db_column='energy_err',
                                   blank=True)
    energy_flag = models.CharField(max_length=3, db_column='energy_flag',
                                   blank=True)
    g = models.IntegerField(null=True, db_column='g', blank=True)
    caseid = models.IntegerField(null=True, db_column='caseID', blank=True)
    qns = models.CharField(max_length=1536, db_column='qns', blank=True)
    class Meta:
        db_table = u'states'

    def qns_xml(self):
        """Yield the XML for the state quantum numbers"""
        qns = Qns.objects.filter(stateid=self.id).order_by('id')
        if qns:
            caseID = qns[0].caseid
            try:
                case = case_prefixes[caseID]
            except KeyError:
                # unrecognised caseID
                return 'unrecognised case'
        caseNS = 'http://vamdc.org/xml/xsams/0.2/cases/%s' % case
        caseNSloc = '../../cases/%s.xsd' % case
        xml = []
        xml.append('<Case xsi:type="%s:Case" caseID="%s"'\
                   ' xmlns:%s="%s" xsi:schemaLocation="%s %s">'\
                  % (case, case, case, caseNS, caseNS, caseNSloc))
        xml.append('<%s:QNs>\n' % case)
        xml.append('\n'.join([qn.xml for qn in qns]))
        xml.append('</%s:QNs>\n' % case)
        xml.append('</Case>\n')
        return ''.join(xml)
        #yield ''.join(xml)
    # associate qns_xml with the XML attribute of the States class
    # so that generators.py checkXML() works:
    XML = qns_xml

class Method:
    def __init__(self, id, category, description):
        self.id = id
        self.category = category
        self.description = description

class Refs(models.Model):
    sourceid = models.CharField(max_length=192, primary_key=True,
                                db_column='sourceID')
    type = models.CharField(max_length=96, blank=True)
    author = models.TextField(blank=True)
    title = models.TextField(blank=True)
    journal = models.TextField(blank=True)
    volume = models.CharField(max_length=30, blank=True)
    page_start = models.CharField(max_length=60, blank=True)
    page_end = models.CharField(max_length=60, blank=True)
    year = models.TextField(blank=True)
    institution = models.TextField(blank=True)
    note = models.TextField(blank=True)
    doi = models.CharField(max_length=192, blank=True)
    cited_as_html = models.TextField(blank=True, db_column="cited_as_html")
    url = models.TextField(blank=True, db_column="url")
    class Meta:
        db_table = u'refs'

    def XML(self):
        yield '<Source sourceID="%s">\n' % self.sourceid
        yield '  <Authors>\n'
        for author in self.author.split(' and '):
            yield '    <Author>\n        <Name>%s</Name>\n    </Author>\n' \
                    % author.strip()
        yield '  </Authors>\n'
        if self.title:
            yield '<Title>%s</Title>\n' % self.title
        if self.year:
            yield '<Year>%s</Year>\n' % self.year
        if self.journal:
            yield '<Category>journal</Category>\n'
            yield '<SourceName>%s</SourceName>\n' % self.journal
        if self.volume:
            yield '<Volume>%s</Volume>\n' % self.volume
        if self.pages:
            pages = self.pages.split('--')
            yield '<PageBegin>%s</PageBegin>\n' % self.pages[0]
            if len(pages)>1:
                yield '<PageEnd>%s</PageEnd>\n' % self.pages[1]
        yield '</Source>\n'

class Trans(models.Model):
    id = models.IntegerField(db_column='id', primary_key=True)
    molecid = models.IntegerField(db_column='molecID')
    isoid = models.IntegerField(db_column='isoID')
    inchikey = models.CharField(max_length=81, db_column='InChIKey')
    initialstateref = models.IntegerField(db_column='InitialStateRef',
                                          blank=True)
    finalstateref = models.IntegerField(db_column='FinalStateRef', blank=True)
    nu = models.FloatField()
    nu_err = models.FloatField(null=True, db_column='nu_err', blank=True)
    nu_ref = models.CharField(max_length=93, db_column='nu_ref', blank=True)
    s = models.FloatField(null=True, db_column='S', blank=True)
    s_err = models.FloatField(null=True, db_column='S_err', blank=True)
    s_ref = models.CharField(max_length=90, db_column='S_ref', blank=True)
    a = models.FloatField(null=True, db_column='A', blank=True)
    a_err = models.FloatField(null=True, db_column='A_err', blank=True)
    a_ref = models.CharField(max_length=90, db_column='A_ref', blank=True)
    multipole = models.CharField(max_length=6, db_column='multipole',
                                 blank=True)
    elower = models.FloatField(null=True, db_column='Elower', blank=True)
    gp = models.IntegerField(null=True, db_column='gp', blank=True)
    gpp = models.IntegerField(null=True, db_column='gpp', blank=True)
    fromdate = models.DateField(null=True, db_column='fromdate', blank=True)
    todate = models.DateField(null=True, db_column='todate', blank=True)
    method = models.CharField(max_length=16, db_column='method', blank=True)
    ierr = models.CharField(max_length=18, db_column='Ierr', blank=True)
    hitranline = models.CharField(max_length=160, db_column='HITRANline',
                                  blank=True)

    prms = []

    def XML_Broadening(self):
        prms = Prms.objects.filter(transid=self.id)
        prm_dict = {}
        for prm in prms:
            prm_dict[prm.prm_name] = prm
            # XXX for now, replace reference with the generic HITRAN08 ref
            prm_dict[prm.prm_name].prm_ref = 'BHIT-B_HITRAN2008'
        broadenings = []
        if 'g_air' in prm_dict.keys() and 'n_air' in prm_dict.keys():
            g_air_val = str(prm_dict['g_air'].prm_val)
            g_air_ref = str(prm_dict['g_air'].prm_ref)
            n_air_val = str(prm_dict['n_air'].prm_val)
            n_air_ref = str(prm_dict['n_air'].prm_ref)
            lineshape_xml = ['      <Lineshape name="Lorentzian">\n'\
   '      <Comments>The temperature-dependent pressure'\
   ' broadening Lorentzian lineshape</Comments>\n'\
   '      <LineshapeParameter name="gammaL">\n'\
   '        <FitParameters functionRef="FgammaL">\n'\
   '          <FitArgument name="T" units="K">\n'\
   '            <LowerLimit>240</LowerLimit>\n'\
   '            <UpperLimit>350</UpperLimit>\n'\
   '          </FitArgument>\n'\
   '          <FitArgument name="p" units="K">\n'\
   '            <LowerLimit>0.</LowerLimit>\n'\
   '            <UpperLimit>1.2</UpperLimit>\n'\
   '          </FitArgument>\n'\
   '          <FitParameter name="gammaL_ref">\n'\
   '            <SourceRef>%s</SourceRef>\n'\
   '            <Value units="1/cm">%s</Value>\n'\
                    % (g_air_ref, g_air_val),]
            g_air_err = prm_dict['g_air'].prm_err
            if g_air_err:
                g_air_err = str(g_air_err)
                lineshape_xml.append('            <Accuracy><Statistical>'\
                      '%s</Statistical></Accuracy>\n' % g_air_err)
            lineshape_xml.append('          </FitParameter>\n'\
   '          <FitParameter name="n">\n'\
   '            <SourceRef>%s</SourceRef>\n'\
   '            <Value units="unitless">%s</Value>\n'\
                    % (n_air_ref, n_air_val))
            n_air_err = prm_dict['n_air'].prm_err
            if n_air_err:
                n_air_err = str(n_air_err)
                lineshape_xml.append('            <Accuracy><Statistical>'\
                      '%s</Statistical></Accuracy>\n' % n_air_err)
            lineshape_xml.append('          </FitParameter>\n'\
   '        </FitParameters>\n'\
   '      </LineshapeParameter>\n</Lineshape>\n')
            broadening = '    <Broadening'\
                ' envRef="Eair-broadening-ref-env" name="pressure">\n'\
                '%s    </Broadening>\n' % ''.join(lineshape_xml)
            broadenings.append(broadening)
        if 'g_self' in prm_dict.keys():
            g_self_val = str(prm_dict['g_self'].prm_val)
            g_self_ref = str(prm_dict['g_self'].prm_ref)
            lineshape_xml = ['      <Lineshape name="Lorentzian">\n'\
       '        <LineshapeParameter name="gammaL">\n'\
       '          <SourceRef>%s</SourceRef>\n'\
       '          <Value units="1/cm">%s</Value>\n'\
                      % (g_self_ref, g_self_val),]
            g_self_err = prm_dict['g_self'].prm_err
            if g_self_err:
                g_self_err = str(g_self_err)
                lineshape_xml.append('          <Accuracy><Statistical>'\
                      '%s</Statistical></Accuracy>\n' % g_self_err)
            lineshape_xml.append('        </LineshapeParameter>\n'\
       '      </Lineshape>\n')
            broadening = '    <Broadening'\
                ' envRef="Eself-broadening-ref-env" name="pressure">\n'\
                '%s    </Broadening>\n' % ''.join(lineshape_xml)
            broadenings.append(broadening)
        # XXX for now, do shiftings at the same time as broadenings
        shiftings = []
        if 'delta_air' in prm_dict.keys():
            delta_air_val = str(prm_dict['delta_air'].prm_val)
            delta_air_ref = str(prm_dict['delta_air'].prm_ref)
            shifting_xml = ['    <Shifting envRef='\
       '"Eair-broadening-ref-env">\n'\
       '      <ShiftingParameter name="delta">\n'\
       '        <FitParameters functionRef="Fdelta">\n'\
       '          <FitArgument name="p" units="K">\n'\
       '            <LowerLimit>0.</LowerLimit>\n'\
       '            <UpperLimit>1.2</UpperLimit>\n'\
       '          </FitArgument>\n'\
       '          <FitParameter name="delta_ref">'\
       '            <SourceRef>%s</SourceRef>\n'\
       '            <Value units="unitless">%s</Value>\n'\
                        % (delta_air_ref, delta_air_val),]
            delta_air_err = prm_dict['delta_air'].prm_err
            if delta_air_err:
                delta_air_err = str(delta_air_err)
                shifting_xml.append('            <Accuracy><Statistical>'\
                    '%s</Statistical></Accuracy>\n' % delta_air_err)
            shifting_xml.append('          </FitParameter>\n'\
       '        </FitParameters>\n'\
       '      </ShiftingParameter>\n'\
       '    </Shifting>\n')
            shiftings.append(''.join(shifting_xml))
        return '    %s\n    %s\n' % (''.join(broadenings), ''.join(shiftings))

    def XML_Shifting(self):
        return ''

    class Meta:
        db_table = u'trans'

class Prms(models.Model):
    id = models.IntegerField(primary_key=True, null=False, db_column='id')
    molecid = models.IntegerField(db_column='molecID')
    isoid = models.IntegerField(db_column='isoID')
    inchikey = models.CharField(max_length=81, db_column='InChIKey')
    #transid = models.CharField(max_length=192, db_column='transID')
    transid = models.ForeignKey('Trans', db_column='transID')
    prm_name = models.CharField(max_length=192, db_column='prm_name')
    prm_val = models.FloatField(db_column='prm_val')
    prm_err = models.FloatField(db_column='prm_err')
    prm_ref = models.CharField(max_length=90, db_column='prm_ref')
    class Meta:
            db_table = u'prms'

class Prm():
    def __init__(self, name, val, err, ref):
        self.name = name
        self.val = val
        self.err = err
        self.ref = ref

class Qns(models.Model):
    id = models.IntegerField(primary_key=True, null=False, db_column='id')
    molecid = models.IntegerField(db_column='molecID')
    isoid = models.IntegerField(db_column='isoID')
    inchikey = models.CharField(max_length=81, db_column='InChIKey')
    stateid = models.CharField(max_length=192, db_column='stateID')
    caseid = models.IntegerField(db_column='caseID')
    qn_name = models.CharField(max_length=192, db_column='qn_name')
    qn_val = models.CharField(max_length=48, db_column='qn_val')
    qn_attr = models.CharField(max_length=384, db_column='qn_attr')
    xml = models.CharField(max_length=768, db_column='xml')
    class Meta:
        db_table = u'qns'

# This is a plumbing class to make my quantum numbers table play nicely
# with Christian's generator code:
class MolQN:
   def __init__(self, stateid, case_prefix, label, value,
                qn_attr, xml=None):
        self.stateid = stateid
        self.case = case_prefix
        self.label = label
        self.value = value
        self.qn_attr = qn_attr
        self.xml = xml

   def __getitem__(self, name):
        return self.__dict__[name]

class Xsec(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    molecid = models.IntegerField(null=False, db_column='molecID', blank=True)
    metaid = models.IntegerField(null=False, db_column='metaID', blank=True)
    t = models.FloatField(null=True, db_column='T', blank=True)
    p = models.FloatField(null=True, db_column='p', blank=True)
    nu_min = models.FloatField(null=False, db_column='nu_min', blank=True)
    nu_max = models.FloatField(null=False, db_column='nu_max', blank=True)
    n = models.FloatField(null=False, db_column='n', blank=True)
    resolution = models.FloatField(null=True, db_column='resolution', blank=True)
    broadener = models.CharField(max_length=4, db_column='broadener', blank=True)
    ref = models.CharField(max_length=30, db_column='ref', blank=True)
    class Meta:
            db_table = u'xsec'

class QNdesc(models.Model):
    caseid = models.IntegerField(primary_key=True, null=False)
    case_prefix = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=32, null=False)
    HTMLname = models.CharField(max_length=64, null=False)
    attributes = models.TextField(blank=True)
    HTMLattributes = models.TextField(blank=True)
    description = models.TextField(blank=False)
    restrictions = models.TextField(blank=True)
    HTMLrestrictions = models.TextField(blank=True)
    col_index = models.IntegerField(null=True)
    col_name = models.IntegerField(null=True)
    class Meta:
        db_table = u'QNdesc'

class Molecule_Names(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    chemical_name = models.CharField(max_length=64, null=False)
    #molecid = models.ForeignKey('Molecules', db_column='molecID')
    molecid = models.IntegerField(primary_key=True, null=False,
                                  db_column='molecID')
    inchikeystem = models.CharField(max_length=42, db_column='InChIKeyStem')
    molec_name = models.CharField(max_length=20, null=False,
                                  db_column='molec_name')
    class Meta:
        db_table = u'molecule_names'
