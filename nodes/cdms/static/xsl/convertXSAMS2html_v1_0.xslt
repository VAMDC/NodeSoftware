<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xsams="http://vamdc.org/xml/xsams/1.0">

  <xsl:output method="html"/>

  <xsl:key name="molecule" match="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule" use="@speciesID"/> 
  <xsl:key name="atom" match="/xsams:XSAMSData/xsams:Species/xsams:Atoms/xsams:Atom/xsams:Isotope/xsams:Ion" use="@speciesID"/> 
  <xsl:key name="particle" match="/xsams:XSAMSData/xsams:Species/xsams:Particles/xsams:Particle" use="@speciesID"/> 
  <xsl:key name="molstate" match="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState" use="@stateID"/>
  <xsl:key name="atomstate" match="/xsams:XSAMSData/xsams:Species/xsams:Atoms/xsams:Atom/xsams:Isotope/xsams:Ion/xsams:AtomicState" use="@stateID"/>


  <xsl:decimal-format name="example" zero-digit ="0" />

  <xsl:template match="/">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules"/>

        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Atoms"/>

	<xsl:text>&#xa;</xsl:text>

        <xsl:call-template name="Partitionfunctions">
        </xsl:call-template>

        <xsl:call-template name="States">
        </xsl:call-template>

        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Processes/xsams:Radiative"/>

        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Processes/xsams:Collisions"/>

        <xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Functions"/>

	<fieldset id="list_sources" class="subpage">
	<div class="legend">Sources</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist full">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Sources/xsams:Source"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>
<!--
  <xsl:template match="xsams:Molecules">
	<fieldset>
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full" style="list-style:none;">
        <xsl:apply-templates select="xsams:Molecule"/>
	</ul>
	</fieldset>
  </xsl:template>
-->
  <xsl:template match="xsams:Molecules">
	<fieldset id="list_molecules" class="subpage">
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<table class="vlist full">
        <xsl:apply-templates select="xsams:Molecule"/>
	</table>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams:Atoms">
	<fieldset id="list_atoms" class="subpage">
	<div class="legend">Atoms</div>
	<xsl:text>&#xa;</xsl:text>
	<table class="full">
        <xsl:apply-templates select="xsams:Atom"/>
	</table>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams:Functions">
	<fieldset id="list_functions" class="subpage">
	<div class="legend">Functions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full">
        <xsl:apply-templates select="xsams:Function"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>


  <xsl:template name="States">
	<fieldset id="list_states" class="subpage">
	<div class="legend">States</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full" style="list-style:none;">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template name="Partitionfunctions">
	<fieldset id="list_pfs"  class="subpage">
	<div class="legend">Partition functions</div>
	<xsl:text>&#xa;</xsl:text>
	<div class="full">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularChemicalSpecies/xsams:PartitionFunction"/>
	</div>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams:MolecularState">
    <li style="clear:both; border-bottom: 1px solid #90bade;">
     <div class="float_right">
       <xsl:call-template name="species_name">
         <xsl:with-param name="mol_id" select=".."/>
       </xsl:call-template>
     </div>
     <xsl:apply-templates select="xsams:MolecularStateCharacterisation"/>
     <div class="float_left"> <xsl:apply-templates select="xsams:Case/*[local-name()='QNs']/*"/> </div>
     <div style="clear:left"></div>
    </li>
  </xsl:template>

  <xsl:template match="xsams:MolecularStateCharacterisation">
    <div class="float_left" style="min-width:5ex;text-align:right">
      <xsl:apply-templates select="xsams:TotalStatisticalWeight"/>
    </div>
    <div class="float_left" style="min-width:15ex;text-align:right">
      <xsl:apply-templates select="xsams:StateEnergy"/>
    </div>
  </xsl:template>

  <xsl:template match="xsams:TotalStatisticalWeight">
    <xsl:value-of select="."/>
  </xsl:template>

  <xsl:template match="xsams:StateEnergy">
    <xsl:call-template name="DataType">
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="DataType">
    <xsl:value-of select="xsams:Value"/><xsl:text> </xsl:text>
    <xsl:value-of select="xsams:Value/@units"/>
    <xsl:if test="xsams:Accuracy">
      <xsl:value-of select="xsams:Accuracy"/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsams:Atom">
    <tr>
      <td>
        <div style="min-width:30ex"><b><xsl:value-of select="xsams:Isotope/xsams:Ion/@speciesID"/></b></div>
        <div class="float_left"> <xsl:value-of select="xsams:Isotope/xsams:Ion/xsams:InChIKey"/></div>
      </td>
      <td>
        <xsl:call-template name="atom-name">
          <xsl:with-param name="atom" select="."/>
        </xsl:call-template>
        <div style="clear:left"></div>
        <div class="float_left highlight"><xsl:value-of select="xsams:Isotope/xsams:Comments"/></div>
      </td>
    </tr>
  </xsl:template>

