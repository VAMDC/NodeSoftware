# ./XsamsPyxb.py
# PyXB bindings for NamespaceModule
# NSM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2010-03-26 08:46:50.789909 by PyXB version 1.1.2-DEV
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:bbba7efa-38ab-11df-b210-000423714bc4')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a Python instance."""
    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace.fallbackNamespace(), location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)


# Atomic SimpleTypeDefinition
class ElementSymbolType (pyxb.binding.datatypes.token):

    """Symbol for a chemical element"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ElementSymbolType')
    _Documentation = u'Symbol for a chemical element'
ElementSymbolType._CF_pattern = pyxb.binding.facets.CF_pattern()
ElementSymbolType._CF_pattern.addPattern(pattern=u'\\p{Lu}\\p{Ll}?')
ElementSymbolType._InitializeFacetMap(ElementSymbolType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'ElementSymbolType', ElementSymbolType)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.IDREFS
class STD_ANON_1 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.IDREF."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.IDREF
STD_ANON_1._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_1._CF_pattern.addPattern(pattern=u'B.+')
STD_ANON_1._InitializeFacetMap(STD_ANON_1._CF_pattern)

# Atomic SimpleTypeDefinition
class STD_ANON_2 (pyxb.binding.datatypes.IDREF):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_2._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_2._CF_pattern.addPattern(pattern=u'M.+')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_pattern)

# Atomic SimpleTypeDefinition
class OrbitalAngularMomentumSymbolType (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OrbitalAngularMomentumSymbolType')
    _Documentation = None
OrbitalAngularMomentumSymbolType._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
OrbitalAngularMomentumSymbolType._CF_pattern = pyxb.binding.facets.CF_pattern()
OrbitalAngularMomentumSymbolType._CF_pattern.addPattern(pattern=u'\\w')
OrbitalAngularMomentumSymbolType._InitializeFacetMap(OrbitalAngularMomentumSymbolType._CF_length,
   OrbitalAngularMomentumSymbolType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'OrbitalAngularMomentumSymbolType', OrbitalAngularMomentumSymbolType)

# Atomic SimpleTypeDefinition
class StateRef (pyxb.binding.datatypes.IDREF):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StateRef')
    _Documentation = None
StateRef._CF_pattern = pyxb.binding.facets.CF_pattern()
StateRef._CF_pattern.addPattern(pattern=u'S.+')
StateRef._InitializeFacetMap(StateRef._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'StateRef', StateRef)

# Atomic SimpleTypeDefinition
class STD_ANON_3 (pyxb.binding.datatypes.ID):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_3._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_3._CF_pattern.addPattern(pattern=u'S.+')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_pattern)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class DataListType (pyxb.binding.basis.STD_list):

    """List of numerical data"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataListType')
    _Documentation = u'List of numerical data'

    _ItemType = pyxb.binding.datatypes.double
DataListType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'DataListType', DataListType)

# Atomic SimpleTypeDefinition
class IAEACodeType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IAEACodeType')
    _Documentation = None
IAEACodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=IAEACodeType, enum_prefix=None)
IAEACodeType.EGN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EGN')
IAEACodeType.EAS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EAS')
IAEACodeType.EBS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EBS')
IAEACodeType.EDX = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDX')
IAEACodeType.EEL = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EEL')
IAEACodeType.ELB = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ELB')
IAEACodeType.ETS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ETS')
IAEACodeType.EDT = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDT')
IAEACodeType.EFL = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EFL')
IAEACodeType.EEX = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EEX')
IAEACodeType.EIN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EIN')
IAEACodeType.EMI = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EMI')
IAEACodeType.ENI = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ENI')
IAEACodeType.EMT = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EMT')
IAEACodeType.EUP = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EUP')
IAEACodeType.EDP = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDP')
IAEACodeType.EIP = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EIP')
IAEACodeType.ERC = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ERC')
IAEACodeType.ERR = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ERR')
IAEACodeType.ERD = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ERD')
IAEACodeType.ERT = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ERT')
IAEACodeType.ERO = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'ERO')
IAEACodeType.EDC = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDC')
IAEACodeType.EDS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDS')
IAEACodeType.EDR = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDR')
IAEACodeType.EDA = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDA')
IAEACodeType.EDE = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDE')
IAEACodeType.EDI = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'EDI')
IAEACodeType.PGN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PGN')
IAEACodeType.PTS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PTS')
IAEACodeType.PDS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PDS')
IAEACodeType.PES = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PES')
IAEACodeType.PMA = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PMA')
IAEACodeType.PDT = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PDT')
IAEACodeType.PFL = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PFL')
IAEACodeType.PEX = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PEX')
IAEACodeType.PIN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PIN')
IAEACodeType.PFF = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PFF')
IAEACodeType.PEA = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PEA')
IAEACodeType.PTA = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PTA')
IAEACodeType.PAD = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PAD')
IAEACodeType.PED = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PED')
IAEACodeType.PNL = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PNL')
IAEACodeType.PZE = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PZE')
IAEACodeType.PSE = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PSE')
IAEACodeType.PGF = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PGF')
IAEACodeType.PTF = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'PTF')
IAEACodeType.HGN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HGN')
IAEACodeType.HAS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HAS')
IAEACodeType.HLB = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HLB')
IAEACodeType.HDS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HDS')
IAEACodeType.HDX = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HDX')
IAEACodeType.HES = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HES')
IAEACodeType.HCX = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HCX')
IAEACodeType.HUP = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HUP')
IAEACodeType.HAS_ = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HAS')
IAEACodeType.HIR = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HIR')
IAEACodeType.HEL = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HEL')
IAEACodeType.HET = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HET')
IAEACodeType.HIP = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HIP')
IAEACodeType.HRC = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HRC')
IAEACodeType.HTS = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HTS')
IAEACodeType.HDT = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HDT')
IAEACodeType.HFL = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HFL')
IAEACodeType.HEX = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HEX')
IAEACodeType.HIN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HIN')
IAEACodeType.HPN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HPN')
IAEACodeType.HST = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HST')
IAEACodeType.HAT = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HAT')
IAEACodeType.HAI = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HAI')
IAEACodeType.HDI = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HDI')
IAEACodeType.HDC = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HDC')
IAEACodeType.HMN = IAEACodeType._CF_enumeration.addEnumeration(unicode_value=u'HMN')
IAEACodeType._InitializeFacetMap(IAEACodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'IAEACodeType', IAEACodeType)

# Atomic SimpleTypeDefinition
class ReferenceFrameType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReferenceFrameType')
    _Documentation = None
ReferenceFrameType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ReferenceFrameType, enum_prefix=None)
ReferenceFrameType.CenterOfMass = ReferenceFrameType._CF_enumeration.addEnumeration(unicode_value=u'CenterOfMass')
ReferenceFrameType.LaboratoryFrame = ReferenceFrameType._CF_enumeration.addEnumeration(unicode_value=u'LaboratoryFrame')
ReferenceFrameType.TargetFrame = ReferenceFrameType._CF_enumeration.addEnumeration(unicode_value=u'TargetFrame')
ReferenceFrameType._InitializeFacetMap(ReferenceFrameType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ReferenceFrameType', ReferenceFrameType)

# Atomic SimpleTypeDefinition
class STD_ANON_4 (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.undef = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'undef')
STD_ANON_4.eVamu = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'eV/amu')
STD_ANON_4.keVamu = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'keV/amu')
STD_ANON_4.MeVamu = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'MeV/amu')
STD_ANON_4.eV = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'eV')
STD_ANON_4.keV = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'keV')
STD_ANON_4.MeV = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'MeV')
STD_ANON_4.au = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'au')
STD_ANON_4.n1cm = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'1/cm')
STD_ANON_4.J = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'J')
STD_ANON_4.Ry = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Ry')
STD_ANON_4.unitless = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'unitless')
STD_ANON_4.kJmol = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'kJ/mol')
STD_ANON_4.kcalmol = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'kcal/mol')
STD_ANON_4.K = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'K')
STD_ANON_4.Hz = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Hz')
STD_ANON_4.kHz = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'kHz')
STD_ANON_4.MHz = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'MHz')
STD_ANON_4.m = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'm')
STD_ANON_4.cm = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'cm')
STD_ANON_4.A = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'A')
STD_ANON_4.nm = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'nm')
STD_ANON_4.deg = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'deg')
STD_ANON_4.rad = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'rad')
STD_ANON_4.srad = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'srad')
STD_ANON_4.s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u's')
STD_ANON_4.m3s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'm3/s')
STD_ANON_4.cm3s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'cm3/s')
STD_ANON_4.cm6s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'cm6/s')
STD_ANON_4.m2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'm2')
STD_ANON_4.cm2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'cm2')
STD_ANON_4.b = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'b')
STD_ANON_4.Mb = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'Mb')
STD_ANON_4.n1s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'1/s')
STD_ANON_4.C_m = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'C.m')
STD_ANON_4.JT = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'J/T')
STD_ANON_4.C_m2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'C.m2')
STD_ANON_4.ms = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'm/s')
STD_ANON_4.cms = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'cm/s')
STD_ANON_4.C = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'C')
STD_ANON_4.electron = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'electron')
STD_ANON_4.g = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'g')
STD_ANON_4.amu = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'amu')
STD_ANON_4.kg = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'kg')
STD_ANON_4.n1m2s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'1/m2/s')
STD_ANON_4.n1cm2s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'1/cm2/s')
STD_ANON_4.Jm2s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'J/m2/s')
STD_ANON_4.Jcm2s = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'J/cm2/s')
STD_ANON_4.n1m2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'1/m2')
STD_ANON_4.n1cm2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'1/cm2')
STD_ANON_4.Jm2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'J/m2')
STD_ANON_4.Jcm2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'J/cm2')
STD_ANON_4.Wm2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'W/m2')
STD_ANON_4.Wcm2 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'W/cm2')
STD_ANON_4.W = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value=u'W')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)

# Atomic SimpleTypeDefinition
class AngularMomentumType (pyxb.binding.datatypes.decimal):

    """non-negative integer or half-integer number (e.g., 2.5)."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AngularMomentumType')
    _Documentation = u'non-negative integer or half-integer number (e.g., 2.5).'
AngularMomentumType._CF_pattern = pyxb.binding.facets.CF_pattern()
AngularMomentumType._CF_pattern.addPattern(pattern=u'\\d+(\\.(0|5)?)?')
AngularMomentumType._InitializeFacetMap(AngularMomentumType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'AngularMomentumType', AngularMomentumType)

# Atomic SimpleTypeDefinition
class ModesListType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ModesListType')
    _Documentation = None
ModesListType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ModesListType, enum_prefix=None)
ModesListType.normalMode = ModesListType._CF_enumeration.addEnumeration(unicode_value=u'normalMode')
ModesListType.stretchingMode = ModesListType._CF_enumeration.addEnumeration(unicode_value=u'stretchingMode')
ModesListType.bendingMode = ModesListType._CF_enumeration.addEnumeration(unicode_value=u'bendingMode')
ModesListType.torsionalMode = ModesListType._CF_enumeration.addEnumeration(unicode_value=u'torsionalMode')
ModesListType.localMode = ModesListType._CF_enumeration.addEnumeration(unicode_value=u'localMode')
ModesListType.inversionMode = ModesListType._CF_enumeration.addEnumeration(unicode_value=u'inversionMode')
ModesListType._InitializeFacetMap(ModesListType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ModesListType', ModesListType)

# Atomic SimpleTypeDefinition
class PrincipalQuantumNumberType (pyxb.binding.datatypes.positiveInteger):

    """Principal quantum number (positive integer)"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PrincipalQuantumNumberType')
    _Documentation = u'Principal quantum number (positive integer)'
PrincipalQuantumNumberType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'PrincipalQuantumNumberType', PrincipalQuantumNumberType)

# Atomic SimpleTypeDefinition
class EfSymmetryType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'EfSymmetryType')
    _Documentation = None
EfSymmetryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=EfSymmetryType, enum_prefix=None)
EfSymmetryType.e = EfSymmetryType._CF_enumeration.addEnumeration(unicode_value=u'e')
EfSymmetryType.f = EfSymmetryType._CF_enumeration.addEnumeration(unicode_value=u'f')
EfSymmetryType._InitializeFacetMap(EfSymmetryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'EfSymmetryType', EfSymmetryType)

# Atomic SimpleTypeDefinition
class ParityType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ParityType')
    _Documentation = None
ParityType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ParityType, enum_prefix=None)
ParityType.even = ParityType._CF_enumeration.addEnumeration(unicode_value=u'even')
ParityType.odd = ParityType._CF_enumeration.addEnumeration(unicode_value=u'odd')
ParityType.undefined = ParityType._CF_enumeration.addEnumeration(unicode_value=u'undefined')
ParityType._InitializeFacetMap(ParityType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ParityType', ParityType)

# Atomic SimpleTypeDefinition
class MethodCategoryType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MethodCategoryType')
    _Documentation = None
MethodCategoryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=MethodCategoryType, enum_prefix=None)
MethodCategoryType.experiment = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'experiment')
MethodCategoryType.theory = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'theory')
MethodCategoryType.recommended = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'recommended')
MethodCategoryType.evaluated = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'evaluated')
MethodCategoryType.empirical = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'empirical')
MethodCategoryType.scalingLaw = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'scalingLaw')
MethodCategoryType.semiempirical = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'semiempirical')
MethodCategoryType.compilation = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'compilation')
MethodCategoryType.derived = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'derived')
MethodCategoryType.observed = MethodCategoryType._CF_enumeration.addEnumeration(unicode_value=u'observed')
MethodCategoryType._InitializeFacetMap(MethodCategoryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'MethodCategoryType', MethodCategoryType)

# Atomic SimpleTypeDefinition
class ParticleNameType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ParticleNameType')
    _Documentation = None
ParticleNameType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ParticleNameType, enum_prefix=None)
ParticleNameType.photon = ParticleNameType._CF_enumeration.addEnumeration(unicode_value=u'photon')
ParticleNameType.electron = ParticleNameType._CF_enumeration.addEnumeration(unicode_value=u'electron')
ParticleNameType.muon = ParticleNameType._CF_enumeration.addEnumeration(unicode_value=u'muon')
ParticleNameType.positron = ParticleNameType._CF_enumeration.addEnumeration(unicode_value=u'positron')
ParticleNameType._InitializeFacetMap(ParticleNameType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ParticleNameType', ParticleNameType)

# Atomic SimpleTypeDefinition
class PermutationSymmetryType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PermutationSymmetryType')
    _Documentation = None
PermutationSymmetryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=PermutationSymmetryType, enum_prefix=None)
PermutationSymmetryType.a = PermutationSymmetryType._CF_enumeration.addEnumeration(unicode_value=u'a')
PermutationSymmetryType.s = PermutationSymmetryType._CF_enumeration.addEnumeration(unicode_value=u's')
PermutationSymmetryType._InitializeFacetMap(PermutationSymmetryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'PermutationSymmetryType', PermutationSymmetryType)

# Atomic SimpleTypeDefinition
class CodeType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CodeType')
    _Documentation = None
CodeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=CodeType, enum_prefix=None)
CodeType.phem = CodeType._CF_enumeration.addEnumeration(unicode_value=u'phem')
CodeType.phab = CodeType._CF_enumeration.addEnumeration(unicode_value=u'phab')
CodeType.phsc = CodeType._CF_enumeration.addEnumeration(unicode_value=u'phsc')
CodeType.elas = CodeType._CF_enumeration.addEnumeration(unicode_value=u'elas')
CodeType.inel = CodeType._CF_enumeration.addEnumeration(unicode_value=u'inel')
CodeType.exci = CodeType._CF_enumeration.addEnumeration(unicode_value=u'exci')
CodeType.dexc = CodeType._CF_enumeration.addEnumeration(unicode_value=u'dexc')
CodeType.ioni = CodeType._CF_enumeration.addEnumeration(unicode_value=u'ioni')
CodeType.tran = CodeType._CF_enumeration.addEnumeration(unicode_value=u'tran')
CodeType.exch = CodeType._CF_enumeration.addEnumeration(unicode_value=u'exch')
CodeType.reco = CodeType._CF_enumeration.addEnumeration(unicode_value=u'reco')
CodeType.elat = CodeType._CF_enumeration.addEnumeration(unicode_value=u'elat')
CodeType.eldt = CodeType._CF_enumeration.addEnumeration(unicode_value=u'eldt')
CodeType.asso = CodeType._CF_enumeration.addEnumeration(unicode_value=u'asso')
CodeType.diss = CodeType._CF_enumeration.addEnumeration(unicode_value=u'diss')
CodeType.intr = CodeType._CF_enumeration.addEnumeration(unicode_value=u'intr')
CodeType.chem = CodeType._CF_enumeration.addEnumeration(unicode_value=u'chem')
CodeType.sure = CodeType._CF_enumeration.addEnumeration(unicode_value=u'sure')
CodeType.suem = CodeType._CF_enumeration.addEnumeration(unicode_value=u'suem')
CodeType.sudp = CodeType._CF_enumeration.addEnumeration(unicode_value=u'sudp')
CodeType.such = CodeType._CF_enumeration.addEnumeration(unicode_value=u'such')
CodeType.sope = CodeType._CF_enumeration.addEnumeration(unicode_value=u'sope')
CodeType.emptyString = CodeType._CF_enumeration.addEnumeration(unicode_value=u'')
CodeType._InitializeFacetMap(CodeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'CodeType', CodeType)

# Atomic SimpleTypeDefinition
class STD_ANON_5 (pyxb.binding.datatypes.ID):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_5._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_5._CF_pattern.addPattern(pattern=u'M.+')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_pattern)

# Atomic SimpleTypeDefinition
class STD_ANON_6 (pyxb.binding.datatypes.IDREF):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_6._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_6._CF_pattern.addPattern(pattern=u'F.+')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_pattern)

# Atomic SimpleTypeDefinition
class MixingClassType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MixingClassType')
    _Documentation = None
MixingClassType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=MixingClassType, enum_prefix=None)
MixingClassType.squared = MixingClassType._CF_enumeration.addEnumeration(unicode_value=u'squared')
MixingClassType.signed = MixingClassType._CF_enumeration.addEnumeration(unicode_value=u'signed')
MixingClassType._InitializeFacetMap(MixingClassType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'MixingClassType', MixingClassType)

# Atomic SimpleTypeDefinition
class C2SymmetryType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'C2SymmetryType')
    _Documentation = None
C2SymmetryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=C2SymmetryType, enum_prefix=None)
C2SymmetryType.emptyString = C2SymmetryType._CF_enumeration.addEnumeration(unicode_value=u'+')
C2SymmetryType.emptyString_ = C2SymmetryType._CF_enumeration.addEnumeration(unicode_value=u'-')
C2SymmetryType._InitializeFacetMap(C2SymmetryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'C2SymmetryType', C2SymmetryType)

# Atomic SimpleTypeDefinition
class MultipoleType (pyxb.binding.datatypes.string):

    """Radiative transition multipole"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MultipoleType')
    _Documentation = u'Radiative transition multipole'
MultipoleType._CF_pattern = pyxb.binding.facets.CF_pattern()
MultipoleType._CF_pattern.addPattern(pattern=u'(E|M)(1-9)\\d*')
MultipoleType._InitializeFacetMap(MultipoleType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'MultipoleType', MultipoleType)

# Atomic SimpleTypeDefinition
class CouplingListType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CouplingListType')
    _Documentation = None
CouplingListType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=CouplingListType, enum_prefix=None)
CouplingListType.bBetaOther = CouplingListType._CF_enumeration.addEnumeration(unicode_value=u'bBetaOther')
CouplingListType.bBetaJ = CouplingListType._CF_enumeration.addEnumeration(unicode_value=u'bBetaJ')
CouplingListType.bBetaS = CouplingListType._CF_enumeration.addEnumeration(unicode_value=u'bBetaS')
CouplingListType.bBetaN = CouplingListType._CF_enumeration.addEnumeration(unicode_value=u'bBetaN')
CouplingListType._InitializeFacetMap(CouplingListType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'CouplingListType', CouplingListType)

# Atomic SimpleTypeDefinition
class AngularMomentumProjectionType (pyxb.binding.datatypes.decimal):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AngularMomentumProjectionType')
    _Documentation = None
AngularMomentumProjectionType._CF_pattern = pyxb.binding.facets.CF_pattern()
AngularMomentumProjectionType._CF_pattern.addPattern(pattern=u'(\\+|-)?\\d+(\\.(0|5)?)?')
AngularMomentumProjectionType._InitializeFacetMap(AngularMomentumProjectionType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'AngularMomentumProjectionType', AngularMomentumProjectionType)

# Atomic SimpleTypeDefinition
class CategoryType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CategoryType')
    _Documentation = None
CategoryType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=CategoryType, enum_prefix=None)
CategoryType.book = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'book')
CategoryType.database = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'database')
CategoryType.journal = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'journal')
CategoryType.preprint = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'preprint')
CategoryType.private_communication = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'private communication')
CategoryType.proceedings = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'proceedings')
CategoryType.report = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'report')
CategoryType.theses = CategoryType._CF_enumeration.addEnumeration(unicode_value=u'theses')
CategoryType._InitializeFacetMap(CategoryType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'CategoryType', CategoryType)

# Atomic SimpleTypeDefinition
class STD_ANON_7 (pyxb.binding.datatypes.ID):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_7._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_7._CF_pattern.addPattern(pattern=u'F.+')
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_pattern)

# Atomic SimpleTypeDefinition
class STD_ANON_8 (pyxb.binding.datatypes.ID):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_8._CF_pattern = pyxb.binding.facets.CF_pattern()
STD_ANON_8._CF_pattern.addPattern(pattern=u'B.+')
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_pattern)

# Atomic SimpleTypeDefinition
class DataDescriptionType (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """Descriptor for the type of collisonal parameter"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataDescriptionType')
    _Documentation = u'Descriptor for the type of collisonal parameter'
DataDescriptionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=DataDescriptionType, enum_prefix=None)
DataDescriptionType.crossSection = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'crossSection')
DataDescriptionType.collisionStrength = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'collisionStrength')
DataDescriptionType.rateCoefficient = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'rateCoefficient')
DataDescriptionType.probability = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'probability')
DataDescriptionType.effectiveCollisionStrength = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'effectiveCollisionStrength')
DataDescriptionType.sputteringYield = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'sputteringYield')
DataDescriptionType.sputteredEnergyCoefficient = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'sputteredEnergyCoefficient')
DataDescriptionType.particleReflectionCoefficient = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'particleReflectionCoefficient')
DataDescriptionType.energyReflectionCoefficient = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'energyReflectionCoefficient')
DataDescriptionType.meanPenetrationDepth = DataDescriptionType._CF_enumeration.addEnumeration(unicode_value=u'meanPenetrationDepth')
DataDescriptionType._InitializeFacetMap(DataDescriptionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'DataDescriptionType', DataDescriptionType)

# Complex type PrimaryType with content type ELEMENT_ONLY
class PrimaryType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PrimaryType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_PrimaryType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, u'Arbitrary comments')

    
    # Attribute sourceRef uses Python identifier sourceRef
    __sourceRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'sourceRef'), 'sourceRef', '__AbsentNamespace0_PrimaryType_sourceRef', STD_ANON_1)
    
    sourceRef = property(__sourceRef.value, __sourceRef.set, None, u'Reference to specific bibliographic items.')

    
    # Attribute methodRef uses Python identifier methodRef
    __methodRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'methodRef'), 'methodRef', '__AbsentNamespace0_PrimaryType_methodRef', STD_ANON_2)
    
    methodRef = property(__methodRef.value, __methodRef.set, None, u'Reference to a specific method.')


    _ElementMap = {
        __Comments.name() : __Comments
    }
    _AttributeMap = {
        __sourceRef.name() : __sourceRef,
        __methodRef.name() : __methodRef
    }
Namespace.addCategoryObject('typeBinding', u'PrimaryType', PrimaryType)


# Complex type AtomicNumericalDataType with content type ELEMENT_ONLY
class AtomicNumericalDataType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomicNumericalDataType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element QuantumDefect uses Python identifier QuantumDefect
    __QuantumDefect = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'QuantumDefect'), 'QuantumDefect', '__AbsentNamespace0_AtomicNumericalDataType_QuantumDefect', False)

    
    QuantumDefect = property(__QuantumDefect.value, __QuantumDefect.set, None, u'Quantum defect')

    
    # Element LandeFactor uses Python identifier LandeFactor
    __LandeFactor = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LandeFactor'), 'LandeFactor', '__AbsentNamespace0_AtomicNumericalDataType_LandeFactor', False)

    
    LandeFactor = property(__LandeFactor.value, __LandeFactor.set, None, u'Lande factor')

    
    # Element TotalLifeTime uses Python identifier TotalLifeTime
    __TotalLifeTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'), 'TotalLifeTime', '__AbsentNamespace0_AtomicNumericalDataType_TotalLifeTime', False)

    
    TotalLifeTime = property(__TotalLifeTime.value, __TotalLifeTime.set, None, u'State lifetime')

    
    # Element Polarizability uses Python identifier Polarizability
    __Polarizability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Polarizability'), 'Polarizability', '__AbsentNamespace0_AtomicNumericalDataType_Polarizability', False)

    
    Polarizability = property(__Polarizability.value, __Polarizability.set, None, u'State polarizability')

    
    # Element StatisticalWeight uses Python identifier StatisticalWeight
    __StatisticalWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'), 'StatisticalWeight', '__AbsentNamespace0_AtomicNumericalDataType_StatisticalWeight', False)

    
    StatisticalWeight = property(__StatisticalWeight.value, __StatisticalWeight.set, None, u'Statistical weight. May be non-integer due to plasma environment effects.')

    
    # Element IonizationEnergy uses Python identifier IonizationEnergy
    __IonizationEnergy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IonizationEnergy'), 'IonizationEnergy', '__AbsentNamespace0_AtomicNumericalDataType_IonizationEnergy', False)

    
    IonizationEnergy = property(__IonizationEnergy.value, __IonizationEnergy.set, None, u'Energy required to remove an electron')

    
    # Element StateEnergy uses Python identifier StateEnergy
    __StateEnergy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StateEnergy'), 'StateEnergy', '__AbsentNamespace0_AtomicNumericalDataType_StateEnergy', False)

    
    StateEnergy = property(__StateEnergy.value, __StateEnergy.set, None, u'Energy from the ground state')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __QuantumDefect.name() : __QuantumDefect,
        __LandeFactor.name() : __LandeFactor,
        __TotalLifeTime.name() : __TotalLifeTime,
        __Polarizability.name() : __Polarizability,
        __StatisticalWeight.name() : __StatisticalWeight,
        __IonizationEnergy.name() : __IonizationEnergy,
        __StateEnergy.name() : __StateEnergy
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AtomicNumericalDataType', AtomicNumericalDataType)


# Complex type MagneticQuantumNumberType with content type ELEMENT_ONLY
class MagneticQuantumNumberType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MagneticQuantumNumberType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comment'), 'Comment', '__AbsentNamespace0_MagneticQuantumNumberType_Comment', False)

    
    Comment = property(__Comment.value, __Comment.set, None, None)

    
    # Element Label uses Python identifier Label
    __Label = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Label'), 'Label', '__AbsentNamespace0_MagneticQuantumNumberType_Label', False)

    
    Label = property(__Label.value, __Label.set, None, None)

    
    # Element Value uses Python identifier Value
    __Value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Value'), 'Value', '__AbsentNamespace0_MagneticQuantumNumberType_Value', False)

    
    Value = property(__Value.value, __Value.set, None, None)

    
    # Attribute quantumNumberID uses Python identifier quantumNumberID
    __quantumNumberID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quantumNumberID'), 'quantumNumberID', '__AbsentNamespace0_MagneticQuantumNumberType_quantumNumberID', pyxb.binding.datatypes.ID)
    
    quantumNumberID = property(__quantumNumberID.value, __quantumNumberID.set, None, None)


    _ElementMap = {
        __Comment.name() : __Comment,
        __Label.name() : __Label,
        __Value.name() : __Value
    }
    _AttributeMap = {
        __quantumNumberID.name() : __quantumNumberID
    }
Namespace.addCategoryObject('typeBinding', u'MagneticQuantumNumberType', MagneticQuantumNumberType)


# Complex type MolecularStateType with content type ELEMENT_ONLY
class MolecularStateType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MolecularStateType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element ElectronicHome uses Python identifier ElectronicHome
    __ElectronicHome = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ElectronicHome'), 'ElectronicHome', '__AbsentNamespace0_MolecularStateType_ElectronicHome', False)

    
    ElectronicHome = property(__ElectronicHome.value, __ElectronicHome.set, None, None)

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_MolecularStateType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, None)

    
    # Element MolecularStateCharacterisation uses Python identifier MolecularStateCharacterisation
    __MolecularStateCharacterisation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MolecularStateCharacterisation'), 'MolecularStateCharacterisation', '__AbsentNamespace0_MolecularStateType_MolecularStateCharacterisation', False)

    
    MolecularStateCharacterisation = property(__MolecularStateCharacterisation.value, __MolecularStateCharacterisation.set, None, None)

    
    # Element TotalSpinMomentumS uses Python identifier TotalSpinMomentumS
    __TotalSpinMomentumS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalSpinMomentumS'), 'TotalSpinMomentumS', '__AbsentNamespace0_MolecularStateType_TotalSpinMomentumS', False)

    
    TotalSpinMomentumS = property(__TotalSpinMomentumS.value, __TotalSpinMomentumS.set, None, None)

    
    # Element TotalMagneticQuantumNumberS uses Python identifier TotalMagneticQuantumNumberS
    __TotalMagneticQuantumNumberS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberS'), 'TotalMagneticQuantumNumberS', '__AbsentNamespace0_MolecularStateType_TotalMagneticQuantumNumberS', False)

    
    TotalMagneticQuantumNumberS = property(__TotalMagneticQuantumNumberS.value, __TotalMagneticQuantumNumberS.set, None, None)

    
    # Element Parity uses Python identifier Parity
    __Parity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parity'), 'Parity', '__AbsentNamespace0_MolecularStateType_Parity', False)

    
    Parity = property(__Parity.value, __Parity.set, None, None)

    
    # Element Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comment'), 'Comment', '__AbsentNamespace0_MolecularStateType_Comment', False)

    
    Comment = property(__Comment.value, __Comment.set, None, None)

    
    # Attribute stateID uses Python identifier stateID
    __stateID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'stateID'), 'stateID', '__AbsentNamespace0_MolecularStateType_stateID', STD_ANON_3)
    
    stateID = property(__stateID.value, __stateID.set, None, u'ID for a specific state/particle.')

    
    # Attribute methodRef inherited from PrimaryType
    
    # Attribute sourceRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __ElectronicHome.name() : __ElectronicHome,
        __Description.name() : __Description,
        __MolecularStateCharacterisation.name() : __MolecularStateCharacterisation,
        __TotalSpinMomentumS.name() : __TotalSpinMomentumS,
        __TotalMagneticQuantumNumberS.name() : __TotalMagneticQuantumNumberS,
        __Parity.name() : __Parity,
        __Comment.name() : __Comment
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        __stateID.name() : __stateID
    })
Namespace.addCategoryObject('typeBinding', u'MolecularStateType', MolecularStateType)


# Complex type CollisionalProcessClassType with content type ELEMENT_ONLY
class CollisionalProcessClassType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CollisionalProcessClassType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element UserDefinition uses Python identifier UserDefinition
    __UserDefinition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'UserDefinition'), 'UserDefinition', '__AbsentNamespace0_CollisionalProcessClassType_UserDefinition', False)

    
    UserDefinition = property(__UserDefinition.value, __UserDefinition.set, None, u'Description of the process')

    
    # Element Code uses Python identifier Code
    __Code = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Code'), 'Code', '__AbsentNamespace0_CollisionalProcessClassType_Code', True)

    
    Code = property(__Code.value, __Code.set, None, u'A 4-letter code describing various processes')

    
    # Element IAEACode uses Python identifier IAEACode
    __IAEACode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IAEACode'), 'IAEACode', '__AbsentNamespace0_CollisionalProcessClassType_IAEACode', False)

    
    IAEACode = property(__IAEACode.value, __IAEACode.set, None, u'From the "IAEA Classification of Processes", October 2003')


    _ElementMap = {
        __UserDefinition.name() : __UserDefinition,
        __Code.name() : __Code,
        __IAEACode.name() : __IAEACode
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'CollisionalProcessClassType', CollisionalProcessClassType)


# Complex type StatesType with content type ELEMENT_ONLY
class StatesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StatesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Atoms uses Python identifier Atoms
    __Atoms = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Atoms'), 'Atoms', '__AbsentNamespace0_StatesType_Atoms', False)

    
    Atoms = property(__Atoms.value, __Atoms.set, None, u'List of atoms')

    
    # Element Particles uses Python identifier Particles
    __Particles = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Particles'), 'Particles', '__AbsentNamespace0_StatesType_Particles', False)

    
    Particles = property(__Particles.value, __Particles.set, None, u'List of elementary particles (electron, photon, etc.)')

    
    # Element Solids uses Python identifier Solids
    __Solids = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Solids'), 'Solids', '__AbsentNamespace0_StatesType_Solids', False)

    
    Solids = property(__Solids.value, __Solids.set, None, u'List of solids and surfaces')

    
    # Element Molecules uses Python identifier Molecules
    __Molecules = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Molecules'), 'Molecules', '__AbsentNamespace0_StatesType_Molecules', False)

    
    Molecules = property(__Molecules.value, __Molecules.set, None, u'List of molecules')


    _ElementMap = {
        __Atoms.name() : __Atoms,
        __Particles.name() : __Particles,
        __Solids.name() : __Solids,
        __Molecules.name() : __Molecules
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'StatesType', StatesType)


# Complex type ExpressionType with content type SIMPLE
class ExpressionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ExpressionType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute computerLanguage uses Python identifier computerLanguage
    __computerLanguage = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'computerLanguage'), 'computerLanguage', '__AbsentNamespace0_ExpressionType_computerLanguage', pyxb.binding.datatypes.string, required=True)
    
    computerLanguage = property(__computerLanguage.value, __computerLanguage.set, None, u'Programming language for the function expression. Example: Fortran2003.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __computerLanguage.name() : __computerLanguage
    }
Namespace.addCategoryObject('typeBinding', u'ExpressionType', ExpressionType)


