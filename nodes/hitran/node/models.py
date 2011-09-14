from django.db import models
import datetime

class Molecule(models.Model):
    molecID = models.IntegerField(primary_key=True, unique=True)
    molecID_str = models.CharField(max_length=40)
    InChI = models.CharField(max_length=200, unique=True)
    InChIKey = models.CharField(max_length=27, unique=True)
    # canonical stoichiometric formula with atoms in increasing order of
    # atomic mass:
    stoichiometric_formula = models.CharField(max_length=40)
    # ordinary formula for display and search:
    ordinary_formula = models.CharField(max_length=40)
    ordinary_formula_html = models.CharField(max_length=200)
    # the single most common name used to refer to this species:
    common_name = models.CharField(max_length=100, null=True, blank=True)
    # CML representation of the species, with no isotope information
    cml = models.TextField(null=True, blank=True)
    class Meta:
            db_table = u'hitranmeta_molecule'

class MoleculeName(models.Model):
    name = models.CharField(max_length=100)
    molecule = models.ForeignKey('Molecule')
    class Meta:
        db_table = 'hitranmeta_moleculename'

class Iso(models.Model):
    isoID = models.IntegerField()
    isoID_str = models.CharField(max_length=50)
    InChI_explicit = models.CharField(max_length=200, null=True, blank=True,
                                      unique=True)
    InChIKey_explicit = models.CharField(max_length=27, null=True, blank=True,
                                         unique=True)
    InChI = models.CharField(max_length=200, unique=True)
    InChIKey = models.CharField(max_length=27, unique=True)
    molecule = models.ForeignKey('Molecule')
    iso_name = models.CharField(max_length=100)
    iso_name_html = models.CharField(max_length=500)
    abundance = models.FloatField(null=True, blank=True)
    afgl_code = models.CharField(max_length=10, null=True, blank=True)
    # CML representation of the species, with all isotopeNumbers
    # specified explicitly:
    cml_explicit = models.TextField(null=True, blank=True)
    # CML representation of the species with only the essential (ie
    # not maximum abundance, apart from Br) isotopeNumbers specified:
    cml = models.TextField(null=True, blank=True)
    case = models.ForeignKey('Case', null=True, blank=True)
    class Meta:
        db_table = 'hitranmeta_iso'

class Case(models.Model):
    case_prefix = models.CharField(max_length=10, unique=True)
    case_description = models.CharField(max_length=50)
    class Meta:
        db_table = 'hitranmeta_case'

class Ref(models.Model):
    # unique ID for this reference
    refID = models.CharField(max_length=100)
    # reference type (e.g. 'article', 'private communication')
    ref_type = models.CharField(max_length=50, )
    # a list of the authors' names in a string as:
    # 'A.N. Other, B.-C. Person Jr., Ch. Someone-Someone, and N.M.L. Haw Haw'
    authors = models.TextField(null=True, blank=True)
    # the article, book, or thesis title
    title = models.TextField(null=True, blank=True)
    # the title as HTML
    title_html = models.TextField(null=True, blank=True)
    # the journal name
    journal = models.CharField(max_length=500, null=True, blank=True)
    # the volume (which may be a string)
    volume = models.CharField(max_length=10, null=True, blank=True)
    # the first page (which may be a string e.g. 'L123')
    page_start = models.CharField(max_length=10, null=True, blank=True)
    # the last page
    page_end = models.CharField(max_length=10, null=True, blank=True)
    # the year of publication, creation, or communication
    year = models.IntegerField(null=True, blank=True)
    # the institution name, if relevant and available
    institution = models.CharField(max_length=500, null=True, blank=True)
    # a note, perhaps containing cross-references of ref_id inside
    # square brackets
    note = models.TextField(null=True, blank=True)
    # the note as HTML
    note_html = models.TextField(null=True, blank=True)
    # the Digital Object Identifier, if available
    doi = models.CharField(max_length=100, null=True, blank=True)
    # a string of HTML to be output on websites citing this reference
    cited_as_html = models.TextField()
    # a URL to the source, if available
    url = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.refID

    class Meta:
        db_table = 'hitranmeta_ref'

class Qns(models.Model):
    case = models.ForeignKey('Case')
    state = models.ForeignKey('State')
    qn_name = models.CharField(max_length=20)
    qn_val = models.CharField(max_length=10)
    qn_attr = models.CharField(max_length=50, blank=True, null=True)
    xml = models.CharField(max_length=500)
    
    class Meta:
        db_table = 'hitranlbl_qns'

class State(models.Model):
    iso = models.ForeignKey('Iso')
    energy = models.FloatField(blank=True, null=True)
    g = models.IntegerField(blank=True, null=True)
    s_qns = models.CharField(max_length=500, blank=True, null=True)
    qns_xml = models.TextField(blank=True, null=True)

    def XML(self):
        xml = []
        case_prefix = self.iso.case.case_prefix
        xml.append('<Case xsi:type="%s:Case" caseID="%s" xmlns:%s='
              '"http://vamdc.org/xml/xsams/0.2/cases/%s">'
            % (case_prefix, case_prefix, case_prefix, case_prefix))
        xml.append(self.qns_xml)
        xml.append('</Case>')
        return '\n'.join(xml)

    class Meta:
        db_table = 'hitranlbl_state'