<!--
  <xsl:template match="xsams:Molecule">
	<li style="clear:left;">
	<h4>
	<xsl:value-of select="@speciesID" />	
	</h4>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Structural Formula</strong>
    	<var><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:OrdinaryStructuralFormula/xsams:Value"/></var>
	</div>

	<div class="columnar" style="clear:left">
  	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Stoichiometric Formula</strong>
    	<var><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Chemical Name</strong>
    	<var><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:ChemicalName/xsams:Value"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">InChi</strong>
    	<var><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:InChI"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">InChiKey</strong>
    	<var><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:InChIKey"/></var>
	</div>

	<div class="columnar" style="clear:left;">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Partition Function</strong>
    	<div style="float:left;min-width:12em;padding-right:1em;text-align:left;">
    	<var><xsl:apply-templates select="xsams:MolecularChemicalSpecies/xsams:PartitionFunction"/></var>
	</div>
	</div>
	</li>

  </xsl:template>
-->
  <xsl:template match="xsams:Molecule">
    <tr>
      <td>
	<div style="min-width:30ex"><b><xsl:value-of select="@speciesID" /></b></div>
        <div class="float_left" style="min-width:30ex"><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:InChIKey"/></div>
      </td>
      <td>
        <!-- <div class="float_left"><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:InChI"/></div> -->
    	<div class="float_left"><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:OrdinaryStructuralFormula/xsams:Value"/></div>
    	<div class="float_left"><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula"/></div> 
    	<div class="float_left"><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:ChemicalName/xsams:Value"/></div>
        <div style="clear:left"></div>
    	<div class="float_left highlight" style="text-align:left;"><xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:Comment"/></div>
      </td>	
    </tr>
  </xsl:template>

  <xsl:template match="xsams:Collisions">
	<fieldset id="list_collisions" class="subpage">
	<div class="legend">Collisional Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2" style="list-style:none;">
        <xsl:apply-templates select="xsams:CollisionalTransition"/>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams:Radiative">
	<fieldset id="list_radiative" class="subpage">
	<div class="legend">Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2" style="list-style:none;">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Processes/xsams:Radiative/xsams:RadiativeTransition"/>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams:RadiativeTransition">
	<li style="clear:both; border-bottom: 1px solid #90bade;">
	
	<div style="float:left; min-width:27em;">
	<ul style="list-style:none;">
	<li style="font-weight:bold">

        <xsl:apply-templates select="xsams:EnergyWavelength"/>

	<div style="float:left;text-align:right; min-width:10ex;">
        <xsl:value-of select="format-number(xsams:Probability/xsams:TransitionProbabilityA/xsams:Value,'0.00000000 ')"/>
	</div>

	 <div style="float:left;text-align:right; min-width:15ex;margin-right:1.0em">
   	  <xsl:value-of select="xsams:SourceRef"/>
	 </div>

	</li>


	<xsl:for-each select="xsams:EnergyWavelength/xsams:Frequency[position() > 1]">
