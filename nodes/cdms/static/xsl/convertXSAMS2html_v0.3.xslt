<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xsams03="http://vamdc.org/xml/xsams/0.3">

  <xsl:output method="html"/>

  <xsl:key name="molecule" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Molecules/xsams03:Molecule" use="@speciesID"/> 
  <xsl:key name="atom" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Atoms/xsams03:Atom/xsams03:Isotope/xsams03:Ion" use="@speciesID"/> 
  <xsl:key name="particle" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Particles/xsams03:Particle" use="@speciesID"/> 
  <xsl:key name="molstate" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Molecules/xsams03:Molecule/xsams03:MolecularState" use="@stateID"/>
  <xsl:key name="atomstate" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Atoms/xsams03:Atom/xsams03:Isotope/xsams03:Ion/xsams03:AtomicState" use="@stateID"/>


  <xsl:decimal-format name="example_v0_3" zero-digit ="0" /> 

  <xsl:template match="xsams03:XSAMSData">
        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Species/xsams03:Molecules"/>

        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Species/xsams03:Atoms"/>

	<xsl:text>&#xa;</xsl:text>

        <xsl:call-template name="Partitionfunctions_v0_3">
        </xsl:call-template>

        <xsl:call-template name="States_v0_3">
        </xsl:call-template>

        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Processes/xsams03:Radiative"/>

        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Processes/xsams03:Collisions"/>

        <xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Functions"/>

	<fieldset id="list_sources" class="subpage">
	<div class="legend">Sources</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist full">
        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Sources/xsams03:Source"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>
<!--
  <xsl:template match="xsams03:Molecules">
	<fieldset>
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full" style="list-style:none;">
        <xsl:apply-templates select="xsams03:Molecule"/>
	</ul>
	</fieldset>
  </xsl:template>
-->
  <xsl:template match="xsams03:Molecules">
	<fieldset id="list_molecules" class="subpage">
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<table class="vlist full">
        <xsl:apply-templates select="xsams03:Molecule"/>
	</table>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams03:Atoms">
	<fieldset id="list_atoms" class="subpage">
	<div class="legend">Atoms</div>
	<xsl:text>&#xa;</xsl:text>
	<table class="full">
        <xsl:apply-templates select="xsams03:Atom"/>
	</table>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams03:Functions">
	<fieldset id="list_functions" class="subpage">
	<div class="legend">Functions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full">
        <xsl:apply-templates select="xsams03:Function"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>


  <xsl:template name="States_v0_3">
	<fieldset id="list_states" class="subpage">
	<div class="legend">States</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full" style="list-style:none;">
	<xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Species/xsams03:Atoms/xsams03:Atom/xsams03:Isotope/xsams03:Ion/xsams03:AtomicState"/>
        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Species/xsams03:Molecules/xsams03:Molecule/xsams03:MolecularState"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template name="Partitionfunctions_v0_3">
	<fieldset id="list_pfs" class="subpage">
	<div class="legend">Partition functions</div>
	<xsl:text>&#xa;</xsl:text>
	<div class="full">
        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Species/xsams03:Molecules/xsams03:Molecule/xsams03:MolecularChemicalSpecies/xsams03:PartitionFunction"/>
	</div>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams03:Methods">
	<fieldset id="list_methods" class="subpage">
	<div class="legend">Methods</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist full">
        <xsl:apply-templates select="xsams03:Method"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>


  <xsl:template match="xsams03:AtomicState">

    <li style="clear:both; border-bottom: 1px solid #90bade;">
    <div style="float:left;min-width:17ex">
      <xsl:value-of select="format-number(xsams03:AtomicNumericalData/xsams03:StatisticalWeight,' 0000', 'example')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="xsams03:AtomicNumericalData/xsams03:StateEnergy/xsams03:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="xsams03:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="xsams03:AtomicComposition"/>
    </li>

  </xsl:template>

  <xsl:template match="xsams03:MolecularState">
