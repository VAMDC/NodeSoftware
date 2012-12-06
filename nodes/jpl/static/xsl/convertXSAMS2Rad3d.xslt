<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:xsams="http://vamdc.org/xml/xsams/0.3">

  <xsl:output method="text"/>

  <xsl:decimal-format name="example" zero-digit ="0" />

  <xsl:template match="/">

    <xsl:if test="count(/xsams:XSAMSData/xsams:Processes/xsams:Collisions) = 0 ">
       <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule"/>
    </xsl:if>

    <xsl:variable name="reactant1" select="/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]/xsams:Reactant[1]/xsams:SpeciesRef"/>
    <xsl:apply-templates select="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule[@speciesID = $reactant1]"/>
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
       <xsl:if test="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:UpperStateRef]/../@speciesID = $species" >
          <xsl:if test = "position() = last()">
	    <xsl:value-of select="position()"/>
         </xsl:if>
       </xsl:if>
    </xsl:for-each>

    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!TRANS + UP + LOW + EINSTEINA(s^-1) + FREQ(GHz) + E_u(K)</xsl:text>
    <xsl:text>&#xa;</xsl:text>


    <xsl:for-each select="/xsams:XSAMSData/xsams:Processes/xsams:Radiative/xsams:RadiativeTransition">
       <xsl:if test="/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:UpperStateRef]/../@speciesID = $species" >
          <xsl:value-of select="position()"/>
          <xsl:text>  </xsl:text>
          <xsl:value-of select="substring-after(xsams:UpperStateRef,'-')"/>
          <xsl:text>  </xsl:text>
          <xsl:value-of select="substring-after(xsams:LowerStateRef,'-')"/>
          <xsl:text>  </xsl:text>
          <xsl:value-of select="format-number(xsams:Probability/xsams:TransitionProbabilityA/xsams:Value,'0.0000000000 ')"/>
          <xsl:text>  </xsl:text>
  	  <xsl:value-of select="format-number(xsams:EnergyWavelength/xsams:Frequency/xsams:Value * 0.001,'000000000.0000 ')"/>
          <xsl:text>  </xsl:text>
	  <xsl:value-of select="format-number(1.43877506*/xsams:XSAMSData/xsams:Species/xsams:Molecules/xsams:Molecule/xsams:MolecularState[@stateID=current()/xsams:UpperStateRef]/xsams:MolecularStateCharacterisation/xsams:StateEnergy/xsams:Value,'.0000')"/>
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

    <xsl:choose>
    <xsl:when test="count(/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition)>0">
    <xsl:call-template name="output-tokens">
      <xsl:with-param name="list">
        <xsl:value-of select="concat('0#',/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]/xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:X[@units='K']/xsams:DataList)" />
      </xsl:with-param>
    </xsl:call-template>
    </xsl:when>
     <xsl:otherwise>
       <xsl:text>0</xsl:text>
     </xsl:otherwise>
    </xsl:choose>
    
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!COLL TEMPS</xsl:text>
    <xsl:text>&#xa;</xsl:text>

    <xsl:for-each select="/xsams:XSAMSData/xsams:Processes/xsams:Collisions/xsams:CollisionalTransition[1]">
      <xsl:value-of select="xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:X[@units='K']/xsams:DataList"/>
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
      <xsl:value-of select="xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:Y[@units='cm3/s']/xsams:DataList"/>
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





 <xsl:template name="list-count">
  <xsl:call-template name="output-tokens">
    <xsl:with-param name="list">
      <xsl:value-of select="xsams:DataSets/xsams:DataSet[@dataDescription='rateCoefficient']/xsams:TabulatedData/xsams:X[@units='K']/xsams:DataList[@units='K']" />
    </xsl:with-param>
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
