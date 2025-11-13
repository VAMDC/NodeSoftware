from django.db.models import *
from django.db.models import Index, UniqueConstraint
import html

# =============================================================================
# CUSTOM FIELD TYPES
# =============================================================================

class RefCharField(CharField):
    description = "Subclass to CharField that returns strings split at commas"

    def from_db_value(self, value, expression, connection):
        """
        Convert database value to Python object.
        This is ALWAYS called when data is loaded from the database.
        """
        if value is None:
            return None
        if isinstance(value, str):
            return value.split(',')
        return value

    def to_python(self, value):
        """
        Convert to Python object during deserialization/validation.
        """
        if value is None:
            return None
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return value.split(',')
        return value


# =============================================================================
# SPECIES MODELS
# =============================================================================

class Species(Model):
    id = AutoField(primary_key=True, db_index=True)
    name = CharField(max_length=10, db_index=True)
    ion = PositiveSmallIntegerField(db_index=True)
    inchi = CharField(max_length=32, db_index=True)
    inchikey = CharField(max_length=28, db_index=True)
    mass = DecimalField(max_digits=8, decimal_places=5, db_index=True)
    massno = PositiveSmallIntegerField(null=True, db_index=True)
    ionen = DecimalField(max_digits=10, decimal_places=3, null=True)
    solariso = DecimalField(max_digits=6, decimal_places=4, null=True)
    ncomp = PositiveSmallIntegerField(null=True)
    atomic = PositiveSmallIntegerField(null=True, db_index=True)
    isotope = PositiveSmallIntegerField(null=True)

    components = ManyToManyField('self',through='SpeciesComp', symmetrical=False)

    def isMolecule(self):
         return self.ncomp and self.ncomp > 1

    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.name)

    class Meta:
        db_table = u'species'


class SpeciesComp(Model):
    """
    Intermediary model for molecule-atom component relationships.
    """
    molecule = ForeignKey(Species,related_name='molec', on_delete=DO_NOTHING)
    atom = ForeignKey(Species,related_name='atom', on_delete=DO_NOTHING)

    class Meta:
        db_table = u'species_components'


# =============================================================================
# STATE MODEL (UNIFIED: ATOMIC + MOLECULAR)
# =============================================================================

