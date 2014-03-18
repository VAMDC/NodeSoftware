<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xsams10="http://vamdc.org/xml/xsams/1.0">

  <xsl:output method="html"/>

  <xsl:key name="molecule" match="/xsams10:XSAMSData/xsams10:Species/xsams10:Molecules/xsams10:Molecule" use="@speciesID"/> 
  <xsl:key name="atom" match="/xsams10:XSAMSData/xsams10:Species/xsams10:Atoms/xsams10:Atom/xsams10:Isotope/xsams10:Ion" use="@speciesID"/> 
  <xsl:key name="particle" match="/xsams10:XSAMSData/xsams10:Species/xsams10:Particles/xsams10:Particle" use="@speciesID"/> 
  <xsl:key name="molstate" match="/xsams10:XSAMSData/xsams10:Species/xsams10:Molecules/xsams10:Molecule/xsams10:MolecularState" use="@stateID"/>
  <xsl:key name="atomstate" match="/xsams10:XSAMSData/xsams10:Species/xsams10:Atoms/xsams10:Atom/xsams10:Isotope/xsams10:Ion/xsams10:AtomicState" use="@stateID"/>


  <xsl:decimal-format name="example" zero-digit ="0" />

  <xsl:template match="xsams10:XSAMSData">
        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Species/xsams10:Molecules"/>

        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Species/xsams10:Atoms"/>

	<xsl:text>&#xa;</xsl:text>

        <xsl:call-template name="Partitionfunctions">
        </xsl:call-template>

        <xsl:call-template name="States">
        </xsl:call-template>

        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Processes/xsams10:Radiative"/>

        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Processes/xsams10:Collisions"/>

        <xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Functions"/>

	<xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Methods"/>

	<fieldset id="list_sources" class="subpage">
	<div class="legend">Sources</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist full">
        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Sources/xsams10:Source"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>


  </xsl:template>
<!--
  <xsl:template match="xsams10:Molecules">
	<fieldset>
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full" style="list-style:none;">
        <xsl:apply-templates select="xsams10:Molecule"/>
	</ul>
	</fieldset>
  </xsl:template>
-->
  <xsl:template match="xsams10:Molecules">
	<fieldset id="list_molecules" class="subpage">
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<table class="vlist full">
        <xsl:apply-templates select="xsams10:Molecule"/>
	</table>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams10:Atoms">
	<fieldset id="list_atoms" class="subpage">
	<div class="legend">Atoms</div>
	<xsl:text>&#xa;</xsl:text>
	<table class="full">
        <xsl:apply-templates select="xsams10:Atom"/>
	</table>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams10:Functions">
	<fieldset id="list_functions" class="subpage">
	<div class="legend">Functions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full">
        <xsl:apply-templates select="xsams10:Function"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template name="States">
	<fieldset id="list_states" class="subpage">
	<div class="legend">States</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full" style="list-style:none;">
	<xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Species/xsams10:Atoms/xsams10:Atom/xsams10:Isotope/xsams10:Ion/xsams10:AtomicState"/>
        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Species/xsams10:Molecules/xsams10:Molecule/xsams10:MolecularState[not(@auxillary='true')]"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template name="Partitionfunctions">
	<fieldset id="list_pfs"  class="subpage">
	<div class="legend">Partition functions</div>
	<xsl:text>&#xa;</xsl:text>
	<div class="full">
        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Species/xsams10:Molecules/xsams10:Molecule/xsams10:MolecularChemicalSpecies/xsams10:PartitionFunction"/>
	</div>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams10:Methods">
	<fieldset id="list_methods" class="subpage">
	<div class="legend">Methods</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist full">
        <xsl:apply-templates select="xsams10:Method"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>


  <xsl:template match="xsams10:AtomicState">

    <li style="clear:both; border-bottom: 1px solid #90bade;">
    <div style="float:left;min-width:17ex">
      <xsl:value-of select="format-number(xsams10:AtomicNumericalData/xsams10:StatisticalWeight,' 0000', 'example')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="xsams10:AtomicNumericalData/xsams10:StateEnergy/xsams10:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="xsams10:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="xsams10:AtomicComposition"/>
    </li>

  </xsl:template>


  <xsl:template match="xsams10:MolecularState">
    <li style="clear:both; border-bottom: 1px solid #90bade;">
     <div class="float_right">
       <xsl:call-template name="species_name">
         <xsl:with-param name="mol_id" select=".."/>
       </xsl:call-template>
     </div>
     <xsl:apply-templates select="xsams10:MolecularStateCharacterisation"/>
     <div class="float_left"> <xsl:apply-templates select="xsams10:Case/*[local-name()='QNs']/*"/> </div>
     <div style="clear:left"></div>
    </li>
  </xsl:template>

  <xsl:template match="xsams10:MolecularStateCharacterisation">
    <div class="float_left" style="min-width:5ex;text-align:right">
      <xsl:apply-templates select="xsams10:TotalStatisticalWeight"/>
    </div>
    <div class="float_left" style="min-width:15ex;text-align:right">
      <xsl:apply-templates select="xsams10:StateEnergy"/>
    </div>
  </xsl:template>

  <xsl:template match="xsams10:TotalStatisticalWeight">
    <xsl:value-of select="."/>
  </xsl:template>

  <xsl:template match="xsams10:StateEnergy">
    <xsl:call-template name="DataType">
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="DataType">
    <xsl:value-of select="xsams10:Value"/><xsl:text> </xsl:text>
    <xsl:value-of select="xsams10:Value/@units"/>
    <xsl:if test="xsams10:Accuracy">
      <xsl:value-of select="xsams10:Accuracy"/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsams10:Atom">
    <tr>
      <td>
        <div style="min-width:30ex"><b><xsl:value-of select="xsams10:Isotope/xsams10:Ion/@speciesID"/></b></div>
        <div class="float_left"> <xsl:value-of select="xsams10:Isotope/xsams10:Ion/xsams10:InChIKey"/></div>
      </td>
      <td>
        <xsl:call-template name="atom-name">
          <xsl:with-param name="atom" select="."/>
        </xsl:call-template>
        <div style="clear:left"></div>
        <div class="float_left highlight"><xsl:value-of select="xsams10:Isotope/xsams10:Comments"/></div>
      </td>
    </tr>
  </xsl:template>