# Complex type NonRadiativeTransitionType with content type ELEMENT_ONLY
class NonRadiativeTransitionType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonRadiativeTransitionType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Probability uses Python identifier Probability
    __Probability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Probability'), 'Probability', '__AbsentNamespace0_NonRadiativeTransitionType_Probability', False)

    
    Probability = property(__Probability.value, __Probability.set, None, u'Transition probability')

    
    # Element FinalStateRef uses Python identifier FinalStateRef
    __FinalStateRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FinalStateRef'), 'FinalStateRef', '__AbsentNamespace0_NonRadiativeTransitionType_FinalStateRef', False)

    
    FinalStateRef = property(__FinalStateRef.value, __FinalStateRef.set, None, u'Reference to the final state')

    
    # Element Type uses Python identifier Type
    __Type = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Type'), 'Type', '__AbsentNamespace0_NonRadiativeTransitionType_Type', False)

    
    Type = property(__Type.value, __Type.set, None, u'Description of the transition (e.g., Coster-Kronig)')

    
    # Element TransitionEnergy uses Python identifier TransitionEnergy
    __TransitionEnergy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TransitionEnergy'), 'TransitionEnergy', '__AbsentNamespace0_NonRadiativeTransitionType_TransitionEnergy', False)

    
    TransitionEnergy = property(__TransitionEnergy.value, __TransitionEnergy.set, None, u'Transition energy')

    
    # Element NonRadiativeWidth uses Python identifier NonRadiativeWidth
    __NonRadiativeWidth = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NonRadiativeWidth'), 'NonRadiativeWidth', '__AbsentNamespace0_NonRadiativeTransitionType_NonRadiativeWidth', False)

    
    NonRadiativeWidth = property(__NonRadiativeWidth.value, __NonRadiativeWidth.set, None, u'NonRadiative width ')

    
    # Element InitialStateRef uses Python identifier InitialStateRef
    __InitialStateRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'InitialStateRef'), 'InitialStateRef', '__AbsentNamespace0_NonRadiativeTransitionType_InitialStateRef', False)

    
    InitialStateRef = property(__InitialStateRef.value, __InitialStateRef.set, None, u'Reference to the initial state')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Probability.name() : __Probability,
        __FinalStateRef.name() : __FinalStateRef,
        __Type.name() : __Type,
        __TransitionEnergy.name() : __TransitionEnergy,
        __NonRadiativeWidth.name() : __NonRadiativeWidth,
        __InitialStateRef.name() : __InitialStateRef
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NonRadiativeTransitionType', NonRadiativeTransitionType)


# Complex type ShellPairType with content type ELEMENT_ONLY
class ShellPairType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ShellPairType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ShellPairTerm uses Python identifier ShellPairTerm
    __ShellPairTerm = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ShellPairTerm'), 'ShellPairTerm', '__AbsentNamespace0_ShellPairType_ShellPairTerm', False)

    
    ShellPairTerm = property(__ShellPairTerm.value, __ShellPairTerm.set, None, None)

    
    # Element Shell1 uses Python identifier Shell1
    __Shell1 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Shell1'), 'Shell1', '__AbsentNamespace0_ShellPairType_Shell1', False)

    
    Shell1 = property(__Shell1.value, __Shell1.set, None, None)

    
    # Element Shell2 uses Python identifier Shell2
    __Shell2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Shell2'), 'Shell2', '__AbsentNamespace0_ShellPairType_Shell2', False)

    
    Shell2 = property(__Shell2.value, __Shell2.set, None, None)

    
    # Attribute shellPairID uses Python identifier shellPairID
    __shellPairID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'shellPairID'), 'shellPairID', '__AbsentNamespace0_ShellPairType_shellPairID', pyxb.binding.datatypes.ID, required=True)
    
    shellPairID = property(__shellPairID.value, __shellPairID.set, None, u'Identifier of the shell pair')


    _ElementMap = {
        __ShellPairTerm.name() : __ShellPairTerm,
        __Shell1.name() : __Shell1,
        __Shell2.name() : __Shell2
    }
    _AttributeMap = {
        __shellPairID.name() : __shellPairID
    }
Namespace.addCategoryObject('typeBinding', u'ShellPairType', ShellPairType)


# Complex type HundCaseBType with content type ELEMENT_ONLY
class HundCaseBType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HundCaseBType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TotalMagneticQuantumNumberJ uses Python identifier TotalMagneticQuantumNumberJ
    __TotalMagneticQuantumNumberJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'), 'TotalMagneticQuantumNumberJ', '__AbsentNamespace0_HundCaseBType_TotalMagneticQuantumNumberJ', False)

    
    TotalMagneticQuantumNumberJ = property(__TotalMagneticQuantumNumberJ.value, __TotalMagneticQuantumNumberJ.set, None, None)

    
    # Element TotalAngularMomentumN uses Python identifier TotalAngularMomentumN
    __TotalAngularMomentumN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), 'TotalAngularMomentumN', '__AbsentNamespace0_HundCaseBType_TotalAngularMomentumN', False)

    
    TotalAngularMomentumN = property(__TotalAngularMomentumN.value, __TotalAngularMomentumN.set, None, None)

    
    # Element TotalAngularMomentumJ uses Python identifier TotalAngularMomentumJ
    __TotalAngularMomentumJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), 'TotalAngularMomentumJ', '__AbsentNamespace0_HundCaseBType_TotalAngularMomentumJ', False)

    
    TotalAngularMomentumJ = property(__TotalAngularMomentumJ.value, __TotalAngularMomentumJ.set, None, None)


    _ElementMap = {
        __TotalMagneticQuantumNumberJ.name() : __TotalMagneticQuantumNumberJ,
        __TotalAngularMomentumN.name() : __TotalAngularMomentumN,
        __TotalAngularMomentumJ.name() : __TotalAngularMomentumJ
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'HundCaseBType', HundCaseBType)


# Complex type ParticlesType with content type ELEMENT_ONLY
class ParticlesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ParticlesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Particle uses Python identifier Particle
    __Particle = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Particle'), 'Particle', '__AbsentNamespace0_ParticlesType_Particle', True)

    
    Particle = property(__Particle.value, __Particle.set, None, None)


    _ElementMap = {
        __Particle.name() : __Particle
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ParticlesType', ParticlesType)


# Complex type WavelengthWavenumberType with content type ELEMENT_ONLY
class WavelengthWavenumberType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'WavelengthWavenumberType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Experimental uses Python identifier Experimental
    __Experimental = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Experimental'), 'Experimental', '__AbsentNamespace0_WavelengthWavenumberType_Experimental', False)

    
    Experimental = property(__Experimental.value, __Experimental.set, None, u'Experimentally measured')

    
    # Element Ritz uses Python identifier Ritz
    __Ritz = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Ritz'), 'Ritz', '__AbsentNamespace0_WavelengthWavenumberType_Ritz', False)

    
    Ritz = property(__Ritz.value, __Ritz.set, None, u'Calculated from the difference of experimental energy levels')

    
    # Element Theoretical uses Python identifier Theoretical
    __Theoretical = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Theoretical'), 'Theoretical', '__AbsentNamespace0_WavelengthWavenumberType_Theoretical', False)

    
    Theoretical = property(__Theoretical.value, __Theoretical.set, None, u'Calculated (theory)')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Experimental.name() : __Experimental,
        __Ritz.name() : __Ritz,
        __Theoretical.name() : __Theoretical
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'WavelengthWavenumberType', WavelengthWavenumberType)


# Complex type MolecularQuantumNumberType with content type ELEMENT_ONLY
class MolecularQuantumNumberType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MolecularQuantumNumberType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Value uses Python identifier Value
    __Value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Value'), 'Value', '__AbsentNamespace0_MolecularQuantumNumberType_Value', False)

    
    Value = property(__Value.value, __Value.set, None, None)

    
    # Element Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comment'), 'Comment', '__AbsentNamespace0_MolecularQuantumNumberType_Comment', False)

    
    Comment = property(__Comment.value, __Comment.set, None, None)

    
    # Element Label uses Python identifier Label
    __Label = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Label'), 'Label', '__AbsentNamespace0_MolecularQuantumNumberType_Label', False)

    
    Label = property(__Label.value, __Label.set, None, None)

    
    # Attribute quantumNumberID uses Python identifier quantumNumberID
    __quantumNumberID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quantumNumberID'), 'quantumNumberID', '__AbsentNamespace0_MolecularQuantumNumberType_quantumNumberID', pyxb.binding.datatypes.ID)
    
    quantumNumberID = property(__quantumNumberID.value, __quantumNumberID.set, None, None)


    _ElementMap = {
        __Value.name() : __Value,
        __Comment.name() : __Comment,
        __Label.name() : __Label
    }
    _AttributeMap = {
        __quantumNumberID.name() : __quantumNumberID
    }
Namespace.addCategoryObject('typeBinding', u'MolecularQuantumNumberType', MolecularQuantumNumberType)


# Complex type EnergyWavelengthType with content type ELEMENT_ONLY
class EnergyWavelengthType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'EnergyWavelengthType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Energy uses Python identifier Energy
    __Energy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Energy'), 'Energy', '__AbsentNamespace0_EnergyWavelengthType_Energy', False)

    
    Energy = property(__Energy.value, __Energy.set, None, u'Transition energy')

    
    # Element Wavenumber uses Python identifier Wavenumber
    __Wavenumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Wavenumber'), 'Wavenumber', '__AbsentNamespace0_EnergyWavelengthType_Wavenumber', False)

    
    Wavenumber = property(__Wavenumber.value, __Wavenumber.set, None, u'Transition wavenumber')

    
    # Element Wavelength uses Python identifier Wavelength
    __Wavelength = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Wavelength'), 'Wavelength', '__AbsentNamespace0_EnergyWavelengthType_Wavelength', False)

    
    Wavelength = property(__Wavelength.value, __Wavelength.set, None, u'Transition wavelength')

    
    # Element Frequency uses Python identifier Frequency
    __Frequency = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Frequency'), 'Frequency', '__AbsentNamespace0_EnergyWavelengthType_Frequency', False)

    
    Frequency = property(__Frequency.value, __Frequency.set, None, u'Transition frequency')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Energy.name() : __Energy,
        __Wavenumber.name() : __Wavenumber,
        __Wavelength.name() : __Wavelength,
        __Frequency.name() : __Frequency
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'EnergyWavelengthType', EnergyWavelengthType)


# Complex type LinearNoElecHyperFType with content type ELEMENT_ONLY
class LinearNoElecHyperFType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LinearNoElecHyperFType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TotalAngularMomentumN uses Python identifier TotalAngularMomentumN
    __TotalAngularMomentumN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), 'TotalAngularMomentumN', '__AbsentNamespace0_LinearNoElecHyperFType_TotalAngularMomentumN', False)

    
    TotalAngularMomentumN = property(__TotalAngularMomentumN.value, __TotalAngularMomentumN.set, None, None)

    
    # Element HyperfineQuantumNumbers uses Python identifier HyperfineQuantumNumbers
    __HyperfineQuantumNumbers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), 'HyperfineQuantumNumbers', '__AbsentNamespace0_LinearNoElecHyperFType_HyperfineQuantumNumbers', False)

    
    HyperfineQuantumNumbers = property(__HyperfineQuantumNumbers.value, __HyperfineQuantumNumbers.set, None, None)


    _ElementMap = {
        __TotalAngularMomentumN.name() : __TotalAngularMomentumN,
        __HyperfineQuantumNumbers.name() : __HyperfineQuantumNumbers
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LinearNoElecHyperFType', LinearNoElecHyperFType)


# Complex type MethodsType with content type ELEMENT_ONLY
class MethodsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MethodsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Method uses Python identifier Method
    __Method = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Method'), 'Method', '__AbsentNamespace0_MethodsType_Method', True)

    
    Method = property(__Method.value, __Method.set, None, None)


    _ElementMap = {
        __Method.name() : __Method
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MethodsType', MethodsType)


# Complex type TermType with content type ELEMENT_ONLY
class TermType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TermType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element jK uses Python identifier jK
    __jK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'jK'), 'jK', '__AbsentNamespace0_TermType_jK', False)

    
    jK = property(__jK.value, __jK.set, None, u'Term in jK-coupling')

    
    # Element LK uses Python identifier LK
    __LK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LK'), 'LK', '__AbsentNamespace0_TermType_LK', False)

    
    LK = property(__LK.value, __LK.set, None, u'Term in LK-coupling')

    
    # Element TermLabel uses Python identifier TermLabel
    __TermLabel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TermLabel'), 'TermLabel', '__AbsentNamespace0_TermType_TermLabel', False)

    
    TermLabel = property(__TermLabel.value, __TermLabel.set, None, u'Arbitrary term label')

    
    # Element LS uses Python identifier LS
    __LS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LS'), 'LS', '__AbsentNamespace0_TermType_LS', False)

    
    LS = property(__LS.value, __LS.set, None, u'Term in LS-coupling')

    
    # Element jj uses Python identifier jj
    __jj = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'jj'), 'jj', '__AbsentNamespace0_TermType_jj', False)

    
    jj = property(__jj.value, __jj.set, None, u'Term in jj-coupling')

    
    # Element J1J2 uses Python identifier J1J2
    __J1J2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'J1J2'), 'J1J2', '__AbsentNamespace0_TermType_J1J2', False)

    
    J1J2 = property(__J1J2.value, __J1J2.set, None, u'Term in J1J2-coupling')


    _ElementMap = {
        __jK.name() : __jK,
        __LK.name() : __LK,
        __TermLabel.name() : __TermLabel,
        __LS.name() : __LS,
        __jj.name() : __jj,
        __J1J2.name() : __J1J2
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TermType', TermType)


# Complex type SymbolType with content type ELEMENT_ONLY
class SymbolType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SymbolType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element LatexExpression uses Python identifier LatexExpression
    __LatexExpression = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LatexExpression'), 'LatexExpression', '__AbsentNamespace0_SymbolType_LatexExpression', False)

    
    LatexExpression = property(__LatexExpression.value, __LatexExpression.set, None, None)

    
    # Element Symbol uses Python identifier Symbol
    __Symbol = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Symbol'), 'Symbol', '__AbsentNamespace0_SymbolType_Symbol', True)

    
    Symbol = property(__Symbol.value, __Symbol.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __LatexExpression.name() : __LatexExpression,
        __Symbol.name() : __Symbol
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'SymbolType', SymbolType)


# Complex type SourcesType with content type ELEMENT_ONLY
class SourcesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SourcesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Source uses Python identifier Source
    __Source = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Source'), 'Source', '__AbsentNamespace0_SourcesType_Source', True)

    
    Source = property(__Source.value, __Source.set, None, u'A bibliography (bibreference) entry')


    _ElementMap = {
        __Source.name() : __Source
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SourcesType', SourcesType)


# Complex type LSCouplingType with content type ELEMENT_ONLY
class LSCouplingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LSCouplingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Multiplicity uses Python identifier Multiplicity
    __Multiplicity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Multiplicity'), 'Multiplicity', '__AbsentNamespace0_LSCouplingType_Multiplicity', False)

    
    Multiplicity = property(__Multiplicity.value, __Multiplicity.set, None, u'2S+1')

    
    # Element L uses Python identifier L
    __L = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'L'), 'L', '__AbsentNamespace0_LSCouplingType_L', False)

    
    L = property(__L.value, __L.set, None, u'Orbital angular momentum of the term in LS-coupling')

    
    # Element S uses Python identifier S
    __S = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'S'), 'S', '__AbsentNamespace0_LSCouplingType_S', False)

    
    S = property(__S.value, __S.set, None, u'Spin angular momentum of the term in LS-coupling')


    _ElementMap = {
        __Multiplicity.name() : __Multiplicity,
        __L.name() : __L,
        __S.name() : __S
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LSCouplingType', LSCouplingType)


# Complex type MaterialCompositionType with content type ELEMENT_ONLY
class MaterialCompositionType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MaterialCompositionType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Component uses Python identifier Component
    __Component = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Component'), 'Component', '__AbsentNamespace0_MaterialCompositionType_Component', True)

    
    Component = property(__Component.value, __Component.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Component.name() : __Component
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'MaterialCompositionType', MaterialCompositionType)


# Complex type DataTableType with content type ELEMENT_ONLY
class DataTableType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataTableType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PositiveError uses Python identifier PositiveError
    __PositiveError = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PositiveError'), 'PositiveError', '__AbsentNamespace0_DataTableType_PositiveError', False)

    
    PositiveError = property(__PositiveError.value, __PositiveError.set, None, u'Positive error for each data point of the list')

    
    # Element NegativeError uses Python identifier NegativeError
    __NegativeError = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NegativeError'), 'NegativeError', '__AbsentNamespace0_DataTableType_NegativeError', False)

    
    NegativeError = property(__NegativeError.value, __NegativeError.set, None, u'Negative error for each data point of')

    
    # Element DataList uses Python identifier DataList
    __DataList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DataList'), 'DataList', '__AbsentNamespace0_DataTableType_DataList', False)

    
    DataList = property(__DataList.value, __DataList.set, None, u'List of data values. Example: 3 15 33.3 1e3')

    
    # Element Error uses Python identifier Error
    __Error = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Error'), 'Error', '__AbsentNamespace0_DataTableType_Error', False)

    
    Error = property(__Error.value, __Error.set, None, u'Error for each data point of the list')

    
    # Element DataDescription uses Python identifier DataDescription
    __DataDescription = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DataDescription'), 'DataDescription', '__AbsentNamespace0_DataTableType_DataDescription', False)

    
    DataDescription = property(__DataDescription.value, __DataDescription.set, None, u'Additional description of the data list')

    
    # Attribute parameter uses Python identifier parameter
    __parameter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'parameter'), 'parameter', '__AbsentNamespace0_DataTableType_parameter', pyxb.binding.datatypes.string)
    
    parameter = property(__parameter.value, __parameter.set, None, None)

    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'units'), 'units', '__AbsentNamespace0_DataTableType_units', STD_ANON_4, required=True)
    
    units = property(__units.value, __units.set, None, u'Description of physical units. Use "unitless" for dimensionless quantities.')


    _ElementMap = {
        __PositiveError.name() : __PositiveError,
        __NegativeError.name() : __NegativeError,
        __DataList.name() : __DataList,
        __Error.name() : __Error,
        __DataDescription.name() : __DataDescription
    }
    _AttributeMap = {
        __parameter.name() : __parameter,
        __units.name() : __units
    }
Namespace.addCategoryObject('typeBinding', u'DataTableType', DataTableType)


# Complex type PseudoStatisticalWeightType with content type ELEMENT_ONLY
class PseudoStatisticalWeightType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PseudoStatisticalWeightType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Value uses Python identifier Value
    __Value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Value'), 'Value', '__AbsentNamespace0_PseudoStatisticalWeightType_Value', False)

    
    Value = property(__Value.value, __Value.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Value.name() : __Value
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'PseudoStatisticalWeightType', PseudoStatisticalWeightType)


# Complex type ReferencedTextType with content type SIMPLE
class ReferencedTextType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReferencedTextType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute sourceRef uses Python identifier sourceRef
    __sourceRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'sourceRef'), 'sourceRef', '__AbsentNamespace0_ReferencedTextType_sourceRef', STD_ANON_1)
    
    sourceRef = property(__sourceRef.value, __sourceRef.set, None, u'Reference to specific bibliographic items.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __sourceRef.name() : __sourceRef
    }
Namespace.addCategoryObject('typeBinding', u'ReferencedTextType', ReferencedTextType)


# Complex type SuperConfigurationType with content type ELEMENT_ONLY
class SuperConfigurationType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SuperConfigurationType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SuperShell uses Python identifier SuperShell
    __SuperShell = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SuperShell'), 'SuperShell', '__AbsentNamespace0_SuperConfigurationType_SuperShell', True)

    
    SuperShell = property(__SuperShell.value, __SuperShell.set, None, u'List of supershells')


    _ElementMap = {
        __SuperShell.name() : __SuperShell
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SuperConfigurationType', SuperConfigurationType)


# Complex type ComplexMolecularQuantumNumberType with content type ELEMENT_ONLY
class ComplexMolecularQuantumNumberType (MolecularQuantumNumberType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ComplexMolecularQuantumNumberType')
    # Base type is MolecularQuantumNumberType
    
    # Element Value (Value) inherited from MolecularQuantumNumberType
    
    # Element Comment (Comment) inherited from MolecularQuantumNumberType
    
    # Element Label (Label) inherited from MolecularQuantumNumberType
    
    # Attribute modesType uses Python identifier modesType
    __modesType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'modesType'), 'modesType', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_modesType', ModesListType)
    
    modesType = property(__modesType.value, __modesType.set, None, None)

    
    # Attribute nuclearSpinRefs2 uses Python identifier nuclearSpinRefs2
    __nuclearSpinRefs2 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'nuclearSpinRefs2'), 'nuclearSpinRefs2', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_nuclearSpinRefs2', pyxb.binding.datatypes.IDREFS)
    
    nuclearSpinRefs2 = property(__nuclearSpinRefs2.value, __nuclearSpinRefs2.set, None, None)

    
    # Attribute vibrationLNu-i uses Python identifier vibrationLNu_i
    __vibrationLNu_i = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'vibrationLNu-i'), 'vibrationLNu_i', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_vibrationLNu_i', AngularMomentumType)
    
    vibrationLNu_i = property(__vibrationLNu_i.value, __vibrationLNu_i.set, None, None)

    
    # Attribute vibrationSymmetryIndex uses Python identifier vibrationSymmetryIndex
    __vibrationSymmetryIndex = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'vibrationSymmetryIndex'), 'vibrationSymmetryIndex', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_vibrationSymmetryIndex', pyxb.binding.datatypes.integer)
    
    vibrationSymmetryIndex = property(__vibrationSymmetryIndex.value, __vibrationSymmetryIndex.set, None, None)

    
    # Attribute spinSumRef uses Python identifier spinSumRef
    __spinSumRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'spinSumRef'), 'spinSumRef', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_spinSumRef', pyxb.binding.datatypes.IDREF)
    
    spinSumRef = property(__spinSumRef.value, __spinSumRef.set, None, None)

    
    # Attribute vibrationSymmetry uses Python identifier vibrationSymmetry
    __vibrationSymmetry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'vibrationSymmetry'), 'vibrationSymmetry', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_vibrationSymmetry', pyxb.binding.datatypes.string)
    
    vibrationSymmetry = property(__vibrationSymmetry.value, __vibrationSymmetry.set, None, u'check vocabulary in herzberg')

    
    # Attribute nuclearSpinRef uses Python identifier nuclearSpinRef
    __nuclearSpinRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'nuclearSpinRef'), 'nuclearSpinRef', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_nuclearSpinRef', pyxb.binding.datatypes.IDREF)
    
    nuclearSpinRef = property(__nuclearSpinRef.value, __nuclearSpinRef.set, None, None)

    
    # Attribute vibrationInversion uses Python identifier vibrationInversion
    __vibrationInversion = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'vibrationInversion'), 'vibrationInversion', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_vibrationInversion', pyxb.binding.datatypes.string)
    
    vibrationInversion = property(__vibrationInversion.value, __vibrationInversion.set, None, None)

    
    # Attribute quantumNumberID inherited from MolecularQuantumNumberType
    
    # Attribute quantumNumberRef uses Python identifier quantumNumberRef
    __quantumNumberRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'quantumNumberRef'), 'quantumNumberRef', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_quantumNumberRef', pyxb.binding.datatypes.IDREF)
    
    quantumNumberRef = property(__quantumNumberRef.value, __quantumNumberRef.set, None, None)

    
    # Attribute electronicSpinRef uses Python identifier electronicSpinRef
    __electronicSpinRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'electronicSpinRef'), 'electronicSpinRef', '__AbsentNamespace0_ComplexMolecularQuantumNumberType_electronicSpinRef', pyxb.binding.datatypes.IDREF)
    
    electronicSpinRef = property(__electronicSpinRef.value, __electronicSpinRef.set, None, None)


    _ElementMap = MolecularQuantumNumberType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = MolecularQuantumNumberType._AttributeMap.copy()
    _AttributeMap.update({
        __modesType.name() : __modesType,
        __nuclearSpinRefs2.name() : __nuclearSpinRefs2,
        __vibrationLNu_i.name() : __vibrationLNu_i,
        __vibrationSymmetryIndex.name() : __vibrationSymmetryIndex,
        __spinSumRef.name() : __spinSumRef,
        __vibrationSymmetry.name() : __vibrationSymmetry,
        __nuclearSpinRef.name() : __nuclearSpinRef,
        __vibrationInversion.name() : __vibrationInversion,
        __quantumNumberRef.name() : __quantumNumberRef,
        __electronicSpinRef.name() : __electronicSpinRef
    })
Namespace.addCategoryObject('typeBinding', u'ComplexMolecularQuantumNumberType', ComplexMolecularQuantumNumberType)


# Complex type ChemicalElementType with content type ELEMENT_ONLY
class ChemicalElementType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ChemicalElementType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element NuclearCharge uses Python identifier NuclearCharge
    __NuclearCharge = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NuclearCharge'), 'NuclearCharge', '__AbsentNamespace0_ChemicalElementType_NuclearCharge', False)

    
    NuclearCharge = property(__NuclearCharge.value, __NuclearCharge.set, None, u'Nuclear charge in units of electron charge')

    
    # Element ElementSymbol uses Python identifier ElementSymbol
    __ElementSymbol = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ElementSymbol'), 'ElementSymbol', '__AbsentNamespace0_ChemicalElementType_ElementSymbol', False)

    
    ElementSymbol = property(__ElementSymbol.value, __ElementSymbol.set, None, u'Standard symbol of a chemical element (e.g., H or Ta)')


    _ElementMap = {
        __NuclearCharge.name() : __NuclearCharge,
        __ElementSymbol.name() : __ElementSymbol
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ChemicalElementType', ChemicalElementType)


# Complex type DataType with content type ELEMENT_ONLY
class DataType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Value uses Python identifier Value
    __Value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Value'), 'Value', '__AbsentNamespace0_DataType_Value', False)

    
    Value = property(__Value.value, __Value.set, None, u'Value of a particular quantity')

    
    # Element Accuracy uses Python identifier Accuracy
    __Accuracy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Accuracy'), 'Accuracy', '__AbsentNamespace0_DataType_Accuracy', False)

    
    Accuracy = property(__Accuracy.value, __Accuracy.set, None, u'Description of the accuracy')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Value.name() : __Value,
        __Accuracy.name() : __Accuracy
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'DataType', DataType)


# Complex type ShellType with content type ELEMENT_ONLY
class ShellType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ShellType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element NumberOfElectrons uses Python identifier NumberOfElectrons
    __NumberOfElectrons = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NumberOfElectrons'), 'NumberOfElectrons', '__AbsentNamespace0_ShellType_NumberOfElectrons', False)

    
    NumberOfElectrons = property(__NumberOfElectrons.value, __NumberOfElectrons.set, None, u'Number of electrons in the shell')

    
    # Element PrincipalQuantumNumber uses Python identifier PrincipalQuantumNumber
    __PrincipalQuantumNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PrincipalQuantumNumber'), 'PrincipalQuantumNumber', '__AbsentNamespace0_ShellType_PrincipalQuantumNumber', False)

    
    PrincipalQuantumNumber = property(__PrincipalQuantumNumber.value, __PrincipalQuantumNumber.set, None, u'Principal quantum number')

    
    # Element Parity uses Python identifier Parity
    __Parity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parity'), 'Parity', '__AbsentNamespace0_ShellType_Parity', False)

    
    Parity = property(__Parity.value, __Parity.set, None, u'Parity of a shell')

    
    # Element Kappa uses Python identifier Kappa
    __Kappa = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Kappa'), 'Kappa', '__AbsentNamespace0_ShellType_Kappa', False)

    
    Kappa = property(__Kappa.value, __Kappa.set, None, u'Relativistic parameter')

    
    # Element TotalAngularMomentum uses Python identifier TotalAngularMomentum
    __TotalAngularMomentum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'), 'TotalAngularMomentum', '__AbsentNamespace0_ShellType_TotalAngularMomentum', False)

    
    TotalAngularMomentum = property(__TotalAngularMomentum.value, __TotalAngularMomentum.set, None, u'Total angular momentum of the shell')

    
    # Element ShellTerm uses Python identifier ShellTerm
    __ShellTerm = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ShellTerm'), 'ShellTerm', '__AbsentNamespace0_ShellType_ShellTerm', False)

    
    ShellTerm = property(__ShellTerm.value, __ShellTerm.set, None, u'Term of the shell')

    
    # Element OrbitalAngularMomentum uses Python identifier OrbitalAngularMomentum
    __OrbitalAngularMomentum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'OrbitalAngularMomentum'), 'OrbitalAngularMomentum', '__AbsentNamespace0_ShellType_OrbitalAngularMomentum', False)

    
    OrbitalAngularMomentum = property(__OrbitalAngularMomentum.value, __OrbitalAngularMomentum.set, None, None)

    
    # Attribute shellID uses Python identifier shellID
    __shellID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'shellID'), 'shellID', '__AbsentNamespace0_ShellType_shellID', pyxb.binding.datatypes.ID)
    
    shellID = property(__shellID.value, __shellID.set, None, u'Shell identifier')


    _ElementMap = {
        __NumberOfElectrons.name() : __NumberOfElectrons,
        __PrincipalQuantumNumber.name() : __PrincipalQuantumNumber,
        __Parity.name() : __Parity,
        __Kappa.name() : __Kappa,
        __TotalAngularMomentum.name() : __TotalAngularMomentum,
        __ShellTerm.name() : __ShellTerm,
        __OrbitalAngularMomentum.name() : __OrbitalAngularMomentum
    }
    _AttributeMap = {
        __shellID.name() : __shellID
    }
Namespace.addCategoryObject('typeBinding', u'ShellType', ShellType)


# Complex type ProcessesType with content type ELEMENT_ONLY
class ProcessesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ProcessesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Collisions uses Python identifier Collisions
    __Collisions = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Collisions'), 'Collisions', '__AbsentNamespace0_ProcessesType_Collisions', False)

    
    Collisions = property(__Collisions.value, __Collisions.set, None, u'List of transitions due to collisions')

    
    # Element NonRadiative uses Python identifier NonRadiative
    __NonRadiative = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'NonRadiative'), 'NonRadiative', '__AbsentNamespace0_ProcessesType_NonRadiative', False)

    
    NonRadiative = property(__NonRadiative.value, __NonRadiative.set, None, u'List of autoionization and predissociation transitions')

    
    # Element Radiative uses Python identifier Radiative
    __Radiative = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Radiative'), 'Radiative', '__AbsentNamespace0_ProcessesType_Radiative', False)

    
    Radiative = property(__Radiative.value, __Radiative.set, None, u'List of radiative transitions')


    _ElementMap = {
        __Collisions.name() : __Collisions,
        __NonRadiative.name() : __NonRadiative,
        __Radiative.name() : __Radiative
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ProcessesType', ProcessesType)


# Complex type HundCaseAType with content type ELEMENT_ONLY
class HundCaseAType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HundCaseAType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TotalMagneticQuantumNumberJ uses Python identifier TotalMagneticQuantumNumberJ
    __TotalMagneticQuantumNumberJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'), 'TotalMagneticQuantumNumberJ', '__AbsentNamespace0_HundCaseAType_TotalMagneticQuantumNumberJ', False)

    
    TotalMagneticQuantumNumberJ = property(__TotalMagneticQuantumNumberJ.value, __TotalMagneticQuantumNumberJ.set, None, None)

    
    # Element TotalAngularMomentumJ uses Python identifier TotalAngularMomentumJ
    __TotalAngularMomentumJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), 'TotalAngularMomentumJ', '__AbsentNamespace0_HundCaseAType_TotalAngularMomentumJ', False)

    
    TotalAngularMomentumJ = property(__TotalAngularMomentumJ.value, __TotalAngularMomentumJ.set, None, None)

    
    # Element TotalMolecularProjectionJ uses Python identifier TotalMolecularProjectionJ
    __TotalMolecularProjectionJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionJ'), 'TotalMolecularProjectionJ', '__AbsentNamespace0_HundCaseAType_TotalMolecularProjectionJ', False)

    
    TotalMolecularProjectionJ = property(__TotalMolecularProjectionJ.value, __TotalMolecularProjectionJ.set, None, None)


    _ElementMap = {
        __TotalMagneticQuantumNumberJ.name() : __TotalMagneticQuantumNumberJ,
        __TotalAngularMomentumJ.name() : __TotalAngularMomentumJ,
        __TotalMolecularProjectionJ.name() : __TotalMolecularProjectionJ
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'HundCaseAType', HundCaseAType)


