from django.db import models

import datetime, time
from hitrandb import hitran_request
from hitrandb import hitran

# Create your models here.
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

    def xsams(self):
        yield '    <Molecule>\n'
        yield '      <MolecularChemicalSpecies>\n'
        yield '        <OrdinaryStructuralFormula>%s' \
                  '</OrdinaryStructuralFormula>\n' % self.molec_name
        yield '        <StoichiometricFormula>%s' \
                  '</StoichiometricFormula>\n' % self.molec_name
        yield '        <ChemicalName>%s' \
                  '</ChemicalName>\n' % self.chemical_names
        yield '      </MolecularChemicalSpecies>\n'

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

class States(models.Model):
    id = models.CharField(primary_key=True, max_length=192, db_column='id')
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

    def xsams(self):
        yield '      <MolecularState stateID="%s">\n' % self.stateid
        yield '        <Description>A molecular state </Description>\n'
        yield '        <MolecularStateCharacterisation>\n'
        if self.energy:
            yield '          <StateEnergy energyOrigin="electronic and ' \
                  'vibrational ground state">\n'
            yield '            <Value units="1/cm">%12.6f</Value>\n' \
                        % self.energy
            yield '          </StateEnergy>\n'
        if self.g:
            yield '          <TotalStatisticalWeight>%d' \
                  '</TotalStatisticalWeight>\n' % self.g
        yield '        </MolecularStateCharacterisation>\n'
        yield '      </MolecularState>\n'

class Refs(models.Model):
    sourceid = models.CharField(max_length=192, primary_key=True,
                                db_column='sourceID')
    type = models.CharField(max_length=96, blank=True)
    author = models.TextField(blank=True)
    title = models.TextField(blank=True)
    journal = models.TextField(blank=True)
    volume = models.CharField(max_length=30, blank=True)
    pages = models.CharField(max_length=60, blank=True)
    year = models.TextField(blank=True)
    institution = models.TextField(blank=True)
    note = models.TextField(blank=True)
    doi = models.CharField(max_length=192, blank=True)
    class Meta:
        db_table = u'refs'

    def xsams(self):
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
    initialstateref = models.CharField(max_length=192,
                                       db_column='InitialStateRef', blank=True)
    finalstateref = models.CharField(max_length=192,
                                       db_column='FinalStateRef', blank=True)
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
    datestamp = models.DateField(null=True, db_column='datestamp', blank=True)
    ierr = models.CharField(max_length=18, db_column='Ierr', blank=True)

    prms = []

    class Meta:
        db_table = u'trans'

    def xsams(self):
        yield '<RadiativeTransition methodRef="MEXP"' \
                ' sourceRef="B_HITRAN2008">\n'
        yield '  <EnergyWavelength>\n'
        yield '    <Wavenumber>\n'
        yield '      <Experimental sourceRef="%s">\n' % self.nu_ref
        yield '        <Value units="1/cm">%12.6f</Value>\n' % self.nu
        if self.nu_err:
            yield '        <Accuracy>%10.3e</Accuracy>\n' % self.nu_err
        yield '      </Experimental>\n'
        yield '    </Wavenumber>\n'
        yield '  </EnergyWavelength>\n'
        yield '  <InitialStateRef>%s</InitialStateRef>\n' \
                        % self.initialstateref
        yield '  <FinalStateRef>%s</FinalStateRef>\n' % self.finalstateref
        yield '  <Probability>\n'
        yield '    <TransitionProbabilityA sourceRef="%s">\n' % self.a_ref
        yield '      <Value units="1/s">%10.3e</Value>\n' % self.a
        if self.a_err:
            yield '      <Accuracy>%10.3e</Accuracy>\n' % self.a_err
        yield '    </TransitionProbabilityA>\n'
        yield '  </Probability>\n'
        yield '</RadiativeTransition>\n'

class Prms(models.Model):
    id = models.IntegerField(primary_key=True, null=False, db_column='id')
    molecid = models.IntegerField(db_column='molecID')
    isoid = models.IntegerField(db_column='isoID')
    inchikey = models.CharField(max_length=81, db_column='InChIKey')
    #transid = models.CharField(max_length=192, db_column='transeID')
    transid = models.ForeignKey('Trans', db_column='transID')
    prm_name = models.CharField(max_length=192, db_column='prm_name')
    prm_val = models.FloatField(db_column='prm_val')
    prm_err = models.FloatField(db_column='prm_err')
    prm_ref = models.CharField(max_length=90, db_column='prm_err')
    class Meta:
            db_table = u'prms'

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

def make_request(form):
    """
    Make and return the HITRANrequest object for the required lines.
    Arguments:
    form: a SearchForm object with the clean and parsed query parameters

    """

    # reset the linelist results list:
    #HITRAN.linelist=[]
    # construct the HITRANrequest object:
    req = hitran_request.HITRANRequest(None)
    req.numin = form.numin
    req.numax = form.numax
    req.Smin = form.Smin
    req.molecIDs = [int(molecID) for molecID in form.selected_molecIDs]

    # hard-code this bit for now.
    req.get_states = True
    output_formats = ['txt',]
    output_params = ['nu', 'nu_err', 'S', 'S_err', 'g_air', 'n_air']
    compression = None
    # NB these are a little different from HITRAN: e.g. n_air is %5.2f
    # to allow -0.xx values instead of -.xx
    fixed_format = ['%12.6f', '%8.6f', '%10.3e', '%10.3e', '%5.4f',
                    '%5.2f']
    sep = ', '

    # integer timestamp: the number of seconds since 00:00 1 January 1970
    # using UTC:
    #ts_int = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    # XXX temporary: use a fixed, constant filestem:
    ts_int=1285072598
    # make the timestamp from the hex representation of ts_int, stripping
    # off the initial '0x' characters:
    #filestem = hex(ts_int)[2:]
    filestem = 'searchapp/results/%s' % hex(ts_int)[2:]

    req.setup_output_objects(output_formats, filestem, compression,
                             output_params, fixed_format, sep)
    return req

def process_request(req):
    """
    Process the HITRANRequest, req.

    """

    hitran_search = hitran.HITRAN(req)
    return hitran_search.read_db()
