<?xml version="1.0" encoding="ISO-8859-1"?>
<!--
This stylesheet generates output for RADEX.
If a filename is specified via '-with' then collisional data are taken from this file and
are merged into the output. 

species1:
  Species-ID of the molecule for which the output is generated

species2:
  Species-ID of the molecule from which the collisional data is taken.
  This specie has to be given in with-file.
-->

<xsl:stylesheet version="1.1"
xmlns:xsl ="http://www.w3.org/1999/XSL/Transform" xmlns:xsams10="http://vamdc.org/xml/xsams/1.0" xmlns:xsams03="http://vamdc.org/xml/xsams/0.3">

<xsl:key name="molecule_by_inchikey" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Molecules/xsams03:Molecule" use="/xsams03:MolecularChemicalSpecies/xsams03:InChIKey"/>

<xsl:key name="molstate" match="//xsams03:MolecularState" use="@stateID"/>
<!--<xsl:key name="molstate" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Molecules/xsams03:Molecule/xsams03:MolecularState" use="@stateID"/>-->
<xsl:key name="atomstate" match="/xsams03:XSAMSData/xsams03:Species/xsams03:Atoms/xsams03:Atom/xsams03:Isotope/xsams03:Ion/xsams03:AtomicState" use="@stateID"/>
<xsl:key name="collision" match="xsams03:CollisionalTransition" use="xsams03:Reactant/xsams03:SpeciesRef"/>
<xsl:key name="replacement" match="replacestate" use="which"/>
<xsl:decimal-format name="example" zero-digit ="0" />

<xsl:output method="text" />
<xsl:param name="with" />
<xsl:param name="species1" />
<xsl:param name="species2" />


