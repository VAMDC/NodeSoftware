<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xsams="http://vamdc.org/xml/xsams/0.2">

  <xsl:output method="text"/>

  <xsl:decimal-format name="example" zero-digit ="0" />

  <xsl:template match="/">
        <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule"/>
	<xsl:text>&#xa;</xsl:text>
  </xsl:template>


  <xsl:template match="xsams:Molecule">
    <xsl:text>!MOLECULE&#xa;</xsl:text>
    <xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula"/>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!MOLECULAR WEIGHT&#xa;</xsl:text>
    <xsl:value-of select="xsams:MolecularChemicalSpecies/xsams:StableMolecularProperties/xsams:MolecularWeight/xsams:Value"/>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!NUMBER OF ENERGY LEVELS&#xa;</xsl:text>
    <xsl:value-of select = "count(xsams:MolecularState)" /> 
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!LEVEL + ENERGIES(cm^-1) + WEIGHT + J&#xa;</xsl:text>
        <xsl:apply-templates select="xsams:MolecularState"/>
    <xsl:text>!NUMBER OF RADIATIVE TRANSITIONS&#xa;</xsl:text>
    <xsl:variable name="species" select="@speciesID"/>

    <xsl:for-each select="/xsams:XSAMSData/xsams:Processes/xsams:Radiative/xsams:RadiativeTransition ">
       <xsl:if test="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:FinalStateRef]/../@speciesID = $species" >
          <xsl:if test = "position() = last()">
	    <xsl:value-of select="position()"/>
         </xsl:if>
       </xsl:if>
    </xsl:for-each>

    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!TRANS + UP + LOW + EINSTEINA(s^-1) + FREQ(GHz) + E_u(K)</xsl:text>
    <xsl:text>&#xa;</xsl:text>


    <xsl:for-each select="/xsams:XSAMSData/xsams:Processes/xsams:Radiative/xsams:RadiativeTransition">
       <xsl:if test="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:FinalStateRef]/../@speciesID = $species" >
          <xsl:value-of select="position()"/>
          <xsl:text>  </xsl:text>
          <xsl:value-of select="substring-after(xsams:InitialStateRef,'-')"/>
          <xsl:text>  </xsl:text>
          <xsl:value-of select="substring-after(xsams:FinalStateRef,'-')"/>
          <xsl:text>  </xsl:text>
          <xsl:value-of select="format-number(xsams:Probability/xsams:TransitionProbabilityA/xsams:Value,'0.0000000000 ')"/>
          <xsl:text>  </xsl:text>
  	  <xsl:value-of select="format-number(xsams:EnergyWavelength/xsams:Frequency/xsams:Value * 0.001,'000000000.0000 ')"/>
          <xsl:text>  </xsl:text>
	  <xsl:value-of select="format-number(1.43877506*/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:FinalStateRef]/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value,'.0000')"/>
          <xsl:text>&#xa;</xsl:text>
       </xsl:if>
    </xsl:for-each>

    <xsl:text>!NUMBER OF COLL PARTNERS</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:value-of select="count(/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]/xsams:Reactant)"/>
    <xsl:text>&#xa;</xsl:text>

    <xsl:text>!COLLISIONS BETWEEN</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:value-of select="count(/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]/xsams:Reactant)"/>
    <xsl:text>  </xsl:text>
    <xsl:value-of select="/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]/xsams:Comments"/>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!NUMBER OF COLL TRANS</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:value-of select="count(/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition)"/>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!NUMBER OF COLL TEMPS</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:call-template name="output-tokens">
      <xsl:with-param name="list"><xsl:value-of select="concat('0#',/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]/xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:DataXY/xsams:X[@units='K']/xsams:DataList[@units='K'])" /></xsl:with-param>
    </xsl:call-template>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!COLL TEMPS</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:for-each select="/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]">
      <xsl:value-of select="xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:DataXY/xsams:X[@units='K']/xsams:DataList[@units='K']"/>
    <xsl:text>&#xa;</xsl:text>
    </xsl:for-each>
    <xsl:text>!TRANS+ UP+ LOW+ COLLRATES(cm^3 s^-1)</xsl:text>
    <xsl:text>&#xa;</xsl:text>
        
    <xsl:for-each select="/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition">
      <xsl:value-of select="position()"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="substring-after(xsams:Reactant/xsams:StateRef,'-')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="substring-after(xsams:Product/xsams:StateRef,'-')"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:DataXY/xsams:Y[@units='cm3/s']/xsams:DataList[@units='cm3/s']"/>
      <xsl:text>&#xa;</xsl:text>
    </xsl:for-each>


  </xsl:template>




  <xsl:template match="xsams:MolecularState">
     <xsl:value-of select="substring-after(@stateID,'-')"/>
     <xsl:text>    </xsl:text>
     <xsl:value-of select="format-number(xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value,'000000000000.00000000 ')"/>
     <xsl:text>    </xsl:text>
     <xsl:value-of select="format-number(xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000', 'example')"/>
     <xsl:text>&#xa;</xsl:text>
  </xsl:template>

  <xsl:template name="xsams:RadiativeTransition">
	<xsl:param name="specie" />