<xsl:for-each select=".">
<xsl:sort select="xsams03:MolecularStateCharacterisation/xsams03:StateEnergy/xsams03:Value" order="ascending" data-type="number"/>
    <li style="clear:both; border-bottom: 1px solid #90bade;">
     <div class="float_right">
       <xsl:call-template name="species_name_v0_3">
         <xsl:with-param name="mol_id" select=".."/>
       </xsl:call-template>
     </div>
     <xsl:apply-templates select="xsams03:MolecularStateCharacterisation"/>
     <div class="float_left"> <xsl:apply-templates select="xsams03:Case/*[local-name()='QNs']/*"/> </div>
     <div style="clear:left"></div>
    </li>
</xsl:for-each>
  </xsl:template>

  <xsl:template match="xsams03:MolecularStateCharacterisation">
    <div class="float_left" style="min-width:5ex;text-align:right">
      <xsl:apply-templates select="xsams03:TotalStatisticalWeight"/>
    </div>
    <div class="float_left" style="min-width:15ex;text-align:right">
      <xsl:apply-templates select="xsams03:StateEnergy"/>
    </div>
  </xsl:template>

  <xsl:template match="xsams03:TotalStatisticalWeight">
    <xsl:value-of select="."/>
  </xsl:template>

  <xsl:template match="xsams03:StateEnergy">
    <xsl:call-template name="DataType_v0_3">
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="DataType_v0_3">
    <xsl:value-of select="xsams03:Value"/><xsl:text> </xsl:text>
    <xsl:value-of select="xsams03:Value/@units"/>
    <xsl:if test="xsams03:Accuracy">
      <xsl:value-of select="xsams03:Accuracy"/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsams03:Atom">
    <tr>
      <td>
        <div style="min-width:30ex"><b><xsl:value-of select="xsams03:Isotope/xsams03:Ion/@speciesID"/></b></div>
        <div class="float_left"> <xsl:value-of select="xsams03:Isotope/xsams03:Ion/xsams03:InChIKey"/></div>
      </td>
      <td>
        <xsl:call-template name="atom-name_v0_3">
          <xsl:with-param name="atom" select="."/>
        </xsl:call-template>
        <div style="clear:left"></div>
        <div class="float_left highlight"><xsl:value-of select="xsams03:Isotope/xsams03:Comments"/></div>
      </td>
    </tr>
  </xsl:template>

<!--
  <xsl:template match="xsams03:Molecule">
	<li style="clear:left;">
	<h4>
	<xsl:value-of select="@speciesID" />	
	</h4>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Structural Formula</strong>
    	<var><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:OrdinaryStructuralFormula/xsams03:Value"/></var>
	</div>

	<div class="columnar" style="clear:left">
  	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Stoichiometric Formula</strong>
    	<var><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:StoichiometricFormula"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Chemical Name</strong>
    	<var><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:ChemicalName/xsams03:Value"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">InChi</strong>
    	<var><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:InChI"/></var>
	</div>

	<div class="columnar" style="clear:left">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">InChiKey</strong>
    	<var><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:InChIKey"/></var>
	</div>

	<div class="columnar" style="clear:left;">
    	<strong style="float:left;min-width:12em;padding-right:1em;text-align:right;">Partition Function</strong>
    	<div style="float:left;min-width:12em;padding-right:1em;text-align:left;">
    	<var><xsl:apply-templates select="xsams03:MolecularChemicalSpecies/xsams03:PartitionFunction"/></var>
	</div>
	</div>
	</li>

  </xsl:template>
