<?xml version="1.0" encoding="UTF-8" ?>
<!--
# VOTable2XHTML
# Version: 1.0
# Author: Jian SANG (China-VO)
# Date: June, 2004
#
# VOTable2XHTMLbasic
# Version: 2.0
# Description: An XSLT converter to transform VOTable file to XHTML file
# Updated by: Chenzhou CUI (ccz@bao.ac.cn)
# Last Modified: September 16, 2005
#
# Changelog:
# 	2.0 (2005-09-16)
#		Support for VOTable with schema designed
#		Only TABLE data and fields are extracted
#
-->
<!--
	For further documentation and updates visit http://services.china-vo.org/votable2xhtml/
	-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:VOT="http://www.ivoa.net/xml/VOTable/v1.2" omit-xml-declaration="yes" exclude-result-prefixes="VOT">
	<xsl:output method="html" encoding="UTF-8" media-type="application/html" indent="no"/>
	<xsl:template match="/">
	  <xsl:for-each select="/*">
	    <xsl:call-template name="withschema"/>
	  </xsl:for-each>
	</xsl:template>

	<xsl:template name="withschema">
		<xsl:for-each select="/VOT:VOTABLE">
			<xsl:call-template name="vot_data_import"/>
		</xsl:for-each>
	</xsl:template>
	<!-- Core part for format transformation -->
	<xsl:template name="vot_data_import">
		<!-- Transformation for each TABLE -->
		<xsl:for-each select="//VOT:TABLE">
			<xsl:call-template name="vot_Ctable"/>
		</xsl:for-each>
	</xsl:template>
	<!-- "TABLEDATA" level transformation -->
	<xsl:template name="vot_Ctable">
		<xsl:if test="//VOT:DATA/VOT:TABLEDATA">
			<xsl:call-template name="vot_Ctabledata"/>
		</xsl:if>
		<xsl:if test=".//VOT:FIELD">
		<!--	<xsl:call-template name="vot_Ctablefield"/> -->
		</xsl:if>
	</xsl:template>
	<xsl:template name="vot_Ctabledata">
		<p> <xsl:value-of select=".//VOT:DESCRIPTION"/></p>
		<table border="1">
			<tr align="center">
				<xsl:for-each select=".//VOT:FIELD">
					<xsl:choose>
						<xsl:when test="@name">
							<th align="center">
								<xsl:value-of select="@name"/>
							</th>
						</xsl:when>
						<xsl:otherwise>
							<th align="center">
								<xsl:value-of select="@ID"/>
							</th>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
			</tr>
			<tr align="center">
				<xsl:for-each select=".//VOT:FIELD">
					<td align="center">
						<xsl:value-of select="@unit"/>
					</td>
				</xsl:for-each>
			</tr>
			<xsl:for-each select="..//VOT:DATA">
				<xsl:for-each select="VOT:TABLEDATA">
					<xsl:for-each select="VOT:TR">
						<tr>
							<xsl:for-each select=".//VOT:TD">
								<td>
									<xsl:value-of select="."/>
								</td>
							</xsl:for-each>
						</tr>
					</xsl:for-each>
				</xsl:for-each>
			</xsl:for-each>
		</table>
	</xsl:template>

</xsl:stylesheet>
