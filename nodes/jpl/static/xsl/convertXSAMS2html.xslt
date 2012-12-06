<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xsams="http://vamdc.org/xml/xsams/0.3">

  <xsl:output method="html"/>

  <xsl:decimal-format name="example" zero-digit ="0" />

  <xsl:template match="/">
	<fieldset>
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full" style="list-style:none;">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule"/>
	</ul>
	</fieldset>
	<xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
	<fieldset>
	<div class="legend">Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2" style="list-style:none;">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Processes/xsams:Radiative/xsams:RadiativeTransition"/>
	</ul>
	</fieldset>
        <xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
	<fieldset>
	<div class="legend">Sources</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist full">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Sources/xsams:Source"/>
        <xsl:text>&#xa;</xsl:text>
	</ul>
	</fieldset>
  </xsl:template>


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

  <xsl:template match="xsams:RadiativeTransition">
	<li style="clear:both; border-bottom: 1px solid #90bade;">
	
	<div style="float:left; min-width:27em;">
	<ul style="list-style:none;">
	<li style="font-weight:bold">

	<xsl:choose>
	  <xsl:when test="xsams:EnergyWavelength/xsams:Frequency">
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(xsams:EnergyWavelength/xsams:Frequency/xsams:Value,'0.0000')"/>
	    </div>
  	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(xsams:EnergyWavelength/xsams:Frequency/xsams:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:when>	
	  <xsl:otherwise>
	    <div style="float:left;text-align:right; min-width:10ex;margin-right:0.5em">
            <xsl:value-of select="format-number(29979.2458*xsams:EnergyWavelength/xsams:Wavenumber/xsams:Value,'0.0000')"/>
	    </div>
	    <div style="float:left;text-align:right; min-width:7ex;margin-right:0.5em">
   	    <xsl:value-of select="format-number(29979.2458*xsams:EnergyWavelength/xsams:Wavenumber/xsams:Accuracy,'0.0000 ')"/>
	    </div>
	  </xsl:otherwise>
	</xsl:choose>


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
<!--        <xsl:value-of select="xsams:LowerStateRef"/><xsl:text>:</xsl:text> -->
	<xsl:for-each select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:LowerStateRef]">
	  <div style="float:left;min-width:17ex">
              <xsl:value-of select="format-number(current()/xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000', 'example')"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="current()/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value"/>
              <xsl:text>  </xsl:text>
  	  </div>
              <xsl:apply-templates select="current()/xsams:Case/*[local-name()='QNs']/*"/>
        </xsl:for-each>
	</div>
	<div>
	
	<div style="float:left;width:5ex">
	<xsl:text>F.S.: </xsl:text>
	</div>
<!--        <xsl:value-of select="xsams:UpperStateRef"/><xsl:text>:</xsl:text> -->
	<xsl:for-each select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:UpperStateRef]">
	   <div style="float:left;min-width:17ex">
              <xsl:value-of select="format-number(current()/xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000')"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="current()/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value"/>
              <xsl:text>  </xsl:text>
           </div>
              <xsl:apply-templates select="current()/*[local-name()='QNs']/*"/>
              <xsl:text>  </xsl:text>
              <xsl:apply-templates select="current()/xsams:Case/*[local-name()='QNs']/*"/>
              <xsl:text>  </xsl:text>
        </xsl:for-each>
	</div>
	</div>
	
	<div style="float:right">
          <xsl:value-of select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule[xsams:MolecularState/@stateID=current()/xsams:UpperStateRef]/@speciesID"/>
          <xsl:text>:</xsl:text>
	  <xsl:value-of select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule[xsams:MolecularState/@stateID=current()/xsams:UpperStateRef]/xsams:MolecularChemicalSpecies/xsams:OrdinaryStructuralFormula" />	
	</div>
	</li>

  </xsl:template>

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

</xsl:stylesheet>
