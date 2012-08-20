<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsams10="http://vamdc.org/xml/xsams/1.0" xmlns:xsams03="http://vamdc.org/xml/xsams/0.3">


<xsl:include href="convertXSAMS2html_v1.0.xslt"/>  
<xsl:include href="convertXSAMS2html_v0.3.xslt"/>

<xsl:template match="/">
  <xsl:apply-templates select="xsams10:XSAMSData"/>
  <xsl:apply-templates select="xsams03:XSAMSData"/>
</xsl:template>


</xsl:stylesheet>