class State(Model):
    id = IntegerField(primary_key=True, db_index=True)

    species = ForeignKey(Species, db_index=False, on_delete=DO_NOTHING)

    energy = DecimalField(max_digits=15, decimal_places=4,null=True, db_index=True)
    energy_scaled = BigIntegerField(null=True, db_index=True)
    lande = DecimalField(max_digits=6, decimal_places=2,null=True)
    config = CharField(max_length=86, null=True)
    term = CharField(max_length=86, null=True)

    hfs_a = FloatField(null=True, db_column=u'hfs_A')
    hfs_a_error = FloatField(null=True, db_column=u'hfs_dA')
    hfs_b = FloatField(null=True, db_column=u'hfs_B')
    hfs_b_error = FloatField(null=True, db_column=u'hfs_dB')

    energy_ref_id= RefCharField(max_length=7, null=True)
    lande_ref_id = RefCharField(max_length=7, null=True)
    level_ref_id = RefCharField(max_length=7, null=True)

    energy_method = PositiveSmallIntegerField(null=True, db_index=True)

    # Common quantum numbers (both atoms and molecules)
    j = DecimalField(max_digits=3, decimal_places=1,db_column=u'J', null=True)
    s = DecimalField(max_digits=3, decimal_places=1,db_column=u'S', null=True)
    p = DecimalField(max_digits=3, decimal_places=1,db_column=u'P', null=True)
    n = PositiveSmallIntegerField(db_column=u'n',null=True)

    # Atomic-specific quantum numbers
    l = PositiveSmallIntegerField(db_column=u'L', null=True)
    j1 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J1', null=True)
    j2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'J2', null=True)
    k = DecimalField(max_digits=3, decimal_places=1,db_column=u'K', null=True)
    s2 = DecimalField(max_digits=3, decimal_places=1,db_column=u'S2', null=True)
    jc = DecimalField(max_digits=3, decimal_places=1,db_column=u'Jc', null=True)
    sn = PositiveSmallIntegerField(db_column=u'Sn',null=True)

    # Molecular quantum numbers (for diatomic molecules)
    v = PositiveSmallIntegerField(db_column=u'v', null=True)
    Lambda = PositiveSmallIntegerField(db_column=u'Lambda', null=True)
    Sigma = DecimalField(max_digits=3, decimal_places=1, db_column=u'Sigma', null=True)
    Omega = DecimalField(max_digits=3, decimal_places=1, db_column=u'Omega', null=True)
    rotN = PositiveSmallIntegerField(db_column=u'rotN', null=True)
    elecstate = CharField(max_length=10, null=True)
    coupling_case = CharField(max_length=2, null=True)

    def jj(self):
        if None not in (self.j1, self.j2):
            return (self.j1, self.j2)

    def multiplicity(self):
        if self.s != None:
            return 2 * self.s + 1

    def description(self):
        """Combine config and term for full level description"""
        if self.config and self.term:
            return f"{self.config} {self.term}"
        elif self.term:
            return self.term
        elif self.config:
            return self.config
        return None

    def j_fmt(self):
        """Format J as integer if whole number, otherwise as decimal"""
        if self.j is None:
            return None
        if self.j % 1 == 0:
            return int(self.j)
        return float(self.j)

    def qn_case(self):
        """Determine appropriate XSAMS case for molecular states"""
        if self.coupling_case == 'Ha':
            return 'hunda'
        elif self.coupling_case == 'Hb':
            return 'hundb'
        elif self.Lambda == 0:
            return 'dcs'
        else:
            return 'hundb'

    def __unicode__(self):
        return u'ID:%s Eng:%s'%(self.id,self.energy)

    def get_Components(self):
        """Required for makeAtomsComponents tagmaker."""
        return self
    Components = property(get_Components)

    class Meta:
        db_table = u'states'
        constraints = [
            UniqueConstraint(
                fields=['species', 'energy_scaled', 'j'],
                name='unique_state'
            )
        ]
        indexes = [
            Index(fields=['species', 'energy_scaled']),
        ]


# =============================================================================
# TRANSITION MODEL
# =============================================================================