class Trans(models.Model):
    iso = models.ForeignKey('Iso')
    statep = models.ForeignKey('State', related_name='trans_upper_set')
    statepp = models.ForeignKey('State', related_name='trans_lower_set')
    nu = models.FloatField()
    Sw = models.FloatField()
    A = models.FloatField()
    multipole = models.CharField(max_length=2, blank=True, null=True)
    Elower = models.FloatField(blank=True, null=True)
    gp = models.IntegerField(blank=True, null=True)
    gpp = models.IntegerField(blank=True, null=True)
    valid_from = models.DateField()
    # the default is for this data 'never' to expire:
    valid_to = models.DateField(default=datetime.date(
            year=3000, month=1, day=1))
    par_line = models.CharField(max_length=160, blank=True, null=True)
    
    class Meta:
        db_table = 'hitranlbl_trans'

    def XML_Broadening(self):
        """
        Build and return the XML for the air- and self-broadening parameters
        gamma_air, n_air, and gamma_self.

        """

        broadening_xml = []
        if 'gamma_air' in self.__dict__:
            lineshape_xml = []
            lineshape_xml.append('      <Lineshape name="Lorentzian">\n'\
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
                   '          <FitParameter name="gammaL_ref">\n')
            if self.gamma_air.ref is not None:
                lineshape_xml.append('            <SourceRef>B%s</SourceRef>\n'
                                     % self.gamma_air.ref)
            lineshape_xml.append('            <Value units="1/cm">%s</Value>\n'
                                 % self.gamma_air.val)
            if self.gamma_air.err is not None:
                lineshape_xml.append('            <Accuracy><Statistical>'
                     '%s</Statistical></Accuracy>\n' % str(self.gamma_air.err))
            lineshape_xml.append('          </FitParameter>\n')
            if 'n_air' in self.__dict__:
                lineshape_xml.append('          <FitParameter name="n">\n')
                if self.n_air.ref is not None:
                    lineshape_xml.append('            <SourceRef>B%s'
                                         '</SourceRef>\n' % self.n_air.ref)
                lineshape_xml.append('            <Value units="unitless">%s'
                                     '</Value>\n' % self.n_air.val)
                if self.n_air.err is not None:
                    lineshape_xml.append('            <Accuracy><Statistical>'
                      '%s</Statistical></Accuracy>\n' % str(self.n_air.err))
                lineshape_xml.append('          </FitParameter>\n')
            lineshape_xml.append('        </FitParameters>\n'\
                                 '      </LineshapeParameter>\n</Lineshape>\n')
            broadening_xml.append('    <Broadening'
                ' envRef="Eair-broadening-ref-env" name="pressure">\n'
                '%s    </Broadening>\n' % ''.join(lineshape_xml))
        if 'gamma_self' in self.__dict__:
            lineshape_xml = []
            lineshape_xml.append('      <Lineshape name="Lorentzian">\n'\
                           '        <LineshapeParameter name="gammaL">\n')
            if self.gamma_self.ref is not None:
                lineshape_xml.append('          <SourceRef>B%s</SourceRef>\n'
                                     % self.gamma_self.ref)
            lineshape_xml.append('          <Value units="1/cm">%s</Value>\n'
                      % self.gamma_self.val)
            if self.gamma_self.err is not None:
                lineshape_xml.append('          <Accuracy><Statistical>'\
                    '%s</Statistical></Accuracy>\n' % str(self.gamma_self.err))
            lineshape_xml.append('        </LineshapeParameter>\n'\
                                 '      </Lineshape>\n')
            broadening_xml.append('    <Broadening'\
                ' envRef="Eself-broadening-ref-env" name="pressure">\n'\
                '%s    </Broadening>\n' % ''.join(lineshape_xml))
        return '    %s\n' % ''.join(broadening_xml)

    def XML_Shifting(self):
        """
        Build and return the XML for the air-shifting parameter, delta_air.

        """

        shifting_xml = []
        if 'delta_air' in self.__dict__:
            shifting_xml.append('<Shifting envRef='
                   '"Eair-broadening-ref-env">\n'
                   '      <ShiftingParameter name="delta">\n'
                   '        <FitParameters functionRef="Fdelta">\n'
                   '          <FitArgument name="p" units="K">\n'
                   '            <LowerLimit>0.</LowerLimit>\n'
                   '            <UpperLimit>1.2</UpperLimit>\n'
                   '          </FitArgument>\n'
                   '          <FitParameter name="delta_ref">\n')
            if self.delta_air.ref is not None:
                shifting_xml.append('            <SourceRef>B%s</SourceRef>\n'
                                    % self.delta_air.ref)
            shifting_xml.append('            <Value units="unitless">%s'
                                '</Value>\n' % self.delta_air.val)
            if self.delta_air.err is not None:
                shifting_xml.append('            <Accuracy><Statistical>'\
                    '%s</Statistical></Accuracy>\n' % str(self.delta_air.err))
            shifting_xml.append('          </FitParameter>\n'\
                                '        </FitParameters>\n'\
                                '      </ShiftingParameter>\n'\
                                '    </Shifting>\n')
        return '    %s\n' % ''.join(shifting_xml)

class Prm(models.Model):
    trans = models.ForeignKey('Trans')
    name = models.CharField(max_length=20)
    val = models.FloatField()
    err = models.FloatField(blank=True, null=True)
    ref = models.ForeignKey('Ref', blank=True, null=True)
    method = models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'hitranlbl_prm'

class Method(object):
    def __init__(self, id, category, description):
        self.id = id
        self.category = category
        self.description = description