<xsl:value-of select="$specie" />
        <xsl:text>  </xsl:text>
        <xsl:value-of select="xsams:InitialStateRef"/>
        <xsl:text>  </xsl:text>
        <xsl:value-of select="xsams:FinalStateRef"/>
        <xsl:text>  </xsl:text>
        <xsl:value-of select="format-number(xsams:Probability/xsams:TransitionProbabilityA/xsams:Value,'0.0000000000 ')"/>
        <xsl:text>  </xsl:text>
	<xsl:value-of select="format-number(xsams:EnergyWavelength/xsams:Frequency/xsams:Value * 0.001,'000000000.0000 ')"/>
        <xsl:text>  </xsl:text>
	<xsl:for-each select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:FinalStateRef]">
              <xsl:value-of select="format-number(1.43877506*current()/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value,'.0000')"/>
        </xsl:for-each>


        <xsl:value-of select="xsams:InitialStateRefxxxx"/>
	<xsl:for-each select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:InitialStateRefxxxx]">
              <xsl:value-of select="format-number(current()/xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000', 'example')"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="current()/xsams:MolecularStateCharacterisation/xsams:StateEnergy/Value"/>
              <xsl:text>  </xsl:text>
              <xsl:apply-templates select="current()/Case/*[local-name()='QNs']/*"/>
        </xsl:for-each>

        <xsl:value-of select="xsams:FinalStateRefxxxx"/>
	<xsl:for-each select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:FinalStateRefxxxx]">
              <xsl:value-of select="format-number(current()/xsams:MolecularStateCharacterisation/xsams:TotalStatisticalWeight,' 0000')"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="current()/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value"/>
              <xsl:text>  </xsl:text>
              <xsl:apply-templates select="current()/*[local-name()='QNs']/*"/>
              <xsl:text>  </xsl:text>
              <xsl:apply-templates select="current()/Case/*[local-name()='QNs']/*"/>
              <xsl:text>  </xsl:text>
              <xsl:value-of select="./../xsams:MolecularChemicalSpecies/xsams:StoichiometricFormula" />	
              <xsl:text>:</xsl:text>
              <xsl:value-of select="./../@speciesID" />	
        </xsl:for-each>

        <xsl:text>&#xa;</xsl:text>

  </xsl:template>

  <xsl:template match="*[local-name()='QNs']/*">
    <xsl:value-of select="local-name()"/>
    <xsl:text>:</xsl:text>
<font style="color:red">
    <xsl:value-of select="text()"/>
</font>
    <xsl:text>;</xsl:text>
  </xsl:template>

  <xsl:template match="xsams:Source">
     <xsl:value-of select="@sourceID"/>
     <xsl:text>: </xsl:text>
     <xsl:value-of select="xsams:Authors/xsams:Author"/>
     <xsl:text>, </xsl:text>
     <xsl:value-of select="xsams:Year"/>
     <xsl:text>, </xsl:text>
     <xsl:value-of select="xsams:SourceName"/>
     <xsl:text>  </xsl:text>
     <xsl:value-of select="xsams:Volume"/>
     <xsl:text>, </xsl:text>
     <xsl:value-of select="xsams:PageBegin"/>
     <xsl:text>&#xa;</xsl:text>
 </xsl:template>

 <xsl:template match="xsams:PartitionFunction">
    <xsl:text>Partitionfunction: &#xa;</xsl:text>
    <xsl:text>T: </xsl:text>
    <xsl:value-of select="xsams:T/xsams:DataList"/>
    <xsl:text>&#xa;Q: </xsl:text>
    <xsl:value-of select="xsams:Q/xsams:DataList"/>
    <xsl:text>&#xa;</xsl:text>
 </xsl:template>


 <xsl:template name="list-count">
  <xsl:call-template name="output-tokens">
    <xsl:with-param name="list"><xsl:value-of select="xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:DataXY/xsams:X[@units='K']/xsams:DataList[@units='K']" /></xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <xsl:template name="output-tokens">
   <xsl:param name="list" />
   <xsl:variable name="counterbefore" select="substring-before($list, '#')" />
   <xsl:variable name="counter" select="$counterbefore+1" />
   <xsl:variable name="content" select="substring-after($list, '#')" />

   <xsl:variable name="newlist" select="concat(normalize-space($content), ' ')" />
   <xsl:variable name="first" select="substring-before($newlist, ' ')" />
   <xsl:variable name="remaining" select="substring-after($newlist, ' ')" />


   <xsl:choose>
     <xsl:when test="$remaining">
        <xsl:variable name="newcounter" select="$counter+1" />

        <xsl:call-template name="output-tokens">
            <xsl:with-param name="list" select="concat($counter,'#',$remaining)" />
       </xsl:call-template>
     </xsl:when>
     <xsl:otherwise>
       <xsl:value-of select="$counter" />
     </xsl:otherwise>
   </xsl:choose>
 </xsl:template>


</xsl:stylesheet>