# Complex type TabulatedDataType with content type ELEMENT_ONLY
class TabulatedDataType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TabulatedDataType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element ReferenceFrame uses Python identifier ReferenceFrame
    __ReferenceFrame = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ReferenceFrame'), 'ReferenceFrame', '__AbsentNamespace0_TabulatedDataType_ReferenceFrame', False)

    
    ReferenceFrame = property(__ReferenceFrame.value, __ReferenceFrame.set, None, u'Reference frame in which is given the energy, velocity...')

    
    # Element PhysicalUncertainty uses Python identifier PhysicalUncertainty
    __PhysicalUncertainty = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'), 'PhysicalUncertainty', '__AbsentNamespace0_TabulatedDataType_PhysicalUncertainty', False)

    
    PhysicalUncertainty = property(__PhysicalUncertainty.value, __PhysicalUncertainty.set, None, None)

    
    # Element DataXY uses Python identifier DataXY
    __DataXY = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DataXY'), 'DataXY', '__AbsentNamespace0_TabulatedDataType_DataXY', False)

    
    DataXY = property(__DataXY.value, __DataXY.set, None, None)

    
    # Element ProductionDate uses Python identifier ProductionDate
    __ProductionDate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ProductionDate'), 'ProductionDate', '__AbsentNamespace0_TabulatedDataType_ProductionDate', False)

    
    ProductionDate = property(__ProductionDate.value, __ProductionDate.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __ReferenceFrame.name() : __ReferenceFrame,
        __PhysicalUncertainty.name() : __PhysicalUncertainty,
        __DataXY.name() : __DataXY,
        __ProductionDate.name() : __ProductionDate
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TabulatedDataType', TabulatedDataType)


# Complex type SolidsType with content type ELEMENT_ONLY
class SolidsType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SolidsType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Solid uses Python identifier Solid
    __Solid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Solid'), 'Solid', '__AbsentNamespace0_SolidsType_Solid', True)

    
    Solid = property(__Solid.value, __Solid.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Solid.name() : __Solid
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'SolidsType', SolidsType)


# Complex type AsymmetricProjectionType with content type ELEMENT_ONLY
class AsymmetricProjectionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AsymmetricProjectionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element AsymmetricKa uses Python identifier AsymmetricKa
    __AsymmetricKa = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AsymmetricKa'), 'AsymmetricKa', '__AbsentNamespace0_AsymmetricProjectionType_AsymmetricKa', False)

    
    AsymmetricKa = property(__AsymmetricKa.value, __AsymmetricKa.set, None, None)

    
    # Element AsymmetricKc uses Python identifier AsymmetricKc
    __AsymmetricKc = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AsymmetricKc'), 'AsymmetricKc', '__AbsentNamespace0_AsymmetricProjectionType_AsymmetricKc', False)

    
    AsymmetricKc = property(__AsymmetricKc.value, __AsymmetricKc.set, None, None)

    
    # Element AsymmetricTau uses Python identifier AsymmetricTau
    __AsymmetricTau = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AsymmetricTau'), 'AsymmetricTau', '__AbsentNamespace0_AsymmetricProjectionType_AsymmetricTau', False)

    
    AsymmetricTau = property(__AsymmetricTau.value, __AsymmetricTau.set, None, None)


    _ElementMap = {
        __AsymmetricKa.name() : __AsymmetricKa,
        __AsymmetricKc.name() : __AsymmetricKc,
        __AsymmetricTau.name() : __AsymmetricTau
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AsymmetricProjectionType', AsymmetricProjectionType)


# Complex type AtomicQuantumNumbersType with content type ELEMENT_ONLY
class AtomicQuantumNumbersType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomicQuantumNumbersType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element MagneticQuantumNumber uses Python identifier MagneticQuantumNumber
    __MagneticQuantumNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MagneticQuantumNumber'), 'MagneticQuantumNumber', '__AbsentNamespace0_AtomicQuantumNumbersType_MagneticQuantumNumber', False)

    
    MagneticQuantumNumber = property(__MagneticQuantumNumber.value, __MagneticQuantumNumber.set, None, u'Magnetic quantum number. Example: -1')

    
    # Element Parity uses Python identifier Parity
    __Parity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parity'), 'Parity', '__AbsentNamespace0_AtomicQuantumNumbersType_Parity', False)

    
    Parity = property(__Parity.value, __Parity.set, None, u'State parity. Example: odd')

    
    # Element HyperfineMomentum uses Python identifier HyperfineMomentum
    __HyperfineMomentum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineMomentum'), 'HyperfineMomentum', '__AbsentNamespace0_AtomicQuantumNumbersType_HyperfineMomentum', False)

    
    HyperfineMomentum = property(__HyperfineMomentum.value, __HyperfineMomentum.set, None, u'Hyperfine momentum. Example: 2')

    
    # Element TotalAngularMomentum uses Python identifier TotalAngularMomentum
    __TotalAngularMomentum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'), 'TotalAngularMomentum', '__AbsentNamespace0_AtomicQuantumNumbersType_TotalAngularMomentum', False)

    
    TotalAngularMomentum = property(__TotalAngularMomentum.value, __TotalAngularMomentum.set, None, u'Total angular momentum. Example: 2.5')

    
    # Element Kappa uses Python identifier Kappa
    __Kappa = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Kappa'), 'Kappa', '__AbsentNamespace0_AtomicQuantumNumbersType_Kappa', False)

    
    Kappa = property(__Kappa.value, __Kappa.set, None, u'Relativistic parameter kappa')


    _ElementMap = {
        __MagneticQuantumNumber.name() : __MagneticQuantumNumber,
        __Parity.name() : __Parity,
        __HyperfineMomentum.name() : __HyperfineMomentum,
        __TotalAngularMomentum.name() : __TotalAngularMomentum,
        __Kappa.name() : __Kappa
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AtomicQuantumNumbersType', AtomicQuantumNumbersType)


# Complex type ElectronicCharacterisationType with content type ELEMENT_ONLY
class ElectronicCharacterisationType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ElectronicCharacterisationType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Configuration uses Python identifier Configuration
    __Configuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Configuration'), 'Configuration', '__AbsentNamespace0_ElectronicCharacterisationType_Configuration', False)

    
    Configuration = property(__Configuration.value, __Configuration.set, None, None)

    
    # Element SymmetryGroup uses Python identifier SymmetryGroup
    __SymmetryGroup = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SymmetryGroup'), 'SymmetryGroup', '__AbsentNamespace0_ElectronicCharacterisationType_SymmetryGroup', False)

    
    SymmetryGroup = property(__SymmetryGroup.value, __SymmetryGroup.set, None, None)

    
    # Element Conformation uses Python identifier Conformation
    __Conformation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Conformation'), 'Conformation', '__AbsentNamespace0_ElectronicCharacterisationType_Conformation', False)

    
    Conformation = property(__Conformation.value, __Conformation.set, None, None)

    
    # Element TermSymbol uses Python identifier TermSymbol
    __TermSymbol = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TermSymbol'), 'TermSymbol', '__AbsentNamespace0_ElectronicCharacterisationType_TermSymbol', False)

    
    TermSymbol = property(__TermSymbol.value, __TermSymbol.set, None, None)


    _ElementMap = {
        __Configuration.name() : __Configuration,
        __SymmetryGroup.name() : __SymmetryGroup,
        __Conformation.name() : __Conformation,
        __TermSymbol.name() : __TermSymbol
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ElectronicCharacterisationType', ElectronicCharacterisationType)


# Complex type SuperShellType with content type ELEMENT_ONLY
class SuperShellType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SuperShellType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element PrincipalQuantumNumber uses Python identifier PrincipalQuantumNumber
    __PrincipalQuantumNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PrincipalQuantumNumber'), 'PrincipalQuantumNumber', '__AbsentNamespace0_SuperShellType_PrincipalQuantumNumber', False)

    
    PrincipalQuantumNumber = property(__PrincipalQuantumNumber.value, __PrincipalQuantumNumber.set, None, u'Principal quantum number. Example: 4')

    
    # Element NumberOfElectrons uses Python identifier NumberOfElectrons
    __NumberOfElectrons = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NumberOfElectrons'), 'NumberOfElectrons', '__AbsentNamespace0_SuperShellType_NumberOfElectrons', False)

    
    NumberOfElectrons = property(__NumberOfElectrons.value, __NumberOfElectrons.set, None, u'Number of electrons. May be noninteger to account for plasma effects. Example: 3')


    _ElementMap = {
        __PrincipalQuantumNumber.name() : __PrincipalQuantumNumber,
        __NumberOfElectrons.name() : __NumberOfElectrons
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SuperShellType', SuperShellType)


# Complex type NonLinearNoElecType with content type ELEMENT_ONLY
class NonLinearNoElecType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonLinearNoElecType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element C2Symmetries uses Python identifier C2Symmetries
    __C2Symmetries = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'C2Symmetries'), 'C2Symmetries', '__AbsentNamespace0_NonLinearNoElecType_C2Symmetries', False)

    
    C2Symmetries = property(__C2Symmetries.value, __C2Symmetries.set, None, None)

    
    # Element TotalAngularMomentumN uses Python identifier TotalAngularMomentumN
    __TotalAngularMomentumN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), 'TotalAngularMomentumN', '__AbsentNamespace0_NonLinearNoElecType_TotalAngularMomentumN', False)

    
    TotalAngularMomentumN = property(__TotalAngularMomentumN.value, __TotalAngularMomentumN.set, None, None)

    
    # Element MolecularProjection uses Python identifier MolecularProjection
    __MolecularProjection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MolecularProjection'), 'MolecularProjection', '__AbsentNamespace0_NonLinearNoElecType_MolecularProjection', False)

    
    MolecularProjection = property(__MolecularProjection.value, __MolecularProjection.set, None, None)


    _ElementMap = {
        __C2Symmetries.name() : __C2Symmetries,
        __TotalAngularMomentumN.name() : __TotalAngularMomentumN,
        __MolecularProjection.name() : __MolecularProjection
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NonLinearNoElecType', NonLinearNoElecType)


# Complex type NonLinearNoElecNoHyperFType with content type ELEMENT_ONLY
class NonLinearNoElecNoHyperFType (NonLinearNoElecType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonLinearNoElecNoHyperFType')
    # Base type is NonLinearNoElecType
    
    # Element TotalAngularMomentumN (TotalAngularMomentumN) inherited from NonLinearNoElecType
    
    # Element C2Symmetries (C2Symmetries) inherited from NonLinearNoElecType
    
    # Element MolecularProjection (MolecularProjection) inherited from NonLinearNoElecType
    
    # Element TotalMagneticQuantumNumberN uses Python identifier TotalMagneticQuantumNumberN
    __TotalMagneticQuantumNumberN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberN'), 'TotalMagneticQuantumNumberN', '__AbsentNamespace0_NonLinearNoElecNoHyperFType_TotalMagneticQuantumNumberN', False)

    
    TotalMagneticQuantumNumberN = property(__TotalMagneticQuantumNumberN.value, __TotalMagneticQuantumNumberN.set, None, None)


    _ElementMap = NonLinearNoElecType._ElementMap.copy()
    _ElementMap.update({
        __TotalMagneticQuantumNumberN.name() : __TotalMagneticQuantumNumberN
    })
    _AttributeMap = NonLinearNoElecType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NonLinearNoElecNoHyperFType', NonLinearNoElecNoHyperFType)


# Complex type IsotopeParametersType with content type ELEMENT_ONLY
class IsotopeParametersType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IsotopeParametersType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element MassNumber uses Python identifier MassNumber
    __MassNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MassNumber'), 'MassNumber', '__AbsentNamespace0_IsotopeParametersType_MassNumber', False)

    
    MassNumber = property(__MassNumber.value, __MassNumber.set, None, u'Mass number. Example: 40.')

    
    # Element Mass uses Python identifier Mass
    __Mass = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Mass'), 'Mass', '__AbsentNamespace0_IsotopeParametersType_Mass', False)

    
    Mass = property(__Mass.value, __Mass.set, None, u'Measured mass.')

    
    # Element NuclearSpin uses Python identifier NuclearSpin
    __NuclearSpin = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NuclearSpin'), 'NuclearSpin', '__AbsentNamespace0_IsotopeParametersType_NuclearSpin', False)

    
    NuclearSpin = property(__NuclearSpin.value, __NuclearSpin.set, None, u'Spin of an isotope')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __MassNumber.name() : __MassNumber,
        __Mass.name() : __Mass,
        __NuclearSpin.name() : __NuclearSpin
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'IsotopeParametersType', IsotopeParametersType)


# Complex type HyperfineQuantumNumbersType with content type ELEMENT_ONLY
class HyperfineQuantumNumbersType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HyperfineQuantumNumbersType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ISum uses Python identifier ISum
    __ISum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ISum'), 'ISum', '__AbsentNamespace0_HyperfineQuantumNumbersType_ISum', True)

    
    ISum = property(__ISum.value, __ISum.set, None, None)

    
    # Element IntermediateHyperfineQuantumNumber uses Python identifier IntermediateHyperfineQuantumNumber
    __IntermediateHyperfineQuantumNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IntermediateHyperfineQuantumNumber'), 'IntermediateHyperfineQuantumNumber', '__AbsentNamespace0_HyperfineQuantumNumbersType_IntermediateHyperfineQuantumNumber', True)

    
    IntermediateHyperfineQuantumNumber = property(__IntermediateHyperfineQuantumNumber.value, __IntermediateHyperfineQuantumNumber.set, None, None)

    
    # Element TotalAngularMomentumF uses Python identifier TotalAngularMomentumF
    __TotalAngularMomentumF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumF'), 'TotalAngularMomentumF', '__AbsentNamespace0_HyperfineQuantumNumbersType_TotalAngularMomentumF', False)

    
    TotalAngularMomentumF = property(__TotalAngularMomentumF.value, __TotalAngularMomentumF.set, None, None)

    
    # Element TotalMagneticQuantumNumberF uses Python identifier TotalMagneticQuantumNumberF
    __TotalMagneticQuantumNumberF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberF'), 'TotalMagneticQuantumNumberF', '__AbsentNamespace0_HyperfineQuantumNumbersType_TotalMagneticQuantumNumberF', False)

    
    TotalMagneticQuantumNumberF = property(__TotalMagneticQuantumNumberF.value, __TotalMagneticQuantumNumberF.set, None, None)


    _ElementMap = {
        __ISum.name() : __ISum,
        __IntermediateHyperfineQuantumNumber.name() : __IntermediateHyperfineQuantumNumber,
        __TotalAngularMomentumF.name() : __TotalAngularMomentumF,
        __TotalMagneticQuantumNumberF.name() : __TotalMagneticQuantumNumberF
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'HyperfineQuantumNumbersType', HyperfineQuantumNumbersType)


# Complex type ParticleType with content type ELEMENT_ONLY
class ParticleType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ParticleType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ParticleProperties uses Python identifier ParticleProperties
    __ParticleProperties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ParticleProperties'), 'ParticleProperties', '__AbsentNamespace0_ParticleType_ParticleProperties', False)

    
    ParticleProperties = property(__ParticleProperties.value, __ParticleProperties.set, None, u'Description of particle properties')

    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_ParticleType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, None)

    
    # Attribute stateID uses Python identifier stateID
    __stateID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'stateID'), 'stateID', '__AbsentNamespace0_ParticleType_stateID', STD_ANON_3, required=True)
    
    stateID = property(__stateID.value, __stateID.set, None, u'ID for a specific state/particle.')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__AbsentNamespace0_ParticleType_name', ParticleNameType)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __ParticleProperties.name() : __ParticleProperties,
        __Comments.name() : __Comments
    }
    _AttributeMap = {
        __stateID.name() : __stateID,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'ParticleType', ParticleType)


# Complex type ProductsType with content type ELEMENT_ONLY
class ProductsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ProductsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element StateRef uses Python identifier StateRef
    __StateRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StateRef'), 'StateRef', '__AbsentNamespace0_ProductsType_StateRef', True)

    
    StateRef = property(__StateRef.value, __StateRef.set, None, u'Reference to a specific state')


    _ElementMap = {
        __StateRef.name() : __StateRef
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ProductsType', ProductsType)


# Complex type MethodType with content type ELEMENT_ONLY
class MethodType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MethodType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_MethodType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, u'Method description. Example: Convergent Close Coupling.')

    
    # Element Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Category'), 'Category', '__AbsentNamespace0_MethodType_Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'Enumerated list of method classifications. Example: theory.')

    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_MethodType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, None)

    
    # Attribute sourceRef uses Python identifier sourceRef
    __sourceRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'sourceRef'), 'sourceRef', '__AbsentNamespace0_MethodType_sourceRef', STD_ANON_1)
    
    sourceRef = property(__sourceRef.value, __sourceRef.set, None, u'Reference to specific bibliographic items.')

    
    # Attribute functionRef uses Python identifier functionRef
    __functionRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'functionRef'), 'functionRef', '__AbsentNamespace0_MethodType_functionRef', STD_ANON_6)
    
    functionRef = property(__functionRef.value, __functionRef.set, None, u'Reference to a specific fit function')

    
    # Attribute methodID uses Python identifier methodID
    __methodID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'methodID'), 'methodID', '__AbsentNamespace0_MethodType_methodID', STD_ANON_5, required=True)
    
    methodID = property(__methodID.value, __methodID.set, None, u'ID for a specific method')


    _ElementMap = {
        __Description.name() : __Description,
        __Category.name() : __Category,
        __Comments.name() : __Comments
    }
    _AttributeMap = {
        __sourceRef.name() : __sourceRef,
        __functionRef.name() : __functionRef,
        __methodID.name() : __methodID
    }
Namespace.addCategoryObject('typeBinding', u'MethodType', MethodType)


# Complex type RoVibronicSplittingType with content type ELEMENT_ONLY
class RoVibronicSplittingType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RoVibronicSplittingType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Type uses Python identifier Type
    __Type = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Type'), 'Type', '__AbsentNamespace0_RoVibronicSplittingType_Type', True)

    
    Type = property(__Type.value, __Type.set, None, None)

    
    # Element Label uses Python identifier Label
    __Label = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Label'), 'Label', '__AbsentNamespace0_RoVibronicSplittingType_Label', True)

    
    Label = property(__Label.value, __Label.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Type.name() : __Type,
        __Label.name() : __Label
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'RoVibronicSplittingType', RoVibronicSplittingType)


# Complex type ParticlePropertiesType with content type ELEMENT_ONLY
class ParticlePropertiesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ParticlePropertiesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ParticleSpin uses Python identifier ParticleSpin
    __ParticleSpin = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ParticleSpin'), 'ParticleSpin', '__AbsentNamespace0_ParticlePropertiesType_ParticleSpin', False)

    
    ParticleSpin = property(__ParticleSpin.value, __ParticleSpin.set, None, u'Spin of the particle')

    
    # Element ParticleCharge uses Python identifier ParticleCharge
    __ParticleCharge = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ParticleCharge'), 'ParticleCharge', '__AbsentNamespace0_ParticlePropertiesType_ParticleCharge', False)

    
    ParticleCharge = property(__ParticleCharge.value, __ParticleCharge.set, None, u'Particle charge')

    
    # Element ParticleMass uses Python identifier ParticleMass
    __ParticleMass = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ParticleMass'), 'ParticleMass', '__AbsentNamespace0_ParticlePropertiesType_ParticleMass', False)

    
    ParticleMass = property(__ParticleMass.value, __ParticleMass.set, None, u'Mass of the particle')

    
    # Element ParticlePolarization uses Python identifier ParticlePolarization
    __ParticlePolarization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ParticlePolarization'), 'ParticlePolarization', '__AbsentNamespace0_ParticlePropertiesType_ParticlePolarization', False)

    
    ParticlePolarization = property(__ParticlePolarization.value, __ParticlePolarization.set, None, u'Polarization of the particle')


    _ElementMap = {
        __ParticleSpin.name() : __ParticleSpin,
        __ParticleCharge.name() : __ParticleCharge,
        __ParticleMass.name() : __ParticleMass,
        __ParticlePolarization.name() : __ParticlePolarization
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ParticlePropertiesType', ParticlePropertiesType)


# Complex type ConfigurationType with content type ELEMENT_ONLY
class ConfigurationType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ConfigurationType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ConfigurationLabel uses Python identifier ConfigurationLabel
    __ConfigurationLabel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ConfigurationLabel'), 'ConfigurationLabel', '__AbsentNamespace0_ConfigurationType_ConfigurationLabel', False)

    
    ConfigurationLabel = property(__ConfigurationLabel.value, __ConfigurationLabel.set, None, u'Arbitrary configuration label')

    
    # Element AtomicCore uses Python identifier AtomicCore
    __AtomicCore = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AtomicCore'), 'AtomicCore', '__AbsentNamespace0_ConfigurationType_AtomicCore', False)

    
    AtomicCore = property(__AtomicCore.value, __AtomicCore.set, None, u'Description of the configuration core')

    
    # Element Shells uses Python identifier Shells
    __Shells = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Shells'), 'Shells', '__AbsentNamespace0_ConfigurationType_Shells', False)

    
    Shells = property(__Shells.value, __Shells.set, None, u'List of electron shells')


    _ElementMap = {
        __ConfigurationLabel.name() : __ConfigurationLabel,
        __AtomicCore.name() : __AtomicCore,
        __Shells.name() : __Shells
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ConfigurationType', ConfigurationType)


# Complex type NonLinearPolyatomicType with content type ELEMENT_ONLY
class NonLinearPolyatomicType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonLinearPolyatomicType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element NonLinearNoElecHyperF uses Python identifier NonLinearNoElecHyperF
    __NonLinearNoElecHyperF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NonLinearNoElecHyperF'), 'NonLinearNoElecHyperF', '__AbsentNamespace0_NonLinearPolyatomicType_NonLinearNoElecHyperF', False)

    
    NonLinearNoElecHyperF = property(__NonLinearNoElecHyperF.value, __NonLinearNoElecHyperF.set, None, None)

    
    # Element NonLinearElecNoHyperF uses Python identifier NonLinearElecNoHyperF
    __NonLinearElecNoHyperF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NonLinearElecNoHyperF'), 'NonLinearElecNoHyperF', '__AbsentNamespace0_NonLinearPolyatomicType_NonLinearElecNoHyperF', False)

    
    NonLinearElecNoHyperF = property(__NonLinearElecNoHyperF.value, __NonLinearElecNoHyperF.set, None, None)

    
    # Element NonLinearNoElecNoHyperF uses Python identifier NonLinearNoElecNoHyperF
    __NonLinearNoElecNoHyperF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NonLinearNoElecNoHyperF'), 'NonLinearNoElecNoHyperF', '__AbsentNamespace0_NonLinearPolyatomicType_NonLinearNoElecNoHyperF', False)

    
    NonLinearNoElecNoHyperF = property(__NonLinearNoElecNoHyperF.value, __NonLinearNoElecNoHyperF.set, None, None)

    
    # Element NonLinearElecHyperF uses Python identifier NonLinearElecHyperF
    __NonLinearElecHyperF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NonLinearElecHyperF'), 'NonLinearElecHyperF', '__AbsentNamespace0_NonLinearPolyatomicType_NonLinearElecHyperF', False)

    
    NonLinearElecHyperF = property(__NonLinearElecHyperF.value, __NonLinearElecHyperF.set, None, None)


    _ElementMap = {
        __NonLinearNoElecHyperF.name() : __NonLinearNoElecHyperF,
        __NonLinearElecNoHyperF.name() : __NonLinearElecNoHyperF,
        __NonLinearNoElecNoHyperF.name() : __NonLinearNoElecNoHyperF,
        __NonLinearElecHyperF.name() : __NonLinearElecHyperF
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NonLinearPolyatomicType', NonLinearPolyatomicType)


# Complex type HyperfineCaseAAlphaType with content type ELEMENT_ONLY
class HyperfineCaseAAlphaType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HyperfineCaseAAlphaType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TotalMagneticQuantumNumberF uses Python identifier TotalMagneticQuantumNumberF
    __TotalMagneticQuantumNumberF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberF'), 'TotalMagneticQuantumNumberF', '__AbsentNamespace0_HyperfineCaseAAlphaType_TotalMagneticQuantumNumberF', False)

    
    TotalMagneticQuantumNumberF = property(__TotalMagneticQuantumNumberF.value, __TotalMagneticQuantumNumberF.set, None, None)

    
    # Element TotalMolecularProjectionF uses Python identifier TotalMolecularProjectionF
    __TotalMolecularProjectionF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionF'), 'TotalMolecularProjectionF', '__AbsentNamespace0_HyperfineCaseAAlphaType_TotalMolecularProjectionF', False)

    
    TotalMolecularProjectionF = property(__TotalMolecularProjectionF.value, __TotalMolecularProjectionF.set, None, None)

    
    # Element TotalAngularMomentumF uses Python identifier TotalAngularMomentumF
    __TotalAngularMomentumF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumF'), 'TotalAngularMomentumF', '__AbsentNamespace0_HyperfineCaseAAlphaType_TotalAngularMomentumF', False)

    
    TotalAngularMomentumF = property(__TotalAngularMomentumF.value, __TotalAngularMomentumF.set, None, None)


    _ElementMap = {
        __TotalMagneticQuantumNumberF.name() : __TotalMagneticQuantumNumberF,
        __TotalMolecularProjectionF.name() : __TotalMolecularProjectionF,
        __TotalAngularMomentumF.name() : __TotalAngularMomentumF
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'HyperfineCaseAAlphaType', HyperfineCaseAAlphaType)


# Complex type BondType with content type EMPTY
class BondType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BondType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute order uses Python identifier order
    __order = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'order'), 'order', '__AbsentNamespace0_BondType_order', pyxb.binding.datatypes.string)
    
    order = property(__order.value, __order.set, None, None)

    
    # Attribute atomRefs2 uses Python identifier atomRefs2
    __atomRefs2 = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'atomRefs2'), 'atomRefs2', '__AbsentNamespace0_BondType_atomRefs2', pyxb.binding.datatypes.IDREFS)
    
    atomRefs2 = property(__atomRefs2.value, __atomRefs2.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __order.name() : __order,
        __atomRefs2.name() : __atomRefs2
    }
Namespace.addCategoryObject('typeBinding', u'BondType', BondType)


# Complex type MolecularProjectionType with content type ELEMENT_ONLY
class MolecularProjectionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MolecularProjectionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element HinderedMotion uses Python identifier HinderedMotion
    __HinderedMotion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HinderedMotion'), 'HinderedMotion', '__AbsentNamespace0_MolecularProjectionType_HinderedMotion', False)

    
    HinderedMotion = property(__HinderedMotion.value, __HinderedMotion.set, None, None)

    
    # Element TotalMolecularProjectionN uses Python identifier TotalMolecularProjectionN
    __TotalMolecularProjectionN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionN'), 'TotalMolecularProjectionN', '__AbsentNamespace0_MolecularProjectionType_TotalMolecularProjectionN', False)

    
    TotalMolecularProjectionN = property(__TotalMolecularProjectionN.value, __TotalMolecularProjectionN.set, None, None)

    
    # Element AsymmetricProjection uses Python identifier AsymmetricProjection
    __AsymmetricProjection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AsymmetricProjection'), 'AsymmetricProjection', '__AbsentNamespace0_MolecularProjectionType_AsymmetricProjection', False)

    
    AsymmetricProjection = property(__AsymmetricProjection.value, __AsymmetricProjection.set, None, None)


    _ElementMap = {
        __HinderedMotion.name() : __HinderedMotion,
        __TotalMolecularProjectionN.name() : __TotalMolecularProjectionN,
        __AsymmetricProjection.name() : __AsymmetricProjection
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MolecularProjectionType', MolecularProjectionType)


# Complex type AuthorsType with content type ELEMENT_ONLY
class AuthorsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthorsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Author uses Python identifier Author
    __Author = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Author'), 'Author', '__AbsentNamespace0_AuthorsType_Author', True)

    
    Author = property(__Author.value, __Author.set, None, u'Author of bibliographic reference.')


    _ElementMap = {
        __Author.name() : __Author
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AuthorsType', AuthorsType)


# Complex type AtomicComponentType with content type ELEMENT_ONLY
class AtomicComponentType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomicComponentType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Configuration uses Python identifier Configuration
    __Configuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Configuration'), 'Configuration', '__AbsentNamespace0_AtomicComponentType_Configuration', False)

    
    Configuration = property(__Configuration.value, __Configuration.set, None, u'Atomic configuration')

    
    # Element SuperConfiguration uses Python identifier SuperConfiguration
    __SuperConfiguration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SuperConfiguration'), 'SuperConfiguration', '__AbsentNamespace0_AtomicComponentType_SuperConfiguration', False)

    
    SuperConfiguration = property(__SuperConfiguration.value, __SuperConfiguration.set, None, u'Superconfiguration')

    
    # Element Term uses Python identifier Term
    __Term = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Term'), 'Term', '__AbsentNamespace0_AtomicComponentType_Term', False)

    
    Term = property(__Term.value, __Term.set, None, u'Atomic term')

    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_AtomicComponentType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, u'Comments on a specific component')

    
    # Element MixingCoefficient uses Python identifier MixingCoefficient
    __MixingCoefficient = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), 'MixingCoefficient', '__AbsentNamespace0_AtomicComponentType_MixingCoefficient', False)

    
    MixingCoefficient = property(__MixingCoefficient.value, __MixingCoefficient.set, None, u'Expansion coefficient in the sum over the basis functions (signed or squared)')


    _ElementMap = {
        __Configuration.name() : __Configuration,
        __SuperConfiguration.name() : __SuperConfiguration,
        __Term.name() : __Term,
        __Comments.name() : __Comments,
        __MixingCoefficient.name() : __MixingCoefficient
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AtomicComponentType', AtomicComponentType)


# Complex type MoleculesType with content type ELEMENT_ONLY
class MoleculesType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MoleculesType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Molecule uses Python identifier Molecule
    __Molecule = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Molecule'), 'Molecule', '__AbsentNamespace0_MoleculesType_Molecule', True)

    
    Molecule = property(__Molecule.value, __Molecule.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Molecule.name() : __Molecule
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'MoleculesType', MoleculesType)


# Complex type MixingCoefficientType with content type SIMPLE
class MixingCoefficientType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.double
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MixingCoefficientType')
    # Base type is pyxb.binding.datatypes.double
    
    # Attribute mixingClass uses Python identifier mixingClass
    __mixingClass = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mixingClass'), 'mixingClass', '__AbsentNamespace0_MixingCoefficientType_mixingClass', MixingClassType, required=True)
    
    mixingClass = property(__mixingClass.value, __mixingClass.set, None, u'Indicator of whether amplitude or amplitude squared is given')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __mixingClass.name() : __mixingClass
    }
Namespace.addCategoryObject('typeBinding', u'MixingCoefficientType', MixingCoefficientType)


# Complex type RadiativeTransitionProbabilityType with content type ELEMENT_ONLY
class RadiativeTransitionProbabilityType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RadiativeTransitionProbabilityType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element TransitionProbabilityA uses Python identifier TransitionProbabilityA
    __TransitionProbabilityA = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TransitionProbabilityA'), 'TransitionProbabilityA', '__AbsentNamespace0_RadiativeTransitionProbabilityType_TransitionProbabilityA', False)

    
    TransitionProbabilityA = property(__TransitionProbabilityA.value, __TransitionProbabilityA.set, None, u'Transition probability (Einstein coefficient)')

    
    # Element OscillatorStrength uses Python identifier OscillatorStrength
    __OscillatorStrength = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'OscillatorStrength'), 'OscillatorStrength', '__AbsentNamespace0_RadiativeTransitionProbabilityType_OscillatorStrength', False)

    
    OscillatorStrength = property(__OscillatorStrength.value, __OscillatorStrength.set, None, u'Oscillator strength')

    
    # Element IdealisedIntensity uses Python identifier IdealisedIntensity
    __IdealisedIntensity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'), 'IdealisedIntensity', '__AbsentNamespace0_RadiativeTransitionProbabilityType_IdealisedIntensity', False)

    
    IdealisedIntensity = property(__IdealisedIntensity.value, __IdealisedIntensity.set, None, u'Line intensity for some specific conditions.')

    
    # Element LineStrength uses Python identifier LineStrength
    __LineStrength = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LineStrength'), 'LineStrength', '__AbsentNamespace0_RadiativeTransitionProbabilityType_LineStrength', False)

    
    LineStrength = property(__LineStrength.value, __LineStrength.set, None, u'Line strength')

    
    # Element Multipole uses Python identifier Multipole
    __Multipole = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Multipole'), 'Multipole', '__AbsentNamespace0_RadiativeTransitionProbabilityType_Multipole', False)

    
    Multipole = property(__Multipole.value, __Multipole.set, None, u'Transition multipole type. Example: E2')

    
    # Element WeightedOscillatorStrength uses Python identifier WeightedOscillatorStrength
    __WeightedOscillatorStrength = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'WeightedOscillatorStrength'), 'WeightedOscillatorStrength', '__AbsentNamespace0_RadiativeTransitionProbabilityType_WeightedOscillatorStrength', False)

    
    WeightedOscillatorStrength = property(__WeightedOscillatorStrength.value, __WeightedOscillatorStrength.set, None, u'Weighted oscillator strength')

    
    # Element Log10WeightedOscillatorStregnth uses Python identifier Log10WeightedOscillatorStregnth
    __Log10WeightedOscillatorStregnth = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'), 'Log10WeightedOscillatorStregnth', '__AbsentNamespace0_RadiativeTransitionProbabilityType_Log10WeightedOscillatorStregnth', False)

    
    Log10WeightedOscillatorStregnth = property(__Log10WeightedOscillatorStregnth.value, __Log10WeightedOscillatorStregnth.set, None, u'Log10 of the weighted oscillator strength')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __TransitionProbabilityA.name() : __TransitionProbabilityA,
        __OscillatorStrength.name() : __OscillatorStrength,
        __IdealisedIntensity.name() : __IdealisedIntensity,
        __LineStrength.name() : __LineStrength,
        __Multipole.name() : __Multipole,
        __WeightedOscillatorStrength.name() : __WeightedOscillatorStrength,
        __Log10WeightedOscillatorStregnth.name() : __Log10WeightedOscillatorStregnth
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'RadiativeTransitionProbabilityType', RadiativeTransitionProbabilityType)


# Complex type LKCouplingType with content type ELEMENT_ONLY
class LKCouplingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LKCouplingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element L uses Python identifier L
    __L = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'L'), 'L', '__AbsentNamespace0_LKCouplingType_L', False)

    
    L = property(__L.value, __L.set, None, u'Value of the sum of orbital angular momenta of the core and external electron ')

    
    # Element K uses Python identifier K
    __K = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'K'), 'K', '__AbsentNamespace0_LKCouplingType_K', False)

    
    K = property(__K.value, __K.set, None, u'Value of the K-number (L + spin of the core)')


    _ElementMap = {
        __L.name() : __L,
        __K.name() : __K
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LKCouplingType', LKCouplingType)


# Complex type StateEnergyType with content type ELEMENT_ONLY
class StateEnergyType (DataType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StateEnergyType')
    # Base type is DataType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Value (Value) inherited from DataType
    
    # Element Accuracy (Accuracy) inherited from DataType
    
    # Attribute energyOrigin uses Python identifier energyOrigin
    __energyOrigin = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'energyOrigin'), 'energyOrigin', '__AbsentNamespace0_StateEnergyType_energyOrigin', pyxb.binding.datatypes.string, required=True)
    
    energyOrigin = property(__energyOrigin.value, __energyOrigin.set, None, None)

    
    # Attribute methodRef inherited from PrimaryType
    
    # Attribute sourceRef inherited from PrimaryType

    _ElementMap = DataType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = DataType._AttributeMap.copy()
    _AttributeMap.update({
        __energyOrigin.name() : __energyOrigin
    })
Namespace.addCategoryObject('typeBinding', u'StateEnergyType', StateEnergyType)


# Complex type SolidType with content type ELEMENT_ONLY
class SolidType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SolidType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Layer uses Python identifier Layer
    __Layer = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Layer'), 'Layer', '__AbsentNamespace0_SolidType_Layer', True)

    
    Layer = property(__Layer.value, __Layer.set, None, None)

    
    # Attribute stateID uses Python identifier stateID
    __stateID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'stateID'), 'stateID', '__AbsentNamespace0_SolidType_stateID', STD_ANON_3, required=True)
    
    stateID = property(__stateID.value, __stateID.set, None, u'ID for a specific state/particle.')

    
    # Attribute methodRef inherited from PrimaryType
    
    # Attribute sourceRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Layer.name() : __Layer
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        __stateID.name() : __stateID
    })
Namespace.addCategoryObject('typeBinding', u'SolidType', SolidType)


