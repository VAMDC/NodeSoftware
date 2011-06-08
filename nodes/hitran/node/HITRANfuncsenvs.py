class chunk:
    def __init__(self, xml):
        self.xml = xml
    def XML(self):
        return self.xml

HITRANfuncs = [
chunk("""<Function functionID="FgammaL">
            <Comments>This function gives the pressure- and temperature-dependence of the Lorentzian
                      component of the pressure-broadened line width (HWHM)</Comments>
            <Expression computerLanguage="Fortran">
                gammaL_ref * p * (296./T)**n
            </Expression>
            <Y name="gammaL" units="1/cm">
            </Y>
            <Arguments>
                <Argument name="T" units="K">
                    <Description>The absolute temperature, in K</Description>
                </Argument>
                <Argument name="p" units="atm">
                    <Description>The partial pressure of the broadening species,
                                 in atm</Description>
                </Argument>
            </Arguments>
            <Parameters>
                <Parameter name="gammaL_ref" units="1/cm">
                    <Description>The Lorentzian HWHM of the line, broadened at
                        Tref = 296 K and broadening species partial pressure
                        pref = 1atm</Description>
                </Parameter>
                <Parameter name="n" units="unitless">
                    <Description>
                        The temperature exponent of the gammaL function
                    </Description>
                </Parameter>
            </Parameters>
        </Function>"""),
chunk("""<Function functionID="Fdelta">
            <Comments>This function gives the pressure-dependence of the absorption
                line wavenumber shift: nu = nu_ref + (delta).(p/pref)</Comments>
            <Expression computerLanguage="Fortran">
                delta_ref * p
            </Expression>
            <Y name="delta" units="1/cm">
            </Y>
            <Arguments>
                <Argument name="p" units="atm">
                    <Description>The pressure of the shifting environment,
                                 in atm</Description>
                </Argument>
            </Arguments>
            <Parameters>
                <Parameter name="delta_ref" units="1/cm">
                    <Description>The pressure-shift of the absorption line at
                        pref = 1 atm</Description>
                </Parameter>
            </Parameters>
            
        </Function>""")
]
HITRANenvs = [
chunk("""<!-- the HITRAN reference temperature, 296 K -->
    <Environment envID="EHITRAN_refT">
        <Temperature>
            <Value units="K">296.</Value>
        </Temperature>
    </Environment>"""),

chunk("""
    <!-- the HITRAN reference pressure and temperature, 1 atm and 296 K -->
    <Environment envID="EHITRAN_refpT">
        <Temperature>
            <Value units="K">296.</Value>
        </Temperature>
        <TotalPressure>
            <Value units="atm">1.</Value>
        </TotalPressure>  
    </Environment>"""),

chunk("""<!-- the HITRAN air-broadening reference conditions -->
    <Environment envID="Eair-broadening-ref-env">
        <Temperature>
            <Value units="K">296.</Value>
        </Temperature>
        <TotalPressure>
            <Value units="atm">1.</Value>
        </TotalPressure>
        <Composition>
            <Species name="N2">
                <MoleFraction>
                    <Value units="unitless">0.79</Value>
                </MoleFraction>
            </Species>
            <Species name="O2">
                <MoleFraction>
                    <Value units="unitless">0.21</Value>
                </MoleFraction>
            </Species>
        </Composition>
    </Environment>"""),

# hard to know what to do about the self-broadening environment...
# for now, just use Species name="self"
chunk("""<!-- the HITRAN self-broadening reference conditions -->
    <Environment envID="Eself-broadening-ref-env">
        <Temperature>
            <Value units="K">296.</Value>
        </Temperature>
        <TotalPressure>
            <Value units="atm">1.</Value>
        </TotalPressure>
        <Composition>
            <Species name="self">
                <MoleFraction>
                    <Value units="unitless">1.</Value>
                </MoleFraction>
            </Species>
        </Composition>
    </Environment>""")

]