<!--
  <xsl:template match="xsams10:Molecule">
	<li style="clear:left;">
	<h4>
	<xsl:value-of select="@speciesID" />	
	</h4>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Structural Formula</strong>
    	<var><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:OrdinaryStructuralFormula/xsams10:Value"/></var>
	</div>

	<div class="columnar" style="clear:left">
  	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Stoichiometric Formula</strong>
    	<var><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:StoichiometricFormula"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Chemical Name</strong>
    	<var><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:ChemicalName/xsams10:Value"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">InChi</strong>
    	<var><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:InChI"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">InChiKey</strong>
    	<var><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:InChIKey"/></var>
	</div>

	<div class="columnar" style="clear:left;">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Partition Function</strong>
    	<div style="float:left;min-width:12em;padding-right:1em;text-align:left;">
    	<var><xsl:apply-templates select="xsams10:MolecularChemicalSpecies/xsams10:PartitionFunction"/></var>
	</div>
	</div>
	</li>

  </xsl:template>
-->
  <xsl:template match="xsams10:Molecule">
    <tr>
      <td>
	<div style="min-width:30ex"><b><xsl:value-of select="@speciesID" /></b></div>
        <div class="float_left" style="min-width:30ex"><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:InChIKey"/></div>
      </td>
      <td>
        <!-- <div class="float_left"><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:InChI"/></div> -->
    	<div class="float_left"><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:OrdinaryStructuralFormula/xsams10:Value"/></div>
    	<div class="float_left"><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:StoichiometricFormula"/></div> 
    	<div class="float_left"><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:ChemicalName/xsams10:Value"/></div>
        <div style="clear:left"></div>
    	<div class="float_left highlight" style="text-align:left;"><xsl:value-of select="xsams10:MolecularChemicalSpecies/xsams10:Comment"/></div>
      </td>	
    </tr>
  </xsl:template>

  <xsl:template match="xsams10:Collisions">
	<fieldset id="list_collisions" class="subpage">
	<div class="legend">Collisional Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2" style="list-style:none;">
        <xsl:apply-templates select="xsams10:CollisionalTransition"/>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams10:Radiative">
	<fieldset id="list_radiative" class="subpage">
	<div class="legend">Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2" style="list-style:none;">
        <xsl:apply-templates select="/xsams10:XSAMSData/xsams10:Processes/xsams10:Radiative/xsams10:RadiativeTransition"/>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams10:RadiativeTransition">
	<li style="clear:both; border-bottom: 1px solid #90bade;">
	
	<div style="float:left; min-width:27em;">
	<ul style="list-style:none;">
	<li style="font-weight:bold">
