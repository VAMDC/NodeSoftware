<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xsams="http://vamdc.org/xml/xsams/0.2">

  <xsl:output method="html"/>

  <xsl:decimal-format name="example" zero-digit ="0" />

  <xsl:template match="/">
	<fieldset>
	<div class="legend">Molecules</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist full">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule"/>
	</ul>
	</fieldset>
	<xsl:text>&#xa;</xsl:text>
        <xsl:text>&#xa;</xsl:text>
	<fieldset>
	<div class="legend">Transitions</div>
	<xsl:text>&#xa;</xsl:text>
	<ul class="vlist2 full">
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
    <li>
	<h3>
	<xsl:value-of select="@speciesID" />	
	</h3>
    <dl>              
    <dt>Chemical Name</dt>
    <dd>
    <xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:ChemicalName/xsams:Value"/>
    </dd>
    <xsl:text>&#xa;</xsl:text>
    <dt>Stoichiometric Formula</dt>
    <dd>
    <xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula"/>
    </dd>
    <xsl:text>&#xa;</xsl:text>
    <dt>InChi</dt>
    <dd>
    <xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:InChI"/>
    </dd>
    <xsl:text>&#xa;</xsl:text>
    <dt>InChiKey</dt>
    <dd>
    <xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:InChIKey"/>
    </dd>
    <xsl:text>&#xa;</xsl:text>
    <dt>Partition Function</dt>
    <dd>
    <xsl:apply-templates select="xsams:MolecularChemicalSpecies/xsams:PartitionFunction"/>
    </dd>
    </dl></li>
  </xsl:template>

  <xsl:template match="xsams:RadiativeTransition">
	<li>
	<span style="text-align:right; min-width:16ex;margin-right:0.5em">
	<xsl:value-of select="format-number(xsams:EnergyWavelength/xsams:Frequency/xsams:Value,'0.0000')"/>
	</span>

	<span style="text-align:right; min-width:16ex;margin-right:0.5em">
   	<xsl:value-of select="format-number(xsams:EnergyWavelength/xsams:Frequency/xsams:Accuracy,'0.0000 ')"/>
	</span>

	<span style="text-align:right; min-width:16ex;">
        <xsl:value-of select="format-number(xsams:Probability/xsams:TransitionProbabilityA/xsams:Value,'0.00000000 ')"/>
	</span>
        <xsl:text>, </xsl:text>
	<div>
	<xsl:text>Initial State </xsl:text>
        <xsl:value-of select="xsams:InitialStateRef"/><xsl:text>:</xsl:text>
	<xsl:for-each select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:InitialStateRef]">
              <xsl:value-of select="format-number(current()/xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000', 'example')"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="current()/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value"/>
              <xsl:text>  </xsl:text>
              <xsl:apply-templates select="current()/xsams:Case/*[local-name()='QNs']/*"/>
        </xsl:for-each>
	</div>
	<div>
	<xsl:text>Final State </xsl:text>
        <xsl:value-of select="xsams:FinalStateRef"/><xsl:text>:</xsl:text>
	<xsl:for-each select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:FinalStateRef]">
              <xsl:value-of select="format-number(current()/xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000')"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="current()/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value"/>
              <xsl:text>  </xsl:text>
              <xsl:apply-templates select="current()/*[local-name()='QNs']/*"/>
              <xsl:text>  </xsl:text>
              <xsl:apply-templates select="current()/xsams:Case/*[local-name()='QNs']/*"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="./../xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula" />	
              <xsl:text>:</xsl:text>
              <xsl:value-of select="./../@speciesID" />	
        </xsl:for-each>
	</div>
</li>

  </xsl:template>

  <xsl:template match="*[local-name()='QNs']/*">
<strong>
    <xsl:value-of select="local-name()"/>
</strong>
     <xsl:text>:</xsl:text>
<var>
    <xsl:value-of select="text()"/>
</var>
    <xsl:text>;</xsl:text>
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
