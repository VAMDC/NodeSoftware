# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

import datetime, time
#import HITRANdb
#import HITRANrequest
#from Output.OutputPAR import *
#from Output.OutputTXT import *
#from Output.OutputXML import *

#HITRAN = HITRANdb.HITRANdb()
def make_request(numin, numax, Smin, selected_molecids, output_params,
                    output_formats, compression=None):
    """
    Make and return the HITRANrequest object for the required lines.
    Arguments:
    numin, numax: the wavenumber range for lines to return
    Smin: the minimum HITRAN line strength minimum,
    selected_molecids: a list identifying the species whose transitions
        are to be returned
    output_params: a list of strings identifying the parameters to output
    output_formats: a list of strings identifying the output formats to
        produce

    """

    # reset the linelist results list:
    HITRAN.linelist=[]
    # construct the HITRANrequest object:
    req = HITRAN.request.HITRANrequest(HITRAN.meta)
    req.numin = numin
    req.numax = numax
    req.Smin = Smin
    req.molecIDs = [int(molecID) for molecID in selected_molecids]
    req.get_states = True

    # integer timestamp: the number of seconds since 00:00 1 January 1970
    # using UTC:
    #ts_int = int(time.mktime(datetime.datetime.utcnow().timetuple()))
    ts_int=1285072598
    # make the timestamp from the hex representation of ts_int, stripping
    # off the initial '0x' characters:
    filestem = hex(ts_int)[2:]

    req.setup_output_objects(output_formats, filestem, compression,
                             output_params)
    return req

class AllStates(models.Model):
    molecid = models.IntegerField(null=True, db_column='molecID', blank=True)
    isoid = models.IntegerField(null=True, db_column='isoID', blank=True)
    stateid = models.CharField(max_length=192, primary_key=True,
                               db_column='stateID')
    assigned = models.IntegerField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    energy_err = models.FloatField(null=True, blank=True)
    energy_flag = models.CharField(max_length=3, blank=True)
    g = models.IntegerField(null=True, blank=True)
    caseid = models.IntegerField(null=True, db_column='caseID', blank=True)
    elecstatelabel = models.CharField(max_length=3,
                                      db_column='ElecStateLabel', blank=True)
    qn1 = models.IntegerField(null=True, db_column='QN1', blank=True)
    qn2 = models.IntegerField(null=True, db_column='QN2', blank=True)
    qn3 = models.IntegerField(null=True, db_column='QN3', blank=True)
    qn4 = models.IntegerField(null=True, db_column='QN4', blank=True)
    qn5 = models.IntegerField(null=True, db_column='QN5', blank=True)
    qn6 = models.IntegerField(null=True, db_column='QN6', blank=True)
    qn7 = models.IntegerField(null=True, db_column='QN7', blank=True)
    qn8 = models.IntegerField(null=True, db_column='QN8', blank=True)
    qn9 = models.IntegerField(null=True, db_column='QN9', blank=True)
    qn10 = models.IntegerField(null=True, db_column='QN10', blank=True)
    sym1 = models.CharField(max_length=12, db_column='Sym1', blank=True)
    sym2 = models.CharField(max_length=12, db_column='Sym2', blank=True)
    sym3 = models.CharField(max_length=12, db_column='Sym3', blank=True)
    sym4 = models.CharField(max_length=12, db_column='Sym4', blank=True)
    sym5 = models.CharField(max_length=12, db_column='Sym5', blank=True)
    sym6 = models.CharField(max_length=12, db_column='Sym6', blank=True)
    sym7 = models.CharField(max_length=12, db_column='Sym7', blank=True)
    sym8 = models.CharField(max_length=12, db_column='Sym8', blank=True)
    sym9 = models.CharField(max_length=12, db_column='Sym9', blank=True)
    sym10 = models.CharField(max_length=12, db_column='Sym10', blank=True)
    sqn1 = models.IntegerField(null=True, db_column='sQN1', blank=True)
    sqn2 = models.IntegerField(null=True, db_column='sQN2', blank=True)
    sqn3 = models.IntegerField(null=True, db_column='sQN3', blank=True)
    sqn4 = models.IntegerField(null=True, db_column='sQN4', blank=True)
    sqn5 = models.IntegerField(null=True, db_column='sQN5', blank=True)
    #timestamp = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'all_states'

    def xsams(self):
        yield '      <MolecularState stateID="%s">\n' % self.stateid
        yield '        <Description>A molecular state </Description>\n'
        yield '        <MolecularStateCharacterisation>\n'
        yield '          <StateEnergy energyOrigin="electronic and ' \
              'vibrational ground state">\n'
        yield '            <Value units="1/cm">%12.6f</Value>\n' \
                    % self.energy
        yield '          </StateEnergy>\n'
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
    initialstateref = models.CharField(max_length=192,
                                       db_column='InitialStateRef', blank=True)
    finalstateref = models.CharField(max_length=192,
                                       db_column='FinalStateRef', blank=True)
    nu = models.FloatField()
    nu_err = models.FloatField(null=True, blank=True)
    nu_ref = models.CharField(max_length=93, blank=True)
    s = models.FloatField(null=True, db_column='S', blank=True)
    s_err = models.FloatField(null=True, db_column='S_err', blank=True)
    s_ref = models.CharField(max_length=90, db_column='S_ref', blank=True)
    a = models.FloatField(null=True, db_column='A', blank=True)
    a_err = models.FloatField(null=True, db_column='A_err', blank=True)
    a_ref = models.CharField(max_length=90, db_column='A_ref', blank=True)
    multipole = models.CharField(max_length=6, blank=True)
    g_air = models.FloatField(null=True, blank=True)
    g_air_err = models.FloatField(null=True, blank=True)
    g_air_ref = models.CharField(max_length=102, blank=True)
    g_self = models.FloatField(null=True, blank=True)
    g_self_err = models.FloatField(null=True, blank=True)
    g_self_ref = models.CharField(max_length=105, blank=True)
    n_air = models.FloatField(null=True, blank=True)
    n_air_err = models.FloatField(null=True, blank=True)
    n_air_ref = models.CharField(max_length=102, blank=True)
    delta_air = models.FloatField(null=True, blank=True)
    delta_air_err = models.FloatField(null=True, blank=True)
    delta_air_ref = models.CharField(max_length=120, blank=True)
    elower = models.FloatField(null=True, db_column='Elower', blank=True)
    gp = models.IntegerField(null=True, blank=True)
    gpp = models.IntegerField(null=True, blank=True)
    datestamp = models.DateField(null=True, blank=True)
    ierr = models.CharField(max_length=18, db_column='Ierr', blank=True)
    class Meta:
        db_table = u'trans'

    def xsams(self):
        yield '<RadiativeTransition methodRef="MEXP"' \
                ' sourceRef="B_HITRAN2008">\n'
        yield '  <EnergyWavelength>\n'
        yield '    <Wavenumber>\n'
        yield '      <Experimental sourceRef="%s">\n' % self.nu_ref
        yield '        <Value units="1/cm">%12.6f</Value>\n' % self.nu
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


class Molecules(models.Model):
    molecid = models.IntegerField(primary_key=True, null=False)
    molec_name = models.CharField(max_length=20, null=False)
    molec_name_html = models.CharField(max_length=128, null=False)
    molec_name_latex = models.CharField(max_length=128, null=False)
    stoichiometric_formula = models.CharField(max_length=40, null=False)
    chemical_names = models.CharField(max_length=256)
    caseid = models.IntegerField(null=True)
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