# Complex type CollisionsType with content type ELEMENT_ONLY
class CollisionsType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CollisionsType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element CollisionalTransition uses Python identifier CollisionalTransition
    __CollisionalTransition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CollisionalTransition'), 'CollisionalTransition', '__AbsentNamespace0_CollisionsType_CollisionalTransition', True)

    
    CollisionalTransition = property(__CollisionalTransition.value, __CollisionalTransition.set, None, u'A specific collisional transition')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __CollisionalTransition.name() : __CollisionalTransition
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'CollisionsType', CollisionsType)


# Complex type RadiativeTransitionType with content type ELEMENT_ONLY
class RadiativeTransitionType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RadiativeTransitionType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Probability uses Python identifier Probability
    __Probability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Probability'), 'Probability', '__AbsentNamespace0_RadiativeTransitionType_Probability', True)

    
    Probability = property(__Probability.value, __Probability.set, None, u'Radiative transition probability and related parameters')

    
    # Element FinalStateRef uses Python identifier FinalStateRef
    __FinalStateRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FinalStateRef'), 'FinalStateRef', '__AbsentNamespace0_RadiativeTransitionType_FinalStateRef', False)

    
    FinalStateRef = property(__FinalStateRef.value, __FinalStateRef.set, None, u'Reference to the final state')

    
    # Element InitialStateRef uses Python identifier InitialStateRef
    __InitialStateRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'InitialStateRef'), 'InitialStateRef', '__AbsentNamespace0_RadiativeTransitionType_InitialStateRef', False)

    
    InitialStateRef = property(__InitialStateRef.value, __InitialStateRef.set, None, u'Reference to the initial state')

    
    # Element EnergyWavelength uses Python identifier EnergyWavelength
    __EnergyWavelength = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EnergyWavelength'), 'EnergyWavelength', '__AbsentNamespace0_RadiativeTransitionType_EnergyWavelength', False)

    
    EnergyWavelength = property(__EnergyWavelength.value, __EnergyWavelength.set, None, u'List of energy/spectrum parameters')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Probability.name() : __Probability,
        __FinalStateRef.name() : __FinalStateRef,
        __InitialStateRef.name() : __InitialStateRef,
        __EnergyWavelength.name() : __EnergyWavelength
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'RadiativeTransitionType', RadiativeTransitionType)


# Complex type VibrationalQuantumNumbersType with content type ELEMENT_ONLY
class VibrationalQuantumNumbersType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VibrationalQuantumNumbersType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element VibrationalNu uses Python identifier VibrationalNu
    __VibrationalNu = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibrationalNu'), 'VibrationalNu', '__AbsentNamespace0_VibrationalQuantumNumbersType_VibrationalNu', True)

    
    VibrationalNu = property(__VibrationalNu.value, __VibrationalNu.set, None, None)

    
    # Element VibronicAngularMomentumP uses Python identifier VibronicAngularMomentumP
    __VibronicAngularMomentumP = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumP'), 'VibronicAngularMomentumP', '__AbsentNamespace0_VibrationalQuantumNumbersType_VibronicAngularMomentumP', False)

    
    VibronicAngularMomentumP = property(__VibronicAngularMomentumP.value, __VibronicAngularMomentumP.set, None, None)

    
    # Element TotalVibrationL uses Python identifier TotalVibrationL
    __TotalVibrationL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalVibrationL'), 'TotalVibrationL', '__AbsentNamespace0_VibrationalQuantumNumbersType_TotalVibrationL', False)

    
    TotalVibrationL = property(__TotalVibrationL.value, __TotalVibrationL.set, None, None)

    
    # Element VibronicAngularMomentumK uses Python identifier VibronicAngularMomentumK
    __VibronicAngularMomentumK = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumK'), 'VibronicAngularMomentumK', '__AbsentNamespace0_VibrationalQuantumNumbersType_VibronicAngularMomentumK', False)

    
    VibronicAngularMomentumK = property(__VibronicAngularMomentumK.value, __VibronicAngularMomentumK.set, None, None)


    _ElementMap = {
        __VibrationalNu.name() : __VibrationalNu,
        __VibronicAngularMomentumP.name() : __VibronicAngularMomentumP,
        __TotalVibrationL.name() : __TotalVibrationL,
        __VibronicAngularMomentumK.name() : __VibronicAngularMomentumK
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'VibrationalQuantumNumbersType', VibrationalQuantumNumbersType)


# Complex type DataSetsType with content type ELEMENT_ONLY
class DataSetsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataSetsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element DataSet uses Python identifier DataSet
    __DataSet = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DataSet'), 'DataSet', '__AbsentNamespace0_DataSetsType_DataSet', True)

    
    DataSet = property(__DataSet.value, __DataSet.set, None, u'List of datasets of different nature (cross sections, rate coefficients, etc.)')


    _ElementMap = {
        __DataSet.name() : __DataSet
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DataSetsType', DataSetsType)


# Complex type ReactantsType with content type ELEMENT_ONLY
class ReactantsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ReactantsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element StateRef uses Python identifier StateRef
    __StateRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StateRef'), 'StateRef', '__AbsentNamespace0_ReactantsType_StateRef', True)

    
    StateRef = property(__StateRef.value, __StateRef.set, None, u'Reference to a specific state')


    _ElementMap = {
        __StateRef.name() : __StateRef
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ReactantsType', ReactantsType)


# Complex type MolecularStateCharacterisation_oldType with content type ELEMENT_ONLY
class MolecularStateCharacterisation_oldType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MolecularStateCharacterisation-oldType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LifeTime uses Python identifier LifeTime
    __LifeTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LifeTime'), 'LifeTime', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_LifeTime', False)

    
    LifeTime = property(__LifeTime.value, __LifeTime.set, None, None)

    
    # Element StateEnergy uses Python identifier StateEnergy
    __StateEnergy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StateEnergy'), 'StateEnergy', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_StateEnergy', False)

    
    StateEnergy = property(__StateEnergy.value, __StateEnergy.set, None, None)

    
    # Element Parameters uses Python identifier Parameters
    __Parameters = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parameters'), 'Parameters', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_Parameters', True)

    
    Parameters = property(__Parameters.value, __Parameters.set, None, None)

    
    # Element NuclearStatisticalWeight uses Python identifier NuclearStatisticalWeight
    __NuclearStatisticalWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'), 'NuclearStatisticalWeight', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_NuclearStatisticalWeight', False)

    
    NuclearStatisticalWeight = property(__NuclearStatisticalWeight.value, __NuclearStatisticalWeight.set, None, None)

    
    # Element TotalStatisticalWeight uses Python identifier TotalStatisticalWeight
    __TotalStatisticalWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'), 'TotalStatisticalWeight', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_TotalStatisticalWeight', False)

    
    TotalStatisticalWeight = property(__TotalStatisticalWeight.value, __TotalStatisticalWeight.set, None, None)

    
    # Element PseudoStatisticalWeight uses Python identifier PseudoStatisticalWeight
    __PseudoStatisticalWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PseudoStatisticalWeight'), 'PseudoStatisticalWeight', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_PseudoStatisticalWeight', False)

    
    PseudoStatisticalWeight = property(__PseudoStatisticalWeight.value, __PseudoStatisticalWeight.set, None, None)

    
    # Element PseudoNuclearStatisticalWeight uses Python identifier PseudoNuclearStatisticalWeight
    __PseudoNuclearStatisticalWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PseudoNuclearStatisticalWeight'), 'PseudoNuclearStatisticalWeight', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_PseudoNuclearStatisticalWeight', False)

    
    PseudoNuclearStatisticalWeight = property(__PseudoNuclearStatisticalWeight.value, __PseudoNuclearStatisticalWeight.set, None, None)

    
    # Element NuclearSpinSymmetry uses Python identifier NuclearSpinSymmetry
    __NuclearSpinSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'), 'NuclearSpinSymmetry', '__AbsentNamespace0_MolecularStateCharacterisation_oldType_NuclearSpinSymmetry', False)

    
    NuclearSpinSymmetry = property(__NuclearSpinSymmetry.value, __NuclearSpinSymmetry.set, None, None)


    _ElementMap = {
        __LifeTime.name() : __LifeTime,
        __StateEnergy.name() : __StateEnergy,
        __Parameters.name() : __Parameters,
        __NuclearStatisticalWeight.name() : __NuclearStatisticalWeight,
        __TotalStatisticalWeight.name() : __TotalStatisticalWeight,
        __PseudoStatisticalWeight.name() : __PseudoStatisticalWeight,
        __PseudoNuclearStatisticalWeight.name() : __PseudoNuclearStatisticalWeight,
        __NuclearSpinSymmetry.name() : __NuclearSpinSymmetry
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MolecularStateCharacterisation-oldType', MolecularStateCharacterisation_oldType)


# Complex type ValueType with content type SIMPLE
class ValueType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.double
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ValueType')
    # Base type is pyxb.binding.datatypes.double
    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'units'), 'units', '__AbsentNamespace0_ValueType_units', STD_ANON_4, required=True)
    
    units = property(__units.value, __units.set, None, u'Description of physical units. Use "unitless" for dimensionless quantities.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __units.name() : __units
    }
Namespace.addCategoryObject('typeBinding', u'ValueType', ValueType)


# Complex type CollisionalTransitionType with content type ELEMENT_ONLY
class CollisionalTransitionType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CollisionalTransitionType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element IntermediateStates uses Python identifier IntermediateStates
    __IntermediateStates = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IntermediateStates'), 'IntermediateStates', '__AbsentNamespace0_CollisionalTransitionType_IntermediateStates', False)

    
    IntermediateStates = property(__IntermediateStates.value, __IntermediateStates.set, None, u'List of intermediate state')

    
    # Element Products uses Python identifier Products
    __Products = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Products'), 'Products', '__AbsentNamespace0_CollisionalTransitionType_Products', False)

    
    Products = property(__Products.value, __Products.set, None, u'List of final states')

    
    # Element Threshold uses Python identifier Threshold
    __Threshold = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Threshold'), 'Threshold', '__AbsentNamespace0_CollisionalTransitionType_Threshold', False)

    
    Threshold = property(__Threshold.value, __Threshold.set, None, u'Reaction threshold')

    
    # Element ProcessClass uses Python identifier ProcessClass
    __ProcessClass = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ProcessClass'), 'ProcessClass', '__AbsentNamespace0_CollisionalTransitionType_ProcessClass', False)

    
    ProcessClass = property(__ProcessClass.value, __ProcessClass.set, None, u'Collisional process')

    
    # Element Reactants uses Python identifier Reactants
    __Reactants = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Reactants'), 'Reactants', '__AbsentNamespace0_CollisionalTransitionType_Reactants', False)

    
    Reactants = property(__Reactants.value, __Reactants.set, None, u'List of reacting systems')

    
    # Element DataSets uses Python identifier DataSets
    __DataSets = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DataSets'), 'DataSets', '__AbsentNamespace0_CollisionalTransitionType_DataSets', False)

    
    DataSets = property(__DataSets.value, __DataSets.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __IntermediateStates.name() : __IntermediateStates,
        __Products.name() : __Products,
        __Threshold.name() : __Threshold,
        __ProcessClass.name() : __ProcessClass,
        __Reactants.name() : __Reactants,
        __DataSets.name() : __DataSets
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'CollisionalTransitionType', CollisionalTransitionType)


# Complex type SimpleSymbolType with content type ELEMENT_ONLY
class SimpleSymbolType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SimpleSymbolType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element RightCoefficient uses Python identifier RightCoefficient
    __RightCoefficient = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RightCoefficient'), 'RightCoefficient', '__AbsentNamespace0_SimpleSymbolType_RightCoefficient', False)

    
    RightCoefficient = property(__RightCoefficient.value, __RightCoefficient.set, None, None)

    
    # Element CentralSymbol uses Python identifier CentralSymbol
    __CentralSymbol = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CentralSymbol'), 'CentralSymbol', '__AbsentNamespace0_SimpleSymbolType_CentralSymbol', False)

    
    CentralSymbol = property(__CentralSymbol.value, __CentralSymbol.set, None, None)

    
    # Element LeftCoefficient uses Python identifier LeftCoefficient
    __LeftCoefficient = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LeftCoefficient'), 'LeftCoefficient', '__AbsentNamespace0_SimpleSymbolType_LeftCoefficient', False)

    
    LeftCoefficient = property(__LeftCoefficient.value, __LeftCoefficient.set, None, None)


    _ElementMap = {
        __RightCoefficient.name() : __RightCoefficient,
        __CentralSymbol.name() : __CentralSymbol,
        __LeftCoefficient.name() : __LeftCoefficient
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SimpleSymbolType', SimpleSymbolType)


# Complex type FunctionsType with content type ELEMENT_ONLY
class FunctionsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FunctionsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Function uses Python identifier Function
    __Function = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Function'), 'Function', '__AbsentNamespace0_FunctionsType_Function', True)

    
    Function = property(__Function.value, __Function.set, None, None)


    _ElementMap = {
        __Function.name() : __Function
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'FunctionsType', FunctionsType)


# Complex type CharacterisationType with content type ELEMENT_ONLY
class CharacterisationType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CharacterisationType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__AbsentNamespace0_CharacterisationType_Name', False)

    
    Name = property(__Name.value, __Name.set, None, None)

    
    # Element StringValue uses Python identifier StringValue
    __StringValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StringValue'), 'StringValue', '__AbsentNamespace0_CharacterisationType_StringValue', False)

    
    StringValue = property(__StringValue.value, __StringValue.set, None, None)

    
    # Element IntValue uses Python identifier IntValue
    __IntValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IntValue'), 'IntValue', '__AbsentNamespace0_CharacterisationType_IntValue', False)

    
    IntValue = property(__IntValue.value, __IntValue.set, None, None)

    
    # Element FloatValue uses Python identifier FloatValue
    __FloatValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FloatValue'), 'FloatValue', '__AbsentNamespace0_CharacterisationType_FloatValue', False)

    
    FloatValue = property(__FloatValue.value, __FloatValue.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Name.name() : __Name,
        __StringValue.name() : __StringValue,
        __IntValue.name() : __IntValue,
        __FloatValue.name() : __FloatValue
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'CharacterisationType', CharacterisationType)


# Complex type MoleculeType with content type ELEMENT_ONLY
class MoleculeType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MoleculeType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element MolecularChemicalSpecies uses Python identifier MolecularChemicalSpecies
    __MolecularChemicalSpecies = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MolecularChemicalSpecies'), 'MolecularChemicalSpecies', '__AbsentNamespace0_MoleculeType_MolecularChemicalSpecies', False)

    
    MolecularChemicalSpecies = property(__MolecularChemicalSpecies.value, __MolecularChemicalSpecies.set, None, None)

    
    # Element MolecularState uses Python identifier MolecularState
    __MolecularState = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MolecularState'), 'MolecularState', '__AbsentNamespace0_MoleculeType_MolecularState', True)

    
    MolecularState = property(__MolecularState.value, __MolecularState.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __MolecularChemicalSpecies.name() : __MolecularChemicalSpecies,
        __MolecularState.name() : __MolecularState
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'MoleculeType', MoleculeType)


# Complex type NonRadiativeType with content type ELEMENT_ONLY
class NonRadiativeType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonRadiativeType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element NonRadiativeTransition uses Python identifier NonRadiativeTransition
    __NonRadiativeTransition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NonRadiativeTransition'), 'NonRadiativeTransition', '__AbsentNamespace0_NonRadiativeType_NonRadiativeTransition', True)

    
    NonRadiativeTransition = property(__NonRadiativeTransition.value, __NonRadiativeTransition.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __NonRadiativeTransition.name() : __NonRadiativeTransition
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NonRadiativeType', NonRadiativeType)


# Complex type RotationalComponentType with content type ELEMENT_ONLY
class RotationalComponentType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RotationalComponentType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element SerialQuantumNumber uses Python identifier SerialQuantumNumber
    __SerialQuantumNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'), 'SerialQuantumNumber', '__AbsentNamespace0_RotationalComponentType_SerialQuantumNumber', False)

    
    SerialQuantumNumber = property(__SerialQuantumNumber.value, __SerialQuantumNumber.set, None, None)

    
    # Element NonLinearPolyatomic uses Python identifier NonLinearPolyatomic
    __NonLinearPolyatomic = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NonLinearPolyatomic'), 'NonLinearPolyatomic', '__AbsentNamespace0_RotationalComponentType_NonLinearPolyatomic', False)

    
    NonLinearPolyatomic = property(__NonLinearPolyatomic.value, __NonLinearPolyatomic.set, None, None)

    
    # Element DiatomAndLinearPolyatomic uses Python identifier DiatomAndLinearPolyatomic
    __DiatomAndLinearPolyatomic = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DiatomAndLinearPolyatomic'), 'DiatomAndLinearPolyatomic', '__AbsentNamespace0_RotationalComponentType_DiatomAndLinearPolyatomic', False)

    
    DiatomAndLinearPolyatomic = property(__DiatomAndLinearPolyatomic.value, __DiatomAndLinearPolyatomic.set, None, None)

    
    # Element MixingCoefficient uses Python identifier MixingCoefficient
    __MixingCoefficient = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), 'MixingCoefficient', '__AbsentNamespace0_RotationalComponentType_MixingCoefficient', False)

    
    MixingCoefficient = property(__MixingCoefficient.value, __MixingCoefficient.set, None, None)


    _ElementMap = {
        __SerialQuantumNumber.name() : __SerialQuantumNumber,
        __NonLinearPolyatomic.name() : __NonLinearPolyatomic,
        __DiatomAndLinearPolyatomic.name() : __DiatomAndLinearPolyatomic,
        __MixingCoefficient.name() : __MixingCoefficient
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'RotationalComponentType', RotationalComponentType)


# Complex type VibrationalCharacterisationType with content type ELEMENT_ONLY
class VibrationalCharacterisationType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VibrationalCharacterisationType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element VibrationalSpeciesNotation uses Python identifier VibrationalSpeciesNotation
    __VibrationalSpeciesNotation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibrationalSpeciesNotation'), 'VibrationalSpeciesNotation', '__AbsentNamespace0_VibrationalCharacterisationType_VibrationalSpeciesNotation', False)

    
    VibrationalSpeciesNotation = property(__VibrationalSpeciesNotation.value, __VibrationalSpeciesNotation.set, None, None)

    
    # Element VibronicSpeciesNotation uses Python identifier VibronicSpeciesNotation
    __VibronicSpeciesNotation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibronicSpeciesNotation'), 'VibronicSpeciesNotation', '__AbsentNamespace0_VibrationalCharacterisationType_VibronicSpeciesNotation', False)

    
    VibronicSpeciesNotation = property(__VibronicSpeciesNotation.value, __VibronicSpeciesNotation.set, None, None)


    _ElementMap = {
        __VibrationalSpeciesNotation.name() : __VibrationalSpeciesNotation,
        __VibronicSpeciesNotation.name() : __VibronicSpeciesNotation
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'VibrationalCharacterisationType', VibrationalCharacterisationType)


# Complex type LinearElecCouplingType with content type ELEMENT_ONLY
class LinearElecCouplingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LinearElecCouplingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element HyperfineCouplingHundCaseB uses Python identifier HyperfineCouplingHundCaseB
    __HyperfineCouplingHundCaseB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'), 'HyperfineCouplingHundCaseB', '__AbsentNamespace0_LinearElecCouplingType_HyperfineCouplingHundCaseB', False)

    
    HyperfineCouplingHundCaseB = property(__HyperfineCouplingHundCaseB.value, __HyperfineCouplingHundCaseB.set, None, None)

    
    # Element HyperfineCaseABeta uses Python identifier HyperfineCaseABeta
    __HyperfineCaseABeta = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineCaseABeta'), 'HyperfineCaseABeta', '__AbsentNamespace0_LinearElecCouplingType_HyperfineCaseABeta', False)

    
    HyperfineCaseABeta = property(__HyperfineCaseABeta.value, __HyperfineCaseABeta.set, None, None)

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_LinearElecCouplingType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, None)

    
    # Element EfSymmetry uses Python identifier EfSymmetry
    __EfSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EfSymmetry'), 'EfSymmetry', '__AbsentNamespace0_LinearElecCouplingType_EfSymmetry', False)

    
    EfSymmetry = property(__EfSymmetry.value, __EfSymmetry.set, None, None)

    
    # Element HundCaseA uses Python identifier HundCaseA
    __HundCaseA = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HundCaseA'), 'HundCaseA', '__AbsentNamespace0_LinearElecCouplingType_HundCaseA', False)

    
    HundCaseA = property(__HundCaseA.value, __HundCaseA.set, None, None)

    
    # Element HyperfineCaseAAlpha uses Python identifier HyperfineCaseAAlpha
    __HyperfineCaseAAlpha = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineCaseAAlpha'), 'HyperfineCaseAAlpha', '__AbsentNamespace0_LinearElecCouplingType_HyperfineCaseAAlpha', False)

    
    HyperfineCaseAAlpha = property(__HyperfineCaseAAlpha.value, __HyperfineCaseAAlpha.set, None, None)

    
    # Element HundCaseB uses Python identifier HundCaseB
    __HundCaseB = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HundCaseB'), 'HundCaseB', '__AbsentNamespace0_LinearElecCouplingType_HundCaseB', False)

    
    HundCaseB = property(__HundCaseB.value, __HundCaseB.set, None, None)


    _ElementMap = {
        __HyperfineCouplingHundCaseB.name() : __HyperfineCouplingHundCaseB,
        __HyperfineCaseABeta.name() : __HyperfineCaseABeta,
        __Description.name() : __Description,
        __EfSymmetry.name() : __EfSymmetry,
        __HundCaseA.name() : __HundCaseA,
        __HyperfineCaseAAlpha.name() : __HyperfineCaseAAlpha,
        __HundCaseB.name() : __HundCaseB
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LinearElecCouplingType', LinearElecCouplingType)


# Complex type IsotopeType with content type ELEMENT_ONLY
class IsotopeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IsotopeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_IsotopeType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, None)

    
    # Element IsotopeParameters uses Python identifier IsotopeParameters
    __IsotopeParameters = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IsotopeParameters'), 'IsotopeParameters', '__AbsentNamespace0_IsotopeType_IsotopeParameters', False)

    
    IsotopeParameters = property(__IsotopeParameters.value, __IsotopeParameters.set, None, u'Parameters of a specific isotope')

    
    # Element IonState uses Python identifier IonState
    __IonState = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IonState'), 'IonState', '__AbsentNamespace0_IsotopeType_IonState', True)

    
    IonState = property(__IonState.value, __IonState.set, None, u'List of ionization states')


    _ElementMap = {
        __Comments.name() : __Comments,
        __IsotopeParameters.name() : __IsotopeParameters,
        __IonState.name() : __IonState
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'IsotopeType', IsotopeType)


# Complex type HinderedMotionType with content type ELEMENT_ONLY
class HinderedMotionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HinderedMotionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element HinderedK1 uses Python identifier HinderedK1
    __HinderedK1 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HinderedK1'), 'HinderedK1', '__AbsentNamespace0_HinderedMotionType_HinderedK1', False)

    
    HinderedK1 = property(__HinderedK1.value, __HinderedK1.set, None, None)

    
    # Element HinderedK2 uses Python identifier HinderedK2
    __HinderedK2 = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HinderedK2'), 'HinderedK2', '__AbsentNamespace0_HinderedMotionType_HinderedK2', False)

    
    HinderedK2 = property(__HinderedK2.value, __HinderedK2.set, None, None)


    _ElementMap = {
        __HinderedK1.name() : __HinderedK1,
        __HinderedK2.name() : __HinderedK2
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'HinderedMotionType', HinderedMotionType)


# Complex type IonStateType with content type ELEMENT_ONLY
class IonStateType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IonStateType')
    # Base type is PrimaryType
    
    # Element IonCharge uses Python identifier IonCharge
    __IonCharge = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IonCharge'), 'IonCharge', '__AbsentNamespace0_IonStateType_IonCharge', False)

    
    IonCharge = property(__IonCharge.value, __IonCharge.set, None, u'Ion charge. Example: 12.')

    
    # Element AtomicState uses Python identifier AtomicState
    __AtomicState = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AtomicState'), 'AtomicState', '__AbsentNamespace0_IonStateType_AtomicState', True)

    
    AtomicState = property(__AtomicState.value, __AtomicState.set, None, u'List of atomic states within an ion')

    
    # Element IsoelectronicSequence uses Python identifier IsoelectronicSequence
    __IsoelectronicSequence = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IsoelectronicSequence'), 'IsoelectronicSequence', '__AbsentNamespace0_IonStateType_IsoelectronicSequence', False)

    
    IsoelectronicSequence = property(__IsoelectronicSequence.value, __IsoelectronicSequence.set, None, u'Chemical element representation of isoelectronic sequence. Example: He.')

    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __IonCharge.name() : __IonCharge,
        __AtomicState.name() : __AtomicState,
        __IsoelectronicSequence.name() : __IsoelectronicSequence
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'IonStateType', IonStateType)


# Complex type MaterialComponentType with content type ELEMENT_ONLY
class MaterialComponentType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MaterialComponentType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Percentage uses Python identifier Percentage
    __Percentage = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Percentage'), 'Percentage', '__AbsentNamespace0_MaterialComponentType_Percentage', False)

    
    Percentage = property(__Percentage.value, __Percentage.set, None, None)

    
    # Element ChemicalElement uses Python identifier ChemicalElement
    __ChemicalElement = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ChemicalElement'), 'ChemicalElement', '__AbsentNamespace0_MaterialComponentType_ChemicalElement', False)

    
    ChemicalElement = property(__ChemicalElement.value, __ChemicalElement.set, None, None)

    
    # Element StoichiometricValue uses Python identifier StoichiometricValue
    __StoichiometricValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StoichiometricValue'), 'StoichiometricValue', '__AbsentNamespace0_MaterialComponentType_StoichiometricValue', False)

    
    StoichiometricValue = property(__StoichiometricValue.value, __StoichiometricValue.set, None, None)


    _ElementMap = {
        __Percentage.name() : __Percentage,
        __ChemicalElement.name() : __ChemicalElement,
        __StoichiometricValue.name() : __StoichiometricValue
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MaterialComponentType', MaterialComponentType)


# Complex type ArgumentType with content type ELEMENT_ONLY
class ArgumentType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ArgumentType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__AbsentNamespace0_ArgumentType_Name', False)

    
    Name = property(__Name.value, __Name.set, None, u'Name of the argument. Example: a')

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_ArgumentType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, u'Further description of the argument if definition in `parameter` is not sufficient')

    
    # Attribute parameter uses Python identifier parameter
    __parameter = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'parameter'), 'parameter', '__AbsentNamespace0_ArgumentType_parameter', pyxb.binding.datatypes.anySimpleType)
    
    parameter = property(__parameter.value, __parameter.set, None, u'type of units (surface, energy, time...)')

    
    # Attribute units uses Python identifier units
    __units = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'units'), 'units', '__AbsentNamespace0_ArgumentType_units', STD_ANON_4, required=True)
    
    units = property(__units.value, __units.set, None, u'Description of physical units. Use "unitless" for dimensionless quantities.')


    _ElementMap = {
        __Name.name() : __Name,
        __Description.name() : __Description
    }
    _AttributeMap = {
        __parameter.name() : __parameter,
        __units.name() : __units
    }
Namespace.addCategoryObject('typeBinding', u'ArgumentType', ArgumentType)


# Complex type OrbitalAngularMomentumType with content type ELEMENT_ONLY
class OrbitalAngularMomentumType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OrbitalAngularMomentumType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Value uses Python identifier Value
    __Value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Value'), 'Value', '__AbsentNamespace0_OrbitalAngularMomentumType_Value', False)

    
    Value = property(__Value.value, __Value.set, None, u'Value of the orbital angular momentum')

    
    # Element Symbol uses Python identifier Symbol
    __Symbol = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Symbol'), 'Symbol', '__AbsentNamespace0_OrbitalAngularMomentumType_Symbol', False)

    
    Symbol = property(__Symbol.value, __Symbol.set, None, u'Symbol of the orbital angular momentum')


    _ElementMap = {
        __Value.name() : __Value,
        __Symbol.name() : __Symbol
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'OrbitalAngularMomentumType', OrbitalAngularMomentumType)


# Complex type jKCouplingType with content type ELEMENT_ONLY
class jKCouplingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'jKCouplingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element j uses Python identifier j
    __j = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'j'), 'j', '__AbsentNamespace0_jKCouplingType_j', False)

    
    j = property(__j.value, __j.set, None, u'Value of the total angular momentum of the core')

    
    # Element K uses Python identifier K
    __K = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'K'), 'K', '__AbsentNamespace0_jKCouplingType_K', False)

    
    K = property(__K.value, __K.set, None, u'Value of the K-number (j + orbital angular momentum of the external electron)')


    _ElementMap = {
        __j.name() : __j,
        __K.name() : __K
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'jKCouplingType', jKCouplingType)


# Complex type AtomicStateType with content type ELEMENT_ONLY
class AtomicStateType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomicStateType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element AtomicNumericalData uses Python identifier AtomicNumericalData
    __AtomicNumericalData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AtomicNumericalData'), 'AtomicNumericalData', '__AbsentNamespace0_AtomicStateType_AtomicNumericalData', False)

    
    AtomicNumericalData = property(__AtomicNumericalData.value, __AtomicNumericalData.set, None, u'Numerical parameters describing an atomic state')

    
    # Element AtomicComposition uses Python identifier AtomicComposition
    __AtomicComposition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AtomicComposition'), 'AtomicComposition', '__AbsentNamespace0_AtomicStateType_AtomicComposition', False)

    
    AtomicComposition = property(__AtomicComposition.value, __AtomicComposition.set, None, u'Expansion of the wavefunction in a specific basis')

    
    # Element AtomicQuantumNumbers uses Python identifier AtomicQuantumNumbers
    __AtomicQuantumNumbers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AtomicQuantumNumbers'), 'AtomicQuantumNumbers', '__AbsentNamespace0_AtomicStateType_AtomicQuantumNumbers', False)

    
    AtomicQuantumNumbers = property(__AtomicQuantumNumbers.value, __AtomicQuantumNumbers.set, None, u'Discrete quantum numbers describing an atomic state')

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_AtomicStateType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, u'An arbitrary label')

    
    # Attribute methodRef inherited from PrimaryType
    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute stateID uses Python identifier stateID
    __stateID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'stateID'), 'stateID', '__AbsentNamespace0_AtomicStateType_stateID', STD_ANON_3, required=True)
    
    stateID = property(__stateID.value, __stateID.set, None, u'ID for a specific state/particle.')


    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __AtomicNumericalData.name() : __AtomicNumericalData,
        __AtomicComposition.name() : __AtomicComposition,
        __AtomicQuantumNumbers.name() : __AtomicQuantumNumbers,
        __Description.name() : __Description
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        __stateID.name() : __stateID
    })
Namespace.addCategoryObject('typeBinding', u'AtomicStateType', AtomicStateType)


# Complex type NonLinearNoElecHyperFType with content type ELEMENT_ONLY
class NonLinearNoElecHyperFType (NonLinearNoElecType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonLinearNoElecHyperFType')
    # Base type is NonLinearNoElecType
    
    # Element TotalAngularMomentumN (TotalAngularMomentumN) inherited from NonLinearNoElecType
    
    # Element C2Symmetries (C2Symmetries) inherited from NonLinearNoElecType
    
    # Element MolecularProjection (MolecularProjection) inherited from NonLinearNoElecType
    
    # Element HyperfineQuantumNumbers uses Python identifier HyperfineQuantumNumbers
    __HyperfineQuantumNumbers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), 'HyperfineQuantumNumbers', '__AbsentNamespace0_NonLinearNoElecHyperFType_HyperfineQuantumNumbers', False)

    
    HyperfineQuantumNumbers = property(__HyperfineQuantumNumbers.value, __HyperfineQuantumNumbers.set, None, None)


    _ElementMap = NonLinearNoElecType._ElementMap.copy()
    _ElementMap.update({
        __HyperfineQuantumNumbers.name() : __HyperfineQuantumNumbers
    })
    _AttributeMap = NonLinearNoElecType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NonLinearNoElecHyperFType', NonLinearNoElecHyperFType)


