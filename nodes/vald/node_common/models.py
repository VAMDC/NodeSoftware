from django.db.models import *
#from vamdctap.bibtextools import *

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

    components = ManyToManyField('self',through='SpeciesComp', symmetrical=False) # only used in case of molecules

    def isMolecule(self):
         return self.ncomp and self.ncomp > 1

    def __unicode__(self):
        return u'ID:%s %s'%(self.id,self.name)
    class Meta:
        db_table = u'species'

class SpeciesComp(Model):
    """
    This is just the intermediary model so that species can refer
    to itself to build molecules.
    """
    molecule = ForeignKey(Species,related_name='molec', on_delete=DO_NOTHING)
    atom = ForeignKey(Species,related_name='atom', on_delete=DO_NOTHING)
    class Meta:
        db_table = u'species_components'

class Reference(Model):
    id = CharField(max_length=7, primary_key=True, db_index=True)
    bibtex = TextField(null=True)
    xml = TextField(null=True)

    def XML(self):
        #return BibTeX2XML( self.bibtex )
        return self.xml

    class Meta:
        db_table = u'refs'
    def __unicode__(self):
        return u'Reference: %s'%self.id

class LineList(Model):
    id = PositiveSmallIntegerField(primary_key=True, db_index=True)
    srcfile = CharField(max_length=128)
    listtype = CharField(max_length=32, null=True, blank=True)
    # vald category mapping = {'exp':0, 'obs':1, 'emp':2, 'pred':3, 'calc':4, 'mix':5}
    # vald->xsams mapping = {0:'experiment', 1:'observed', 2:'empirical', 3:'theory', 4:'semiempirical', 5:'compilation'}
    method = PositiveSmallIntegerField(null=True, db_index=True) # 0-5
    def __unicode__(self):
        return u'ID%s: %s'%(self.id,self.srcfile)
    class Meta:
        db_table = u'linelists'

# Environments
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

# Functions

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
import html
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