<xsl:element name="a">
  <xsl:attribute name="class">tooltip</xsl:attribute>
  <xsl:attribute name="title">
Source: <xsl:value-of select="xsams10:SourceRef"/>
Method: <xsl:value-of select="xsams10:EnergyWavelength/*/@methodRef"/>
</xsl:attribute>
        <xsl:apply-templates select="xsams10:EnergyWavelength"/>

	<div style="float:left;text-align:right; min-width:10ex;">
        <xsl:value-of select="format-number(xsams10:Probability/xsams10:TransitionProbabilityA/xsams10:Value,'0.00000000 ')"/>
	</div>
<!--
	 <div style="float:left;text-align:right; min-width:15ex;margin-right:1.0em">
   	  <xsl:value-of select="xsams10:SourceRef"/>
   	  <xsl:value-of select=""/>
	 </div>
-->
</xsl:element>
	</li>


	<xsl:for-each select="xsams10:EnergyWavelength/xsams10:Frequency[position() > 1]">
<li style="clear:left">

<xsl:element name="a">
  <xsl:attribute name="class">tooltip</xsl:attribute>
  <xsl:attribute name="title">
Source: <xsl:value-of select="xsams10:SourceRef"/>
Method: <xsl:value-of select="@methodRef"/>
</xsl:attribute>

 	 <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
	  <xsl:value-of select="format-number(xsams10:Value,'0.0000')"/>
	 </div>

	 <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	  <xsl:value-of select="format-number(xsams10:Accuracy,'0.0000 ')"/>
	 </div>