# Complex type DiatomAndLinearPolyatomicType with content type ELEMENT_ONLY
class DiatomAndLinearPolyatomicType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DiatomAndLinearPolyatomicType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LinearNoElecHyperF uses Python identifier LinearNoElecHyperF
    __LinearNoElecHyperF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LinearNoElecHyperF'), 'LinearNoElecHyperF', '__AbsentNamespace0_DiatomAndLinearPolyatomicType_LinearNoElecHyperF', False)

    
    LinearNoElecHyperF = property(__LinearNoElecHyperF.value, __LinearNoElecHyperF.set, None, None)

    
    # Element LinearNoElecNoHyperF uses Python identifier LinearNoElecNoHyperF
    __LinearNoElecNoHyperF = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LinearNoElecNoHyperF'), 'LinearNoElecNoHyperF', '__AbsentNamespace0_DiatomAndLinearPolyatomicType_LinearNoElecNoHyperF', False)

    
    LinearNoElecNoHyperF = property(__LinearNoElecNoHyperF.value, __LinearNoElecNoHyperF.set, None, None)

    
    # Element LinearElecCoupling uses Python identifier LinearElecCoupling
    __LinearElecCoupling = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LinearElecCoupling'), 'LinearElecCoupling', '__AbsentNamespace0_DiatomAndLinearPolyatomicType_LinearElecCoupling', False)

    
    LinearElecCoupling = property(__LinearElecCoupling.value, __LinearElecCoupling.set, None, None)


    _ElementMap = {
        __LinearNoElecHyperF.name() : __LinearNoElecHyperF,
        __LinearNoElecNoHyperF.name() : __LinearNoElecNoHyperF,
        __LinearElecCoupling.name() : __LinearElecCoupling
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DiatomAndLinearPolyatomicType', DiatomAndLinearPolyatomicType)


# Complex type AtomicCoreType with content type ELEMENT_ONLY
class AtomicCoreType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomicCoreType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TotalAngularMomentum uses Python identifier TotalAngularMomentum
    __TotalAngularMomentum = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'), 'TotalAngularMomentum', '__AbsentNamespace0_AtomicCoreType_TotalAngularMomentum', False)

    
    TotalAngularMomentum = property(__TotalAngularMomentum.value, __TotalAngularMomentum.set, None, u'Total angular momentum of the core')

    
    # Element Term uses Python identifier Term
    __Term = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Term'), 'Term', '__AbsentNamespace0_AtomicCoreType_Term', False)

    
    Term = property(__Term.value, __Term.set, None, u'Term of the core')

    
    # Element Configuration uses Python identifier Configuration
    __Configuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Configuration'), 'Configuration', '__AbsentNamespace0_AtomicCoreType_Configuration', False)

    
    Configuration = property(__Configuration.value, __Configuration.set, None, u'Configuration of the core')

    
    # Element ElementCore uses Python identifier ElementCore
    __ElementCore = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ElementCore'), 'ElementCore', '__AbsentNamespace0_AtomicCoreType_ElementCore', False)

    
    ElementCore = property(__ElementCore.value, __ElementCore.set, None, u'Isoelectronic atom of the core. Example: Xe')


    _ElementMap = {
        __TotalAngularMomentum.name() : __TotalAngularMomentum,
        __Term.name() : __Term,
        __Configuration.name() : __Configuration,
        __ElementCore.name() : __ElementCore
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AtomicCoreType', AtomicCoreType)


# Complex type MolecularStateCharacterisationType with content type ELEMENT_ONLY
class MolecularStateCharacterisationType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MolecularStateCharacterisationType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Parameters uses Python identifier Parameters
    __Parameters = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parameters'), 'Parameters', '__AbsentNamespace0_MolecularStateCharacterisationType_Parameters', True)

    
    Parameters = property(__Parameters.value, __Parameters.set, None, None)

    
    # Element StateEnergy uses Python identifier StateEnergy
    __StateEnergy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StateEnergy'), 'StateEnergy', '__AbsentNamespace0_MolecularStateCharacterisationType_StateEnergy', False)

    
    StateEnergy = property(__StateEnergy.value, __StateEnergy.set, None, None)

    
    # Element TotalStatisticalWeight uses Python identifier TotalStatisticalWeight
    __TotalStatisticalWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'), 'TotalStatisticalWeight', '__AbsentNamespace0_MolecularStateCharacterisationType_TotalStatisticalWeight', False)

    
    TotalStatisticalWeight = property(__TotalStatisticalWeight.value, __TotalStatisticalWeight.set, None, None)

    
    # Element NuclearStatisticalWeight uses Python identifier NuclearStatisticalWeight
    __NuclearStatisticalWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'), 'NuclearStatisticalWeight', '__AbsentNamespace0_MolecularStateCharacterisationType_NuclearStatisticalWeight', False)

    
    NuclearStatisticalWeight = property(__NuclearStatisticalWeight.value, __NuclearStatisticalWeight.set, None, None)

    
    # Element NuclearSpinSymmetry uses Python identifier NuclearSpinSymmetry
    __NuclearSpinSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'), 'NuclearSpinSymmetry', '__AbsentNamespace0_MolecularStateCharacterisationType_NuclearSpinSymmetry', False)

    
    NuclearSpinSymmetry = property(__NuclearSpinSymmetry.value, __NuclearSpinSymmetry.set, None, None)

    
    # Element LifeTime uses Python identifier LifeTime
    __LifeTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LifeTime'), 'LifeTime', '__AbsentNamespace0_MolecularStateCharacterisationType_LifeTime', False)

    
    LifeTime = property(__LifeTime.value, __LifeTime.set, None, None)


    _ElementMap = {
        __Parameters.name() : __Parameters,
        __StateEnergy.name() : __StateEnergy,
        __TotalStatisticalWeight.name() : __TotalStatisticalWeight,
        __NuclearStatisticalWeight.name() : __NuclearStatisticalWeight,
        __NuclearSpinSymmetry.name() : __NuclearSpinSymmetry,
        __LifeTime.name() : __LifeTime
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MolecularStateCharacterisationType', MolecularStateCharacterisationType)


# Complex type AtomsType with content type ELEMENT_ONLY
class AtomsType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomsType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Atom uses Python identifier Atom
    __Atom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Atom'), 'Atom', '__AbsentNamespace0_AtomsType_Atom', True)

    
    Atom = property(__Atom.value, __Atom.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Atom.name() : __Atom
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AtomsType', AtomsType)


# Complex type RotationalHomeType with content type ELEMENT_ONLY
class RotationalHomeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RotationalHomeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_RotationalHomeType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, None)

    
    # Element Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comment'), 'Comment', '__AbsentNamespace0_RotationalHomeType_Comment', False)

    
    Comment = property(__Comment.value, __Comment.set, None, None)

    
    # Element RotationalCharacterisation uses Python identifier RotationalCharacterisation
    __RotationalCharacterisation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RotationalCharacterisation'), 'RotationalCharacterisation', '__AbsentNamespace0_RotationalHomeType_RotationalCharacterisation', False)

    
    RotationalCharacterisation = property(__RotationalCharacterisation.value, __RotationalCharacterisation.set, None, None)

    
    # Element RotationalComponent uses Python identifier RotationalComponent
    __RotationalComponent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RotationalComponent'), 'RotationalComponent', '__AbsentNamespace0_RotationalHomeType_RotationalComponent', True)

    
    RotationalComponent = property(__RotationalComponent.value, __RotationalComponent.set, None, None)


    _ElementMap = {
        __Description.name() : __Description,
        __Comment.name() : __Comment,
        __RotationalCharacterisation.name() : __RotationalCharacterisation,
        __RotationalComponent.name() : __RotationalComponent
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'RotationalHomeType', RotationalHomeType)


# Complex type RotationalCharacterisationType with content type ELEMENT_ONLY
class RotationalCharacterisationType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RotationalCharacterisationType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element InversionSymmetry uses Python identifier InversionSymmetry
    __InversionSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'InversionSymmetry'), 'InversionSymmetry', '__AbsentNamespace0_RotationalCharacterisationType_InversionSymmetry', False)

    
    InversionSymmetry = property(__InversionSymmetry.value, __InversionSymmetry.set, None, u'corresponds to (a) or (s)')

    
    # Element RovibronicSpeciesNotation uses Python identifier RovibronicSpeciesNotation
    __RovibronicSpeciesNotation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RovibronicSpeciesNotation'), 'RovibronicSpeciesNotation', '__AbsentNamespace0_RotationalCharacterisationType_RovibronicSpeciesNotation', False)

    
    RovibronicSpeciesNotation = property(__RovibronicSpeciesNotation.value, __RovibronicSpeciesNotation.set, None, None)

    
    # Element PermutationSymmetry uses Python identifier PermutationSymmetry
    __PermutationSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PermutationSymmetry'), 'PermutationSymmetry', '__AbsentNamespace0_RotationalCharacterisationType_PermutationSymmetry', False)

    
    PermutationSymmetry = property(__PermutationSymmetry.value, __PermutationSymmetry.set, None, u'corresponds to (a) or (s)')

    
    # Element RovibrationalSpeciesNotation uses Python identifier RovibrationalSpeciesNotation
    __RovibrationalSpeciesNotation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RovibrationalSpeciesNotation'), 'RovibrationalSpeciesNotation', '__AbsentNamespace0_RotationalCharacterisationType_RovibrationalSpeciesNotation', False)

    
    RovibrationalSpeciesNotation = property(__RovibrationalSpeciesNotation.value, __RovibrationalSpeciesNotation.set, None, None)

    
    # Element RovibronicAngularMomentumP uses Python identifier RovibronicAngularMomentumP
    __RovibronicAngularMomentumP = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RovibronicAngularMomentumP'), 'RovibronicAngularMomentumP', '__AbsentNamespace0_RotationalCharacterisationType_RovibronicAngularMomentumP', False)

    
    RovibronicAngularMomentumP = property(__RovibronicAngularMomentumP.value, __RovibronicAngularMomentumP.set, None, None)


    _ElementMap = {
        __InversionSymmetry.name() : __InversionSymmetry,
        __RovibronicSpeciesNotation.name() : __RovibronicSpeciesNotation,
        __PermutationSymmetry.name() : __PermutationSymmetry,
        __RovibrationalSpeciesNotation.name() : __RovibrationalSpeciesNotation,
        __RovibronicAngularMomentumP.name() : __RovibronicAngularMomentumP
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'RotationalCharacterisationType', RotationalCharacterisationType)


# Complex type RadiativeType with content type ELEMENT_ONLY
class RadiativeType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RadiativeType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element RadiativeTransition uses Python identifier RadiativeTransition
    __RadiativeTransition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RadiativeTransition'), 'RadiativeTransition', '__AbsentNamespace0_RadiativeType_RadiativeTransition', True)

    
    RadiativeTransition = property(__RadiativeTransition.value, __RadiativeTransition.set, None, u'Description of a specific radiative transition')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __RadiativeTransition.name() : __RadiativeTransition
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'RadiativeType', RadiativeType)


# Complex type CentralSymbolType with content type SIMPLE
class CentralSymbolType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CentralSymbolType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute LowerRightValue uses Python identifier LowerRightValue
    __LowerRightValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LowerRightValue'), 'LowerRightValue', '__AbsentNamespace0_CentralSymbolType_LowerRightValue', pyxb.binding.datatypes.string)
    
    LowerRightValue = property(__LowerRightValue.value, __LowerRightValue.set, None, None)

    
    # Attribute UpperRightValue uses Python identifier UpperRightValue
    __UpperRightValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'UpperRightValue'), 'UpperRightValue', '__AbsentNamespace0_CentralSymbolType_UpperRightValue', pyxb.binding.datatypes.string)
    
    UpperRightValue = property(__UpperRightValue.value, __UpperRightValue.set, None, None)

    
    # Attribute UpperLeftValue uses Python identifier UpperLeftValue
    __UpperLeftValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'UpperLeftValue'), 'UpperLeftValue', '__AbsentNamespace0_CentralSymbolType_UpperLeftValue', pyxb.binding.datatypes.string)
    
    UpperLeftValue = property(__UpperLeftValue.value, __UpperLeftValue.set, None, None)

    
    # Attribute LowerLeftValue uses Python identifier LowerLeftValue
    __LowerLeftValue = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'LowerLeftValue'), 'LowerLeftValue', '__AbsentNamespace0_CentralSymbolType_LowerLeftValue', pyxb.binding.datatypes.string)
    
    LowerLeftValue = property(__LowerLeftValue.value, __LowerLeftValue.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __LowerRightValue.name() : __LowerRightValue,
        __UpperRightValue.name() : __UpperRightValue,
        __UpperLeftValue.name() : __UpperLeftValue,
        __LowerLeftValue.name() : __LowerLeftValue
    }
Namespace.addCategoryObject('typeBinding', u'CentralSymbolType', CentralSymbolType)


# Complex type ElectronicComponentType with content type ELEMENT_ONLY
class ElectronicComponentType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ElectronicComponentType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_ElectronicComponentType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, None)

    
    # Element TotalMolecularProjectionL uses Python identifier TotalMolecularProjectionL
    __TotalMolecularProjectionL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionL'), 'TotalMolecularProjectionL', '__AbsentNamespace0_ElectronicComponentType_TotalMolecularProjectionL', False)

    
    TotalMolecularProjectionL = property(__TotalMolecularProjectionL.value, __TotalMolecularProjectionL.set, None, None)

    
    # Element Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comment'), 'Comment', '__AbsentNamespace0_ElectronicComponentType_Comment', False)

    
    Comment = property(__Comment.value, __Comment.set, None, None)

    
    # Element SerialQuantumNumber uses Python identifier SerialQuantumNumber
    __SerialQuantumNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'), 'SerialQuantumNumber', '__AbsentNamespace0_ElectronicComponentType_SerialQuantumNumber', False)

    
    SerialQuantumNumber = property(__SerialQuantumNumber.value, __SerialQuantumNumber.set, None, None)

    
    # Element MixingCoefficient uses Python identifier MixingCoefficient
    __MixingCoefficient = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), 'MixingCoefficient', '__AbsentNamespace0_ElectronicComponentType_MixingCoefficient', False)

    
    MixingCoefficient = property(__MixingCoefficient.value, __MixingCoefficient.set, None, None)

    
    # Element ElectronicCharacterisation uses Python identifier ElectronicCharacterisation
    __ElectronicCharacterisation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ElectronicCharacterisation'), 'ElectronicCharacterisation', '__AbsentNamespace0_ElectronicComponentType_ElectronicCharacterisation', False)

    
    ElectronicCharacterisation = property(__ElectronicCharacterisation.value, __ElectronicCharacterisation.set, None, None)

    
    # Element VibrationalHome uses Python identifier VibrationalHome
    __VibrationalHome = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibrationalHome'), 'VibrationalHome', '__AbsentNamespace0_ElectronicComponentType_VibrationalHome', False)

    
    VibrationalHome = property(__VibrationalHome.value, __VibrationalHome.set, None, None)


    _ElementMap = {
        __Description.name() : __Description,
        __TotalMolecularProjectionL.name() : __TotalMolecularProjectionL,
        __Comment.name() : __Comment,
        __SerialQuantumNumber.name() : __SerialQuantumNumber,
        __MixingCoefficient.name() : __MixingCoefficient,
        __ElectronicCharacterisation.name() : __ElectronicCharacterisation,
        __VibrationalHome.name() : __VibrationalHome
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ElectronicComponentType', ElectronicComponentType)


# Complex type AtomicCompositionType with content type ELEMENT_ONLY
class AtomicCompositionType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomicCompositionType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Component uses Python identifier Component
    __Component = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Component'), 'Component', '__AbsentNamespace0_AtomicCompositionType_Component', True)

    
    Component = property(__Component.value, __Component.set, None, u'Component of the state wavefunction')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Component.name() : __Component
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AtomicCompositionType', AtomicCompositionType)


# Complex type MoleculeNuclearSpinsType with content type ELEMENT_ONLY
class MoleculeNuclearSpinsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MoleculeNuclearSpinsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element AtomArray uses Python identifier AtomArray
    __AtomArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AtomArray'), 'AtomArray', '__AbsentNamespace0_MoleculeNuclearSpinsType_AtomArray', False)

    
    AtomArray = property(__AtomArray.value, __AtomArray.set, None, None)

    
    # Element BondArray uses Python identifier BondArray
    __BondArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'BondArray'), 'BondArray', '__AbsentNamespace0_MoleculeNuclearSpinsType_BondArray', False)

    
    BondArray = property(__BondArray.value, __BondArray.set, None, None)


    _ElementMap = {
        __AtomArray.name() : __AtomArray,
        __BondArray.name() : __BondArray
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MoleculeNuclearSpinsType', MoleculeNuclearSpinsType)


# Complex type BondArrayType with content type ELEMENT_ONLY
class BondArrayType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BondArrayType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Bond uses Python identifier Bond
    __Bond = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Bond'), 'Bond', '__AbsentNamespace0_BondArrayType_Bond', True)

    
    Bond = property(__Bond.value, __Bond.set, None, None)


    _ElementMap = {
        __Bond.name() : __Bond
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'BondArrayType', BondArrayType)


# Complex type MolecularPropertiesType with content type ELEMENT_ONLY
class MolecularPropertiesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MolecularPropertiesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element MolecularWeight uses Python identifier MolecularWeight
    __MolecularWeight = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MolecularWeight'), 'MolecularWeight', '__AbsentNamespace0_MolecularPropertiesType_MolecularWeight', False)

    
    MolecularWeight = property(__MolecularWeight.value, __MolecularWeight.set, None, None)

    
    # Element OtherProperties uses Python identifier OtherProperties
    __OtherProperties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'OtherProperties'), 'OtherProperties', '__AbsentNamespace0_MolecularPropertiesType_OtherProperties', True)

    
    OtherProperties = property(__OtherProperties.value, __OtherProperties.set, None, None)


    _ElementMap = {
        __MolecularWeight.name() : __MolecularWeight,
        __OtherProperties.name() : __OtherProperties
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MolecularPropertiesType', MolecularPropertiesType)


# Complex type MolecularChemicalSpeciesType with content type ELEMENT_ONLY
class MolecularChemicalSpeciesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MolecularChemicalSpeciesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element StableMolecularProperties uses Python identifier StableMolecularProperties
    __StableMolecularProperties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'), 'StableMolecularProperties', '__AbsentNamespace0_MolecularChemicalSpeciesType_StableMolecularProperties', False)

    
    StableMolecularProperties = property(__StableMolecularProperties.value, __StableMolecularProperties.set, None, None)

    
    # Element URLFigure uses Python identifier URLFigure
    __URLFigure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'URLFigure'), 'URLFigure', '__AbsentNamespace0_MolecularChemicalSpeciesType_URLFigure', False)

    
    URLFigure = property(__URLFigure.value, __URLFigure.set, None, None)

    
    # Element InChI uses Python identifier InChI
    __InChI = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'InChI'), 'InChI', '__AbsentNamespace0_MolecularChemicalSpeciesType_InChI', False)

    
    InChI = property(__InChI.value, __InChI.set, None, None)

    
    # Element IUPACName uses Python identifier IUPACName
    __IUPACName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IUPACName'), 'IUPACName', '__AbsentNamespace0_MolecularChemicalSpeciesType_IUPACName', False)

    
    IUPACName = property(__IUPACName.value, __IUPACName.set, None, None)

    
    # Element CASRegistryNumber uses Python identifier CASRegistryNumber
    __CASRegistryNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'), 'CASRegistryNumber', '__AbsentNamespace0_MolecularChemicalSpeciesType_CASRegistryNumber', False)

    
    CASRegistryNumber = property(__CASRegistryNumber.value, __CASRegistryNumber.set, None, None)

    
    # Element OrdinaryStructuralFormula uses Python identifier OrdinaryStructuralFormula
    __OrdinaryStructuralFormula = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'OrdinaryStructuralFormula'), 'OrdinaryStructuralFormula', '__AbsentNamespace0_MolecularChemicalSpeciesType_OrdinaryStructuralFormula', False)

    
    OrdinaryStructuralFormula = property(__OrdinaryStructuralFormula.value, __OrdinaryStructuralFormula.set, None, None)

    
    # Element CNPIGroup uses Python identifier CNPIGroup
    __CNPIGroup = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CNPIGroup'), 'CNPIGroup', '__AbsentNamespace0_MolecularChemicalSpeciesType_CNPIGroup', False)

    
    CNPIGroup = property(__CNPIGroup.value, __CNPIGroup.set, None, None)

    
    # Element ChemicalName uses Python identifier ChemicalName
    __ChemicalName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ChemicalName'), 'ChemicalName', '__AbsentNamespace0_MolecularChemicalSpeciesType_ChemicalName', False)

    
    ChemicalName = property(__ChemicalName.value, __ChemicalName.set, None, None)

    
    # Element MoleculeNuclearSpins uses Python identifier MoleculeNuclearSpins
    __MoleculeNuclearSpins = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'), 'MoleculeNuclearSpins', '__AbsentNamespace0_MolecularChemicalSpeciesType_MoleculeNuclearSpins', False)

    
    MoleculeNuclearSpins = property(__MoleculeNuclearSpins.value, __MoleculeNuclearSpins.set, None, None)

    
    # Element StoichiometricFormula uses Python identifier StoichiometricFormula
    __StoichiometricFormula = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'StoichiometricFormula'), 'StoichiometricFormula', '__AbsentNamespace0_MolecularChemicalSpeciesType_StoichiometricFormula', False)

    
    StoichiometricFormula = property(__StoichiometricFormula.value, __StoichiometricFormula.set, None, None)

    
    # Element IonCharge uses Python identifier IonCharge
    __IonCharge = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'IonCharge'), 'IonCharge', '__AbsentNamespace0_MolecularChemicalSpeciesType_IonCharge', False)

    
    IonCharge = property(__IonCharge.value, __IonCharge.set, None, None)

    
    # Element Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comment'), 'Comment', '__AbsentNamespace0_MolecularChemicalSpeciesType_Comment', False)

    
    Comment = property(__Comment.value, __Comment.set, None, None)


    _ElementMap = {
        __StableMolecularProperties.name() : __StableMolecularProperties,
        __URLFigure.name() : __URLFigure,
        __InChI.name() : __InChI,
        __IUPACName.name() : __IUPACName,
        __CASRegistryNumber.name() : __CASRegistryNumber,
        __OrdinaryStructuralFormula.name() : __OrdinaryStructuralFormula,
        __CNPIGroup.name() : __CNPIGroup,
        __ChemicalName.name() : __ChemicalName,
        __MoleculeNuclearSpins.name() : __MoleculeNuclearSpins,
        __StoichiometricFormula.name() : __StoichiometricFormula,
        __IonCharge.name() : __IonCharge,
        __Comment.name() : __Comment
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MolecularChemicalSpeciesType', MolecularChemicalSpeciesType)


# Complex type ParametersType with content type ELEMENT_ONLY
class ParametersType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ParametersType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Parameter uses Python identifier Parameter
    __Parameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parameter'), 'Parameter', '__AbsentNamespace0_ParametersType_Parameter', True)

    
    Parameter = property(__Parameter.value, __Parameter.set, None, None)


    _ElementMap = {
        __Parameter.name() : __Parameter
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ParametersType', ParametersType)


# Complex type FunctionType with content type ELEMENT_ONLY
class FunctionType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FunctionType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__AbsentNamespace0_FunctionType_Name', False)

    
    Name = property(__Name.value, __Name.set, None, u'Function name. Example: BELI')

    
    # Element SourceCodeURL uses Python identifier SourceCodeURL
    __SourceCodeURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SourceCodeURL'), 'SourceCodeURL', '__AbsentNamespace0_FunctionType_SourceCodeURL', False)

    
    SourceCodeURL = property(__SourceCodeURL.value, __SourceCodeURL.set, None, u'Location of source code ')

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_FunctionType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, u'Description of a function.')

    
    # Element Y uses Python identifier Y
    __Y = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Y'), 'Y', '__AbsentNamespace0_FunctionType_Y', False)

    
    Y = property(__Y.value, __Y.set, None, None)

    
    # Element Arguments uses Python identifier Arguments
    __Arguments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Arguments'), 'Arguments', '__AbsentNamespace0_FunctionType_Arguments', False)

    
    Arguments = property(__Arguments.value, __Arguments.set, None, None)

    
    # Element Expression uses Python identifier Expression
    __Expression = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Expression'), 'Expression', '__AbsentNamespace0_FunctionType_Expression', False)

    
    Expression = property(__Expression.value, __Expression.set, None, u'Function expression in a specified programming language. Example: a*X1**2+2.5 (a is the parameter defined in the "parameters" list).')

    
    # Element Parameters uses Python identifier Parameters
    __Parameters = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parameters'), 'Parameters', '__AbsentNamespace0_FunctionType_Parameters', False)

    
    Parameters = property(__Parameters.value, __Parameters.set, None, u'List of parameters used in the function')

    
    # Element ReferenceFrame uses Python identifier ReferenceFrame
    __ReferenceFrame = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ReferenceFrame'), 'ReferenceFrame', '__AbsentNamespace0_FunctionType_ReferenceFrame', False)

    
    ReferenceFrame = property(__ReferenceFrame.value, __ReferenceFrame.set, None, u'Reference frame in which is given the velocity, energy...')

    
    # Attribute functionID uses Python identifier functionID
    __functionID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'functionID'), 'functionID', '__AbsentNamespace0_FunctionType_functionID', STD_ANON_7, required=True)
    
    functionID = property(__functionID.value, __functionID.set, None, u'ID for a specific function')

    
    # Attribute methodRef inherited from PrimaryType
    
    # Attribute sourceRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Name.name() : __Name,
        __SourceCodeURL.name() : __SourceCodeURL,
        __Description.name() : __Description,
        __Y.name() : __Y,
        __Arguments.name() : __Arguments,
        __Expression.name() : __Expression,
        __Parameters.name() : __Parameters,
        __ReferenceFrame.name() : __ReferenceFrame
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        __functionID.name() : __functionID
    })
Namespace.addCategoryObject('typeBinding', u'FunctionType', FunctionType)


# Complex type SourceType with content type ELEMENT_ONLY
class SourceType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SourceType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element City uses Python identifier City
    __City = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'City'), 'City', '__AbsentNamespace0_SourceType_City', False)

    
    City = property(__City.value, __City.set, None, u'City of publication. Example: Bristol.')

    
    # Element DigitalObjectIdentifier uses Python identifier DigitalObjectIdentifier
    __DigitalObjectIdentifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'DigitalObjectIdentifier'), 'DigitalObjectIdentifier', '__AbsentNamespace0_SourceType_DigitalObjectIdentifier', False)

    
    DigitalObjectIdentifier = property(__DigitalObjectIdentifier.value, __DigitalObjectIdentifier.set, None, u'Digital Object Identifier. Example: doi:10.1016/j.adt.2007.11.003')

    
    # Element Editors uses Python identifier Editors
    __Editors = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Editors'), 'Editors', '__AbsentNamespace0_SourceType_Editors', False)

    
    Editors = property(__Editors.value, __Editors.set, None, None)

    
    # Element SourceName uses Python identifier SourceName
    __SourceName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SourceName'), 'SourceName', '__AbsentNamespace0_SourceType_SourceName', False)

    
    SourceName = property(__SourceName.value, __SourceName.set, None, u'Bibliographic reference name. Example: Physical Review')

    
    # Element Volume uses Python identifier Volume
    __Volume = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Volume'), 'Volume', '__AbsentNamespace0_SourceType_Volume', False)

    
    Volume = property(__Volume.value, __Volume.set, None, u'Volume of the bibliographic reference. Example: 72A')

    
    # Element Title uses Python identifier Title
    __Title = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Title'), 'Title', '__AbsentNamespace0_SourceType_Title', False)

    
    Title = property(__Title.value, __Title.set, None, u'Title')

    
    # Element ProductionDate uses Python identifier ProductionDate
    __ProductionDate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ProductionDate'), 'ProductionDate', '__AbsentNamespace0_SourceType_ProductionDate', False)

    
    ProductionDate = property(__ProductionDate.value, __ProductionDate.set, None, u'Date of the reference')

    
    # Element PageEnd uses Python identifier PageEnd
    __PageEnd = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PageEnd'), 'PageEnd', '__AbsentNamespace0_SourceType_PageEnd', False)

    
    PageEnd = property(__PageEnd.value, __PageEnd.set, None, u'Final page of a bibliographic reference. Example: 23')

    
    # Element Version uses Python identifier Version
    __Version = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Version'), 'Version', '__AbsentNamespace0_SourceType_Version', False)

    
    Version = property(__Version.value, __Version.set, None, u'Version of a database, code, etc.')

    
    # Element Authors uses Python identifier Authors
    __Authors = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Authors'), 'Authors', '__AbsentNamespace0_SourceType_Authors', False)

    
    Authors = property(__Authors.value, __Authors.set, None, None)

    
    # Element UniformResourceIdentifier uses Python identifier UniformResourceIdentifier
    __UniformResourceIdentifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'UniformResourceIdentifier'), 'UniformResourceIdentifier', '__AbsentNamespace0_SourceType_UniformResourceIdentifier', False)

    
    UniformResourceIdentifier = property(__UniformResourceIdentifier.value, __UniformResourceIdentifier.set, None, u'A Uniform Resource Identifier of a bibliographic reference. Example: http://www.iop.org/EJ/abstract/0953-4075/41/10/105002')

    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_SourceType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, None)

    
    # Element Year uses Python identifier Year
    __Year = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Year'), 'Year', '__AbsentNamespace0_SourceType_Year', False)

    
    Year = property(__Year.value, __Year.set, None, u'Year of the bibliographic reference. Example: 2008')

    
    # Element Publisher uses Python identifier Publisher
    __Publisher = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Publisher'), 'Publisher', '__AbsentNamespace0_SourceType_Publisher', False)

    
    Publisher = property(__Publisher.value, __Publisher.set, None, u'Publisher of a bibliographic reference. Example: IOP Publishing Ltd')

    
    # Element Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Category'), 'Category', '__AbsentNamespace0_SourceType_Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'Bibliographic reference type. Example: journal')

    
    # Element PageBegin uses Python identifier PageBegin
    __PageBegin = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PageBegin'), 'PageBegin', '__AbsentNamespace0_SourceType_PageBegin', False)

    
    PageBegin = property(__PageBegin.value, __PageBegin.set, None, u'Initial page of a bibliographic reference. Example: 22')

    
    # Attribute sourceID uses Python identifier sourceID
    __sourceID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(Namespace, u'sourceID'), 'sourceID', '__AbsentNamespace0_SourceType_sourceID', STD_ANON_8, required=True)
    
    sourceID = property(__sourceID.value, __sourceID.set, None, None)


    _ElementMap = {
        __City.name() : __City,
        __DigitalObjectIdentifier.name() : __DigitalObjectIdentifier,
        __Editors.name() : __Editors,
        __SourceName.name() : __SourceName,
        __Volume.name() : __Volume,
        __Title.name() : __Title,
        __ProductionDate.name() : __ProductionDate,
        __PageEnd.name() : __PageEnd,
        __Version.name() : __Version,
        __Authors.name() : __Authors,
        __UniformResourceIdentifier.name() : __UniformResourceIdentifier,
        __Comments.name() : __Comments,
        __Year.name() : __Year,
        __Publisher.name() : __Publisher,
        __Category.name() : __Category,
        __PageBegin.name() : __PageBegin
    }
    _AttributeMap = {
        __sourceID.name() : __sourceID
    }
Namespace.addCategoryObject('typeBinding', u'SourceType', SourceType)


# Complex type FitParametersType with content type ELEMENT_ONLY
class FitParametersType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FitParametersType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Parameter uses Python identifier Parameter
    __Parameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Parameter'), 'Parameter', '__AbsentNamespace0_FitParametersType_Parameter', True)

    
    Parameter = property(__Parameter.value, __Parameter.set, None, None)


    _ElementMap = {
        __Parameter.name() : __Parameter
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'FitParametersType', FitParametersType)


# Complex type VibrationalHomeType with content type ELEMENT_ONLY
class VibrationalHomeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VibrationalHomeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Polyad uses Python identifier Polyad
    __Polyad = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Polyad'), 'Polyad', '__AbsentNamespace0_VibrationalHomeType_Polyad', False)

    
    Polyad = property(__Polyad.value, __Polyad.set, None, None)

    
    # Element VibrationalComponent uses Python identifier VibrationalComponent
    __VibrationalComponent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibrationalComponent'), 'VibrationalComponent', '__AbsentNamespace0_VibrationalHomeType_VibrationalComponent', True)

    
    VibrationalComponent = property(__VibrationalComponent.value, __VibrationalComponent.set, None, None)


    _ElementMap = {
        __Polyad.name() : __Polyad,
        __VibrationalComponent.name() : __VibrationalComponent
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'VibrationalHomeType', VibrationalHomeType)


# Complex type ShellsType with content type ELEMENT_ONLY
class ShellsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ShellsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Shell uses Python identifier Shell
    __Shell = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Shell'), 'Shell', '__AbsentNamespace0_ShellsType_Shell', True)

    
    Shell = property(__Shell.value, __Shell.set, None, u'Atomic shell')

    
    # Element ShellPair uses Python identifier ShellPair
    __ShellPair = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ShellPair'), 'ShellPair', '__AbsentNamespace0_ShellsType_ShellPair', True)

    
    ShellPair = property(__ShellPair.value, __ShellPair.set, None, None)


    _ElementMap = {
        __Shell.name() : __Shell,
        __ShellPair.name() : __ShellPair
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ShellsType', ShellsType)


# Complex type LinearNoElecNoHyperFType with content type ELEMENT_ONLY
class LinearNoElecNoHyperFType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LinearNoElecNoHyperFType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element TotalAngularMomentumN uses Python identifier TotalAngularMomentumN
    __TotalAngularMomentumN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), 'TotalAngularMomentumN', '__AbsentNamespace0_LinearNoElecNoHyperFType_TotalAngularMomentumN', False)

    
    TotalAngularMomentumN = property(__TotalAngularMomentumN.value, __TotalAngularMomentumN.set, None, None)

    
    # Element TotalMagneticQuantumNumberN uses Python identifier TotalMagneticQuantumNumberN
    __TotalMagneticQuantumNumberN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberN'), 'TotalMagneticQuantumNumberN', '__AbsentNamespace0_LinearNoElecNoHyperFType_TotalMagneticQuantumNumberN', False)

    
    TotalMagneticQuantumNumberN = property(__TotalMagneticQuantumNumberN.value, __TotalMagneticQuantumNumberN.set, None, None)


    _ElementMap = {
        __TotalAngularMomentumN.name() : __TotalAngularMomentumN,
        __TotalMagneticQuantumNumberN.name() : __TotalMagneticQuantumNumberN
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LinearNoElecNoHyperFType', LinearNoElecNoHyperFType)


# Complex type jjCouplingType with content type ELEMENT_ONLY
class jjCouplingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'jjCouplingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element j uses Python identifier j
    __j = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'j'), 'j', '__AbsentNamespace0_jjCouplingType_j', True)

    
    j = property(__j.value, __j.set, None, u'Value of the total angular momentum')


    _ElementMap = {
        __j.name() : __j
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'jjCouplingType', jjCouplingType)


# Complex type AuthorType with content type ELEMENT_ONLY
class AuthorType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AuthorType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__AbsentNamespace0_AuthorType_Name', False)

    
    Name = property(__Name.value, __Name.set, None, u"Author's name. Example: A. Einstein")

    
    # Element Address uses Python identifier Address
    __Address = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Address'), 'Address', '__AbsentNamespace0_AuthorType_Address', False)

    
    Address = property(__Address.value, __Address.set, None, u"Author's address. Example: AMD Unit, IAEA, Vienna, Austria")


    _ElementMap = {
        __Name.name() : __Name,
        __Address.name() : __Address
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AuthorType', AuthorType)


# Complex type TotalSpinMomentumSType with content type SIMPLE
class TotalSpinMomentumSType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = AngularMomentumType
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TotalSpinMomentumSType')
    # Base type is AngularMomentumType
    
    # Attribute electronicSpinId uses Python identifier electronicSpinId
    __electronicSpinId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'electronicSpinId'), 'electronicSpinId', '__AbsentNamespace0_TotalSpinMomentumSType_electronicSpinId', pyxb.binding.datatypes.ID)
    
    electronicSpinId = property(__electronicSpinId.value, __electronicSpinId.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __electronicSpinId.name() : __electronicSpinId
    }
Namespace.addCategoryObject('typeBinding', u'TotalSpinMomentumSType', TotalSpinMomentumSType)


# Complex type EditorsType with content type ELEMENT_ONLY
class EditorsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'EditorsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__AbsentNamespace0_EditorsType_Name', True)

    
    Name = property(__Name.value, __Name.set, None, u'Name of an editor')


    _ElementMap = {
        __Name.name() : __Name
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'EditorsType', EditorsType)