class Transition(Model):
    id = AutoField(primary_key=True)
    upstate = ForeignKey(State,related_name='isupperstate_trans',db_column='upstate',null=True, db_index=False, on_delete=DO_NOTHING)
    lostate = ForeignKey(State,related_name='islowerstate_trans',db_column='lostate',null=True, db_index=False, on_delete=DO_NOTHING)

    wave = DecimalField(max_digits=16, decimal_places=8, db_index=True)
    waveritz = DecimalField(max_digits=16, decimal_places=8, db_index=True)

    species = ForeignKey(Species, db_index=True, on_delete=DO_NOTHING)
    loggf = DecimalField(max_digits=8, decimal_places=3, null=True)
    einsteina = FloatField(db_index=True, null=True)
    gammarad = DecimalField(max_digits=6, decimal_places=2,null=True)
    gammastark = DecimalField(max_digits=7, decimal_places=3,null=True)
    gammawaals = DecimalField(max_digits=6, decimal_places=3,null=True)
    sigmawaals = PositiveSmallIntegerField(null=True)
    alphawaals = DecimalField(max_digits=6, decimal_places=3,null=True)

    accurflag = CharField(max_length=1, null=True)
    accur = CharField(max_length=10, null=True)
    loggf_err = DecimalField(max_digits=6, decimal_places=3, null=True)

    wave_ref_id = RefCharField(max_length=7, null=True)
    waveritz_ref_id = RefCharField(max_length=7, null=True)
    loggf_ref_id = RefCharField(max_length=7, null=True)
    gammarad_ref_id = RefCharField(max_length=7, null=True)
    gammastark_ref_id = RefCharField(max_length=7, null=True)
    waals_ref_id = RefCharField(max_length=7, null=True)

    transition_type = CharField(max_length=2, null=True)
    autoionized = BooleanField(default=False, null=True)
    wave_method = PositiveSmallIntegerField(null=True, db_index=True)

    def get_waves(self):
        return self.wave, self.waveritz

    def get_wave_comments(self):
        return 'Vacuum wavelength from measurements (non-RITZ)','Vacuum wavelength from state energies (RITZ)'

    def get_wave_refs(self):
        return self.wave_ref_id, self.waveritz_ref_id

    def get_wave_methods(self):
        return self.wave_method, 6

    def get_waals(self):
        if self.gammawaals: return self.gammawaals
        elif self.sigmawaals and self.alphawaals: return [self.sigmawaals, self.alphawaals]
        else: return ""

    def get_waals_name(self):
        if self.gammawaals: return "log(gamma)"
        elif self.sigmawaals and self.alphawaals: return ["sigma", "alpha"]
        else: return ""

    def get_waals_units(self):
        if self.gammawaals: return "1/cm3/s"
        elif self.sigmawaals and self.alphawaals: return ["unitless", "unitless"]
        else: return ""

    def get_waals_function(self):
        if self.gammawaals: return "waals"
        elif self.sigmawaals and self.alphawaals: return "waals-barklem"
        else: return ""

    def get_accur_type(self):
        if self.accurflag in (u"N", u"E"): return u"estimated"
        elif self.accurflag == u'C': return u"arbitrary"
        elif self.accurflag == u'P': return u"systematic"
        else: return ""

    def get_accur_relative(self):
        return str(self.accurflag in (u"N", u"E", u"C")).lower()

    def get_accur_comment(self):
        flag_descriptions = {
            u'N': u'NIST quality class',
            u'E': u'Estimated error in dex',
            u'C': u'Cancellation factor',
            u'P': u'Predicted line',
            u'_': u'Quality indicator'
        }
        return flag_descriptions.get(self.accurflag, u'')

    def __unicode__(self):
        return u'ID:%s Wavel: %s' % (self.id, self.wave)

    class Meta:
        db_table = u'transitions'
        indexes = [
            Index(fields=['species', 'wave'], name='speciesid_wave'),
        ]


# =============================================================================
# REFERENCE MODEL
# =============================================================================

class Reference(Model):
    id = CharField(max_length=7, primary_key=True, db_index=True)
    bibtex = TextField(null=True)
    xml = TextField(null=True)

    def XML(self):
        return self.xml

    class Meta:
        db_table = u'refs'

    def __unicode__(self):
        return u'Reference: %s'%self.id


# =============================================================================
# LINE LIST MODEL
# =============================================================================

class LineList(Model):
    id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    srcfile = CharField(max_length=128)
    listtype = CharField(max_length=32, null=True, blank=True)
    method = PositiveSmallIntegerField(null=True, db_index=True)

    def __unicode__(self):
        return u'ID%s: %s'%(self.id,self.srcfile)

    class Meta:
        db_table = u'linelists'


# =============================================================================
# ENVIRONMENT DEFINITIONS
# =============================================================================

class EnvClass(object):
    def __init__(self,xml):
        self.xml = xml
    def XML(self):
        return self.xml

EnvGeneral="""<Environment envID="%s">
<Comments>%s</Comments>
<Temperature><Value units="K">1.0E4</Value></Temperature>
<TotalNumberDensity><Comments>The broadening parameters are given in
Hz per number density (i.e. 1/cm3/s), so they can simply
be scaled with the number density. Note that unless otherwise noted,
log10(gamma) is given.</Comments>
<Value units="1/cm3/s">1</Value>
</TotalNumberDensity>
</Environment>
"""

EnvStark=EnvGeneral%('Evald-stark',"""A given gamma can be scaled with
gamma = gamma_given * (T / T_ref)^1/6 * number density of free electrons.""")

EnvWaals=EnvGeneral%('Evald-waals',"""A given gamma can be scaled with gamma =
gamma_given * (T / T_ref)^alpha * number density for any neutral perturber.
If alpha is not given, it is 1/3. Note that for some transitions additional parameters
are available, allowing a more accurate broadening calculation by Anstee, Barklem and O'Mara.""")