-->
  <xsl:template match="xsams03:Molecule">
    <tr>
      <td>
	<div style="min-width:30ex"><b><xsl:value-of select="@speciesID" /></b></div>
        <div class="float_left" style="min-width:30ex"><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:InChIKey"/></div>
      </td>
      <td>
        <!-- <div class="float_left"><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:InChI"/></div> -->
    	<div class="float_left"><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:OrdinaryStructuralFormula/xsams03:Value"/></div>
    	<div class="float_left"><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:StoichiometricFormula"/></div> 
    	<div class="float_left"><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:ChemicalName/xsams03:Value"/></div>
        <div style="clear:left"></div>
    	<div class="float_left highlight" style="text-align:left;"><xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:Comment"/></div>
      </td>	
    </tr>
  </xsl:template>

  <xsl:template match="xsams03:Collisions">
	<fieldset id="list_collisions" class="subpage">
	<div class="legend">Collisional Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2" style="list-style:none;">
        <xsl:apply-templates select="xsams03:CollisionalTransition"/>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams03:Radiative">
	<fieldset id="list_radiative" class="subpage">
	<div class="legend">Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2" style="list-style:none;">
        <xsl:apply-templates select="/xsams03:XSAMSData/xsams03:Processes/xsams03:Radiative/xsams03:RadiativeTransition"/>
	</ul>
	</fieldset>
  </xsl:template>

  <xsl:template match="xsams03:RadiativeTransition">
	<li style="clear:both; border-bottom: 1px solid #90bade;">
	
	<div style="float:left; min-width:27em;">
	<ul style="list-style:none;">
	<li style="font-weight:bold">

        <xsl:apply-templates select="xsams03:EnergyWavelength"/>

	<div style="float:left;text-align:right; min-width:10ex;">
        <xsl:value-of select="format-number(xsams03:Probability/xsams03:TransitionProbabilityA/xsams03:Value,'0.00000000 ')"/>
	</div>

	 <div style="float:left;text-align:right; min-width:15ex;margin-right:1.0em">
   	  <xsl:value-of select="xsams03:SourceRef"/>
	 </div>

	</li>


	<xsl:for-each select="xsams03:EnergyWavelength/xsams03:Frequency[position() > 1]">