# Complex type FitDataType with content type ELEMENT_ONLY
class FitDataType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FitDataType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element PhysicalUncertainty uses Python identifier PhysicalUncertainty
    __PhysicalUncertainty = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'), 'PhysicalUncertainty', '__AbsentNamespace0_FitDataType_PhysicalUncertainty', False)

    
    PhysicalUncertainty = property(__PhysicalUncertainty.value, __PhysicalUncertainty.set, None, u'Description of physical uncertainty')

    
    # Element FitAccuracy uses Python identifier FitAccuracy
    __FitAccuracy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FitAccuracy'), 'FitAccuracy', '__AbsentNamespace0_FitDataType_FitAccuracy', False)

    
    FitAccuracy = property(__FitAccuracy.value, __FitAccuracy.set, None, u'Description of fit accuracy')

    
    # Element FunctionRef uses Python identifier FunctionRef
    __FunctionRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FunctionRef'), 'FunctionRef', '__AbsentNamespace0_FitDataType_FunctionRef', False)

    
    FunctionRef = property(__FunctionRef.value, __FunctionRef.set, None, u'Reference to the fitting function')

    
    # Element FitValidityLimits uses Python identifier FitValidityLimits
    __FitValidityLimits = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FitValidityLimits'), 'FitValidityLimits', '__AbsentNamespace0_FitDataType_FitValidityLimits', True)

    
    FitValidityLimits = property(__FitValidityLimits.value, __FitValidityLimits.set, None, u'Limits of the fit validity')

    
    # Element FitParameters uses Python identifier FitParameters
    __FitParameters = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FitParameters'), 'FitParameters', '__AbsentNamespace0_FitDataType_FitParameters', False)

    
    FitParameters = property(__FitParameters.value, __FitParameters.set, None, u'Fitting parameters')

    
    # Element ProductionDate uses Python identifier ProductionDate
    __ProductionDate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ProductionDate'), 'ProductionDate', '__AbsentNamespace0_FitDataType_ProductionDate', False)

    
    ProductionDate = property(__ProductionDate.value, __ProductionDate.set, None, u'Fit production date')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __PhysicalUncertainty.name() : __PhysicalUncertainty,
        __FitAccuracy.name() : __FitAccuracy,
        __FunctionRef.name() : __FunctionRef,
        __FitValidityLimits.name() : __FitValidityLimits,
        __FitParameters.name() : __FitParameters,
        __ProductionDate.name() : __ProductionDate
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'FitDataType', FitDataType)


# Complex type VibrationalComponentType with content type ELEMENT_ONLY
class VibrationalComponentType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VibrationalComponentType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_VibrationalComponentType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, None)

    
    # Element MixingCoefficient uses Python identifier MixingCoefficient
    __MixingCoefficient = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), 'MixingCoefficient', '__AbsentNamespace0_VibrationalComponentType_MixingCoefficient', False)

    
    MixingCoefficient = property(__MixingCoefficient.value, __MixingCoefficient.set, None, None)

    
    # Element SerialQuantumNumber uses Python identifier SerialQuantumNumber
    __SerialQuantumNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'), 'SerialQuantumNumber', '__AbsentNamespace0_VibrationalComponentType_SerialQuantumNumber', False)

    
    SerialQuantumNumber = property(__SerialQuantumNumber.value, __SerialQuantumNumber.set, None, None)

    
    # Element VibrationalCharacterisation uses Python identifier VibrationalCharacterisation
    __VibrationalCharacterisation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibrationalCharacterisation'), 'VibrationalCharacterisation', '__AbsentNamespace0_VibrationalComponentType_VibrationalCharacterisation', False)

    
    VibrationalCharacterisation = property(__VibrationalCharacterisation.value, __VibrationalCharacterisation.set, None, None)

    
    # Element VibrationalQuantumNumbers uses Python identifier VibrationalQuantumNumbers
    __VibrationalQuantumNumbers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'VibrationalQuantumNumbers'), 'VibrationalQuantumNumbers', '__AbsentNamespace0_VibrationalComponentType_VibrationalQuantumNumbers', False)

    
    VibrationalQuantumNumbers = property(__VibrationalQuantumNumbers.value, __VibrationalQuantumNumbers.set, None, None)

    
    # Element RotationalHome uses Python identifier RotationalHome
    __RotationalHome = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RotationalHome'), 'RotationalHome', '__AbsentNamespace0_VibrationalComponentType_RotationalHome', False)

    
    RotationalHome = property(__RotationalHome.value, __RotationalHome.set, None, None)

    
    # Element Comment uses Python identifier Comment
    __Comment = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comment'), 'Comment', '__AbsentNamespace0_VibrationalComponentType_Comment', False)

    
    Comment = property(__Comment.value, __Comment.set, None, None)


    _ElementMap = {
        __Description.name() : __Description,
        __MixingCoefficient.name() : __MixingCoefficient,
        __SerialQuantumNumber.name() : __SerialQuantumNumber,
        __VibrationalCharacterisation.name() : __VibrationalCharacterisation,
        __VibrationalQuantumNumbers.name() : __VibrationalQuantumNumbers,
        __RotationalHome.name() : __RotationalHome,
        __Comment.name() : __Comment
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'VibrationalComponentType', VibrationalComponentType)


# Complex type AtomArrayType with content type ELEMENT_ONLY
class AtomArrayType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomArrayType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element AtomN uses Python identifier AtomN
    __AtomN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'AtomN'), 'AtomN', '__AbsentNamespace0_AtomArrayType_AtomN', True)

    
    AtomN = property(__AtomN.value, __AtomN.set, None, None)


    _ElementMap = {
        __AtomN.name() : __AtomN
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AtomArrayType', AtomArrayType)


# Complex type AtomNType with content type ELEMENT_ONLY
class AtomNType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomNType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Attribute nuclearSpinID uses Python identifier nuclearSpinID
    __nuclearSpinID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'nuclearSpinID'), 'nuclearSpinID', '__AbsentNamespace0_AtomNType_nuclearSpinID', pyxb.binding.datatypes.ID)
    
    nuclearSpinID = property(__nuclearSpinID.value, __nuclearSpinID.set, None, None)

    
    # Attribute hydrogenCount uses Python identifier hydrogenCount
    __hydrogenCount = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'hydrogenCount'), 'hydrogenCount', '__AbsentNamespace0_AtomNType_hydrogenCount', pyxb.binding.datatypes.positiveInteger)
    
    hydrogenCount = property(__hydrogenCount.value, __hydrogenCount.set, None, None)

    
    # Attribute elementSymbol uses Python identifier elementSymbol
    __elementSymbol = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'elementSymbol'), 'elementSymbol', '__AbsentNamespace0_AtomNType_elementSymbol', ElementSymbolType)
    
    elementSymbol = property(__elementSymbol.value, __elementSymbol.set, None, None)

    
    # Attribute methodRef inherited from PrimaryType
    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute isotope uses Python identifier isotope
    __isotope = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'isotope'), 'isotope', '__AbsentNamespace0_AtomNType_isotope', pyxb.binding.datatypes.anySimpleType, unicode_default=u'xs:float')
    
    isotope = property(__isotope.value, __isotope.set, None, None)

    
    # Attribute nuclearSpin uses Python identifier nuclearSpin
    __nuclearSpin = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'nuclearSpin'), 'nuclearSpin', '__AbsentNamespace0_AtomNType_nuclearSpin', AngularMomentumType)
    
    nuclearSpin = property(__nuclearSpin.value, __nuclearSpin.set, None, None)

    
    # Attribute count uses Python identifier count
    __count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__AbsentNamespace0_AtomNType_count', pyxb.binding.datatypes.positiveInteger)
    
    count = property(__count.value, __count.set, None, None)


    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        __nuclearSpinID.name() : __nuclearSpinID,
        __hydrogenCount.name() : __hydrogenCount,
        __elementSymbol.name() : __elementSymbol,
        __isotope.name() : __isotope,
        __nuclearSpin.name() : __nuclearSpin,
        __count.name() : __count
    })
Namespace.addCategoryObject('typeBinding', u'AtomNType', AtomNType)


# Complex type ArgumentsType with content type ELEMENT_ONLY
class ArgumentsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ArgumentsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Argument uses Python identifier Argument
    __Argument = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Argument'), 'Argument', '__AbsentNamespace0_ArgumentsType_Argument', True)

    
    Argument = property(__Argument.value, __Argument.set, None, None)


    _ElementMap = {
        __Argument.name() : __Argument
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ArgumentsType', ArgumentsType)


# Complex type NonLinearElecCouplingType with content type ELEMENT_ONLY
class NonLinearElecCouplingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonLinearElecCouplingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element MolecularProjection uses Python identifier MolecularProjection
    __MolecularProjection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MolecularProjection'), 'MolecularProjection', '__AbsentNamespace0_NonLinearElecCouplingType_MolecularProjection', False)

    
    MolecularProjection = property(__MolecularProjection.value, __MolecularProjection.set, None, None)

    
    # Element TotalAngularMomentumJ uses Python identifier TotalAngularMomentumJ
    __TotalAngularMomentumJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), 'TotalAngularMomentumJ', '__AbsentNamespace0_NonLinearElecCouplingType_TotalAngularMomentumJ', False)

    
    TotalAngularMomentumJ = property(__TotalAngularMomentumJ.value, __TotalAngularMomentumJ.set, None, None)

    
    # Element EfSymmetry uses Python identifier EfSymmetry
    __EfSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'EfSymmetry'), 'EfSymmetry', '__AbsentNamespace0_NonLinearElecCouplingType_EfSymmetry', False)

    
    EfSymmetry = property(__EfSymmetry.value, __EfSymmetry.set, None, None)

    
    # Element RoVibronicSplitting uses Python identifier RoVibronicSplitting
    __RoVibronicSplitting = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'RoVibronicSplitting'), 'RoVibronicSplitting', '__AbsentNamespace0_NonLinearElecCouplingType_RoVibronicSplitting', False)

    
    RoVibronicSplitting = property(__RoVibronicSplitting.value, __RoVibronicSplitting.set, None, None)

    
    # Element Label uses Python identifier Label
    __Label = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Label'), 'Label', '__AbsentNamespace0_NonLinearElecCouplingType_Label', False)

    
    Label = property(__Label.value, __Label.set, None, None)

    
    # Element TotalAngularMomentumN uses Python identifier TotalAngularMomentumN
    __TotalAngularMomentumN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), 'TotalAngularMomentumN', '__AbsentNamespace0_NonLinearElecCouplingType_TotalAngularMomentumN', False)

    
    TotalAngularMomentumN = property(__TotalAngularMomentumN.value, __TotalAngularMomentumN.set, None, None)


    _ElementMap = {
        __MolecularProjection.name() : __MolecularProjection,
        __TotalAngularMomentumJ.name() : __TotalAngularMomentumJ,
        __EfSymmetry.name() : __EfSymmetry,
        __RoVibronicSplitting.name() : __RoVibronicSplitting,
        __Label.name() : __Label,
        __TotalAngularMomentumN.name() : __TotalAngularMomentumN
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'NonLinearElecCouplingType', NonLinearElecCouplingType)


# Complex type NonLinearElecHyperFType with content type ELEMENT_ONLY
class NonLinearElecHyperFType (NonLinearElecCouplingType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonLinearElecHyperFType')
    # Base type is NonLinearElecCouplingType
    
    # Element TotalAngularMomentumJ (TotalAngularMomentumJ) inherited from NonLinearElecCouplingType
    
    # Element MolecularProjection (MolecularProjection) inherited from NonLinearElecCouplingType
    
    # Element EfSymmetry (EfSymmetry) inherited from NonLinearElecCouplingType
    
    # Element RoVibronicSplitting (RoVibronicSplitting) inherited from NonLinearElecCouplingType
    
    # Element HyperfineQuantumNumbers uses Python identifier HyperfineQuantumNumbers
    __HyperfineQuantumNumbers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), 'HyperfineQuantumNumbers', '__AbsentNamespace0_NonLinearElecHyperFType_HyperfineQuantumNumbers', False)

    
    HyperfineQuantumNumbers = property(__HyperfineQuantumNumbers.value, __HyperfineQuantumNumbers.set, None, None)

    
    # Element Label (Label) inherited from NonLinearElecCouplingType
    
    # Element TotalAngularMomentumN (TotalAngularMomentumN) inherited from NonLinearElecCouplingType

    _ElementMap = NonLinearElecCouplingType._ElementMap.copy()
    _ElementMap.update({
        __HyperfineQuantumNumbers.name() : __HyperfineQuantumNumbers
    })
    _AttributeMap = NonLinearElecCouplingType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NonLinearElecHyperFType', NonLinearElecHyperFType)


# Complex type XSAMSDataType with content type ELEMENT_ONLY
class XSAMSDataType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'XSAMSDataType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_XSAMSDataType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, u'Any relevant comments')

    
    # Element States uses Python identifier States
    __States = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'States'), 'States', '__AbsentNamespace0_XSAMSDataType_States', False)

    
    States = property(__States.value, __States.set, None, u'List of atomic states, molecular states, particles, surfaces, and solids')

    
    # Element Processes uses Python identifier Processes
    __Processes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Processes'), 'Processes', '__AbsentNamespace0_XSAMSDataType_Processes', False)

    
    Processes = property(__Processes.value, __Processes.set, None, u'Physical processes connecting states (e.g., radiative, collisional, autoionization, etc.)')

    
    # Element Sources uses Python identifier Sources
    __Sources = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Sources'), 'Sources', '__AbsentNamespace0_XSAMSDataType_Sources', False)

    
    Sources = property(__Sources.value, __Sources.set, None, u'All relevant references to data sources')

    
    # Element Methods uses Python identifier Methods
    __Methods = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Methods'), 'Methods', '__AbsentNamespace0_XSAMSDataType_Methods', False)

    
    Methods = property(__Methods.value, __Methods.set, None, u'List of methods used to produce the data')

    
    # Element Functions uses Python identifier Functions
    __Functions = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Functions'), 'Functions', '__AbsentNamespace0_XSAMSDataType_Functions', False)

    
    Functions = property(__Functions.value, __Functions.set, None, u'List of functions used for data description and/or presentation (e.g., fitting)')


    _ElementMap = {
        __Comments.name() : __Comments,
        __States.name() : __States,
        __Processes.name() : __Processes,
        __Sources.name() : __Sources,
        __Methods.name() : __Methods,
        __Functions.name() : __Functions
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'XSAMSDataType', XSAMSDataType)


# Complex type DataSetType with content type ELEMENT_ONLY
class DataSetType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataSetType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element TabulatedData uses Python identifier TabulatedData
    __TabulatedData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TabulatedData'), 'TabulatedData', '__AbsentNamespace0_DataSetType_TabulatedData', True)

    
    TabulatedData = property(__TabulatedData.value, __TabulatedData.set, None, u'Tables of data')

    
    # Element FitData uses Python identifier FitData
    __FitData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'FitData'), 'FitData', '__AbsentNamespace0_DataSetType_FitData', True)

    
    FitData = property(__FitData.value, __FitData.set, None, u'Fits of data')

    
    # Attribute methodRef inherited from PrimaryType
    
    # Attribute dataDescription uses Python identifier dataDescription
    __dataDescription = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dataDescription'), 'dataDescription', '__AbsentNamespace0_DataSetType_dataDescription', DataDescriptionType, required=True)
    
    dataDescription = property(__dataDescription.value, __dataDescription.set, None, None)

    
    # Attribute sourceRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __TabulatedData.name() : __TabulatedData,
        __FitData.name() : __FitData
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        __dataDescription.name() : __dataDescription
    })
Namespace.addCategoryObject('typeBinding', u'DataSetType', DataSetType)


# Complex type ElectronicHomeType with content type ELEMENT_ONLY
class ElectronicHomeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ElectronicHomeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ElectronicComponent uses Python identifier ElectronicComponent
    __ElectronicComponent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ElectronicComponent'), 'ElectronicComponent', '__AbsentNamespace0_ElectronicHomeType_ElectronicComponent', True)

    
    ElectronicComponent = property(__ElectronicComponent.value, __ElectronicComponent.set, None, None)


    _ElementMap = {
        __ElectronicComponent.name() : __ElectronicComponent
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ElectronicHomeType', ElectronicHomeType)


# Complex type HyperfineCaseABetaType with content type ELEMENT_ONLY
class HyperfineCaseABetaType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HyperfineCaseABetaType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element HyperfineQuantumNumbers uses Python identifier HyperfineQuantumNumbers
    __HyperfineQuantumNumbers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), 'HyperfineQuantumNumbers', '__AbsentNamespace0_HyperfineCaseABetaType_HyperfineQuantumNumbers', False)

    
    HyperfineQuantumNumbers = property(__HyperfineQuantumNumbers.value, __HyperfineQuantumNumbers.set, None, None)

    
    # Element TotalMolecularProjectionJ uses Python identifier TotalMolecularProjectionJ
    __TotalMolecularProjectionJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionJ'), 'TotalMolecularProjectionJ', '__AbsentNamespace0_HyperfineCaseABetaType_TotalMolecularProjectionJ', False)

    
    TotalMolecularProjectionJ = property(__TotalMolecularProjectionJ.value, __TotalMolecularProjectionJ.set, None, None)

    
    # Element TotalAngularMomentumJ uses Python identifier TotalAngularMomentumJ
    __TotalAngularMomentumJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), 'TotalAngularMomentumJ', '__AbsentNamespace0_HyperfineCaseABetaType_TotalAngularMomentumJ', False)

    
    TotalAngularMomentumJ = property(__TotalAngularMomentumJ.value, __TotalAngularMomentumJ.set, None, None)


    _ElementMap = {
        __HyperfineQuantumNumbers.name() : __HyperfineQuantumNumbers,
        __TotalMolecularProjectionJ.name() : __TotalMolecularProjectionJ,
        __TotalAngularMomentumJ.name() : __TotalAngularMomentumJ
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'HyperfineCaseABetaType', HyperfineCaseABetaType)


# Complex type HyperfineCouplingBType with content type ELEMENT_ONLY
class HyperfineCouplingBType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'HyperfineCouplingBType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element HyperfineQuantumNumbers uses Python identifier HyperfineQuantumNumbers
    __HyperfineQuantumNumbers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), 'HyperfineQuantumNumbers', '__AbsentNamespace0_HyperfineCouplingBType_HyperfineQuantumNumbers', False)

    
    HyperfineQuantumNumbers = property(__HyperfineQuantumNumbers.value, __HyperfineQuantumNumbers.set, None, None)

    
    # Element CouplingType uses Python identifier CouplingType
    __CouplingType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'CouplingType'), 'CouplingType', '__AbsentNamespace0_HyperfineCouplingBType_CouplingType', False)

    
    CouplingType = property(__CouplingType.value, __CouplingType.set, None, None)

    
    # Element TotalAngularMomentumN uses Python identifier TotalAngularMomentumN
    __TotalAngularMomentumN = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), 'TotalAngularMomentumN', '__AbsentNamespace0_HyperfineCouplingBType_TotalAngularMomentumN', False)

    
    TotalAngularMomentumN = property(__TotalAngularMomentumN.value, __TotalAngularMomentumN.set, None, None)

    
    # Element TotalAngularMomentumJ uses Python identifier TotalAngularMomentumJ
    __TotalAngularMomentumJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), 'TotalAngularMomentumJ', '__AbsentNamespace0_HyperfineCouplingBType_TotalAngularMomentumJ', False)

    
    TotalAngularMomentumJ = property(__TotalAngularMomentumJ.value, __TotalAngularMomentumJ.set, None, None)


    _ElementMap = {
        __HyperfineQuantumNumbers.name() : __HyperfineQuantumNumbers,
        __CouplingType.name() : __CouplingType,
        __TotalAngularMomentumN.name() : __TotalAngularMomentumN,
        __TotalAngularMomentumJ.name() : __TotalAngularMomentumJ
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'HyperfineCouplingBType', HyperfineCouplingBType)


# Complex type FitValidityLimitsType with content type ELEMENT_ONLY
class FitValidityLimitsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FitValidityLimitsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element LowerLimit uses Python identifier LowerLimit
    __LowerLimit = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'LowerLimit'), 'LowerLimit', '__AbsentNamespace0_FitValidityLimitsType_LowerLimit', False)

    
    LowerLimit = property(__LowerLimit.value, __LowerLimit.set, None, u'Lower limit of fit validity')

    
    # Element UpperLimit uses Python identifier UpperLimit
    __UpperLimit = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'UpperLimit'), 'UpperLimit', '__AbsentNamespace0_FitValidityLimitsType_UpperLimit', False)

    
    UpperLimit = property(__UpperLimit.value, __UpperLimit.set, None, u'Upper limit of fit validity')


    _ElementMap = {
        __LowerLimit.name() : __LowerLimit,
        __UpperLimit.name() : __UpperLimit
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'FitValidityLimitsType', FitValidityLimitsType)


# Complex type MaterialType with content type ELEMENT_ONLY
class MaterialType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MaterialType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element MaterialTopology uses Python identifier MaterialTopology
    __MaterialTopology = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MaterialTopology'), 'MaterialTopology', '__AbsentNamespace0_MaterialType_MaterialTopology', False)

    
    MaterialTopology = property(__MaterialTopology.value, __MaterialTopology.set, None, u'Description of the material topology')

    
    # Element MaterialTemperature uses Python identifier MaterialTemperature
    __MaterialTemperature = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MaterialTemperature'), 'MaterialTemperature', '__AbsentNamespace0_MaterialType_MaterialTemperature', False)

    
    MaterialTemperature = property(__MaterialTemperature.value, __MaterialTemperature.set, None, u'Temperature of the material')

    
    # Element MaterialThickness uses Python identifier MaterialThickness
    __MaterialThickness = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MaterialThickness'), 'MaterialThickness', '__AbsentNamespace0_MaterialType_MaterialThickness', False)

    
    MaterialThickness = property(__MaterialThickness.value, __MaterialThickness.set, None, u'Thickness of a material')

    
    # Element MaterialName uses Python identifier MaterialName
    __MaterialName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MaterialName'), 'MaterialName', '__AbsentNamespace0_MaterialType_MaterialName', False)

    
    MaterialName = property(__MaterialName.value, __MaterialName.set, None, u'Name of a material. Example: bronze')

    
    # Element Comments uses Python identifier Comments
    __Comments = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Comments'), 'Comments', '__AbsentNamespace0_MaterialType_Comments', False)

    
    Comments = property(__Comments.value, __Comments.set, None, None)

    
    # Element MaterialComposition uses Python identifier MaterialComposition
    __MaterialComposition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'MaterialComposition'), 'MaterialComposition', '__AbsentNamespace0_MaterialType_MaterialComposition', False)

    
    MaterialComposition = property(__MaterialComposition.value, __MaterialComposition.set, None, u'Composition of a material')


    _ElementMap = {
        __MaterialTopology.name() : __MaterialTopology,
        __MaterialTemperature.name() : __MaterialTemperature,
        __MaterialThickness.name() : __MaterialThickness,
        __MaterialName.name() : __MaterialName,
        __Comments.name() : __Comments,
        __MaterialComposition.name() : __MaterialComposition
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'MaterialType', MaterialType)


# Complex type ParameterType with content type ELEMENT_ONLY
class ParameterType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ParameterType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Name'), 'Name', '__AbsentNamespace0_ParameterType_Name', False)

    
    Name = property(__Name.value, __Name.set, None, u'Name of a parameter. Example: a')

    
    # Element Description uses Python identifier Description
    __Description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Description'), 'Description', '__AbsentNamespace0_ParameterType_Description', False)

    
    Description = property(__Description.value, __Description.set, None, u'Description of a parameter')


    _ElementMap = {
        __Name.name() : __Name,
        __Description.name() : __Description
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ParameterType', ParameterType)


# Complex type AtomType with content type ELEMENT_ONLY
class AtomType (PrimaryType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AtomType')
    # Base type is PrimaryType
    
    # Element Comments (Comments) inherited from PrimaryType
    
    # Element Isotope uses Python identifier Isotope
    __Isotope = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Isotope'), 'Isotope', '__AbsentNamespace0_AtomType_Isotope', True)

    
    Isotope = property(__Isotope.value, __Isotope.set, None, u'List of isotopes')

    
    # Element ChemicalElement uses Python identifier ChemicalElement
    __ChemicalElement = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'ChemicalElement'), 'ChemicalElement', '__AbsentNamespace0_AtomType_ChemicalElement', False)

    
    ChemicalElement = property(__ChemicalElement.value, __ChemicalElement.set, None, u'Description of chemical elements')

    
    # Attribute sourceRef inherited from PrimaryType
    
    # Attribute methodRef inherited from PrimaryType

    _ElementMap = PrimaryType._ElementMap.copy()
    _ElementMap.update({
        __Isotope.name() : __Isotope,
        __ChemicalElement.name() : __ChemicalElement
    })
    _AttributeMap = PrimaryType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AtomType', AtomType)


# Complex type DataXYType with content type ELEMENT_ONLY
class DataXYType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataXYType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element X uses Python identifier X
    __X = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'X'), 'X', '__AbsentNamespace0_DataXYType_X', True)

    
    X = property(__X.value, __X.set, None, None)

    
    # Element Y uses Python identifier Y
    __Y = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'Y'), 'Y', '__AbsentNamespace0_DataXYType_Y', False)

    
    Y = property(__Y.value, __Y.set, None, u'Data value')


    _ElementMap = {
        __X.name() : __X,
        __Y.name() : __Y
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DataXYType', DataXYType)


# Complex type NonLinearElecNoHyperFType with content type ELEMENT_ONLY
class NonLinearElecNoHyperFType (NonLinearElecCouplingType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NonLinearElecNoHyperFType')
    # Base type is NonLinearElecCouplingType
    
    # Element TotalAngularMomentumJ (TotalAngularMomentumJ) inherited from NonLinearElecCouplingType
    
    # Element MolecularProjection (MolecularProjection) inherited from NonLinearElecCouplingType
    
    # Element EfSymmetry (EfSymmetry) inherited from NonLinearElecCouplingType
    
    # Element RoVibronicSplitting (RoVibronicSplitting) inherited from NonLinearElecCouplingType
    
    # Element Label (Label) inherited from NonLinearElecCouplingType
    
    # Element TotalMagneticQuantumNumberJ uses Python identifier TotalMagneticQuantumNumberJ
    __TotalMagneticQuantumNumberJ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'), 'TotalMagneticQuantumNumberJ', '__AbsentNamespace0_NonLinearElecNoHyperFType_TotalMagneticQuantumNumberJ', False)

    
    TotalMagneticQuantumNumberJ = property(__TotalMagneticQuantumNumberJ.value, __TotalMagneticQuantumNumberJ.set, None, None)

    
    # Element TotalAngularMomentumN (TotalAngularMomentumN) inherited from NonLinearElecCouplingType

    _ElementMap = NonLinearElecCouplingType._ElementMap.copy()
    _ElementMap.update({
        __TotalMagneticQuantumNumberJ.name() : __TotalMagneticQuantumNumberJ
    })
    _AttributeMap = NonLinearElecCouplingType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NonLinearElecNoHyperFType', NonLinearElecNoHyperFType)


# Complex type C2SymmetriesType with content type ELEMENT_ONLY
class C2SymmetriesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'C2SymmetriesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element C2aSymmetry uses Python identifier C2aSymmetry
    __C2aSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'C2aSymmetry'), 'C2aSymmetry', '__AbsentNamespace0_C2SymmetriesType_C2aSymmetry', False)

    
    C2aSymmetry = property(__C2aSymmetry.value, __C2aSymmetry.set, None, None)

    
    # Element C2bSymmetry uses Python identifier C2bSymmetry
    __C2bSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'C2bSymmetry'), 'C2bSymmetry', '__AbsentNamespace0_C2SymmetriesType_C2bSymmetry', False)

    
    C2bSymmetry = property(__C2bSymmetry.value, __C2bSymmetry.set, None, None)

    
    # Element C2cSymmetry uses Python identifier C2cSymmetry
    __C2cSymmetry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(None, u'C2cSymmetry'), 'C2cSymmetry', '__AbsentNamespace0_C2SymmetriesType_C2cSymmetry', False)

    
    C2cSymmetry = property(__C2cSymmetry.value, __C2cSymmetry.set, None, u'Vol II, p 51')


    _ElementMap = {
        __C2aSymmetry.name() : __C2aSymmetry,
        __C2bSymmetry.name() : __C2bSymmetry,
        __C2cSymmetry.name() : __C2cSymmetry
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'C2SymmetriesType', C2SymmetriesType)


Particles = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Particles'), ParticlesType)
Namespace.addCategoryObject('elementBinding', Particles.name().localName(), Particles)

Sources = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Sources'), SourcesType, documentation=u'All relevant references to data sources')
Namespace.addCategoryObject('elementBinding', Sources.name().localName(), Sources)

Methods = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Methods'), MethodsType, documentation=u'List of methods used to produce the data')
Namespace.addCategoryObject('elementBinding', Methods.name().localName(), Methods)

Functions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Functions'), FunctionsType, documentation=u'List of functions used for data description and/or presentation (e.g., fitting)')
Namespace.addCategoryObject('elementBinding', Functions.name().localName(), Functions)

NonRadiative = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NonRadiative'), NonRadiativeType, documentation=u'List of autoionization and predissociation transitions')
Namespace.addCategoryObject('elementBinding', NonRadiative.name().localName(), NonRadiative)

Radiative = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Radiative'), RadiativeType, documentation=u'Radiative transitions (both emission and absorption)')
Namespace.addCategoryObject('elementBinding', Radiative.name().localName(), Radiative)

Collisions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Collisions'), CollisionsType, documentation=u'List of collisional processes')
Namespace.addCategoryObject('elementBinding', Collisions.name().localName(), Collisions)

Solids = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Solids'), SolidsType, documentation=u'Solids, surfaces, etc.')
Namespace.addCategoryObject('elementBinding', Solids.name().localName(), Solids)

Atoms = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Atoms'), AtomsType, documentation=u'Atoms or atomic ions')
Namespace.addCategoryObject('elementBinding', Atoms.name().localName(), Atoms)

XSAMSData = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'XSAMSData'), XSAMSDataType, documentation=u'XML schema for description of atomic, molecular, and particle-solid-interaction processes')
Namespace.addCategoryObject('elementBinding', XSAMSData.name().localName(), XSAMSData)



PrimaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=PrimaryType, documentation=u'Arbitrary comments'))
PrimaryType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=PrimaryType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



AtomicNumericalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'QuantumDefect'), DataType, scope=AtomicNumericalDataType, documentation=u'Quantum defect'))

AtomicNumericalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LandeFactor'), DataType, scope=AtomicNumericalDataType, documentation=u'Lande factor'))

AtomicNumericalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'), DataType, scope=AtomicNumericalDataType, documentation=u'State lifetime'))

AtomicNumericalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Polarizability'), DataType, scope=AtomicNumericalDataType, documentation=u'State polarizability'))

AtomicNumericalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'), pyxb.binding.datatypes.double, scope=AtomicNumericalDataType, documentation=u'Statistical weight. May be non-integer due to plasma environment effects.'))

AtomicNumericalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IonizationEnergy'), DataType, scope=AtomicNumericalDataType, documentation=u'Energy required to remove an electron'))

AtomicNumericalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StateEnergy'), DataType, scope=AtomicNumericalDataType, documentation=u'Energy from the ground state'))
AtomicNumericalDataType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'QuantumDefect'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'LandeFactor'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polarizability'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonizationEnergy'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateEnergy'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polarizability'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'QuantumDefect'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'LandeFactor'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polarizability'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'QuantumDefect'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polarizability'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'QuantumDefect'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'LandeFactor'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polarizability'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonizationEnergy'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'QuantumDefect'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'LandeFactor'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalLifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polarizability'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonizationEnergy'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateEnergy'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polarizability'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=AtomicNumericalDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'StatisticalWeight'))),
    ])
    , 9 : pyxb.binding.content.ContentModelState(state=9, is_final=True, transitions=[
    ])
})



MagneticQuantumNumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comment'), pyxb.binding.datatypes.string, scope=MagneticQuantumNumberType))

MagneticQuantumNumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Label'), pyxb.binding.datatypes.string, scope=MagneticQuantumNumberType))

MagneticQuantumNumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Value'), AngularMomentumProjectionType, scope=MagneticQuantumNumberType))
MagneticQuantumNumberType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MagneticQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MagneticQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MagneticQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



MolecularStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ElectronicHome'), ElectronicHomeType, scope=MolecularStateType))

MolecularStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=MolecularStateType))

MolecularStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MolecularStateCharacterisation'), MolecularStateCharacterisationType, scope=MolecularStateType))

MolecularStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalSpinMomentumS'), MolecularQuantumNumberType, scope=MolecularStateType))

MolecularStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberS'), MagneticQuantumNumberType, scope=MolecularStateType))

MolecularStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parity'), ParityType, scope=MolecularStateType))

MolecularStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comment'), pyxb.binding.datatypes.string, scope=MolecularStateType))
MolecularStateType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberS'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalSpinMomentumS'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularStateCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parity'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicHome'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalSpinMomentumS'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parity'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberS'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parity'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberS'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 9 : pyxb.binding.content.ContentModelState(state=9, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parity'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
})



CollisionalProcessClassType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'UserDefinition'), pyxb.binding.datatypes.anyType, scope=CollisionalProcessClassType, documentation=u'Description of the process'))

CollisionalProcessClassType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Code'), CodeType, scope=CollisionalProcessClassType, documentation=u'A 4-letter code describing various processes'))

