<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output encoding="UTF-8" method="xml" version="1.0"
		indent="yes" />

	<xsl:template match="/">
		<XSAMSData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			xsi:noNamespaceSchemaLocation="http://www-amdis.iaea.org/xsams/schema/xsams-0.1.xsd">

			<Sources>
				<xsl:apply-templates select="vald/refs" />
			</Sources>

			<Methods>
				<Method methodID="M1">
					<Category>measured</Category>
					<Description></Description>
				</Method>
			</Methods>

			<xsl:apply-templates select="vald/data" />


		</XSAMSData>
	</xsl:template>


	<xsl:template match="vald/data">
		<xsl:for-each select="transition">
		  <xsl:value-of select="ion" />
		  <xsl:value-of select="atomic" />
		  <xsl:value-of select="wavel" />
		</xsl:for-each>
	</xsl:template>


	<xsl:template match="refs">
		<Source sourceID="S1">
			<Authors>
				<Author>
					<Name>Testname</Name>
				</Author>
			</Authors>
			<Category>journal</Category>
			<Year>2002</Year>
			<SourceName>sone journal</SourceName>
			<Volume>666</Volume>
			<PageBegin>1337</PageBegin>
		</Source>
	</xsl:template>

	<xsl:template match="bla">
	</xsl:template>
</xsl:stylesheet> 