EnvNatural="""<Environment envID="Evald-natural">
<Comments>There are no parameters for natural/radiative broadening.</Comments>
</Environment>"""

Environments = [EnvClass(EnvStark), EnvClass(EnvWaals), EnvClass(EnvNatural)]


# =============================================================================
# FUNCTION DEFINITIONS
# =============================================================================

class FuncClass(object):
    def __init__(self, xml):
        self.xml = xml
    def XML(self):
        return self.xml

starkfunc = FuncClass("""<Function functionID="Fvald-stark">
<Name>Stark Broadening</Name>
<Expression computerLanguage="Fortran">
    gammawaal * (T / 10000.0) ** (1.0/6.0) * N
</Expression>
<Y name="gammaL" units="1/cm3/s"></Y>
<Arguments>
    <Argument name="T" units="K">
        <Description>The absolute temperature, in K</Description>
    </Argument>
    <Argument name="N" units="1/cm3">
        <Description>Number density of neutral perturbers</Description>
    </Argument>
</Arguments>
<Parameters>
    <Parameter name="gammawaal" units="1/cm3/s">
       <Description>Lorentzian FWHM of the line</Description>
    </Parameter>
</Parameters>
<Description>This function gives the temperature dependence of Stark broadening.</Description>
</Function>""")

waalsfunc = FuncClass("""<Function functionID="Fvald-waals">
<Name>Waals broadening</Name>
<Expression computerLanguage="Fortran">
    gammawaal * (T / 10000.0) ** (1.0/3.0) * N
</Expression>
<Y name="gammaL" units="1/cm3/s"></Y>
<Arguments>
    <Argument name="T" units="K">
        <Description>The absolute temperature, in K</Description>
    </Argument>
    <Argument name="N" units="1/cm3">
        <Description>Number density of neutral perturbers</Description>
    </Argument>
</Arguments>
<Parameters>
    <Parameter name="gammawaal" units="1/cm3/s">
       <Description>Lorentzian FWHM of the line</Description>
    </Parameter>
</Parameters>
<Description>This function gives the temperature dependence of Van der Waals broadening.</Description>
</Function>""")

waalsbfunc = FuncClass(r"""<Function functionID="Fvald-waals-barklem">
<Name>Waals broadening, Barklem correction</Name>
<Expression computerLanguage="LaTeX">
    $\left(\frac{4}{\pi}\right)^{\alpha/2}\cdot\Gamma\left(\frac{6-\alpha}{2}\right)\cdot v_0\cdot\sigma({v_0})\cdot\left(\frac{\bar{v}}{v_0}\right)^{1-\alpha}\cdot N$
</Expression>
<Y name="gammaL" units="1/cm3/s"></Y>
<Arguments>
    <Argument name="v" units="m/s">
        <Description>Collisional speed, $\sqrt{\frac{8kT,\pi\mu}}$, where $\mu=\frac{1,\frac{1,1.008}+\frac{1, m_A}}$.</Description>
    </Argument>
    <Argument name="v0" units="m/s">
        <Description>Calculated collisional speed - 10 000 m/s</Description>
    </Argument>
    <Argument name="N" units="1/m3">
        <Description>Number density of neutral perturbers</Description>
    </Argument>
</Arguments>
<Parameters>
    <Parameter name="sigma" units="unitless">
       <Description>Broadening cross section in atomic size units (Bohr radii)</Description>
    </Parameter>
    <Parameter name="alpha" units="unitless">
       <Description>Velocity dependence of the cross section, assuming $\sigma(v) \propto v^{-\alpha}$</Description>
    </Parameter>
</Parameters>
<Description>%s</Description>
<SourceCodeURL>http://www.astro.uu.se/~barklem/howto.html</SourceCodeURL>
</Function>
""" % html.escape("This function gives the temperature dependence of Van der Waals broadening using a more exact formula by Anstee, Barklem & O'Mara."))

Functions = [starkfunc, waalsfunc, waalsbfunc]