CollisionalProcessClassType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IAEACode'), IAEACodeType, scope=CollisionalProcessClassType, documentation=u'From the "IAEA Classification of Processes", October 2003'))
CollisionalProcessClassType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CollisionalProcessClassType._UseForTag(pyxb.namespace.ExpandedName(None, u'Code'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CollisionalProcessClassType._UseForTag(pyxb.namespace.ExpandedName(None, u'UserDefinition'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionalProcessClassType._UseForTag(pyxb.namespace.ExpandedName(None, u'IAEACode'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CollisionalProcessClassType._UseForTag(pyxb.namespace.ExpandedName(None, u'Code'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionalProcessClassType._UseForTag(pyxb.namespace.ExpandedName(None, u'IAEACode'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



StatesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Atoms'), AtomsType, scope=StatesType, documentation=u'List of atoms'))

StatesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Particles'), ParticlesType, scope=StatesType, documentation=u'List of elementary particles (electron, photon, etc.)'))

StatesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Solids'), SolidsType, scope=StatesType, documentation=u'List of solids and surfaces'))

StatesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Molecules'), MoleculesType, scope=StatesType, documentation=u'List of molecules'))
StatesType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=StatesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Atoms'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
StatesType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=StatesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Molecules'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
StatesType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=StatesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Solids'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
StatesType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=StatesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Particles'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(StatesType._ContentModel_1, False),
    pyxb.binding.content.ModelGroupAllAlternative(StatesType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(StatesType._ContentModel_3, False),
    pyxb.binding.content.ModelGroupAllAlternative(StatesType._ContentModel_4, False),
])
StatesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



NonRadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Probability'), DataType, scope=NonRadiativeTransitionType, documentation=u'Transition probability'))

NonRadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FinalStateRef'), StateRef, scope=NonRadiativeTransitionType, documentation=u'Reference to the final state'))

NonRadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Type'), pyxb.binding.datatypes.string, scope=NonRadiativeTransitionType, documentation=u'Description of the transition (e.g., Coster-Kronig)'))

NonRadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TransitionEnergy'), DataType, scope=NonRadiativeTransitionType, documentation=u'Transition energy'))

NonRadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NonRadiativeWidth'), DataType, scope=NonRadiativeTransitionType, documentation=u'NonRadiative width '))

NonRadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'InitialStateRef'), StateRef, scope=NonRadiativeTransitionType, documentation=u'Reference to the initial state'))
NonRadiativeTransitionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'InitialStateRef'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'InitialStateRef'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'TransitionEnergy'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Type'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'FinalStateRef'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Probability'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Probability'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonRadiativeWidth'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'TransitionEnergy'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Type'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=NonRadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Type'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
    ])
})



ShellPairType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ShellPairTerm'), TermType, scope=ShellPairType))

ShellPairType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Shell1'), ShellType, scope=ShellPairType))

ShellPairType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Shell2'), ShellType, scope=ShellPairType))
ShellPairType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellPairType._UseForTag(pyxb.namespace.ExpandedName(None, u'Shell1'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ShellPairType._UseForTag(pyxb.namespace.ExpandedName(None, u'Shell2'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ShellPairType._UseForTag(pyxb.namespace.ExpandedName(None, u'ShellPairTerm'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



HundCaseBType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'), MagneticQuantumNumberType, scope=HundCaseBType))

HundCaseBType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), MolecularQuantumNumberType, scope=HundCaseBType))

HundCaseBType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), ComplexMolecularQuantumNumberType, scope=HundCaseBType))
HundCaseBType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=HundCaseBType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=HundCaseBType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=HundCaseBType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



ParticlesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Particle'), ParticleType, scope=ParticlesType))
ParticlesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ParticlesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Particle'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ParticlesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Particle'))),
    ])
})



WavelengthWavenumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Experimental'), DataType, scope=WavelengthWavenumberType, documentation=u'Experimentally measured'))

WavelengthWavenumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Ritz'), DataType, scope=WavelengthWavenumberType, documentation=u'Calculated from the difference of experimental energy levels'))

WavelengthWavenumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Theoretical'), DataType, scope=WavelengthWavenumberType, documentation=u'Calculated (theory)'))
WavelengthWavenumberType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Theoretical'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Experimental'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Ritz'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Theoretical'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Experimental'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Theoretical'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Experimental'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Ritz'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=WavelengthWavenumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Theoretical'))),
    ])
})



MolecularQuantumNumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Value'), AngularMomentumType, scope=MolecularQuantumNumberType))

MolecularQuantumNumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comment'), pyxb.binding.datatypes.string, scope=MolecularQuantumNumberType))

MolecularQuantumNumberType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Label'), pyxb.binding.datatypes.string, scope=MolecularQuantumNumberType))
MolecularQuantumNumberType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



EnergyWavelengthType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Energy'), WavelengthWavenumberType, scope=EnergyWavelengthType, documentation=u'Transition energy'))

EnergyWavelengthType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Wavenumber'), WavelengthWavenumberType, scope=EnergyWavelengthType, documentation=u'Transition wavenumber'))

EnergyWavelengthType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Wavelength'), WavelengthWavenumberType, scope=EnergyWavelengthType, documentation=u'Transition wavelength'))

EnergyWavelengthType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Frequency'), WavelengthWavenumberType, scope=EnergyWavelengthType, documentation=u'Transition frequency'))
EnergyWavelengthType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Frequency'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Wavelength'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Wavenumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Energy'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Frequency'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Energy'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Frequency'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Energy'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Frequency'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Wavelength'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Wavenumber'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Energy'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Frequency'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=EnergyWavelengthType._UseForTag(pyxb.namespace.ExpandedName(None, u'Wavelength'))),
    ])
})



LinearNoElecHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), MolecularQuantumNumberType, scope=LinearNoElecHyperFType))

LinearNoElecHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), HyperfineQuantumNumbersType, scope=LinearNoElecHyperFType))
LinearNoElecHyperFType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LinearNoElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=LinearNoElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



MethodsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Method'), MethodType, scope=MethodsType))
MethodsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MethodsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Method'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MethodsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Method'))),
    ])
})



TermType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'jK'), jKCouplingType, scope=TermType, documentation=u'Term in jK-coupling'))

TermType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LK'), LKCouplingType, scope=TermType, documentation=u'Term in LK-coupling'))

TermType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TermLabel'), pyxb.binding.datatypes.string, scope=TermType, documentation=u'Arbitrary term label'))

TermType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LS'), LSCouplingType, scope=TermType, documentation=u'Term in LS-coupling'))

TermType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'jj'), jjCouplingType, scope=TermType, documentation=u'Term in jj-coupling'))

TermType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'J1J2'), jjCouplingType, scope=TermType, documentation=u'Term in J1J2-coupling'))
TermType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'jK'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'LK'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'TermLabel'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'LS'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'jj'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'J1J2'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'LK'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'J1J2'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'TermLabel'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'jK'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'TermLabel'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'LK'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'jK'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'TermLabel'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'LK'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'TermLabel'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'jK'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'LK'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'J1J2'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'jj'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=TermType._UseForTag(pyxb.namespace.ExpandedName(None, u'TermLabel'))),
    ])
})



SymbolType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LatexExpression'), pyxb.binding.datatypes.string, scope=SymbolType))

SymbolType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Symbol'), SimpleSymbolType, scope=SymbolType))
SymbolType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'Symbol'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'Symbol'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'Symbol'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=SymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'LatexExpression'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



SourcesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Source'), SourceType, scope=SourcesType, documentation=u'A bibliography (bibreference) entry'))
SourcesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourcesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Source'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourcesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Source'))),
    ])
})



LSCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Multiplicity'), pyxb.binding.datatypes.positiveInteger, scope=LSCouplingType, documentation=u'2S+1'))

LSCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'L'), OrbitalAngularMomentumType, scope=LSCouplingType, documentation=u'Orbital angular momentum of the term in LS-coupling'))

LSCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'S'), AngularMomentumType, scope=LSCouplingType, documentation=u'Spin angular momentum of the term in LS-coupling'))
LSCouplingType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LSCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'L'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
LSCouplingType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LSCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'S'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
LSCouplingType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LSCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multiplicity'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(LSCouplingType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(LSCouplingType._ContentModel_2, True),
    pyxb.binding.content.ModelGroupAllAlternative(LSCouplingType._ContentModel_3, False),
])
LSCouplingType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



MaterialCompositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Component'), MaterialComponentType, scope=MaterialCompositionType))
MaterialCompositionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MaterialCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Component'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MaterialCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Component'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MaterialCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Component'))),
    ])
})



DataTableType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PositiveError'), DataListType, scope=DataTableType, documentation=u'Positive error for each data point of the list'))

DataTableType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NegativeError'), DataListType, scope=DataTableType, documentation=u'Negative error for each data point of'))

DataTableType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DataList'), DataListType, scope=DataTableType, documentation=u'List of data values. Example: 3 15 33.3 1e3'))

DataTableType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Error'), DataListType, scope=DataTableType, documentation=u'Error for each data point of the list'))

DataTableType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DataDescription'), pyxb.binding.datatypes.anyType, scope=DataTableType, documentation=u'Additional description of the data list'))
DataTableType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataTableType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataList'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
DataTableType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataTableType._UseForTag(pyxb.namespace.ExpandedName(None, u'Error'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
DataTableType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataTableType._UseForTag(pyxb.namespace.ExpandedName(None, u'NegativeError'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
DataTableType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataTableType._UseForTag(pyxb.namespace.ExpandedName(None, u'PositiveError'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
DataTableType._ContentModel_5 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataTableType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataDescription'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(DataTableType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(DataTableType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(DataTableType._ContentModel_3, False),
    pyxb.binding.content.ModelGroupAllAlternative(DataTableType._ContentModel_4, False),
    pyxb.binding.content.ModelGroupAllAlternative(DataTableType._ContentModel_5, False),
])
DataTableType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



PseudoStatisticalWeightType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Value'), pyxb.binding.datatypes.positiveInteger, scope=PseudoStatisticalWeightType))
PseudoStatisticalWeightType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=PseudoStatisticalWeightType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=PseudoStatisticalWeightType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=PseudoStatisticalWeightType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



SuperConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SuperShell'), SuperShellType, scope=SuperConfigurationType, documentation=u'List of supershells'))
SuperConfigurationType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SuperConfigurationType._UseForTag(pyxb.namespace.ExpandedName(None, u'SuperShell'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SuperConfigurationType._UseForTag(pyxb.namespace.ExpandedName(None, u'SuperShell'))),
    ])
})


ComplexMolecularQuantumNumberType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ComplexMolecularQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ComplexMolecularQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ComplexMolecularQuantumNumberType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



ChemicalElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NuclearCharge'), pyxb.binding.datatypes.positiveInteger, scope=ChemicalElementType, documentation=u'Nuclear charge in units of electron charge'))

ChemicalElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ElementSymbol'), ElementSymbolType, scope=ChemicalElementType, documentation=u'Standard symbol of a chemical element (e.g., H or Ta)'))
ChemicalElementType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ChemicalElementType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearCharge'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ChemicalElementType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ChemicalElementType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElementSymbol'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(ChemicalElementType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(ChemicalElementType._ContentModel_2, False),
])
ChemicalElementType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



DataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Value'), ValueType, scope=DataType, documentation=u'Value of a particular quantity'))

DataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Accuracy'), pyxb.binding.datatypes.string, scope=DataType, documentation=u'Description of the accuracy'))
DataType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=DataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=DataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Accuracy'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



ShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NumberOfElectrons'), pyxb.binding.datatypes.double, scope=ShellType, documentation=u'Number of electrons in the shell'))

ShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PrincipalQuantumNumber'), PrincipalQuantumNumberType, scope=ShellType, documentation=u'Principal quantum number'))

ShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parity'), ParityType, scope=ShellType, documentation=u'Parity of a shell'))

ShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Kappa'), AngularMomentumType, scope=ShellType, documentation=u'Relativistic parameter'))

ShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'), AngularMomentumType, scope=ShellType, documentation=u'Total angular momentum of the shell'))

ShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ShellTerm'), TermType, scope=ShellType, documentation=u'Term of the shell'))

ShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'OrbitalAngularMomentum'), OrbitalAngularMomentumType, scope=ShellType))
ShellType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'PrincipalQuantumNumber'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ShellType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'OrbitalAngularMomentum'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ShellType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'NumberOfElectrons'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ShellType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parity'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ShellType._ContentModel_5 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'Kappa'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ShellType._ContentModel_6 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ShellType._ContentModel_7 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'ShellTerm'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(ShellType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(ShellType._ContentModel_2, True),
    pyxb.binding.content.ModelGroupAllAlternative(ShellType._ContentModel_3, True),
    pyxb.binding.content.ModelGroupAllAlternative(ShellType._ContentModel_4, False),
    pyxb.binding.content.ModelGroupAllAlternative(ShellType._ContentModel_5, False),
    pyxb.binding.content.ModelGroupAllAlternative(ShellType._ContentModel_6, False),
    pyxb.binding.content.ModelGroupAllAlternative(ShellType._ContentModel_7, False),
])
ShellType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



ProcessesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Collisions'), CollisionsType, scope=ProcessesType, documentation=u'List of transitions due to collisions'))

ProcessesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NonRadiative'), NonRadiativeType, scope=ProcessesType, documentation=u'List of autoionization and predissociation transitions'))

ProcessesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Radiative'), RadiativeType, scope=ProcessesType, documentation=u'List of radiative transitions'))
ProcessesType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ProcessesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Radiative'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ProcessesType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ProcessesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NonRadiative'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ProcessesType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ProcessesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Collisions'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(ProcessesType._ContentModel_1, False),
    pyxb.binding.content.ModelGroupAllAlternative(ProcessesType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(ProcessesType._ContentModel_3, False),
])
ProcessesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



HundCaseAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'), MagneticQuantumNumberType, scope=HundCaseAType))

HundCaseAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), ComplexMolecularQuantumNumberType, scope=HundCaseAType))

HundCaseAType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionJ'), MolecularQuantumNumberType, scope=HundCaseAType))
HundCaseAType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=HundCaseAType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=HundCaseAType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionJ'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=HundCaseAType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



TabulatedDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ReferenceFrame'), ReferenceFrameType, scope=TabulatedDataType, documentation=u'Reference frame in which is given the energy, velocity...'))

TabulatedDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'), pyxb.binding.datatypes.string, scope=TabulatedDataType))

TabulatedDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DataXY'), DataXYType, scope=TabulatedDataType))

TabulatedDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ProductionDate'), pyxb.binding.datatypes.date, scope=TabulatedDataType))
TabulatedDataType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataXY'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProductionDate'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'ReferenceFrame'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataXY'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProductionDate'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=TabulatedDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProductionDate'))),
    ])
})



SolidsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Solid'), SolidType, scope=SolidsType))
SolidsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SolidsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SolidsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Solid'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SolidsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Solid'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SolidsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Solid'))),
    ])
})



AsymmetricProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AsymmetricKa'), MolecularQuantumNumberType, scope=AsymmetricProjectionType))

AsymmetricProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AsymmetricKc'), MolecularQuantumNumberType, scope=AsymmetricProjectionType))

AsymmetricProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AsymmetricTau'), MagneticQuantumNumberType, scope=AsymmetricProjectionType))
AsymmetricProjectionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AsymmetricProjectionType._UseForTag(pyxb.namespace.ExpandedName(None, u'AsymmetricKa'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AsymmetricProjectionType._UseForTag(pyxb.namespace.ExpandedName(None, u'AsymmetricTau'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AsymmetricProjectionType._UseForTag(pyxb.namespace.ExpandedName(None, u'AsymmetricKc'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AsymmetricProjectionType._UseForTag(pyxb.namespace.ExpandedName(None, u'AsymmetricKa'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



AtomicQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MagneticQuantumNumber'), AngularMomentumProjectionType, scope=AtomicQuantumNumbersType, documentation=u'Magnetic quantum number. Example: -1'))

AtomicQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parity'), ParityType, scope=AtomicQuantumNumbersType, documentation=u'State parity. Example: odd'))

AtomicQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineMomentum'), AngularMomentumType, scope=AtomicQuantumNumbersType, documentation=u'Hyperfine momentum. Example: 2'))

AtomicQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'), AngularMomentumType, scope=AtomicQuantumNumbersType, documentation=u'Total angular momentum. Example: 2.5'))

AtomicQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Kappa'), AngularMomentumType, scope=AtomicQuantumNumbersType, documentation=u'Relativistic parameter kappa'))
AtomicQuantumNumbersType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parity'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicQuantumNumbersType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicQuantumNumbersType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'Kappa'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicQuantumNumbersType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineMomentum'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicQuantumNumbersType._ContentModel_5 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'MagneticQuantumNumber'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(AtomicQuantumNumbersType._ContentModel_1, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicQuantumNumbersType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicQuantumNumbersType._ContentModel_3, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicQuantumNumbersType._ContentModel_4, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicQuantumNumbersType._ContentModel_5, False),
])
AtomicQuantumNumbersType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



ElectronicCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Configuration'), ReferencedTextType, scope=ElectronicCharacterisationType))

ElectronicCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SymmetryGroup'), SymbolType, scope=ElectronicCharacterisationType))

ElectronicCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Conformation'), pyxb.binding.datatypes.string, scope=ElectronicCharacterisationType))

ElectronicCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TermSymbol'), SymbolType, scope=ElectronicCharacterisationType))
ElectronicCharacterisationType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'SymmetryGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Configuration'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Conformation'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'TermSymbol'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'SymmetryGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Conformation'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'SymmetryGroup'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'SymmetryGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Configuration'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ElectronicCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Conformation'))),
    ])
})



SuperShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PrincipalQuantumNumber'), pyxb.binding.datatypes.positiveInteger, scope=SuperShellType, documentation=u'Principal quantum number. Example: 4'))

SuperShellType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NumberOfElectrons'), pyxb.binding.datatypes.double, scope=SuperShellType, documentation=u'Number of electrons. May be noninteger to account for plasma effects. Example: 3'))
SuperShellType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SuperShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'PrincipalQuantumNumber'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SuperShellType._UseForTag(pyxb.namespace.ExpandedName(None, u'NumberOfElectrons'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



NonLinearNoElecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'C2Symmetries'), C2SymmetriesType, scope=NonLinearNoElecType))

NonLinearNoElecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), MolecularQuantumNumberType, scope=NonLinearNoElecType))

NonLinearNoElecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MolecularProjection'), MolecularProjectionType, scope=NonLinearNoElecType))
NonLinearNoElecType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearNoElecType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearNoElecType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularProjection'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearNoElecType._UseForTag(pyxb.namespace.ExpandedName(None, u'C2Symmetries'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



NonLinearNoElecNoHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberN'), MagneticQuantumNumberType, scope=NonLinearNoElecNoHyperFType))
NonLinearNoElecNoHyperFType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearNoElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearNoElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularProjection'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearNoElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'C2Symmetries'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearNoElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberN'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearNoElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberN'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
    ])
})



IsotopeParametersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MassNumber'), pyxb.binding.datatypes.integer, scope=IsotopeParametersType, documentation=u'Mass number. Example: 40.'))

IsotopeParametersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Mass'), DataType, scope=IsotopeParametersType, documentation=u'Measured mass.'))

IsotopeParametersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NuclearSpin'), AngularMomentumType, scope=IsotopeParametersType, documentation=u'Spin of an isotope'))
IsotopeParametersType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=IsotopeParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'MassNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=IsotopeParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=IsotopeParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'Mass'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=IsotopeParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpin'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=IsotopeParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'MassNumber'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=IsotopeParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpin'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
    ])
})



HyperfineQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ISum'), ComplexMolecularQuantumNumberType, scope=HyperfineQuantumNumbersType))

HyperfineQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IntermediateHyperfineQuantumNumber'), ComplexMolecularQuantumNumberType, scope=HyperfineQuantumNumbersType))

HyperfineQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumF'), ComplexMolecularQuantumNumberType, scope=HyperfineQuantumNumbersType))

HyperfineQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberF'), MagneticQuantumNumberType, scope=HyperfineQuantumNumbersType))
HyperfineQuantumNumbersType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=HyperfineQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumF'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=HyperfineQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'IntermediateHyperfineQuantumNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=HyperfineQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'ISum'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=HyperfineQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberF'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



ParticleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ParticleProperties'), ParticlePropertiesType, scope=ParticleType, documentation=u'Description of particle properties'))

ParticleType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=ParticleType))
ParticleType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ParticleType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticleProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ParticleType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ParticleType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



ProductsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StateRef'), StateRef, scope=ProductsType, documentation=u'Reference to a specific state'))
ProductsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ProductsType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateRef'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ProductsType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateRef'))),
    ])
})



MethodType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=MethodType, documentation=u'Method description. Example: Convergent Close Coupling.'))

MethodType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Category'), MethodCategoryType, scope=MethodType, documentation=u'Enumerated list of method classifications. Example: theory.'))

MethodType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=MethodType))
MethodType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MethodType._UseForTag(pyxb.namespace.ExpandedName(None, u'Category'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MethodType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MethodType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



RoVibronicSplittingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Type'), pyxb.binding.datatypes.string, scope=RoVibronicSplittingType))

RoVibronicSplittingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Label'), pyxb.binding.datatypes.string, scope=RoVibronicSplittingType))
RoVibronicSplittingType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RoVibronicSplittingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RoVibronicSplittingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RoVibronicSplittingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Type'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RoVibronicSplittingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RoVibronicSplittingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
    ])
})



ParticlePropertiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ParticleSpin'), AngularMomentumType, scope=ParticlePropertiesType, documentation=u'Spin of the particle'))

ParticlePropertiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ParticleCharge'), pyxb.binding.datatypes.integer, scope=ParticlePropertiesType, documentation=u'Particle charge'))

ParticlePropertiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ParticleMass'), DataType, scope=ParticlePropertiesType, documentation=u'Mass of the particle'))

ParticlePropertiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ParticlePolarization'), AngularMomentumProjectionType, scope=ParticlePropertiesType, documentation=u'Polarization of the particle'))
ParticlePropertiesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticleMass'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticleCharge'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticleSpin'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticlePolarization'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticleMass'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticleSpin'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticlePolarization'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticleSpin'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticlePolarization'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ParticlePropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ParticlePolarization'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
    ])
})



ConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ConfigurationLabel'), pyxb.binding.datatypes.string, scope=ConfigurationType, documentation=u'Arbitrary configuration label'))

ConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AtomicCore'), AtomicCoreType, scope=ConfigurationType, documentation=u'Description of the configuration core'))

ConfigurationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Shells'), ShellsType, scope=ConfigurationType, documentation=u'List of electron shells'))
ConfigurationType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ConfigurationType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicCore'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ConfigurationType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ConfigurationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Shells'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
ConfigurationType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ConfigurationType._UseForTag(pyxb.namespace.ExpandedName(None, u'ConfigurationLabel'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(ConfigurationType._ContentModel_1, False),
    pyxb.binding.content.ModelGroupAllAlternative(ConfigurationType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(ConfigurationType._ContentModel_3, False),
])
ConfigurationType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



NonLinearPolyatomicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NonLinearNoElecHyperF'), NonLinearNoElecHyperFType, scope=NonLinearPolyatomicType))

NonLinearPolyatomicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NonLinearElecNoHyperF'), NonLinearElecNoHyperFType, scope=NonLinearPolyatomicType))

NonLinearPolyatomicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NonLinearNoElecNoHyperF'), NonLinearNoElecNoHyperFType, scope=NonLinearPolyatomicType))

NonLinearPolyatomicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NonLinearElecHyperF'), NonLinearElecHyperFType, scope=NonLinearPolyatomicType))
NonLinearPolyatomicType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearPolyatomicType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonLinearElecNoHyperF'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearPolyatomicType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonLinearNoElecNoHyperF'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearPolyatomicType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonLinearElecHyperF'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearPolyatomicType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonLinearNoElecHyperF'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



HyperfineCaseAAlphaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberF'), MagneticQuantumNumberType, scope=HyperfineCaseAAlphaType))

HyperfineCaseAAlphaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionF'), MolecularQuantumNumberType, scope=HyperfineCaseAAlphaType))

HyperfineCaseAAlphaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumF'), ComplexMolecularQuantumNumberType, scope=HyperfineCaseAAlphaType))
HyperfineCaseAAlphaType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=HyperfineCaseAAlphaType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumF'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=HyperfineCaseAAlphaType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionF'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=HyperfineCaseAAlphaType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberF'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



MolecularProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HinderedMotion'), HinderedMotionType, scope=MolecularProjectionType))

MolecularProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionN'), MolecularQuantumNumberType, scope=MolecularProjectionType))

MolecularProjectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AsymmetricProjection'), AsymmetricProjectionType, scope=MolecularProjectionType))
MolecularProjectionType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularProjectionType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
MolecularProjectionType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularProjectionType._UseForTag(pyxb.namespace.ExpandedName(None, u'AsymmetricProjection'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
MolecularProjectionType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularProjectionType._UseForTag(pyxb.namespace.ExpandedName(None, u'HinderedMotion'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(MolecularProjectionType._ContentModel_1, False),
    pyxb.binding.content.ModelGroupAllAlternative(MolecularProjectionType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(MolecularProjectionType._ContentModel_3, False),
])
MolecularProjectionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



AuthorsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Author'), AuthorType, scope=AuthorsType, documentation=u'Author of bibliographic reference.'))
AuthorsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AuthorsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Author'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AuthorsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Author'))),
    ])
})



AtomicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Configuration'), ConfigurationType, scope=AtomicComponentType, documentation=u'Atomic configuration'))

AtomicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SuperConfiguration'), SuperConfigurationType, scope=AtomicComponentType, documentation=u'Superconfiguration'))

AtomicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Term'), TermType, scope=AtomicComponentType, documentation=u'Atomic term'))

AtomicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=AtomicComponentType, documentation=u'Comments on a specific component'))

AtomicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), MixingCoefficientType, scope=AtomicComponentType, documentation=u'Expansion coefficient in the sum over the basis functions (signed or squared)'))
AtomicComponentType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'SuperConfiguration'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicComponentType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Configuration'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicComponentType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Term'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicComponentType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
AtomicComponentType._ContentModel_5 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(AtomicComponentType._ContentModel_1, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicComponentType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicComponentType._ContentModel_3, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicComponentType._ContentModel_4, False),
    pyxb.binding.content.ModelGroupAllAlternative(AtomicComponentType._ContentModel_5, False),
])
AtomicComponentType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



MoleculesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Molecule'), MoleculeType, scope=MoleculesType))
MoleculesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MoleculesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MoleculesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Molecule'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MoleculesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Molecule'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MoleculesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Molecule'))),
    ])
})



RadiativeTransitionProbabilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TransitionProbabilityA'), DataType, scope=RadiativeTransitionProbabilityType, documentation=u'Transition probability (Einstein coefficient)'))

RadiativeTransitionProbabilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'OscillatorStrength'), DataType, scope=RadiativeTransitionProbabilityType, documentation=u'Oscillator strength'))

RadiativeTransitionProbabilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'), DataType, scope=RadiativeTransitionProbabilityType, documentation=u'Line intensity for some specific conditions.'))

RadiativeTransitionProbabilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LineStrength'), DataType, scope=RadiativeTransitionProbabilityType, documentation=u'Line strength'))

RadiativeTransitionProbabilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Multipole'), MultipoleType, scope=RadiativeTransitionProbabilityType, documentation=u'Transition multipole type. Example: E2'))

RadiativeTransitionProbabilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'WeightedOscillatorStrength'), DataType, scope=RadiativeTransitionProbabilityType, documentation=u'Weighted oscillator strength'))

RadiativeTransitionProbabilityType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'), DataType, scope=RadiativeTransitionProbabilityType, documentation=u'Log10 of the weighted oscillator strength'))
RadiativeTransitionProbabilityType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'TransitionProbabilityA'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'OscillatorStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'LineStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'WeightedOscillatorStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'LineStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'OscillatorStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'WeightedOscillatorStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'LineStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'WeightedOscillatorStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'TransitionProbabilityA'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'OscillatorStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'LineStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'WeightedOscillatorStrength'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'IdealisedIntensity'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Multipole'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'Log10WeightedOscillatorStregnth'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeTransitionProbabilityType._UseForTag(pyxb.namespace.ExpandedName(None, u'WeightedOscillatorStrength'))),
    ])
    , 9 : pyxb.binding.content.ContentModelState(state=9, is_final=True, transitions=[
    ])
})



LKCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'L'), OrbitalAngularMomentumType, scope=LKCouplingType, documentation=u'Value of the sum of orbital angular momenta of the core and external electron '))

LKCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'K'), AngularMomentumType, scope=LKCouplingType, documentation=u'Value of the K-number (L + spin of the core)'))
LKCouplingType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LKCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'L'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
LKCouplingType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LKCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'K'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(LKCouplingType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(LKCouplingType._ContentModel_2, True),
])
LKCouplingType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})


StateEnergyType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=StateEnergyType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=StateEnergyType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=StateEnergyType._UseForTag(pyxb.namespace.ExpandedName(None, u'Accuracy'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=StateEnergyType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



SolidType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Layer'), MaterialType, scope=SolidType))
SolidType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SolidType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SolidType._UseForTag(pyxb.namespace.ExpandedName(None, u'Layer'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SolidType._UseForTag(pyxb.namespace.ExpandedName(None, u'Layer'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SolidType._UseForTag(pyxb.namespace.ExpandedName(None, u'Layer'))),
    ])
})



CollisionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CollisionalTransition'), CollisionalTransitionType, scope=CollisionsType, documentation=u'A specific collisional transition'))
CollisionsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CollisionsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionsType._UseForTag(pyxb.namespace.ExpandedName(None, u'CollisionalTransition'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionsType._UseForTag(pyxb.namespace.ExpandedName(None, u'CollisionalTransition'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionsType._UseForTag(pyxb.namespace.ExpandedName(None, u'CollisionalTransition'))),
    ])
})



RadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Probability'), RadiativeTransitionProbabilityType, scope=RadiativeTransitionType, documentation=u'Radiative transition probability and related parameters'))

RadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FinalStateRef'), StateRef, scope=RadiativeTransitionType, documentation=u'Reference to the final state'))

RadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'InitialStateRef'), StateRef, scope=RadiativeTransitionType, documentation=u'Reference to the initial state'))

RadiativeTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EnergyWavelength'), EnergyWavelengthType, scope=RadiativeTransitionType, documentation=u'List of energy/spectrum parameters'))
RadiativeTransitionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'EnergyWavelength'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Probability'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'EnergyWavelength'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Probability'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'FinalStateRef'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'InitialStateRef'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Probability'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'FinalStateRef'))),
    ])
})



VibrationalQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibrationalNu'), ComplexMolecularQuantumNumberType, scope=VibrationalQuantumNumbersType))

VibrationalQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumP'), MagneticQuantumNumberType, scope=VibrationalQuantumNumbersType))

VibrationalQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalVibrationL'), MolecularQuantumNumberType, scope=VibrationalQuantumNumbersType))

VibrationalQuantumNumbersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumK'), MagneticQuantumNumberType, scope=VibrationalQuantumNumbersType))
VibrationalQuantumNumbersType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalVibrationL'))),
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=VibrationalQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalNu'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=VibrationalQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumP'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=VibrationalQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumK'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=VibrationalQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumP'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=VibrationalQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumK'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=VibrationalQuantumNumbersType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibronicAngularMomentumP'))),
    ])
})



DataSetsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DataSet'), DataSetType, scope=DataSetsType, documentation=u'List of datasets of different nature (cross sections, rate coefficients, etc.)'))
DataSetsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataSetsType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataSet'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataSetsType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataSet'))),
    ])
})



ReactantsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StateRef'), StateRef, scope=ReactantsType, documentation=u'Reference to a specific state'))
ReactantsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ReactantsType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateRef'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ReactantsType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateRef'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ReactantsType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateRef'))),
    ])
})



MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LifeTime'), DataType, scope=MolecularStateCharacterisation_oldType))

MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StateEnergy'), StateEnergyType, scope=MolecularStateCharacterisation_oldType))

MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parameters'), CharacterisationType, scope=MolecularStateCharacterisation_oldType))

MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'), pyxb.binding.datatypes.positiveInteger, scope=MolecularStateCharacterisation_oldType))

MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'), pyxb.binding.datatypes.positiveInteger, scope=MolecularStateCharacterisation_oldType))

MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PseudoStatisticalWeight'), PseudoStatisticalWeightType, scope=MolecularStateCharacterisation_oldType))

MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PseudoNuclearStatisticalWeight'), PseudoStatisticalWeightType, scope=MolecularStateCharacterisation_oldType))

MolecularStateCharacterisation_oldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'), pyxb.binding.datatypes.string, scope=MolecularStateCharacterisation_oldType))
MolecularStateCharacterisation_oldType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateEnergy'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoNuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoNuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoNuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoNuclearStatisticalWeight'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisation_oldType._UseForTag(pyxb.namespace.ExpandedName(None, u'PseudoNuclearStatisticalWeight'))),
    ])
})



CollisionalTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IntermediateStates'), ProductsType, scope=CollisionalTransitionType, documentation=u'List of intermediate state'))

CollisionalTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Products'), ProductsType, scope=CollisionalTransitionType, documentation=u'List of final states'))

CollisionalTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Threshold'), DataType, scope=CollisionalTransitionType, documentation=u'Reaction threshold'))

CollisionalTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ProcessClass'), CollisionalProcessClassType, scope=CollisionalTransitionType, documentation=u'Collisional process'))

CollisionalTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Reactants'), ReactantsType, scope=CollisionalTransitionType, documentation=u'List of reacting systems'))

CollisionalTransitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DataSets'), DataSetsType, scope=CollisionalTransitionType))
CollisionalTransitionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProcessClass'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProcessClass'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Reactants'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'IntermediateStates'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Products'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataSets'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Threshold'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Threshold'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataSets'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataSets'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'DataSets'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Products'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=CollisionalTransitionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Threshold'))),
    ])
})



SimpleSymbolType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RightCoefficient'), pyxb.binding.datatypes.string, scope=SimpleSymbolType))

SimpleSymbolType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CentralSymbol'), CentralSymbolType, scope=SimpleSymbolType))

SimpleSymbolType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LeftCoefficient'), pyxb.binding.datatypes.string, scope=SimpleSymbolType))
SimpleSymbolType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SimpleSymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'CentralSymbol'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=SimpleSymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'RightCoefficient'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=SimpleSymbolType._UseForTag(pyxb.namespace.ExpandedName(None, u'LeftCoefficient'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



FunctionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Function'), FunctionType, scope=FunctionsType))
FunctionsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=FunctionsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Function'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=FunctionsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Function'))),
    ])
})



CharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Name'), pyxb.binding.datatypes.string, scope=CharacterisationType))

CharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StringValue'), pyxb.binding.datatypes.string, scope=CharacterisationType))

CharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IntValue'), pyxb.binding.datatypes.integer, scope=CharacterisationType))

CharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FloatValue'), pyxb.binding.datatypes.float, scope=CharacterisationType))
CharacterisationType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'StringValue'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'IntValue'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'FloatValue'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'StringValue'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'IntValue'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'FloatValue'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'StringValue'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'IntValue'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=CharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'FloatValue'))),
    ])
})



MoleculeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MolecularChemicalSpecies'), MolecularChemicalSpeciesType, scope=MoleculeType))

MoleculeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MolecularState'), MolecularStateType, scope=MoleculeType))
MoleculeType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MoleculeType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularChemicalSpecies'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MoleculeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MoleculeType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularState'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MoleculeType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularChemicalSpecies'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MoleculeType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularState'))),
    ])
})



NonRadiativeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NonRadiativeTransition'), NonRadiativeTransitionType, scope=NonRadiativeType))
NonRadiativeType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonRadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonRadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonRadiativeTransition'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonRadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonRadiativeTransition'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonRadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonRadiativeTransition'))),
    ])
})



RotationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'), pyxb.binding.datatypes.string, scope=RotationalComponentType))

RotationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NonLinearPolyatomic'), NonLinearPolyatomicType, scope=RotationalComponentType))

RotationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DiatomAndLinearPolyatomic'), DiatomAndLinearPolyatomicType, scope=RotationalComponentType))

RotationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), MixingCoefficientType, scope=RotationalComponentType))
RotationalComponentType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RotationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'NonLinearPolyatomic'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RotationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'DiatomAndLinearPolyatomic'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RotationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RotationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



VibrationalCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibrationalSpeciesNotation'), SymbolType, scope=VibrationalCharacterisationType))

VibrationalCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibronicSpeciesNotation'), SymbolType, scope=VibrationalCharacterisationType))
VibrationalCharacterisationType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=VibrationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalSpeciesNotation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibronicSpeciesNotation'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibronicSpeciesNotation'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



LinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'), HyperfineCouplingBType, scope=LinearElecCouplingType))

LinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineCaseABeta'), HyperfineCaseABetaType, scope=LinearElecCouplingType))

LinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=LinearElecCouplingType))

LinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EfSymmetry'), EfSymmetryType, scope=LinearElecCouplingType))

LinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HundCaseA'), HundCaseAType, scope=LinearElecCouplingType))

LinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineCaseAAlpha'), HyperfineCaseAAlphaType, scope=LinearElecCouplingType))

LinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HundCaseB'), HundCaseBType, scope=LinearElecCouplingType))
LinearElecCouplingType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCaseABeta'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HundCaseA'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'EfSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCaseAAlpha'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HundCaseB'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HundCaseA'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCaseABeta'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCaseAAlpha'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HundCaseB'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCaseABeta'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCaseAAlpha'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HundCaseB'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCaseABeta'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HundCaseB'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineCouplingHundCaseB'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=LinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'HundCaseB'))),
    ])
})



IsotopeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=IsotopeType))

IsotopeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IsotopeParameters'), IsotopeParametersType, scope=IsotopeType, documentation=u'Parameters of a specific isotope'))

IsotopeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IonState'), IonStateType, scope=IsotopeType, documentation=u'List of ionization states'))
IsotopeType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=IsotopeType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonState'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=IsotopeType._UseForTag(pyxb.namespace.ExpandedName(None, u'IsotopeParameters'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=IsotopeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=IsotopeType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonState'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=IsotopeType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonState'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



HinderedMotionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HinderedK1'), MolecularQuantumNumberType, scope=HinderedMotionType))

HinderedMotionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HinderedK2'), MolecularQuantumNumberType, scope=HinderedMotionType))
HinderedMotionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=HinderedMotionType._UseForTag(pyxb.namespace.ExpandedName(None, u'HinderedK1'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=HinderedMotionType._UseForTag(pyxb.namespace.ExpandedName(None, u'HinderedK2'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



IonStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IonCharge'), pyxb.binding.datatypes.integer, scope=IonStateType, documentation=u'Ion charge. Example: 12.'))

IonStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AtomicState'), AtomicStateType, scope=IonStateType, documentation=u'List of atomic states within an ion'))

IonStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IsoelectronicSequence'), ElementSymbolType, scope=IonStateType, documentation=u'Chemical element representation of isoelectronic sequence. Example: He.'))
IonStateType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=IonStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=IonStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonCharge'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=IonStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonCharge'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=IonStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicState'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=IonStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'IsoelectronicSequence'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=IonStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicState'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=IonStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicState'))),
    ])
})



MaterialComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Percentage'), pyxb.binding.datatypes.decimal, scope=MaterialComponentType))

MaterialComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ChemicalElement'), ChemicalElementType, scope=MaterialComponentType))

MaterialComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StoichiometricValue'), pyxb.binding.datatypes.decimal, scope=MaterialComponentType))
MaterialComponentType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'ChemicalElement'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MaterialComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'StoichiometricValue'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MaterialComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Percentage'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



ArgumentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Name'), pyxb.binding.datatypes.anyType, scope=ArgumentType, documentation=u'Name of the argument. Example: a'))

ArgumentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.anyType, scope=ArgumentType, documentation=u'Further description of the argument if definition in `parameter` is not sufficient'))
ArgumentType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ArgumentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ArgumentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



OrbitalAngularMomentumType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Value'), pyxb.binding.datatypes.nonNegativeInteger, scope=OrbitalAngularMomentumType, documentation=u'Value of the orbital angular momentum'))

OrbitalAngularMomentumType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Symbol'), OrbitalAngularMomentumSymbolType, scope=OrbitalAngularMomentumType, documentation=u'Symbol of the orbital angular momentum'))
OrbitalAngularMomentumType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=OrbitalAngularMomentumType._UseForTag(pyxb.namespace.ExpandedName(None, u'Value'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
OrbitalAngularMomentumType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=OrbitalAngularMomentumType._UseForTag(pyxb.namespace.ExpandedName(None, u'Symbol'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(OrbitalAngularMomentumType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(OrbitalAngularMomentumType._ContentModel_2, False),
])
OrbitalAngularMomentumType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



jKCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'j'), AngularMomentumType, scope=jKCouplingType, documentation=u'Value of the total angular momentum of the core'))

jKCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'K'), AngularMomentumType, scope=jKCouplingType, documentation=u'Value of the K-number (j + orbital angular momentum of the external electron)'))
jKCouplingType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=jKCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'j'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
jKCouplingType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=jKCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'K'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(jKCouplingType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(jKCouplingType._ContentModel_2, True),
])
jKCouplingType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



AtomicStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AtomicNumericalData'), AtomicNumericalDataType, scope=AtomicStateType, documentation=u'Numerical parameters describing an atomic state'))

AtomicStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AtomicComposition'), AtomicCompositionType, scope=AtomicStateType, documentation=u'Expansion of the wavefunction in a specific basis'))

AtomicStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AtomicQuantumNumbers'), AtomicQuantumNumbersType, scope=AtomicStateType, documentation=u'Discrete quantum numbers describing an atomic state'))

AtomicStateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=AtomicStateType, documentation=u'An arbitrary label'))
AtomicStateType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicComposition'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicNumericalData'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicComposition'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicNumericalData'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicComposition'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicComposition'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicNumericalData'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicStateType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomicComposition'))),
    ])
})



NonLinearNoElecHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), HyperfineQuantumNumbersType, scope=NonLinearNoElecHyperFType))
NonLinearNoElecHyperFType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearNoElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearNoElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularProjection'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearNoElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'C2Symmetries'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearNoElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearNoElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
    ])
})



DiatomAndLinearPolyatomicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LinearNoElecHyperF'), LinearNoElecHyperFType, scope=DiatomAndLinearPolyatomicType))

DiatomAndLinearPolyatomicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LinearNoElecNoHyperF'), LinearNoElecNoHyperFType, scope=DiatomAndLinearPolyatomicType))

DiatomAndLinearPolyatomicType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LinearElecCoupling'), LinearElecCouplingType, scope=DiatomAndLinearPolyatomicType))
DiatomAndLinearPolyatomicType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DiatomAndLinearPolyatomicType._UseForTag(pyxb.namespace.ExpandedName(None, u'LinearNoElecNoHyperF'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DiatomAndLinearPolyatomicType._UseForTag(pyxb.namespace.ExpandedName(None, u'LinearNoElecHyperF'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DiatomAndLinearPolyatomicType._UseForTag(pyxb.namespace.ExpandedName(None, u'LinearElecCoupling'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



AtomicCoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'), AngularMomentumType, scope=AtomicCoreType, documentation=u'Total angular momentum of the core'))

AtomicCoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Term'), TermType, scope=AtomicCoreType, documentation=u'Term of the core'))

AtomicCoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Configuration'), ConfigurationType, scope=AtomicCoreType, documentation=u'Configuration of the core'))

AtomicCoreType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ElementCore'), ElementSymbolType, scope=AtomicCoreType, documentation=u'Isoelectronic atom of the core. Example: Xe'))
AtomicCoreType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'Term'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'Configuration'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElementCore'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'Term'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentum'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'Term'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomicCoreType._UseForTag(pyxb.namespace.ExpandedName(None, u'Configuration'))),
    ])
})



MolecularStateCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parameters'), CharacterisationType, scope=MolecularStateCharacterisationType))

MolecularStateCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StateEnergy'), StateEnergyType, scope=MolecularStateCharacterisationType))

MolecularStateCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'), pyxb.binding.datatypes.positiveInteger, scope=MolecularStateCharacterisationType))

MolecularStateCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'), pyxb.binding.datatypes.positiveInteger, scope=MolecularStateCharacterisationType))

MolecularStateCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'), pyxb.binding.datatypes.string, scope=MolecularStateCharacterisationType))

MolecularStateCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LifeTime'), DataType, scope=MolecularStateCharacterisationType))
MolecularStateCharacterisationType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'StateEnergy'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearSpinSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'NuclearStatisticalWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularStateCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'LifeTime'))),
    ])
})



AtomsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Atom'), AtomType, scope=AtomsType))
AtomsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Atom'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Atom'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Atom'))),
    ])
})



RotationalHomeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=RotationalHomeType))

RotationalHomeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comment'), pyxb.binding.datatypes.string, scope=RotationalHomeType))

RotationalHomeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RotationalCharacterisation'), RotationalCharacterisationType, scope=RotationalHomeType))

RotationalHomeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RotationalComponent'), RotationalComponentType, scope=RotationalHomeType))
RotationalHomeType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalComponent'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalComponent'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalComponent'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalComponent'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalComponent'))),
    ])
})



RotationalCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'InversionSymmetry'), PermutationSymmetryType, scope=RotationalCharacterisationType, documentation=u'corresponds to (a) or (s)'))

RotationalCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RovibronicSpeciesNotation'), SymbolType, scope=RotationalCharacterisationType))

RotationalCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PermutationSymmetry'), PermutationSymmetryType, scope=RotationalCharacterisationType, documentation=u'corresponds to (a) or (s)'))

RotationalCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RovibrationalSpeciesNotation'), SymbolType, scope=RotationalCharacterisationType))

RotationalCharacterisationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RovibronicAngularMomentumP'), MagneticQuantumNumberType, scope=RotationalCharacterisationType))
RotationalCharacterisationType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'RovibronicSpeciesNotation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'RovibronicAngularMomentumP'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'PermutationSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'RovibrationalSpeciesNotation'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'InversionSymmetry'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'InversionSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'PermutationSymmetry'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'PermutationSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'RovibronicSpeciesNotation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'RovibronicAngularMomentumP'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'InversionSymmetry'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'InversionSymmetry'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'PermutationSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'RovibronicAngularMomentumP'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RotationalCharacterisationType._UseForTag(pyxb.namespace.ExpandedName(None, u'InversionSymmetry'))),
    ])
})



RadiativeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RadiativeTransition'), RadiativeTransitionType, scope=RadiativeType, documentation=u'Description of a specific radiative transition'))
RadiativeType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=RadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RadiativeTransition'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RadiativeTransition'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=RadiativeType._UseForTag(pyxb.namespace.ExpandedName(None, u'RadiativeTransition'))),
    ])
})



ElectronicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.token, scope=ElectronicComponentType))

ElectronicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionL'), MolecularQuantumNumberType, scope=ElectronicComponentType))

ElectronicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comment'), pyxb.binding.datatypes.string, scope=ElectronicComponentType))

ElectronicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'), pyxb.binding.datatypes.string, scope=ElectronicComponentType))

ElectronicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), MixingCoefficientType, scope=ElectronicComponentType))

ElectronicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ElectronicCharacterisation'), ElectronicCharacterisationType, scope=ElectronicComponentType))

ElectronicComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibrationalHome'), VibrationalHomeType, scope=ElectronicComponentType))
ElectronicComponentType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionL'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalHome'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionL'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalHome'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionL'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalHome'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionL'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalHome'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionL'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalHome'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ElectronicComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalHome'))),
    ])
})



AtomicCompositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Component'), AtomicComponentType, scope=AtomicCompositionType, documentation=u'Component of the state wavefunction'))
AtomicCompositionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomicCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Component'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Component'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomicCompositionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Component'))),
    ])
})



MoleculeNuclearSpinsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AtomArray'), AtomArrayType, scope=MoleculeNuclearSpinsType))

MoleculeNuclearSpinsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'BondArray'), BondArrayType, scope=MoleculeNuclearSpinsType))
MoleculeNuclearSpinsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MoleculeNuclearSpinsType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomArray'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MoleculeNuclearSpinsType._UseForTag(pyxb.namespace.ExpandedName(None, u'BondArray'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



BondArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Bond'), BondType, scope=BondArrayType))
BondArrayType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=BondArrayType._UseForTag(pyxb.namespace.ExpandedName(None, u'Bond'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=BondArrayType._UseForTag(pyxb.namespace.ExpandedName(None, u'Bond'))),
    ])
})



MolecularPropertiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MolecularWeight'), DataType, scope=MolecularPropertiesType))

MolecularPropertiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'OtherProperties'), CharacterisationType, scope=MolecularPropertiesType))
MolecularPropertiesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularPropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularWeight'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularPropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'OtherProperties'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularPropertiesType._UseForTag(pyxb.namespace.ExpandedName(None, u'OtherProperties'))),
    ])
})



MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'), MolecularPropertiesType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'URLFigure'), pyxb.binding.datatypes.anyURI, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'InChI'), ReferencedTextType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IUPACName'), ReferencedTextType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'), ReferencedTextType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'OrdinaryStructuralFormula'), ReferencedTextType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CNPIGroup'), SymbolType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ChemicalName'), ReferencedTextType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'), MoleculeNuclearSpinsType, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'StoichiometricFormula'), pyxb.binding.datatypes.string, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'IonCharge'), pyxb.binding.datatypes.integer, scope=MolecularChemicalSpeciesType))

MolecularChemicalSpeciesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comment'), pyxb.binding.datatypes.string, scope=MolecularChemicalSpeciesType))
MolecularChemicalSpeciesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'OrdinaryStructuralFormula'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StoichiometricFormula'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CNPIGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'URLFigure'))),
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'InChI'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'IUPACName'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CNPIGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ChemicalName'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=11, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'IonCharge'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'InChI'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CNPIGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'URLFigure'))),
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'InChI'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'IUPACName'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CNPIGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'URLFigure'))),
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'InChI'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CNPIGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 9 : pyxb.binding.content.ContentModelState(state=9, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 10 : pyxb.binding.content.ContentModelState(state=10, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CNPIGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 11 : pyxb.binding.content.ContentModelState(state=11, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'URLFigure'))),
        pyxb.binding.content.ContentModelTransition(next_state=12, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'StableMolecularProperties'))),
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'InChI'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'IUPACName'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CASRegistryNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'CNPIGroup'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'ChemicalName'))),
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'MoleculeNuclearSpins'))),
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 12 : pyxb.binding.content.ContentModelState(state=12, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=13, element_use=MolecularChemicalSpeciesType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 13 : pyxb.binding.content.ContentModelState(state=13, is_final=True, transitions=[
    ])
})



ParametersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parameter'), ParameterType, scope=ParametersType))
ParametersType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameter'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameter'))),
    ])
})



FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Name'), pyxb.binding.datatypes.string, scope=FunctionType, documentation=u'Function name. Example: BELI'))

FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SourceCodeURL'), pyxb.binding.datatypes.string, scope=FunctionType, documentation=u'Location of source code '))

FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=FunctionType, documentation=u'Description of a function.'))

FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Y'), ArgumentType, scope=FunctionType))

FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Arguments'), ArgumentsType, scope=FunctionType))

FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Expression'), ExpressionType, scope=FunctionType, documentation=u'Function expression in a specified programming language. Example: a*X1**2+2.5 (a is the parameter defined in the "parameters" list).'))

FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parameters'), ParametersType, scope=FunctionType, documentation=u'List of parameters used in the function'))

FunctionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ReferenceFrame'), ReferenceFrameType, scope=FunctionType, documentation=u'Reference frame in which is given the velocity, energy...'))
FunctionType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Expression'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Expression'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Expression'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'SourceCodeURL'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'ReferenceFrame'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Y'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'SourceCodeURL'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=9, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Arguments'))),
    ])
    , 9 : pyxb.binding.content.ContentModelState(state=9, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'ReferenceFrame'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'SourceCodeURL'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameters'))),
        pyxb.binding.content.ContentModelTransition(next_state=10, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
    ])
    , 10 : pyxb.binding.content.ContentModelState(state=10, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FunctionType._UseForTag(pyxb.namespace.ExpandedName(None, u'SourceCodeURL'))),
    ])
})



SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'City'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'City of publication. Example: Bristol.'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'DigitalObjectIdentifier'), pyxb.binding.datatypes.token, scope=SourceType, documentation=u'Digital Object Identifier. Example: doi:10.1016/j.adt.2007.11.003'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Editors'), EditorsType, scope=SourceType))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SourceName'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'Bibliographic reference name. Example: Physical Review'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Volume'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'Volume of the bibliographic reference. Example: 72A'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Title'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'Title'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ProductionDate'), pyxb.binding.datatypes.date, scope=SourceType, documentation=u'Date of the reference'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PageEnd'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'Final page of a bibliographic reference. Example: 23'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Version'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'Version of a database, code, etc.'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Authors'), AuthorsType, scope=SourceType))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'UniformResourceIdentifier'), pyxb.binding.datatypes.anyURI, scope=SourceType, documentation=u'A Uniform Resource Identifier of a bibliographic reference. Example: http://www.iop.org/EJ/abstract/0953-4075/41/10/105002'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=SourceType))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Year'), pyxb.binding.datatypes.gYear, scope=SourceType, documentation=u'Year of the bibliographic reference. Example: 2008'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Publisher'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'Publisher of a bibliographic reference. Example: IOP Publishing Ltd'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Category'), CategoryType, scope=SourceType, documentation=u'Bibliographic reference type. Example: journal'))

SourceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PageBegin'), pyxb.binding.datatypes.string, scope=SourceType, documentation=u'Initial page of a bibliographic reference. Example: 22'))
SourceType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Category'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'SourceName'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Year'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Authors'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_5 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Title'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_6 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Volume'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_7 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'DigitalObjectIdentifier'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_8 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'PageBegin'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_9 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'PageEnd'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_10 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'UniformResourceIdentifier'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_11 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Publisher'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_12 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'City'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_13 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Editors'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_14 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProductionDate'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_15 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Version'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
SourceType._ContentModel_16 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=SourceType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_2, True),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_3, True),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_4, True),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_5, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_6, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_7, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_8, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_9, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_10, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_11, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_12, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_13, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_14, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_15, False),
    pyxb.binding.content.ModelGroupAllAlternative(SourceType._ContentModel_16, False),
])
SourceType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



FitParametersType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Parameter'), pyxb.binding.datatypes.double, scope=FitParametersType))
FitParametersType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=1, element_use=FitParametersType._UseForTag(pyxb.namespace.ExpandedName(None, u'Parameter'))),
    ])
})



VibrationalHomeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Polyad'), CharacterisationType, scope=VibrationalHomeType))

VibrationalHomeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibrationalComponent'), VibrationalComponentType, scope=VibrationalHomeType))
VibrationalHomeType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=VibrationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'Polyad'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalComponent'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalComponent'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalComponent'))),
    ])
})



ShellsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Shell'), ShellType, scope=ShellsType, documentation=u'Atomic shell'))

ShellsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ShellPair'), ShellPairType, scope=ShellsType))
ShellsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Shell'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ShellsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Shell'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ShellsType._UseForTag(pyxb.namespace.ExpandedName(None, u'ShellPair'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ShellsType._UseForTag(pyxb.namespace.ExpandedName(None, u'ShellPair'))),
    ])
})



LinearNoElecNoHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), MolecularQuantumNumberType, scope=LinearNoElecNoHyperFType))

LinearNoElecNoHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberN'), MagneticQuantumNumberType, scope=LinearNoElecNoHyperFType))
LinearNoElecNoHyperFType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=LinearNoElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=LinearNoElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberN'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



jjCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'j'), AngularMomentumType, scope=jjCouplingType, documentation=u'Value of the total angular momentum'))
jjCouplingType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=jjCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'j'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=jjCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'j'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=jjCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'j'))),
    ])
})



AuthorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Name'), pyxb.binding.datatypes.string, scope=AuthorType, documentation=u"Author's name. Example: A. Einstein"))

AuthorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Address'), pyxb.binding.datatypes.string, scope=AuthorType, documentation=u"Author's address. Example: AMD Unit, IAEA, Vienna, Austria"))
AuthorType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AuthorType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AuthorType._UseForTag(pyxb.namespace.ExpandedName(None, u'Address'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



EditorsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Name'), pyxb.binding.datatypes.string, scope=EditorsType, documentation=u'Name of an editor'))
EditorsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=EditorsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=EditorsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
    ])
})



FitDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'), pyxb.binding.datatypes.string, scope=FitDataType, documentation=u'Description of physical uncertainty'))

FitDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FitAccuracy'), pyxb.binding.datatypes.string, scope=FitDataType, documentation=u'Description of fit accuracy'))

FitDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FunctionRef'), pyxb.binding.datatypes.IDREF, scope=FitDataType, documentation=u'Reference to the fitting function'))

FitDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FitValidityLimits'), FitValidityLimitsType, scope=FitDataType, documentation=u'Limits of the fit validity'))

FitDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FitParameters'), FitParametersType, scope=FitDataType, documentation=u'Fitting parameters'))

FitDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ProductionDate'), pyxb.binding.datatypes.date, scope=FitDataType, documentation=u'Fit production date'))
FitDataType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'FunctionRef'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'FunctionRef'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'FitValidityLimits'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'FitValidityLimits'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'FitParameters'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'FitAccuracy'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProductionDate'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'PhysicalUncertainty'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProductionDate'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FitDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'ProductionDate'))),
    ])
})



VibrationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=VibrationalComponentType))

VibrationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'), MixingCoefficientType, scope=VibrationalComponentType))

VibrationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'), pyxb.binding.datatypes.string, scope=VibrationalComponentType))

VibrationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibrationalCharacterisation'), VibrationalCharacterisationType, scope=VibrationalComponentType))

VibrationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'VibrationalQuantumNumbers'), VibrationalQuantumNumbersType, scope=VibrationalComponentType))

VibrationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RotationalHome'), RotationalHomeType, scope=VibrationalComponentType))

VibrationalComponentType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comment'), pyxb.binding.datatypes.token, scope=VibrationalComponentType))
VibrationalComponentType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalHome'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalHome'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'SerialQuantumNumber'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'MixingCoefficient'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalCharacterisation'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'VibrationalQuantumNumbers'))),
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalHome'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'RotationalHome'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=VibrationalComponentType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comment'))),
    ])
})



AtomArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'AtomN'), AtomNType, scope=AtomArrayType))
AtomArrayType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomArrayType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomArrayType._UseForTag(pyxb.namespace.ExpandedName(None, u'AtomN'))),
    ])
})


AtomNType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomNType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



ArgumentsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Argument'), ArgumentType, scope=ArgumentsType))
ArgumentsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ArgumentsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Argument'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ArgumentsType._UseForTag(pyxb.namespace.ExpandedName(None, u'Argument'))),
    ])
})



NonLinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MolecularProjection'), MolecularProjectionType, scope=NonLinearElecCouplingType))

NonLinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), ComplexMolecularQuantumNumberType, scope=NonLinearElecCouplingType))

NonLinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'EfSymmetry'), EfSymmetryType, scope=NonLinearElecCouplingType))

NonLinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'RoVibronicSplitting'), RoVibronicSplittingType, scope=NonLinearElecCouplingType))

NonLinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Label'), pyxb.binding.datatypes.string, scope=NonLinearElecCouplingType))

NonLinearElecCouplingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), MolecularQuantumNumberType, scope=NonLinearElecCouplingType))
NonLinearElecCouplingType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'EfSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'EfSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularProjection'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=NonLinearElecCouplingType._UseForTag(pyxb.namespace.ExpandedName(None, u'RoVibronicSplitting'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
    ])
})



NonLinearElecHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), HyperfineQuantumNumbersType, scope=NonLinearElecHyperFType))
NonLinearElecHyperFType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'EfSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'EfSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularProjection'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'RoVibronicSplitting'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearElecHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
})



XSAMSDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=XSAMSDataType, documentation=u'Any relevant comments'))

XSAMSDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'States'), StatesType, scope=XSAMSDataType, documentation=u'List of atomic states, molecular states, particles, surfaces, and solids'))

XSAMSDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Processes'), ProcessesType, scope=XSAMSDataType, documentation=u'Physical processes connecting states (e.g., radiative, collisional, autoionization, etc.)'))

XSAMSDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Sources'), SourcesType, scope=XSAMSDataType, documentation=u'All relevant references to data sources'))

XSAMSDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Methods'), MethodsType, scope=XSAMSDataType, documentation=u'List of methods used to produce the data'))

XSAMSDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Functions'), FunctionsType, scope=XSAMSDataType, documentation=u'List of functions used for data description and/or presentation (e.g., fitting)'))
XSAMSDataType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=XSAMSDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'States'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
XSAMSDataType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=XSAMSDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Processes'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
XSAMSDataType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=XSAMSDataType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Sources'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
XSAMSDataType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=XSAMSDataType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Methods'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
XSAMSDataType._ContentModel_5 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=XSAMSDataType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Functions'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
XSAMSDataType._ContentModel_6 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=XSAMSDataType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(XSAMSDataType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(XSAMSDataType._ContentModel_2, False),
    pyxb.binding.content.ModelGroupAllAlternative(XSAMSDataType._ContentModel_3, True),
    pyxb.binding.content.ModelGroupAllAlternative(XSAMSDataType._ContentModel_4, False),
    pyxb.binding.content.ModelGroupAllAlternative(XSAMSDataType._ContentModel_5, False),
    pyxb.binding.content.ModelGroupAllAlternative(XSAMSDataType._ContentModel_6, False),
])
XSAMSDataType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



DataSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TabulatedData'), TabulatedDataType, scope=DataSetType, documentation=u'Tables of data'))

DataSetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'FitData'), FitDataType, scope=DataSetType, documentation=u'Fits of data'))
DataSetType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'FitData'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'TabulatedData'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'TabulatedData'))),
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataSetType._UseForTag(pyxb.namespace.ExpandedName(None, u'FitData'))),
    ])
})



ElectronicHomeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ElectronicComponent'), ElectronicComponentType, scope=ElectronicHomeType))
ElectronicHomeType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicComponent'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ElectronicHomeType._UseForTag(pyxb.namespace.ExpandedName(None, u'ElectronicComponent'))),
    ])
})



HyperfineCaseABetaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), HyperfineQuantumNumbersType, scope=HyperfineCaseABetaType))

HyperfineCaseABetaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionJ'), MolecularQuantumNumberType, scope=HyperfineCaseABetaType))

HyperfineCaseABetaType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), ComplexMolecularQuantumNumberType, scope=HyperfineCaseABetaType))
HyperfineCaseABetaType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=HyperfineCaseABetaType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=HyperfineCaseABetaType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMolecularProjectionJ'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=HyperfineCaseABetaType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
    ])
})



HyperfineCouplingBType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'), HyperfineQuantumNumbersType, scope=HyperfineCouplingBType))

HyperfineCouplingBType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'CouplingType'), CouplingListType, scope=HyperfineCouplingBType))

HyperfineCouplingBType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'), MolecularQuantumNumberType, scope=HyperfineCouplingBType))

HyperfineCouplingBType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'), ComplexMolecularQuantumNumberType, scope=HyperfineCouplingBType))
HyperfineCouplingBType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=HyperfineCouplingBType._UseForTag(pyxb.namespace.ExpandedName(None, u'CouplingType'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=HyperfineCouplingBType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=HyperfineCouplingBType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=HyperfineCouplingBType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=HyperfineCouplingBType._UseForTag(pyxb.namespace.ExpandedName(None, u'HyperfineQuantumNumbers'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=True, transitions=[
    ])
})



FitValidityLimitsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'LowerLimit'), pyxb.binding.datatypes.double, scope=FitValidityLimitsType, documentation=u'Lower limit of fit validity'))

FitValidityLimitsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'UpperLimit'), pyxb.binding.datatypes.double, scope=FitValidityLimitsType, documentation=u'Upper limit of fit validity'))
FitValidityLimitsType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=FitValidityLimitsType._UseForTag(pyxb.namespace.ExpandedName(None, u'LowerLimit'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FitValidityLimitsType._UseForTag(pyxb.namespace.ExpandedName(None, u'UpperLimit'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=FitValidityLimitsType._UseForTag(pyxb.namespace.ExpandedName(None, u'UpperLimit'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



MaterialType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MaterialTopology'), pyxb.binding.datatypes.string, scope=MaterialType, documentation=u'Description of the material topology'))

MaterialType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MaterialTemperature'), DataType, scope=MaterialType, documentation=u'Temperature of the material'))

MaterialType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MaterialThickness'), DataType, scope=MaterialType, documentation=u'Thickness of a material'))

MaterialType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MaterialName'), pyxb.binding.datatypes.string, scope=MaterialType, documentation=u'Name of a material. Example: bronze'))

MaterialType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Comments'), pyxb.binding.datatypes.string, scope=MaterialType))

MaterialType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'MaterialComposition'), MaterialCompositionType, scope=MaterialType, documentation=u'Composition of a material'))
MaterialType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialType._UseForTag(pyxb.namespace.ExpandedName(None, u'MaterialName'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
MaterialType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialType._UseForTag(pyxb.namespace.ExpandedName(None, u'MaterialComposition'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
MaterialType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialType._UseForTag(pyxb.namespace.ExpandedName(None, u'MaterialThickness'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
MaterialType._ContentModel_4 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialType._UseForTag(pyxb.namespace.ExpandedName(None, u'MaterialTopology'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
MaterialType._ContentModel_5 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialType._UseForTag(pyxb.namespace.ExpandedName(None, u'MaterialTemperature'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
MaterialType._ContentModel_6 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=MaterialType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(MaterialType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(MaterialType._ContentModel_2, True),
    pyxb.binding.content.ModelGroupAllAlternative(MaterialType._ContentModel_3, False),
    pyxb.binding.content.ModelGroupAllAlternative(MaterialType._ContentModel_4, False),
    pyxb.binding.content.ModelGroupAllAlternative(MaterialType._ContentModel_5, False),
    pyxb.binding.content.ModelGroupAllAlternative(MaterialType._ContentModel_6, False),
])
MaterialType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})



ParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Name'), pyxb.binding.datatypes.token, scope=ParameterType, documentation=u'Name of a parameter. Example: a'))

ParameterType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Description'), pyxb.binding.datatypes.string, scope=ParameterType, documentation=u'Description of a parameter'))
ParameterType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=ParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'Name'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=ParameterType._UseForTag(pyxb.namespace.ExpandedName(None, u'Description'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



AtomType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Isotope'), IsotopeType, scope=AtomType, documentation=u'List of isotopes'))

AtomType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'ChemicalElement'), ChemicalElementType, scope=AtomType, documentation=u'Description of chemical elements'))
AtomType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=AtomType._UseForTag(pyxb.namespace.ExpandedName(None, u'Comments'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomType._UseForTag(pyxb.namespace.ExpandedName(None, u'ChemicalElement'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=AtomType._UseForTag(pyxb.namespace.ExpandedName(None, u'ChemicalElement'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomType._UseForTag(pyxb.namespace.ExpandedName(None, u'Isotope'))),
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=AtomType._UseForTag(pyxb.namespace.ExpandedName(None, u'Isotope'))),
    ])
})



DataXYType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'X'), DataTableType, scope=DataXYType))

DataXYType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'Y'), DataTableType, scope=DataXYType, documentation=u'Data value'))
DataXYType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataXYType._UseForTag(pyxb.namespace.ExpandedName(None, u'X'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=DataXYType._UseForTag(pyxb.namespace.ExpandedName(None, u'X'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=DataXYType._UseForTag(pyxb.namespace.ExpandedName(None, u'Y'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
})



NonLinearElecNoHyperFType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'), MagneticQuantumNumberType, scope=NonLinearElecNoHyperFType))
NonLinearElecNoHyperFType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'Label'))),
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'EfSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=4, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'EfSymmetry'))),
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 3 : pyxb.binding.content.ContentModelState(state=3, is_final=True, transitions=[
    ])
    , 4 : pyxb.binding.content.ContentModelState(state=4, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=5, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumN'))),
    ])
    , 5 : pyxb.binding.content.ContentModelState(state=5, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=6, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalAngularMomentumJ'))),
    ])
    , 6 : pyxb.binding.content.ContentModelState(state=6, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=7, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'MolecularProjection'))),
    ])
    , 7 : pyxb.binding.content.ContentModelState(state=7, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=8, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'RoVibronicSplitting'))),
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'))),
    ])
    , 8 : pyxb.binding.content.ContentModelState(state=8, is_final=True, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=3, element_use=NonLinearElecNoHyperFType._UseForTag(pyxb.namespace.ExpandedName(None, u'TotalMagneticQuantumNumberJ'))),
    ])
})



C2SymmetriesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'C2aSymmetry'), C2SymmetryType, scope=C2SymmetriesType))

C2SymmetriesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'C2bSymmetry'), C2SymmetryType, scope=C2SymmetriesType))

C2SymmetriesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, u'C2cSymmetry'), C2SymmetryType, scope=C2SymmetriesType, documentation=u'Vol II, p 51'))
C2SymmetriesType._ContentModel_1 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=C2SymmetriesType._UseForTag(pyxb.namespace.ExpandedName(None, u'C2bSymmetry'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
C2SymmetriesType._ContentModel_2 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=C2SymmetriesType._UseForTag(pyxb.namespace.ExpandedName(None, u'C2cSymmetry'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
C2SymmetriesType._ContentModel_3 = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, element_use=C2SymmetriesType._UseForTag(pyxb.namespace.ExpandedName(None, u'C2aSymmetry'))),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
__AModelGroup = pyxb.binding.content.ModelGroupAll(alternatives=[
    pyxb.binding.content.ModelGroupAllAlternative(C2SymmetriesType._ContentModel_1, True),
    pyxb.binding.content.ModelGroupAllAlternative(C2SymmetriesType._ContentModel_2, True),
    pyxb.binding.content.ModelGroupAllAlternative(C2SymmetriesType._ContentModel_3, True),
])
C2SymmetriesType._ContentModel = pyxb.binding.content.ContentModel(state_map = {
      1 : pyxb.binding.content.ContentModelState(state=1, is_final=False, transitions=[
        pyxb.binding.content.ContentModelTransition(next_state=2, term=__AModelGroup),
    ])
    , 2 : pyxb.binding.content.ContentModelState(state=2, is_final=True, transitions=[
    ])
})
