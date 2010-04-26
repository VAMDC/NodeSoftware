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
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" xmlns:VOT="http://www.ivoa.net/xml/VOTable/v1.1">
	<xsl:output method="xml" encoding="UTF-8" media-type="application/xhtml+xml" indent="no" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" omit-xml-declaration="no"/>
	<xsl:template match="/">
		<html>
			<head>
				<meta content="Created by VOTable2XHTML 2.0 (China-VO)"/>
				<title>VOTable</title>
				<style type="text/css">
					<!--
# Change the display style to what you want here
-->
					<xsl:comment>

.databody {COLOR: #000000; FONT-FAMILY: arial,verdana,helvetica,sans-serif; FONT-SIZE: 10pt}
.header {COLOR: #000000; FONT-FAMILY: arial,verdana,helvetica,sans-serif; FONT-SIZE: 10pt;FONT-WEIGHT: bold}
.groupHeader {COLOR: #0000ff; FONT-FAMILY: arial,verdana,helvetica,sans-serif; FONT-SIZE: 10pt;FONT-WEIGHT: bold}
.topHeader {COLOR: #000000 FONT-FAMILY: arial,verdana,helvetica,sans-serif; FONT-SIZE: 12pt;FONT-WEIGHT: bold}
.comments {COLOR: #000000; FONT-FAMILY: arial,verdana,helvetica,sans-serif; FONT-SIZE: 10pt}
</xsl:comment>
				</style>
			</head>
			<body>
				<xsl:for-each select="/*">
					<!-- When there is no namespace (xmlns) designed to the VOTable file, "noschema" template will be used, otherwise, "withschema" will be used -->
					<xsl:choose>
						<xsl:when test="namespace-uri()">
							<xsl:call-template name="withschema"/>
						</xsl:when>
						<xsl:otherwise>
							<xsl:call-template name="noschema"/>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
			</body>
		</html>
	</xsl:template>
	<!-- Transformation template for VOTable file without (xmlns) namespace -->
	<xsl:template name="noschema">
		<xsl:for-each select="/VOTABLE">
			<xsl:call-template name="data_import"/>
		</xsl:for-each>
	</xsl:template>
	<!-- Core part for format transformation -->
	<xsl:template name="data_import">
		<!-- Transformation for each TABLE -->
		<xsl:for-each select="//TABLE">
			<xsl:call-template name="Ctable"/>
		</xsl:for-each>
	</xsl:template>
	<!-- "TABLEDATA" level transformation -->
	<xsl:template name="Ctable">
		<xsl:if test="//DATA/TABLEDATA">
			<xsl:call-template name="Ctabledata"/>
		</xsl:if>
		<xsl:if test=".//FIELD">
			<xsl:call-template name="Ctablefield"/>
		</xsl:if>
	</xsl:template>
	<xsl:template name="Ctabledata">
		<p class="topHeader">Table Data:
		</p>
		<table border="1">
			<tr align="center">
				<xsl:for-each select=".//FIELD">
					<xsl:choose>
						<xsl:when test="@name">
							<th class="header" align="center">
								<xsl:value-of select="@name"/>
							</th>
						</xsl:when>
						<xsl:otherwise>
							<th class="header" align="center">
								<xsl:value-of select="@ID"/>
							</th>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
			</tr>
			<tr align="center">
				<xsl:for-each select=".//FIELD">
					<td class="databody" align="center">
						<xsl:value-of select="@unit"/>
					</td>
				</xsl:for-each>
			</tr>
			<xsl:for-each select="..//DATA">
				<xsl:for-each select="TABLEDATA">
					<xsl:for-each select="TR">
						<tr>
							<xsl:for-each select=".//TD">
								<td class="databody">
									<xsl:value-of select="."/>
								</td>
							</xsl:for-each>
						</tr>
					</xsl:for-each>
				</xsl:for-each>
			</xsl:for-each>
		</table>
	</xsl:template>
	<xsl:template name="Ctablefield">
		<p class="topHeader">Table Fields:
		</p>
		<table border="1">
			<tr align="center">
				<th class="header">
						ID
					</th>
				<th class="header">
						name
					</th>
				<th class="header">
						datatype
					</th>
				<th class="header">
						unit
					</th>
				<th class="header">
						precision
					</th>
				<th class="header">
						width
					</th>
				<th class="header">
						ref
					</th>
				<th class="header">
						ucd
					</th>
				<th class="header">
						utype
					</th>
				<th class="header">
						arraysize
					</th>
				<th class="header">
						type
					</th>
				<th class="header">
						Description
					</th>
				<th class="header">
						Link
					</th>
			</tr>
			<xsl:for-each select="FIELD">
				<tr>
					<td class="databody">
						<xsl:value-of select="@ID"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@name"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@datatype"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@unit"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@precision"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@width"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@ref"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@ucd"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@utype"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@arraysize"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@type"/>
					</td>
					<td class="databody">
						<xsl:value-of select="DESCRIPTION"/>
					</td>
					<td class="databody">
						<xsl:for-each select="LINK">
							<xsl:variable name="flink">
								<xsl:value-of select="@href"/>
							</xsl:variable>
							<a href="{$flink}">
								<xsl:value-of select="$flink"/>
							</a>
						</xsl:for-each>
					</td>
				</tr>
			</xsl:for-each>
		</table>
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
			<xsl:call-template name="vot_Ctablefield"/>
		</xsl:if>
	</xsl:template>
	<xsl:template name="vot_Ctabledata">
		<p class="topHeader">Table Data:
		</p>
		<table border="1">
			<tr align="center">
				<xsl:for-each select=".//VOT:FIELD">
					<xsl:choose>
						<xsl:when test="@name">
							<th class="header" align="center">
								<xsl:value-of select="@name"/>
							</th>
						</xsl:when>
						<xsl:otherwise>
							<th class="header" align="center">
								<xsl:value-of select="@ID"/>
							</th>
						</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
			</tr>
			<tr align="center">
				<xsl:for-each select=".//VOT:FIELD">
					<td class="databody" align="center">
						<xsl:value-of select="@unit"/>
					</td>
				</xsl:for-each>
			</tr>
			<xsl:for-each select="..//VOT:DATA">
				<xsl:for-each select="VOT:TABLEDATA">
					<xsl:for-each select="VOT:TR">
						<tr>
							<xsl:for-each select=".//VOT:TD">
								<td class="databody">
									<xsl:value-of select="."/>
								</td>
							</xsl:for-each>
						</tr>
					</xsl:for-each>
				</xsl:for-each>
			</xsl:for-each>
		</table>
	</xsl:template>
	<xsl:template name="vot_Ctablefield">
		<p class="topHeader">Table Fields:
		</p>
		<table border="1">
			<tr align="center">
				<th class="header">
						ID
					</th>
				<th class="header">
						name
					</th>
				<th class="header">
						datatype
					</th>
				<th class="header">
						unit
					</th>
				<th class="header">
						precision
					</th>
				<th class="header">
						width
					</th>
				<th class="header">
						ref
					</th>
				<th class="header">
						ucd
					</th>
				<th class="header">
						utype
					</th>
				<th class="header">
						arraysize
					</th>
				<th class="header">
						type
					</th>
				<th class="header">
						Description
					</th>
				<th class="header">
						Link
					</th>
			</tr>
			<xsl:for-each select="VOT:FIELD">
				<tr>
					<td class="databody">
						<xsl:value-of select="@ID"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@name"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@datatype"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@unit"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@precision"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@width"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@ref"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@ucd"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@utype"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@arraysize"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@type"/>
					</td>
					<td class="databody">
						<xsl:value-of select="VOT:DESCRIPTION"/>
					</td>
					<td class="databody">
						<xsl:for-each select="VOT:LINK">
							<xsl:variable name="flink">
								<xsl:value-of select="@href"/>
							</xsl:variable>
							<a href="{$flink}">
								<xsl:value-of select="$flink"/>
							</a>
						</xsl:for-each>
					</td>
				</tr>
			</xsl:for-each>
		</table>
	</xsl:template>
</xsl:stylesheet>