</xsl:element>

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
          <xsl:with-param name="state" select="key('molstate',current()/xsams10:LowerStateRef)"/>
        </xsl:call-template>
	<xsl:call-template name="atomic_state">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams10:LowerStateRef)"/>
        </xsl:call-template>

	</div>
	<div>
	
	<div style="float:left;width:5ex">
	<xsl:text>F.S.: </xsl:text>
	</div>

	<xsl:call-template name="molec_state">
          <xsl:with-param name="state" select="key('molstate',current()/xsams10:UpperStateRef)"/>
        </xsl:call-template>
	<xsl:call-template name="atomic_state">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams10:UpperStateRef)"/>
        </xsl:call-template>

	</div>
	</div>
	
	<div style="float:right">
          <xsl:call-template name="species_name">
          <xsl:with-param name="mol_id" select="key('molstate',current()/xsams10:UpperStateRef)/../."/>
          <xsl:with-param name="atom_id" select="key('atomstate',current()/xsams10:UpperStateRef)/../."/>
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
        <xsl:value-of select="$mol_id/xsams10:MolecularChemicalSpecies/xsams10:OrdinaryStructuralFormula"/>
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


  <xsl:template match="xsams10:EnergyWavelength">
	<xsl:choose>
	  <xsl:when test="xsams10:Frequency">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(xsams10:Frequency/xsams10:Value,'0.0000')"/>
	    </div>
  	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(xsams10:Frequency/xsams10:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>	
	  <xsl:when test="xsams10:Wavenumber">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(29979.2458*xsams10:Wavenumber/xsams10:Value,'0.0000')"/>
	    </div>
	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(29979.2458*xsams10:Wavenumber/xsams10:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>
	  <xsl:when test="xsams10:Wavelength">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(xsams10:Wavelength/xsams10:Value,'0.00000 ')"/>
            <xsl:value-of select="xsams10:Wavelength/xsams10:Value/@units"/>
	    </div>
	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(xsams10:Wavelength/xsams10:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>
	</xsl:choose>
  </xsl:template>

<!-- PRINT COLLISIONAL TRANSITION (currently only Species info) -->
  <xsl:template match="xsams10:CollisionalTransition">
   <li style="clear:both; border-bottom: 1px solid #90bade;">

    <xsl:apply-templates select="xsams10:Reactant"/>
    <xsl:text> -> </xsl:text>      
    <xsl:apply-templates select="xsams10:Product"/>
    <xsl:text> : </xsl:text>          
    <xsl:apply-templates select="xsams10:DataSets/xsams10:DataSet/xsams10:FitData"/>
    <xsl:apply-templates select="xsams10:DataSets/xsams10:DataSet/xsams10:TabulatedData"/>
   </li>
  </xsl:template>


  <xsl:template match="xsams10:Reactant">
    <b>
    <xsl:choose>
      <xsl:when test="key('molecule',current()/xsams10:SpeciesRef)">
        <xsl:value-of select="key('molecule',current()/xsams10:SpeciesRef)/xsams10:MolecularChemicalSpecies/xsams10:StoichiometricFormula"/>
[
	<xsl:call-template name="molec_state_qn">
          <xsl:with-param name="state" select="key('molstate',current()/xsams10:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:when test="key('particle',current()/xsams10:SpeciesRef)">
        <xsl:value-of select="key('particle',current()/xsams10:SpeciesRef)/@name"/>
        [<xsl:value-of select="xsams10:StateRef"/>]    
      </xsl:when>
      <xsl:when test="key('atom',current()/xsams10:SpeciesRef)">
	<xsl:call-template name="atom-name">
          <xsl:with-param name="atom" select="key('atom',current()/xsams10:SpeciesRef)/../.."/>
        </xsl:call-template>
[
	<xsl:call-template name="atomic_state_qn">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams10:StateRef)"/>
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

  <xsl:template match="xsams10:Product">
    <b>
    <xsl:choose>
      <xsl:when test="key('molecule',current()/xsams10:SpeciesRef)">
        <xsl:value-of select="key('molecule',current()/xsams10:SpeciesRef)/xsams10:MolecularChemicalSpecies/xsams10:StoichiometricFormula"/>
[
	<xsl:call-template name="molec_state_qn">
          <xsl:with-param name="state" select="key('molstate',current()/xsams10:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:when test="key('particle',current()/xsams10:SpeciesRef)">
        <xsl:value-of select="key('particle',current()/xsams10:SpeciesRef)/@name"/>
        [<xsl:value-of select="xsams10:StateRef"/>]    
      </xsl:when>
      <xsl:when test="key('atom',current()/xsams10:SpeciesRef)">
	<xsl:call-template name="atom-name">
          <xsl:with-param name="atom" select="key('atom',current()/xsams10:SpeciesRef)/../.."/>
        </xsl:call-template>
[
	<xsl:call-template name="atomic_state_qn">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams10:StateRef)"/>
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
      <xsl:value-of select="format-number($state/xsams10:MolecularStateCharacterisation/xsams10:TotalStatisticalWeight,' 0000', 'example')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="$state/xsams10:MolecularStateCharacterisation/xsams10:StateEnergy/xsams10:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="$state/xsams10:Case/*[local-name()='QNs']/*"/>
    </xsl:if>
  </xsl:template>


  <xsl:template name="atomic_state">
    <xsl:param name="state"/>
    <xsl:if test="count($state)>0">
    <div style="float:left;min-width:17ex">
      <xsl:value-of select="format-number($state/xsams10:AtomicNumericalData/xsams10:StatisticalWeight,' 0000', 'example')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="$state/xsams10:AtomicNumericalData/xsams10:StateEnergy/xsams10:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="$state/xsams10:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="$state/xsams10:AtomicComposition"/>
    </xsl:if>

  </xsl:template>


  <xsl:template name="molec_state_qn">
    <xsl:param name="state"/>

    <xsl:apply-templates select="$state/xsams10:Case/*[local-name()='QNs']/*"/>
  </xsl:template>


  <xsl:template name="atomic_state_qn">
    <xsl:param name="state"/>
    <xsl:apply-templates select="$state/xsams10:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="$state/xsams10:AtomicComposition"/>
  </xsl:template>

  <xsl:template match="xsams10:Function">
     <p><b><a name="{@functionID}"><xsl:value-of select="@functionID"/>:
     <xsl:value-of select="xsams10:Name"/>
     </a></b>
     <div><xsl:value-of select="xsams10:Y/xsams10:Description"/></div>
        <xsl:value-of select="xsams10:Y/@name"/>
        [<xsl:value-of select="xsams10:Y/@units"/>]
     = <xsl:value-of select="xsams10:Expression"/></p>
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
  <xsl:template match="xsams10:AtomicQuantumNumbers">
    <xsl:apply-templates select="xsams10:TotalAngularMomentum"/>    
  </xsl:template>

  <xsl:template match="xsams10:TotalAngularMomentum">
    J:<xsl:value-of select="."/>;    
  </xsl:template>

  <xsl:template match="xsams10:AtomicComposition">
    <xsl:apply-templates select="xsams10:Component/xsams10:Term/xsams10:LS"/>
  </xsl:template>
 
  <xsl:template match="xsams10:LS">
    L:<xsl:value-of select="xsams10:L/xsams10:Value"/>;
    S:<xsl:value-of select="xsams10:S"/>;
  </xsl:template>

  <xsl:template match="xsams10:Source">
     <li>
     <xsl:value-of select="@sourceID"/>
     <xsl:text>: </xsl:text>
     <xsl:value-of select="xsams10:Authors/xsams10:Author"/>
     <i>
     <xsl:value-of select="xsams10:SourceName"/>
     </i>
     <xsl:text>  </xsl:text>
     <b>
     <xsl:value-of select="xsams10:Volume"/>
     </b>
     <xsl:text>, </xsl:text>
     <xsl:value-of select="xsams10:PageBegin"/>
     <xsl:text>&#xa;</xsl:text>
     <xsl:text> (</xsl:text>
     <xsl:value-of select="xsams10:Year"/>
     <xsl:text>) </xsl:text>
     </li>
 </xsl:template>

  <xsl:template match="xsams10:Method">
     <li>
     <b><xsl:value-of select="@methodID"/>
     <xsl:text>: </xsl:text>
     <cap><xsl:value-of select="xsams10:Category"/></cap>
     </b>
     <p>Sources:
     <xsl:for-each select="xsams10:SourceRef">
         <xsl:value-of select="."/>
         <xsl:text>;</xsl:text>
     </xsl:for-each>
     </p>
     <xsl:text>  </xsl:text>
     <p><xsl:value-of select="xsams10:Comments"/></p>
     <xsl:text>  </xsl:text>
     <p><xsl:value-of select="xsams10:Description"/></p>
     </li>
 </xsl:template>


<!--
  <xsl:template match="xsams10:PartitionFunction">
    <dl>
    <dt>T</dt>
    <dd>
    <xsl:value-of select="xsams10:T/xsams10:DataList"/>
    </dd>
    <dt>Q</dt>
    <dd>
    <xsl:value-of select="xsams10:Q/xsams10:DataList"/>
    </dd>
    </dl>
  </xsl:template>
-->
  <xsl:template match="xsams10:PartitionFunction2">
    <table class="full" style="font-size:smaller">
    <caption> Partition functions for

       <xsl:call-template name="species_name">
         <xsl:with-param name="mol_id" select="../.."/>
       </xsl:call-template>

    </caption>
    <thead>
    <tr><th>T</th>
    <xsl:call-template name="datalist2col">
      <xsl:with-param name="list" select="normalize-space(xsams10:T/xsams10:DataList)"/>
      <xsl:with-param name="cell" select="'th'"/>
    </xsl:call-template>
    </tr></thead><tbody>
    <tr><th>Q</th>
    <xsl:call-template name="datalist2col">
      <xsl:with-param name="list" select="normalize-space(xsams10:Q/xsams10:DataList)"/>
    </xsl:call-template>
    </tr></tbody>
    </table>
  </xsl:template>

  <xsl:template match="xsams10:PartitionFunction">
    <table class="full" style="font-size:smaller">
    <caption> Partition functions for

       <xsl:call-template name="species_name">
         <xsl:with-param name="mol_id" select="../.."/>
       </xsl:call-template>

    </caption>
    <thead><tr><th>T</th><th>Q</th></tr></thead>
    <tbody>

<xsl:variable name="temperatures">
<xsl:choose>
           <xsl:when test="xsams10:T/xsams10:LinearSequence">
<xsl:call-template name="LinearSequence">
         <xsl:with-param name="count" select="xsams10:T/xsams10:LinearSequence/@count"/>
         <xsl:with-param name="initial" select="xsams10:T/xsams10:LinearSequence/@initial"/>
         <xsl:with-param name="increment" select="xsams10:T/xsams10:LinearSequence/@increment"/>
</xsl:call-template>
</xsl:when>
<xsl:otherwise>
<xsl:value-of select="normalize-space(xsams10:T/xsams10:DataList)"/>
</xsl:otherwise>
</xsl:choose>  
</xsl:variable>

      <xsl:call-template name="datalist2row">
        <xsl:with-param name="Tlist" select="normalize-space($temperatures)"/>
        <xsl:with-param name="Qlist" select="normalize-space(xsams10:Q/xsams10:DataList)"/>
      </xsl:call-template>
    </tbody>
    </table>
  </xsl:template>

  <xsl:template name="LinearSequence">
    <xsl:param name="count"/>
    <xsl:param name="increment"/>
    <xsl:param name="initial"/>  
    <xsl:value-of select="$initial"/>
    <xsl:text> </xsl:text>
    <xsl:if test="$count &gt; 1">
       <xsl:call-template name="LinearSequence">
         <xsl:with-param name="count" select="$count - 1"/>
         <xsl:with-param name="initial" select="$initial + $increment"/>
         <xsl:with-param name="increment" select="$increment"/>
       </xsl:call-template>
    </xsl:if>
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


  <xsl:template name="datalist2row">
    <xsl:param name="Tlist"/>
    <xsl:param name="Qlist"/>
    <xsl:variable name="next_Tval" select="substring-before($Tlist,' ')"/>
    <xsl:variable name="Tremaining" select="substring-after($Tlist,' ')"/>
    <xsl:variable name="next_Qval" select="substring-before($Qlist,' ')"/>
    <xsl:variable name="Qremaining" select="substring-after($Qlist,' ')"/>
    <tr>
      <td><xsl:value-of select="$next_Tval"/></td>
      <td><xsl:value-of select="$next_Qval"/></td>
    </tr>
    <xsl:if test="$Tremaining">
       <xsl:call-template name="datalist2row">
          <xsl:with-param name="Tlist" select="$Tremaining"/>
          <xsl:with-param name="Qlist" select="$Qremaining"/>
       </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsams10:TabulatedData">
    <table class="full" style="border-style:solid">
    <caption> 
    <xsl:value-of select="xsams10:Comments"/>
    </caption>
    <thead>
    <tr><th>X</th>
    <th>
    <xsl:value-of select="xsams10:X/xsams10:DataList"/>
    </th>
    </tr></thead><tbody>
    <tr><th>Y</th>
    <td>
    <xsl:value-of select="xsams10:Y/xsams10:DataList"/>
    </td>
    </tr></tbody>
    </table>
  </xsl:template>


  <xsl:template match="xsams10:FitData">
    <xsl:apply-templates select="xsams10:FitParameters"/>
  </xsl:template>

  <xsl:template match="xsams10:FitParameters">
    <div><a href="#{@functionRef}">
<xsl:value-of select="@functionRef"/></a>
    </div>
    <div> Args:
    <xsl:apply-templates select="xsams10:FitArgument"/>
    </div>
    <div> Param.:
    <xsl:apply-templates select="xsams10:FitParameter"/>
    </div>
  </xsl:template>
  
  <xsl:template match="xsams10:FitArgument">
    <xsl:value-of select="@name"/>
    <xsl:text>(</xsl:text>
    <xsl:value-of select="@units"/>
    <xsl:text>)</xsl:text>
    <xsl:text>[</xsl:text>
    <xsl:value-of select="xsams10:LowerLimit"/>
    <xsl:text>-</xsl:text>
    <xsl:value-of select="xsams10:UpperLimit"/>
    <xsl:text>]</xsl:text>
    <xsl:text>;</xsl:text>
  </xsl:template>

  <xsl:template match="xsams10:FitParameter">
    <xsl:value-of select="@name"/>
    <xsl:text>=</xsl:text>
    <xsl:value-of select="xsams10:Value"/>
    <xsl:text>;</xsl:text>
  </xsl:template>

  <xsl:template name="atom-name">
    <xsl:param name="atom"/>
    <xsl:choose>
       <xsl:when test="$atom/xsams10:Isotope/xsams10:IsotopeParameters/xsams10:MassNumber">
         <sup><xsl:value-of select="$atom/xsams10:Isotope/xsams10:IsotopeParameters/xsams10:MassNumber"/></sup>
         <xsl:value-of select="$atom/xsams10:ChemicalElement/xsams10:ElementSymbol"/>
       </xsl:when>
       <xsl:otherwise>
         <xsl:value-of select="$atom/xsams10:ChemicalElement/xsams10:ElementSymbol"/>
       </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="plot-charge">
      <xsl:with-param name="charge" select="$atom/xsams10:Isotope/xsams10:Ion/xsams10:IonCharge"/>
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