<xsl:template match="/xsams03:XSAMSData">


   <xsl:if test="string($species1)=''">
      <xsl:message terminate="yes">
         <xsl:text>No species specified (parameter 'species1')</xsl:text>
      </xsl:message>
   </xsl:if>


   <!-- filter molecules -->
   <xsl:variable name="molecule1">
     <xsl:copy-of select="//xsams03:Molecule[@speciesID=$species1][1]"/>
   </xsl:variable>
   <!-- or atoms -->
   <xsl:variable name="atom1">
     <xsl:copy-of select="//xsams03:Atom[@speciesID=$species1][1]"/>
   </xsl:variable>
  
   <xsl:if test="count($molecule1/*)+count($atom1/*)=0">
      <xsl:message terminate="yes">
         <xsl:text>Species1 not found</xsl:text>
      </xsl:message>
   </xsl:if>

   <!-- Get a map which contains the position of each state (RADEX STATE INDECES should start from 1 to #states 
        instead of an arbitrary id.
    -->
   <xsl:variable name="position_map">
     <xsl:call-template name="generate_statepos">
       <xsl:with-param name="states" select="$molecule1/xsams03:Molecule/xsams03:MolecularState"/>
       </xsl:call-template>
   </xsl:variable>

   <xsl:variable name="transitions1">
      <xsl:for-each select="//xsams03:RadiativeTransition">
        <xsl:choose>
          <!-- filter via SpeciesRef if specified -->
          <xsl:when test="xsams03:SpeciesRef"> 
             <xsl:if test="xsams03:SpeciesRef=$species1">
               <xsl:copy-of select="."/>
             </xsl:if>
          </xsl:when>
          <!-- slower: get SpeciesRef via UpperStateRef and StateID -->
          <xsl:otherwise>
            <xsl:if test="key('molstate',xsams03:UpperStateRef)/../@speciesID=$species1">
               <xsl:copy-of select="."/> 
            </xsl:if>-
          </xsl:otherwise>
        </xsl:choose>

      </xsl:for-each>
   </xsl:variable>

   <xsl:message># of Transitions</xsl:message>
   <xsl:message><xsl:value-of select="count($transitions1/*)"/></xsl:message>


   <!-- GENERATE RADEX OUTPUT: STATES AND TRANSITIONS -->

   <!-- molecular part -->
   <xsl:call-template name="radexoutput-molecule">
     <xsl:with-param name="molecule" select="$molecule1"/>
   </xsl:call-template>

   <!-- radiative transitions -->
   <xsl:call-template name="radexoutput-radiative-header">
     <xsl:with-param name="num_transitions" select="count(//xsams03:RadiativeTransition)"/>
   </xsl:call-template>
   <xsl:apply-templates select="//xsams03:RadiativeTransition">
     <xsl:with-param name="position_map" select="$position_map"/>
   </xsl:apply-templates>


   <!-- PROCESS ADDITIONAL FILE WHICH SHOULD CONTAIN COLLISIONS -->

   <xsl:choose>
   <xsl:when test="string($with)=''">
      <xsl:message>
         <xsl:text>No input file specified (parameter 'with')</xsl:text>
      </xsl:message>
   </xsl:when>
   <xsl:otherwise>
   <xsl:message>
      <xsl:text />Merging input with '<xsl:value-of select="$with" />
      <xsl:text>'</xsl:text>
   </xsl:message>

   <xsl:if test="string($species2)=''">
      <xsl:message><xsl:text>No species to merge with specified (parameter 'species2')</xsl:text></xsl:message>
      <xsl:message><xsl:text>Available species are:</xsl:text></xsl:message>
      <xsl:for-each select="document($with,/*)//xsams03:Molecule">
        <xsl:message>
          <xsl:value-of select="@speciesID"/>:
          <xsl:value-of select="xsams03:MolecularChemicalSpecies/xsams03:StoichiometricFormula"/>
        </xsl:message>
      </xsl:for-each>   
      <xsl:message terminate="yes"/>
   </xsl:if>

   <!-- READ NODES FROM ADDITIONAL FILE -->
   <xsl:variable name="nodes2" select="document($with,/*)/node()" />

   <!-- Get 'table' which contains a list of matches for states from species2 to states from species1 -->
   <xsl:variable name="mstates">
     <xsl:call-template name="merge-states">
        <xsl:with-param name="states_return" select="$molecule1/xsams03:Molecule/xsams03:MolecularState"/>
        <xsl:with-param name="states_rest" select="$nodes2/xsams03:Species/xsams03:Molecules/xsams03:Molecule[@speciesID=$species2]/xsams03:MolecularState"/>
     </xsl:call-template>
   </xsl:variable>
   
   <!-- Output matches -->
   <xsl:message>Replace states of species2 by states of species1 </xsl:message>
   <xsl:for-each select="$mstates/replacestate">
     <xsl:message><xsl:value-of select="which"/> by
     <xsl:value-of select="by"/></xsl:message>
   </xsl:for-each>




   <!-- copy all collisions in which species2 occurs either as product or reactant -->
   <xsl:variable name="collisions">
     <!-- for-each is used to make key working (environment has to be nodes2) -->
     <xsl:for-each select="$nodes2/xsams03:Species/xsams03:Molecules/xsams03:Molecule[@speciesID=$species2]">
       <!--<xsl:copy-of select="key('collision',@speciesID)"/>-->
       
       <!-- Create a copy of each collision in which the stateIDs which match with states from main XSAMS file are 
            replaces 
       -->
       <xsl:for-each select="key('collision',@speciesID)">
         <xsl:copy>
           <!-- <xsl:for-each select="*[not(name()='Product') and not(name()='Reactant')]|@*"> -->
           <!-- attach all elements/attributes to CollisionalTransition -->
           <xsl:for-each select="*|@*">
             <xsl:choose>
               <!-- For reactants and products the state id has to be checked and replaced if it has changed -->
               <xsl:when test="(name()='Reactant' or name()='Product') and xsams03:StateRef">
                 <!-- get new state id from the replacement list-->
                 <xsl:variable name="stateid">
                   <xsl:call-template name="replace_stateid">
                     <xsl:with-param name="id" select="xsams03:StateRef" />
                     <xsl:with-param name="states" select="$mstates/replacestate" />
                   </xsl:call-template>
                 </xsl:variable>
                 <xsl:choose>
                   <!-- State id still exists and does not have to be replaced -->
                   <xsl:when test="$stateid=''">
                     <xsl:copy-of select="."/>
                   </xsl:when>                
                   <!-- Generate new Reactant/Product - element with new stateID --> 
                   <xsl:otherwise>
                      <xsl:copy>
                        <xsl:element name="xsams03:StateRef" ><xsl:value-of select="$position_map/*[@id=$stateid]"/></xsl:element>
                        <xsl:element name="xsams03:SpeciesRef" ><xsl:value-of select="$species1"/></xsl:element>
                     </xsl:copy>                        
                   </xsl:otherwise>
                 </xsl:choose>
                
               </xsl:when>
               <!-- just copy the element/attribute if it is not product or reactant element -->
               <xsl:otherwise>
                 <xsl:copy-of select="."/>
               </xsl:otherwise>
             </xsl:choose>
           </xsl:for-each>       
         </xsl:copy>
       </xsl:for-each>

     </xsl:for-each>
   </xsl:variable>






   <!-- GENERATE RADEX OUTPUT : COLLISIONS-->

   <!-- collisional transitions -->
   <!-- MESSAGE -->
   <xsl:message># Collisions </xsl:message>
   <xsl:message><xsl:value-of select="count($collisions/*)"/></xsl:message>

   <!-- only print collisional data if it exists -->
   <xsl:if test="count($collisions/*)>0">

     <xsl:variable name="col_partners">
       <xsl:copy-of select="$collisions/*[1]/xsams03:Reactant"/>
     </xsl:variable>
 
     <xsl:variable name="col_temps">
       <xsl:for-each select="$collisions/*[1]">
         <xsl:value-of select="xsams03:DataSets/xsams03:DataSet[@dataDescription='rateCoefficient']/xsams03:TabulatedData/xsams03:X[@units='K']/xsams03:DataList"/>
       </xsl:for-each>
     </xsl:variable>
 
     <!-- calculate the number of temperatures. The information is taken from the first collisional transition.
        As the info is given as a list separated by spaces, some transformation is needed -->        
     <xsl:variable name="num_col_temps">
       <xsl:choose>
         <xsl:when test="count($collisions/*)>0">
           <xsl:call-template name="output-tokens">
             <xsl:with-param name="list">
               <xsl:value-of select="concat('0#',$collisions/*[1]/xsams03:DataSets/xsams03:DataSet[@dataDescription='rateCoefficient']/xsams03:TabulatedData/xsams03:X[@units='K']/xsams03:DataList)" />
             </xsl:with-param>
           </xsl:call-template>
         </xsl:when>
         <xsl:otherwise>
           <xsl:text>0</xsl:text>
         </xsl:otherwise>
       </xsl:choose>
     </xsl:variable>

     <xsl:call-template name="radexoutput-collision-header" >
       <xsl:with-param name="num_col_partners" select="count($col_partners/*)"/> <!--collisions/*[1]/xsams03:Reactant)"/>-->
       <xsl:with-param name="partners" select="$col_partners/*"/>
       <xsl:with-param name="comments" select="$collisions/*[1]/xsams03:Comments"/>
       <xsl:with-param name="num_col_trans" select="count($collisions/*)"/>
       <xsl:with-param name="num_col_temps" select="$num_col_temps"/>
       <xsl:with-param name="col_temps" select="$col_temps"/>
     </xsl:call-template>

     <xsl:apply-templates select="$collisions/*">
       <xsl:with-param name="speciesid" select="$species1"/>
     </xsl:apply-templates>

   </xsl:if>


  </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- TEMPLATES FOR RADEX - OUTPUT -->

  <xsl:template name="radexoutput-molecule">
    <xsl:param name="molecule"/>
    <xsl:text>!MOLECULE&#xa;</xsl:text>
    <xsl:value-of select="$molecule/xsams03:Molecule/xsams03:MolecularChemicalSpecies/xsams03:StoichiometricFormula"/>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!MOLECULAR WEIGHT&#xa;</xsl:text>
    <xsl:value-of select="$molecule/xsams03:Molecule/xsams03:MolecularChemicalSpecies/xsams03:StableMolecularProperties/xsams03:MolecularWeight/xsams03:Value"/>
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!NUMBER OF ENERGY LEVELS&#xa;</xsl:text>
    <xsl:value-of select = "count($molecule/xsams03:Molecule/xsams03:MolecularState)" /> 
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!LEVEL + ENERGIES(cm^-1) + WEIGHT + J&#xa;</xsl:text>
        <xsl:apply-templates select="$molecule/xsams03:Molecule/xsams03:MolecularState"/>

  </xsl:template>


  <xsl:template match="xsams03:MolecularState">
     <xsl:value-of select="position()"/>
     <xsl:text>    </xsl:text>
<!--     <xsl:value-of select="substring-after(@stateID,'-')"/>
     <xsl:text>    </xsl:text>-->
     <xsl:value-of select="format-number(xsams03:MolecularStateCharacterisation/xsams03:StateEnergy/xsams03:Value,'000000000000.00000000 ')"/>
     <xsl:text>    </xsl:text>
     <xsl:value-of select="format-number(xsams03:MolecularStateCharacterisation/xsams03:TotalStatisticalWeight,' 0000', 'example')"/>
     <xsl:text>&#xa;</xsl:text>
  </xsl:template>

  <xsl:template name="radexoutput-radiative-header">
    <xsl:param name="num_transitions"/>
       
    <xsl:text>!NUMBER OF RADIATIVE TRANSITIONS&#xa;</xsl:text>
    <xsl:value-of select="$num_transitions"/>
    <xsl:text>&#xa;</xsl:text>

    <xsl:text>!TRANS + UP + LOW + EINSTEINA(s^-1) + FREQ(GHz) + E_u(K)</xsl:text>
    <xsl:text>&#xa;</xsl:text>
  </xsl:template>

  <xsl:template name="radexoutput-radiative" match="xsams03:RadiativeTransition">
       <xsl:param name="position_map"/>
       <xsl:variable name="upperstate"><xsl:value-of select="xsams03:UpperStateRef"/></xsl:variable>
       <xsl:variable name="lowerstate"><xsl:value-of select="xsams03:LowerStateRef"/></xsl:variable>

       <xsl:value-of select="position()"/>
       <xsl:text>  </xsl:text>
       <xsl:value-of select="$position_map/*[@id=$upperstate]"/>
       <xsl:text>  </xsl:text>
<!--       <xsl:value-of select="substring-after(xsams03:UpperStateRef,'-')"/>
       <xsl:text>  </xsl:text>-->
       <xsl:value-of select="$position_map/*[@id=$lowerstate]"/>
       <xsl:text>  </xsl:text>
<!--       <xsl:value-of select="substring-after(xsams03:LowerStateRef,'-')"/>
       <xsl:text>  </xsl:text>-->
       <xsl:value-of select="format-number(xsams03:Probability/xsams03:TransitionProbabilityA/xsams03:Value,'0.0000000000 ')"/>
       <xsl:text>  </xsl:text>
       <xsl:value-of select="format-number(xsams03:EnergyWavelength/xsams03:Frequency/xsams03:Value * 0.001,'000000000.0000 ')"/>
       <xsl:text>  </xsl:text>
       <xsl:value-of select="format-number(1.43877506* key('molstate',xsams03:UpperStateRef)/xsams03:MolecularStateCharacterisation/xsams03:StateEnergy/xsams03:Value,'.0000')"/>
       <xsl:text>&#xa;</xsl:text>

  </xsl:template>
  
  <xsl:template name="radexoutput-collision-header" >        
    <xsl:param name="num_col_partners"/>
    <xsl:param name="partners"/>
    <xsl:param name="comments"/>
    <xsl:param name="num_col_trans"/>
    <xsl:param name="num_col_temps"/>
    <xsl:param name="col_temps"/>

    <xsl:text>!NUMBER OF COLL PARTNERS</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:value-of select="$num_col_partners"/>
    <xsl:text>&#xa;</xsl:text>

    <xsl:text>!COLLISIONS BETWEEN</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:for-each select="$partners/xsams03:SpeciesRef">
      <xsl:value-of select="."/>
      <xsl:text>   </xsl:text>
    </xsl:for-each>
    <xsl:value-of select="$comments"/>
    <xsl:text>&#xa;</xsl:text>
<!--    <xsl:text>  </xsl:text>
    <xsl:value-of select="$partner2"/>
    <xsl:text>&#xa;</xsl:text>-->

    <xsl:text>!NUMBER OF COLL TRANS</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:value-of select="$num_col_trans"/>
    <xsl:text>&#xa;</xsl:text>

    <xsl:text>!NUMBER OF COLL TEMPS</xsl:text>
    <xsl:text>&#xa;</xsl:text>
    <xsl:value-of select="$num_col_temps"/>
    
    <xsl:text>&#xa;</xsl:text>
    <xsl:text>!COLL TEMPS</xsl:text>
    <xsl:text>&#xa;</xsl:text>

    <xsl:if test="$col_temps">
    <xsl:for-each select="$col_temps">
      <xsl:value-of select="."/>
      <xsl:text>&#xa;</xsl:text>
    </xsl:for-each>
    </xsl:if>

    <xsl:text>!TRANS+ UP+ LOW+ COLLRATES(cm^3 s^-1)</xsl:text>
    <xsl:text>&#xa;</xsl:text>
  </xsl:template>

  <xsl:template name="radexoutput-collision" match="xsams03:CollisionalTransition"> 
      <xsl:param name="speciesid"/>       
      <xsl:value-of select="position()"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="xsams03:Reactant[xsams03:SpeciesRef=$speciesid]/xsams03:StateRef"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="xsams03:Product[xsams03:SpeciesRef=$speciesid]/xsams03:StateRef"/>
      <xsl:text>  </xsl:text>
      <xsl:value-of select="xsams03:DataSets/xsams03:DataSet[@dataDescription='rateCoefficient']/xsams03:TabulatedData/xsams03:Y[@units='cm3/s']/xsams03:DataList"/>
      <xsl:text>&#xa;</xsl:text>
  </xsl:template>


<!-- TEMPLATES TO REMATCH STATES -->

  <xsl:template name="generate_statepos">        
    <xsl:param name="states"/>
    <xsl:for-each select="$states">      
      <xsl:element name="pos">
        <xsl:attribute name="id"><xsl:value-of select="@stateID"/></xsl:attribute>
        <xsl:value-of select="position()"/>
      </xsl:element>     
    </xsl:for-each>
  </xsl:template>


<xsl:template name="replace_stateid">
   <xsl:param name="id"/>
   <xsl:param name="states"/>
   <xsl:value-of select="$states[which=$id]/by"/>
</xsl:template>



<xsl:template name="merge-states">
   <xsl:param name="states_return" />
   <xsl:param name="states_rest" />
   <xsl:choose>
     <xsl:when test="count($states_rest)>0">

       <xsl:variable name="state">
          <xsl:copy-of select="$states_rest[1]" />
       </xsl:variable>

       <!-- get state id of state in list of returned states; '!' if not found -->
       <xsl:variable name="stateid">
         <xsl:call-template name="find-state">
            <xsl:with-param name="states" select="$states_return" />
            <xsl:with-param name="state2find" select="$states_rest[1]" />
         </xsl:call-template>
       </xsl:variable>
       <xsl:choose>
         <xsl:when test="$stateid ='!'">
           <!-- add the state to the list of states to be shown in the result and continue -->
<!--            <xsl:message><xsl:value-of select="$diff-states"/></xsl:message> -->
            <xsl:call-template name="merge-states">
              <xsl:with-param name="states_return" select="$states_return | $states_rest[1]" />
              <xsl:with-param name="states_rest" select="$states_rest[position()>1]" />
            </xsl:call-template>
         </xsl:when>
         <xsl:otherwise>
           <!-- do not add the state to the list of states to be shown in the result and continue -->
           <replacestate>
                <which><xsl:value-of select="$states_rest[1]/@stateID"/></which>
                <by><xsl:value-of select="$stateid"/></by>
           </replacestate>
            <xsl:call-template name="merge-states">
              <xsl:with-param name="states_return" select="$states_return" />
              <xsl:with-param name="states_rest" select="$states_rest[position()>1]" />
            </xsl:call-template>
            
         </xsl:otherwise>
       </xsl:choose>
     </xsl:when>
     <xsl:otherwise>
<!-- <states> -->
        <xsl:for-each select="$states_return">
	  <xsl:copy-of select="."/>
<!-- <xsl:message> merges states <xsl:value-of select="@stateID"/> </xsl:message> -->
        </xsl:for-each>
<!--</states> -->
     </xsl:otherwise>
   </xsl:choose>

</xsl:template>


<!-- find a state in a list of states
   return the stateID of the state which matches first
   return '!' if no state matches
-->
<xsl:template name="find-state">
   <xsl:param name="states" />
   <xsl:param name="state2find" />
   <xsl:choose>
      <xsl:when test="count($states)>0">
        <xsl:variable name="diff_state">
          <xsl:call-template name="compare-states">
            <xsl:with-param name="state1" select="$state2find" />
            <xsl:with-param name="state2" select="$states[1]" />
          </xsl:call-template>
        </xsl:variable>
        <xsl:choose>
          <xsl:when test="$diff_state='='"><xsl:value-of select="$states[1]/@stateID"/></xsl:when>
          <xsl:otherwise><xsl:call-template name="find-state">
              <xsl:with-param name="states" select="$states[position()>1]" />
              <xsl:with-param name="state2find" select="$state2find" />
            </xsl:call-template></xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>!</xsl:otherwise>
   </xsl:choose>
</xsl:template>


<xsl:template name="compare-mols">
  <xsl:param name="mol1" />
  <xsl:param name="mol2" />
  <xsl:choose>
  <xsl:when test="$mol1/xsams03:MolecularChemicalSpecies/xsams03:InChIKey = $mol2/xsams03:MolecularChemicalSpecies/xsams03:InChIKey">=</xsl:when>
  <xsl:otherwise>!</xsl:otherwise>
  </xsl:choose>
</xsl:template>


<xsl:template name="compare-states">
  <xsl:param name="state1" />
  <xsl:param name="state2" />
   <!-- Check if qn of state1 is in qns of state2 -->
   <xsl:variable name="diff-qns">
     <xsl:call-template name="is_qns1_in_qns2">
       <xsl:with-param name="qns1" select="$state1/xsams03:Case/*/*" />
       <xsl:with-param name="qns2" select="$state2/xsams03:Case/*/*" />
     </xsl:call-template>
   </xsl:variable>
  
   <xsl:value-of select="$diff-qns"/>
   
</xsl:template>

<xsl:template name="is_qns1_in_qns2">
  <xsl:param name="qns1" />
  <xsl:param name="qns2" />
  <xsl:variable name="qns1_first" select="$qns1[1]"/>
  <xsl:variable name="qns1_rest" select="$qns1[position()!=1]"/>

  <!-- Check if qn of state1 is in qns of state2 -->
  <xsl:variable name="diff-qns">
    <xsl:for-each select="$qns2">
      <xsl:call-template name="compare-qn">
        <xsl:with-param name="qn1" select="$qns1_first" />
        <xsl:with-param name="qn2" select="." />
      </xsl:call-template>
    </xsl:for-each>
  </xsl:variable>

  <xsl:choose>
    <xsl:when test="contains($diff-qns,'=')"> 
      <xsl:choose> 
        <xsl:when test="count($qns1_rest)=0">=</xsl:when>
        <xsl:otherwise>
          <xsl:call-template name="is_qns1_in_qns2">
            <xsl:with-param name="qns1" select="$qns1_rest" />
            <xsl:with-param name="qns2" select="$qns2" />
          </xsl:call-template>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>!</xsl:otherwise>
  </xsl:choose> 
</xsl:template>


<xsl:template name="compare-qn">
  <xsl:param name="qn1" />
  <xsl:param name="qn2" />
  <xsl:choose>
    <xsl:when test="name($qn1) = name($qn2)"> 
      <xsl:choose> 
        <xsl:when test="$qn1=$qn2">=</xsl:when>
        <xsl:otherwise>!</xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>!</xsl:otherwise>
  </xsl:choose> 
</xsl:template>



 <!-- OTHER - TEMPLATES (HELPER FUNCTIONS) -->
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