<li style="clear:left">
 	 <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
	  <xsl:value-of select="format-number(xsams03:Value,'0.0000')"/>
	 </div>

	 <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	  <xsl:value-of select="format-number(xsams03:Accuracy,'0.0000 ')"/>
	 </div>

	 <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5ex">
	<xsl:text>- </xsl:text>
	 </div>

	 <div style="float:left;text-align:right; min-width:15ex;margin-right:1.0em">
   	  <xsl:value-of select="xsams03:SourceRef"/>
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

	<xsl:call-template name="molec_state_v0_3">
          <xsl:with-param name="state" select="key('molstate',current()/xsams03:LowerStateRef)"/>
        </xsl:call-template>
	<xsl:call-template name="atomic_state_v0_3">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams03:LowerStateRef)"/>
        </xsl:call-template>

	</div>
	<div>
	
	<div style="float:left;width:5ex">
	<xsl:text>F.S.: </xsl:text>
	</div>

	<xsl:call-template name="molec_state_v0_3">
          <xsl:with-param name="state" select="key('molstate',current()/xsams03:UpperStateRef)"/>
        </xsl:call-template>
	<xsl:call-template name="atomic_state_v0_3">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams03:UpperStateRef)"/>
        </xsl:call-template>

	</div>
	</div>
	
	<div style="float:right">
          <xsl:call-template name="species_name_v0_3">
          <xsl:with-param name="mol_id" select="key('molstate',current()/xsams03:UpperStateRef)/../."/>
          <xsl:with-param name="atom_id" select="key('atomstate',current()/xsams03:UpperStateRef)/../."/>
          </xsl:call-template>
	</div>
	</li>

  </xsl:template>


  <xsl:template name="species_name_v0_3">
    <xsl:param name="mol_id"/>
    <xsl:param name="atom_id"/>
 
    <xsl:choose>
      <xsl:when test="$mol_id">
        <xsl:value-of select="$mol_id/@speciesID"/>:
        <xsl:value-of select="$mol_id/xsams03:MolecularChemicalSpecies/xsams03:OrdinaryStructuralFormula"/>
      </xsl:when>
      <xsl:when test="$atom_id">
        <xsl:value-of select="$atom_id/@speciesID"/>:
	<xsl:call-template name="atom-name_v0_3">
          <xsl:with-param name="atom" select="$atom_id/../.."/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:text>N.N.</xsl:text>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>


  <xsl:template match="xsams03:EnergyWavelength">
	<xsl:choose>
	  <xsl:when test="xsams03:Frequency">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(xsams03:Frequency/xsams03:Value,'0.0000')"/>
	    </div>
  	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(xsams03:Frequency/xsams03:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>	
	  <xsl:when test="xsams03:Wavenumber">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(29979.2458*xsams03:Wavenumber/xsams03:Value,'0.0000')"/>
	    </div>
	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(29979.2458*xsams03:Wavenumber/xsams03:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>
	  <xsl:when test="xsams03:Wavelength">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(xsams03:Wavelength/xsams03:Value,'0.00000 ')"/>
            <xsl:value-of select="xsams03:Wavelength/xsams03:Value/@units"/>
	    </div>
	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(xsams03:Wavelength/xsams03:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>
	</xsl:choose>
  </xsl:template>

<!-- PRINT COLLISIONAL TRANSITION (currently only Species info) -->
  <xsl:template match="xsams03:CollisionalTransition">
   <li style="clear:both; border-bottom: 1px solid #90bade;">

    <xsl:apply-templates select="xsams03:Reactant"/>
    <xsl:text> -> </xsl:text>      
    <xsl:apply-templates select="xsams03:Product"/>
    <xsl:text> : </xsl:text>          
    <xsl:apply-templates select="xsams03:DataSets/xsams03:DataSet/xsams03:FitData"/>
    <xsl:apply-templates select="xsams03:DataSets/xsams03:DataSet/xsams03:TabulatedData"/>
   </li>
  </xsl:template>


  <xsl:template match="xsams03:Reactant">
    <b>
    <xsl:choose>
      <xsl:when test="key('molecule',current()/xsams03:SpeciesRef)">
        <xsl:value-of select="key('molecule',current()/xsams03:SpeciesRef)/xsams03:MolecularChemicalSpecies/xsams03:StoichiometricFormula"/>
[
	<xsl:call-template name="molec_state_qn_v0_3">
          <xsl:with-param name="state" select="key('molstate',current()/xsams03:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:when test="key('particle',current()/xsams03:SpeciesRef)">
        <xsl:value-of select="key('particle',current()/xsams03:SpeciesRef)/@name"/>
        [<xsl:value-of select="xsams03:StateRef"/>]    
      </xsl:when>
      <xsl:when test="key('atom',current()/xsams03:SpeciesRef)">
	<xsl:call-template name="atom-name_v0_3">
          <xsl:with-param name="atom" select="key('atom',current()/xsams03:SpeciesRef)/../.."/>
        </xsl:call-template>
[
	<xsl:call-template name="atomic_state_qn_v0_3">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams03:StateRef)"/>
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

  <xsl:template match="xsams03:Product">
    <b>
    <xsl:choose>
      <xsl:when test="key('molecule',current()/xsams03:SpeciesRef)">
        <xsl:value-of select="key('molecule',current()/xsams03:SpeciesRef)/xsams03:MolecularChemicalSpecies/xsams03:StoichiometricFormula"/>
[
	<xsl:call-template name="molec_state_qn_v0_3">
          <xsl:with-param name="state" select="key('molstate',current()/xsams03:StateRef)"/>
        </xsl:call-template>
]
      </xsl:when>
      <xsl:when test="key('particle',current()/xsams03:SpeciesRef)">
        <xsl:value-of select="key('particle',current()/xsams03:SpeciesRef)/@name"/>
        [<xsl:value-of select="xsams03:StateRef"/>]    
      </xsl:when>
      <xsl:when test="key('atom',current()/xsams03:SpeciesRef)">
	<xsl:call-template name="atom-name_v0_3">
          <xsl:with-param name="atom" select="key('atom',current()/xsams03:SpeciesRef)/../.."/>
        </xsl:call-template>
[
	<xsl:call-template name="atomic_state_qn_v0_3">
          <xsl:with-param name="state" select="key('atomstate',current()/xsams03:StateRef)"/>
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


  <xsl:template name="molec_state_v0_3">
    <xsl:param name="state"/>

    <xsl:if test="count($state)>0">
    <div style="float:left;min-width:17ex">
      <xsl:value-of select="format-number($state/xsams03:MolecularStateCharacterisation/xsams03:TotalStatisticalWeight,' 0000', 'example_v0_3')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="$state/xsams03:MolecularStateCharacterisation/xsams03:StateEnergy/xsams03:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="$state/xsams03:Case/*[local-name()='QNs']/*"/>
    </xsl:if>
  </xsl:template>


  <xsl:template name="atomic_state_v0_3">
    <xsl:param name="state"/>
    <xsl:if test="count($state)>0">
    <div style="float:left;min-width:17ex">
      <xsl:value-of select="format-number($state/xsams03:AtomicNumericalData/xsams03:StatisticalWeight,' 0000', 'example_v0_3')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="$state/xsams03:AtomicNumericalData/xsams03:StateEnergy/xsams03:Value"/>
      <xsl:text>  </xsl:text>
    </div>
    <xsl:apply-templates select="$state/xsams03:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="$state/xsams03:AtomicComposition"/>
    </xsl:if>

  </xsl:template>


  <xsl:template name="molec_state_qn_v0_3">
    <xsl:param name="state"/>

    <xsl:apply-templates select="$state/xsams03:Case/*[local-name()='QNs']/*"/>
  </xsl:template>


  <xsl:template name="atomic_state_qn_v0_3">
    <xsl:param name="state"/>
    <xsl:apply-templates select="$state/xsams03:AtomicQuantumNumbers"/>
    <xsl:apply-templates select="$state/xsams03:AtomicComposition"/>
  </xsl:template>

  <xsl:template match="xsams03:Function">
     <p><b><a name="{@functionID}"><xsl:value-of select="@functionID"/>:
     <xsl:value-of select="xsams03:Name"/>
     </a></b>
     <div><xsl:value-of select="xsams03:Y/xsams03:Description"/></div>
        <xsl:value-of select="xsams03:Y/@name"/>
        [<xsl:value-of select="xsams03:Y/@units"/>]
     = <xsl:value-of select="xsams03:Expression"/></p>
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
  <xsl:template match="xsams03:AtomicQuantumNumbers">
    <xsl:apply-templates select="xsams03:TotalAngularMomentum"/>    
  </xsl:template>

  <xsl:template match="xsams03:TotalAngularMomentum">
    J:<xsl:value-of select="."/>;    
  </xsl:template>

  <xsl:template match="xsams03:AtomicComposition">
    <xsl:apply-templates select="xsams03:Component/xsams03:Term/xsams03:LS"/>
  </xsl:template>
 
  <xsl:template match="xsams03:LS">
    L:<xsl:value-of select="xsams03:L/xsams03:Value"/>;
    S:<xsl:value-of select="xsams03:S"/>;
  </xsl:template>

  <xsl:template match="xsams03:Source">
     <li>
     <xsl:value-of select="@sourceID"/>
     <xsl:text>: </xsl:text>
     <xsl:value-of select="xsams03:Authors/xsams03:Author"/>
     <i>
     <xsl:value-of select="xsams03:SourceName"/>
     </i>
     <xsl:text>  </xsl:text>
     <b>
     <xsl:value-of select="xsams03:Volume"/>
     </b>
     <xsl:text>, </xsl:text>
     <xsl:value-of select="xsams03:PageBegin"/>
     <xsl:text>&#xa;</xsl:text>
     <xsl:text> (</xsl:text>
     <xsl:value-of select="xsams03:Year"/>
     <xsl:text>) </xsl:text>
     </li>
 </xsl:template>


  <xsl:template match="xsams03:Method">
     <li>
     <b><xsl:value-of select="@methodID"/>
     <xsl:text>: </xsl:text>
     <cap><xsl:value-of select="xsams03:Category"/></cap>
     </b>
     <p>Sources:
     <xsl:for-each select="xsams03:SourceRef">
         <xsl:value-of select="."/>
         <xsl:text>;</xsl:text>
     </xsl:for-each>
     </p>
     <xsl:text>  </xsl:text>
     <p><xsl:value-of select="xsams03:Comments"/></p>
     <xsl:text>  </xsl:text>
     <p><xsl:value-of select="xsams03:Description"/></p>
     </li>
 </xsl:template>

<!--
  <xsl:template match="xsams03:PartitionFunction">
    <dl>
    <dt>T</dt>
    <dd>
    <xsl:value-of select="xsams03:T/xsams03:DataList"/>
    </dd>
    <dt>Q</dt>
    <dd>
    <xsl:value-of select="xsams03:Q/xsams03:DataList"/>
    </dd>
    </dl>
  </xsl:template>
-->
  <xsl:template match="xsams03:PartitionFunction">
    <table class="full" style="font-size:smaller">
    <caption> Partition functions for

       <xsl:call-template name="species_name_v0_3">
         <xsl:with-param name="mol_id" select="../.."/>
       </xsl:call-template>

    </caption>
    <thead>
    <tr><th>T</th>
    <xsl:call-template name="datalist2col_v0_3">
      <xsl:with-param name="list" select="normalize-space(xsams03:T/xsams03:DataList)"/>
      <xsl:with-param name="cell" select="'th'"/>
    </xsl:call-template>
    </tr></thead><tbody>
    <tr><th>Q</th>
    <xsl:call-template name="datalist2col_v0_3">
      <xsl:with-param name="list" select="normalize-space(xsams03:Q/xsams03:DataList)"/>
    </xsl:call-template>
    </tr></tbody>
    </table>
  </xsl:template>

  <xsl:template name="datalist2col_v0_3">
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
       <xsl:call-template name="datalist2col_v0_3">
          <xsl:with-param name="list" select="$remaining"/>
          <xsl:with-param name="cell" select="$cell"/>
       </xsl:call-template>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsams03:TabulatedData">
    <table class="full" style="border-style:solid">
    <caption> 
    <xsl:value-of select="xsams03:Comments"/>
    </caption>
    <thead>
    <tr><th>X</th>
    <th>
    <xsl:value-of select="xsams03:X/xsams03:DataList"/>
    </th>
    </tr></thead><tbody>
    <tr><th>Y</th>
    <td>
    <xsl:value-of select="xsams03:Y/xsams03:DataList"/>
    </td>
    </tr></tbody>
    </table>
  </xsl:template>


  <xsl:template match="xsams03:FitData">
    <xsl:apply-templates select="xsams03:FitParameters"/>
  </xsl:template>

  <xsl:template match="xsams03:FitParameters">
    <div><a href="#{@functionRef}">
<xsl:value-of select="@functionRef"/></a>
    </div>
    <div> Args:
    <xsl:apply-templates select="xsams03:FitArgument"/>
    </div>
    <div> Param.:
    <xsl:apply-templates select="xsams03:FitParameter"/>
    </div>
  </xsl:template>
  
  <xsl:template match="xsams03:FitArgument">
    <xsl:value-of select="@name"/>
    <xsl:text>(</xsl:text>
    <xsl:value-of select="@units"/>
    <xsl:text>)</xsl:text>
    <xsl:text>[</xsl:text>
    <xsl:value-of select="xsams03:LowerLimit"/>
    <xsl:text>-</xsl:text>
    <xsl:value-of select="xsams03:UpperLimit"/>
    <xsl:text>]</xsl:text>
    <xsl:text>;</xsl:text>
  </xsl:template>

  <xsl:template match="xsams03:FitParameter">
    <xsl:value-of select="@name"/>
    <xsl:text>=</xsl:text>
    <xsl:value-of select="xsams03:Value"/>
    <xsl:text>;</xsl:text>
  </xsl:template>

  <xsl:template name="atom-name_v0_3">
    <xsl:param name="atom"/>
    <xsl:choose>
       <xsl:when test="$atom/xsams03:Isotope/xsams03:IsotopeParameters/xsams03:MassNumber">
         <sup><xsl:value-of select="$atom/xsams03:Isotope/xsams03:IsotopeParameters/xsams03:MassNumber"/></sup>
         <xsl:value-of select="$atom/xsams03:ChemicalElement/xsams03:ElementSymbol"/>
       </xsl:when>
       <xsl:otherwise>
         <xsl:value-of select="$atom/xsams03:ChemicalElement/xsams03:ElementSymbol"/>
       </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="plot-charge_v0_3">
      <xsl:with-param name="charge" select="$atom/xsams03:Isotope/xsams03:Ion/xsams03:IonCharge"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="plot-charge_v0_3">
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