<li style="clear:left">
 	 <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
	  <xsl:value-of select="format-number(xsams:Value,'0.0000')"/>
	 </div>

	 <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	  <xsl:value-of select="format-number(xsams:Accuracy,'0.0000 ')"/>
	 </div>

	 <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5ex">
	<xsl:text>- </xsl:text>
	 </div>

	 <div style="float:left;text-align:right; min-width:15ex;margin-right:1.0em">
   	  <xsl:value-of select="xsams:SourceRef"/>
	 </div>

</li>
        </xsl:for-each>

</ul>

	</div>

	<div style="float:left">
	<div>
	<div style="float:left;width:5ex">
	<xsl:text>I.S.: </xsl:text>
	</div>

	<xsl:call-template name="molec_state">
          <xsl:with-param name="state" select="key('molstate',current()/xsams:LowerStateRef)"/>
        </xsl:call-template>
	<xsl:call-template name="atomic_state">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams:LowerStateRef)"/>
        </xsl:call-template>

	</div>
	<div>
	
	<div style="float:left;width:5ex">
	<xsl:text>F.S.: </xsl:text>
	</div>

	<xsl:call-template name="molec_state">
          <xsl:with-param name="state" select="key('molstate',current()/xsams:UpperStateRef)"/>
        </xsl:call-template>
	<xsl:call-template name="atomic_state">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams:UpperStateRef)"/>
        </xsl:call-template>

	</div>
	</div>
	
	<div style="float:right">
          <xsl:call-template name="species_name">
          <xsl:with-param name="mol_id" select="key('molstate',current()/xsams:UpperStateRef)/../."/>
          <xsl:with-param name="atom_id" select="key('atomstate',current()/xsams:UpperStateRef)/../."/>
          </xsl:call-template>
	</div>
	</li>

  </xsl:template>


  <xsl:template name="species_name">
    <xsl:param name="mol_id"/>
    <xsl:param name="atom_id"/>
 
    <xsl:choose>
      <xsl:when test="$mol_id">
        <xsl:value-of select="$mol_id/@speciesID"/>:
        <xsl:value-of select="$mol_id/xsams:MolecularChemicalSpecies/xsams:OrdinaryStructuralFormula"/>
      </xsl:when>
      <xsl:when test="$atom_id">
        <xsl:value-of select="$atom_id/@speciesID"/>:
	<xsl:call-template name="atom-name">
          <xsl:with-param name="atom" select="$atom_id/../.."/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>N.N.</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>


  <xsl:template match="xsams:EnergyWavelength">
	<xsl:choose>
	  <xsl:when test="xsams:Frequency">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(xsams:Frequency/xsams:Value,'0.0000')"/>
	    </div>
  	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(xsams:Frequency/xsams:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>	
	  <xsl:when test="xsams:Wavenumber">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(29979.2458*xsams:Wavenumber/xsams:Value,'0.0000')"/>
	    </div>
	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(29979.2458*xsams:Wavenumber/xsams:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>
	  <xsl:when test="xsams:Wavelength">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(xsams:Wavelength/xsams:Value,'0.00000 ')"/>
            <xsl:value-of select="xsams:Wavelength/xsams:Value/@units"/>
	    </div>
	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(xsams:Wavelength/xsams:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>
	</xsl:choose>
  </xsl:template>

<!-- PRINT COLLISIONAL TRANSITION (currently only Species info) -->
  <xsl:template match="xsams:CollisionalTransition">
   <li style="clear:both; border-bottom: 1px solid #90bade;">

    <xsl:apply-templates select="xsams:Reactant"/>
    <xsl:text> -> </xsl:text>      
    <xsl:apply-templates select="xsams:Product"/>
    <xsl:text> : </xsl:text>          
    <xsl:apply-templates select="xsams:DataSets/xsams:DataSet/xsams:FitData"/>
    <xsl:apply-templates select="xsams:DataSets/xsams:DataSet/xsams:TabulatedData"/>
   </li>
  </xsl:template>


  <xsl:template match="xsams:Reactant">
    <b>
    <xsl:choose>
      <xsl:when test="key('molecule',current()/xsams:SpeciesRef)">
        <xsl:value-of select="key('molecule',current()/xsams:SpeciesRef)/xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula"/>
[
	<xsl:call-template name="molec_state_qn">
          <xsl:with-param name="state" select="key('molstate',current()/xsams:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:when test="key('particle',current()/xsams:SpeciesRef)">
        <xsl:value-of select="key('particle',current()/xsams:SpeciesRef)/@name"/>
        [<xsl:value-of select="xsams:StateRef"/>]    
      </xsl:when>
      <xsl:when test="key('atom',current()/xsams:SpeciesRef)">
	<xsl:call-template name="atom-name">
          <xsl:with-param name="atom" select="key('atom',current()/xsams:SpeciesRef)/../.."/>
        </xsl:call-template>
[
	<xsl:call-template name="atomic_state_qn">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>N.N.</xsl:text>
      </xsl:otherwise>
    </xsl:choose>

    
    <xsl:if test="position()!=last()">
      <xsl:text> + </xsl:text>
    </xsl:if>
    </b>
  </xsl:template>

  <xsl:template match="xsams:Product">
    <b>
    <xsl:choose>
      <xsl:when test="key('molecule',current()/xsams:SpeciesRef)">
        <xsl:value-of select="key('molecule',current()/xsams:SpeciesRef)/xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula"/>
[
	<xsl:call-template name="molec_state_qn">
          <xsl:with-param name="state" select="key('molstate',current()/xsams:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:when test="key('particle',current()/xsams:SpeciesRef)">
        <xsl:value-of select="key('particle',current()/xsams:SpeciesRef)/@name"/>
        [<xsl:value-of select="xsams:StateRef"/>]    
      </xsl:when>
      <xsl:when test="key('atom',current()/xsams:SpeciesRef)">
	<xsl:call-template name="atom-name">
          <xsl:with-param name="atom" select="key('atom',current()/xsams:SpeciesRef)/../.."/>
        </xsl:call-template>
[
	<xsl:call-template name="atomic_state_qn">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>N.N.</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
    
    <xsl:if test="position()!=last()">
      <xsl:text> + </xsl:text>
    </xsl:if>
    </b>
  </xsl:template>


  <xsl:template name="molec_state">
    <xsl:param name="state"/>

    <xsl:if test="count($state)>0">
    <div style="float:left;min-width:17ex">
      <xsl:value-of select="format-number($state/xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000', 'example')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="$state/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="$state/xsams:Case/*[local-name()='QNs']/*"/>
    </xsl:if>
  </xsl:template>


  <xsl:template name="atomic_state">
    <xsl:param name="state"/>
    <xsl:if test="count($state)>0">
    <div style="float:left;min-width:17ex">
      <xsl:value-of select="format-number($state/xsams:AtomicNumericalData/xsams:StatisticalWeight,' 0000', 'example')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="$state/xsams:AtomicNumericalData/xsams:StateEnergy/xsams:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="$state/xsams:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="$state/xsams:AtomicComposition"/>
    </xsl:if>

  </xsl:template>


  <xsl:template name="molec_state_qn">
    <xsl:param name="state"/>

    <xsl:apply-templates select="$state/xsams:Case/*[local-name()='QNs']/*"/>
  </xsl:template>


  <xsl:template name="atomic_state_qn">
    <xsl:param name="state"/>
    <xsl:apply-templates select="$state/xsams:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="$state/xsams:AtomicComposition"/>
  </xsl:template>

  <xsl:template match="xsams:Function">
     <p><b><a name="{@functionID}"><xsl:value-of select="@functionID"/>:
     <xsl:value-of select="xsams:Name"/>
     </a></b>
     <div><xsl:value-of select="xsams:Y/xsams:Description"/></div>
        <xsl:value-of select="xsams:Y/@name"/>
        [<xsl:value-of select="xsams:Y/@units"/>]
     = <xsl:value-of select="xsams:Expression"/></p>
  </xsl:template>

<!--
  <xsl:template match="*[local-name()='QNs']/*">
    <xsl:if test="text()!= 'X'">
      <div style="float:left;font-weight:bold;margin-left:0.5ex">
        <xsl:value-of select="local-name()"/>
        <xsl:text>:</xsl:text>
      </div>
      <div style="text-align:right;float:left;font-style:italic;min-width:3ex">
        <xsl:value-of select="text()"/>
      </div>
    </xsl:if>
  </xsl:template>
-->
  <xsl:template match="*[local-name()='QNs']/*">
    <xsl:if test="text()!= 'X'">
      <xsl:value-of select="local-name()"/>
      <xsl:text>:</xsl:text>
      <i><xsl:value-of select="text()"/></i>;
    </xsl:if>
  </xsl:template>

<!-- ATOMIC QUANTUM NUMBERS -->
  <xsl:template match="xsams:AtomicQuantumNumbers">
    <xsl:apply-templates select="xsams:TotalAngularMomentum"/>    
  </xsl:template>

  <xsl:template match="xsams:TotalAngularMomentum">
    J:<xsl:value-of select="."/>;    
  </xsl:template>

  <xsl:template match="xsams:AtomicComposition">
    <xsl:apply-templates select="xsams:Component/xsams:Term/xsams:LS"/>
  </xsl:template>
 
  <xsl:template match="xsams:LS">
    L:<xsl:value-of select="xsams:L/xsams:Value"/>;
    S:<xsl:value-of select="xsams:S"/>;
  </xsl:template>

  <xsl:template match="xsams:Source">
     <li>
     <xsl:value-of select="@sourceID"/>
     <xsl:text>: </xsl:text>
     <xsl:value-of select="xsams:Authors/xsams:Author"/>
     <i>
     <xsl:value-of select="xsams:SourceName"/>
     </i>
     <xsl:text>  </xsl:text>
     <b>
     <xsl:value-of select="xsams:Volume"/>
     </b>
     <xsl:text>, </xsl:text>
     <xsl:value-of select="xsams:PageBegin"/>
     <xsl:text>&#xa;</xsl:text>
     <xsl:text> (</xsl:text>
     <xsl:value-of select="xsams:Year"/>
     <xsl:text>) </xsl:text>
     </li>
 </xsl:template>
<!--
  <xsl:template match="xsams:PartitionFunction">
    <dl>
    <dt>T</dt>
    <dd>
    <xsl:value-of select="xsams:T/xsams:DataList"/>
    </dd>
    <dt>Q</dt>
    <dd>
    <xsl:value-of select="xsams:Q/xsams:DataList"/>
    </dd>
    </dl>
  </xsl:template>
-->
  <xsl:template match="xsams:PartitionFunction">
    <table class="full" style="font-size:smaller">
    <caption> Partition functions for

       <xsl:call-template name="species_name">
         <xsl:with-param name="mol_id" select="../.."/>
       </xsl:call-template>

    </caption>
    <thead>
    <tr><th>T</th>
    <xsl:call-template name="datalist2col">
      <xsl:with-param name="list" select="normalize-space(xsams:T/xsams:DataList)"/>
      <xsl:with-param name="cell" select="'th'"/>
    </xsl:call-template>
    </tr></thead><tbody>
    <tr><th>Q</th>
    <xsl:call-template name="datalist2col">
      <xsl:with-param name="list" select="normalize-space(xsams:Q/xsams:DataList)"/>
    </xsl:call-template>
    </tr></tbody>
    </table>
  </xsl:template>

  <xsl:template name="datalist2col">
    <xsl:param name="list"/>
    <xsl:param name="cell"/>
    <xsl:variable name="next_val" select="substring-before($list,' ')"/>
    <xsl:variable name="remaining" select="substring-after($list,' ')"/>
    <xsl:choose>      
      <xsl:when test="$cell='th'">
        <th><xsl:value-of select="$next_val"/></th>
      </xsl:when>
      <xsl:otherwise>
        <td><xsl:value-of select="$next_val"/></td>
      </xsl:otherwise>
    </xsl:choose>      
    <xsl:if test="$remaining">
       <xsl:call-template name="datalist2col">
          <xsl:with-param name="list" select="$remaining"/>
          <xsl:with-param name="cell" select="$cell"/>
       </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsams:TabulatedData">
    <table class="full" style="border-style:solid">
    <caption> 
    <xsl:value-of select="xsams:Comments"/>
    </caption>
    <thead>
    <tr><th>X</th>
    <th>
    <xsl:value-of select="xsams:X/xsams:DataList"/>
    </th>
    </tr></thead><tbody>
    <tr><th>Y</th>
    <td>
    <xsl:value-of select="xsams:Y/xsams:DataList"/>
    </td>
    </tr></tbody>
    </table>
  </xsl:template>


  <xsl:template match="xsams:FitData">
    <xsl:apply-templates select="xsams:FitParameters"/>
  </xsl:template>

  <xsl:template match="xsams:FitParameters">
    <div><a href="#{@functionRef}">
<xsl:value-of select="@functionRef"/></a>
    </div>
    <div> Args:
    <xsl:apply-templates select="xsams:FitArgument"/>
    </div>
    <div> Param.:
    <xsl:apply-templates select="xsams:FitParameter"/>
    </div>
  </xsl:template>
  
  <xsl:template match="xsams:FitArgument">
    <xsl:value-of select="@name"/>
    <xsl:text>(</xsl:text>
    <xsl:value-of select="@units"/>
    <xsl:text>)</xsl:text>
    <xsl:text>[</xsl:text>
    <xsl:value-of select="xsams:LowerLimit"/>
    <xsl:text>-</xsl:text>
    <xsl:value-of select="xsams:UpperLimit"/>
    <xsl:text>]</xsl:text>
    <xsl:text>;</xsl:text>
  </xsl:template>

  <xsl:template match="xsams:FitParameter">
    <xsl:value-of select="@name"/>
    <xsl:text>=</xsl:text>
    <xsl:value-of select="xsams:Value"/>
    <xsl:text>;</xsl:text>
  </xsl:template>

  <xsl:template name="atom-name">
    <xsl:param name="atom"/>
    <xsl:choose>
       <xsl:when test="$atom/xsams:Isotope/xsams:IsotopeParameters/xsams:MassNumber">
         <sup><xsl:value-of select="$atom/xsams:Isotope/xsams:IsotopeParameters/xsams:MassNumber"/></sup>
         <xsl:value-of select="$atom/xsams:ChemicalElement/xsams:ElementSymbol"/>
       </xsl:when>
       <xsl:otherwise>
         <xsl:value-of select="$atom/xsams:ChemicalElement/xsams:ElementSymbol"/>
       </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="plot-charge">
      <xsl:with-param name="charge" select="$atom/xsams:Isotope/xsams:Ion/xsams:IonCharge"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="plot-charge">
    <xsl:param name="charge"/>

    <xsl:choose>
      <xsl:when test="$charge &gt; 1">
       <sup><xsl:value-of select="$charge"/>+</sup>
      </xsl:when>
      <xsl:when test="$charge &lt; -1">
       <sup><xsl:value-of select="-$charge"/>-</sup>
      </xsl:when>
      <xsl:when test="$charge = -1">
       <sup>-</sup>
      </xsl:when>
      <xsl:when test="$charge = 1">
       <sup>+</sup>
      </xsl:when>
      <xsl:otherwise/>
    </xsl:choose>

  </xsl:template>


</xsl:stylesheet>
