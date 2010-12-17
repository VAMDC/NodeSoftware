<?xml version="1.0" encoding="UTF-8" ?>
<!--
# VOTable2XHTML
# Version: 1.0
# Author: Jian SANG (China-VO)
# Date: June, 2004
#
# VOTable2XHTML
# Version: 2.0
# Description: An XSLT converter to transform VOTable file to XHTML file
# Updated by: Chenzhou CUI (ccz@bao.ac.cn)
# Last Modified: September, 2005
#
# Changelog:
# 	2.0 (2005-09-16)
#		Support for VOTable with schema designed
#		Much more information displayed including "GROUP" element
#
-->
<!--
	For further documentation and updates visit http://services.china-vo.org/votable2xhtml/
	-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" xmlns:VOT="http://www.ivoa.net/xml/VOTable/v1.2">
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
.topHeader {COLOR: #000000; FONT-FAMILY: Arial Black,verdana,helvetica,sans-serif; FONT-SIZE: 12pt}
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
		<!-- Transformation for each RESOURCE -->
		<xsl:for-each select="//RESOURCE">
			<xsl:call-template name="Cresource"/>
		</xsl:for-each>
		<!-- Transformation for the root VOTABLE -->
		<xsl:for-each select="/VOTABLE">
			<xsl:call-template name="VOTABLE"/>
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
		<xsl:if test=".//PARAM">
			<xsl:call-template name="Ctableparam"/>
		</xsl:if>
		<xsl:if test=".//GROUP">
			<xsl:call-template name="Ctablegroup"/>
		</xsl:if>
		<xsl:call-template name="Ctableother"/>
	</xsl:template>
	<xsl:template name="Ctabledata">
		<p class="topHeader">Data in Table:
		<xsl:call-template name="table_name">
			</xsl:call-template>
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
		<p class="topHeader">Fields in Table:
					<xsl:call-template name="table_name">
			</xsl:call-template>
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
	<xsl:template name="Ctablegroup">
		<p class="topHeader">Groups Defined in Table: 
			<xsl:call-template name="table_name">
			</xsl:call-template>
		</p>
		<table border="1">
			<xsl:for-each select="GROUP">
				<tr>
					<xsl:choose>
						<xsl:when test="@ID">
							<td class="groupHeader">
								Group Name
							</td>
							<td class="databody">
								<xsl:value-of select="@ID"/>
							</td>
						</xsl:when>
						<xsl:otherwise>
							<td class="groupHeader">
								Group Name
							</td>
							<td class="databody">
								<xsl:value-of select="@name"/>
							</td>
						</xsl:otherwise>
					</xsl:choose>
				</tr>
				<xsl:if test="./FIELDref">
					<tr>
						<td class="header">
							FIELDref
						</td>
						<xsl:for-each select="FIELDref">
							<td class="databody">
								<xsl:value-of select="@ref"/>
							</td>
						</xsl:for-each>
					</tr>
				</xsl:if>
				<xsl:if test="./PARAMref">
					<tr>
						<td class="header">
							PARAMref
						</td>
						<xsl:for-each select="PARAMref">
							<td class="databody">
								<xsl:value-of select="@ref"/>
							</td>
						</xsl:for-each>
					</tr>
				</xsl:if>
				<tr>
					<td class="header">
						Attributes
					</td>
					<td class="databody">
						ID
					</td>
					<td class="databody">
						name
					</td>
					<td class="databody">
						ref
					</td>
					<td class="databody">
						ucd
					</td>
					<td class="databody">
						utype
					</td>
					<td class="databody">
						Description
					</td>
				</tr>
				<tr>
					<td/>
					<td class="databody">
						<xsl:value-of select="@ID"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@name"/>
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
						<xsl:value-of select="DESCRIPTION"/>
					</td>
				</tr>
				<xsl:if test="./PARAM">
					<tr>
						<td class="header">
							PARAMETERS
						</td>
					</tr>
					<xsl:call-template name="PARAMETERS"/>
				</xsl:if>
				<tr></tr>
			</xsl:for-each>
		</table>
	</xsl:template>
	<xsl:template name="Ctableparam">
		<p class="topHeader">Parameters for Table: <xsl:call-template name="table_name">
			</xsl:call-template>
		</p>
		<xsl:if test="PARAM">
			<table border="1">
				<xsl:call-template name="PARAMETERS"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="Ctableother">
		<xsl:if test="(@*|DESCRIPTION|LINK)">
			<p class="topHeader">Other Metadata for Table: <xsl:call-template name="table_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:if test="@*">
					<tr>
						<td class="header">
							Attributes
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							name
						</td>
						<td class="databody">
							ref
						</td>
						<td class="databody">
							ucd
						</td>
						<td class="databody">
							utype
						</td>
						<td class="databody">
							nrows
						</td>
					</tr>
					<tr>
						<td/>
						<td class="databody">
							<xsl:value-of select="@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@name"/>
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
							<xsl:value-of select="@nrows"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="DESCRIPTION">
					<tr>
						<td class="header">
							Description
						</td>
						<td class="databody">
							<xsl:value-of select="DESCRIPTION"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:for-each select="LINK">
					<tr>
						<td class="databody">
							Link
						
						</td>
						<tr>
							<td/>
							<td class="databody">
								<xsl:variable name="flink">
									<xsl:value-of select="@href"/>
								</xsl:variable>
								<a href="{$flink}">
									<xsl:value-of select="$flink"/>
								</a>
							</td>
						</tr>
					</tr>
				</xsl:for-each>
			</table>
		</xsl:if>
	</xsl:template>
	<!-- "RESOURCE" level transformation -->
	<xsl:template name="Cresource">
		<xsl:call-template name="Cresourceparam"/>
		<xsl:call-template name="Cresourceinfo"/>
		<xsl:call-template name="Cresourceother"/>
	</xsl:template>
	<xsl:template name="Cresourceparam">
		<xsl:if test="PARAM">
			<p class="topHeader">Parameters for Resource: 	<xsl:call-template name="RES_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="PARAMETERS"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="Cresourceinfo">
		<xsl:if test="INFO">
			<p class="topHeader">Information for Resource:<xsl:call-template name="RES_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="INFORMATION"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="Cresourceother">
		<xsl:if test="(@*|DESCRIPTION|COOSYS|LINK)">
			<p class="topHeader">Other Metadata for Resource: 		<xsl:call-template name="RES_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:if test="@*">
					<tr>
						<td class="header">
							Attributes
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							name
						</td>
						<td class="databody">
							utype
						</td>
						<td class="databody">
							type
						</td>
					</tr>
					<tr>
						<td/>
						<td class="databody">
							<xsl:value-of select="@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@name"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@utype"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@type"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="DESCRIPTION">
					<tr>
						<td class="header">
							Description
						</td>
						<td class="databody">
							<xsl:value-of select="DESCRIPTION"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="COOSYS">
					<tr>
						<td class="header">
							Coordinates System
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							equinox
						</td>
						<td class="databody">
							epoch
						</td>
						<td class="databody">
							system
						</td>
					</tr>
					<tr>
						<td class="databody">
							<p/>
						</td>
						<td class="databody">
							<xsl:value-of select="COOSYS/@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="COOSYS/@equinox"/>
						</td>
						<td class="databody">
							<xsl:value-of select="COOSYS/@epoch"/>
						</td>
						<td class="databody">
							<xsl:value-of select="COOSYS/@system"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:for-each select="LINK">
					<tr>
						<td class="header">
							Link
						
						</td>
						<tr>
							<td/>
							<td class="databody">
								<xsl:variable name="flink">
									<xsl:value-of select="@href"/>
								</xsl:variable>
								<a href="{$flink}">
									<xsl:value-of select="$flink"/>
								</a>
							</td>
						</tr>
					</tr>
				</xsl:for-each>
			</table>
		</xsl:if>
	</xsl:template>
	<!-- "VOTABLE" or ROOT level transformation -->
	<xsl:template name="VOTABLE">
		<xsl:call-template name="VOTABLEparam"/>
		<xsl:call-template name="VOTABLEinfo"/>
		<xsl:call-template name="VOTABLEother"/>
	</xsl:template>
	<xsl:template name="VOTABLEparam">
		<xsl:if test="PARAM">
			<p class="topHeader">Parameters for VOTable: 		<xsl:call-template name="final_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="PARAMETERS"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="VOTABLEinfo">
		<xsl:if test="INFO">
			<p class="topHeader">Information for VOTable: 	<xsl:call-template name="final_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="INFORMATION"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="VOTABLEother">
		<xsl:if test="(/VOTABLE[@ID]|/VOTABLE[@version]|/VOTABLE/DESCRIPTION|/VOTABLE/COOSYS|/VOTABLE/DEFINITIONS)">
			<p class="topHeader">Other Metadata for VOTable: 			<xsl:call-template name="final_name">

				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:if test="/VOTABLE[@ID]">
					<tr>
						<td class="header">
							Document ID
						</td>
						<td class="databody">
							<xsl:value-of select="/VOTABLE/@ID"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="/VOTABLE[@version]">
					<tr>
						<td class="header">
							Version
						</td>
						<td class="databody">
							<xsl:value-of select="/VOTABLE/@version"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="/VOTABLE/DESCRIPTION">
					<tr>
						<td class="header">
							Description
						</td>
						<td class="databody">
							<xsl:value-of select="/VOTABLE/DESCRIPTION"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="/VOTABLE/COOSYS">
					<tr>
						<td class="header">
							Coordinates System
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							equinox
						</td>
						<td class="databody">
							epoch
						</td>
						<td class="databody">
							system
						</td>
					</tr>
					<tr>
						<td class="databody">
							<p/>
						</td>
						<td class="databody">
							<xsl:value-of select="@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@equinox"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@epoch"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@system"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:for-each select="/VOTABLE/DEFINITIONS">
					<xsl:for-each select="COOSYS">
						<tr>
							<td class="header">
								Definition: Coordinates System
							</td>
							<td class="databody">
								ID
							</td>
							<td class="databody">
								equinox
							</td>
							<td class="databody">
								epoch
							</td>
							<td class="databody">
								system
							</td>
						</tr>
						<tr>
							<td class="databody">
								<p/>
							</td>
							<td class="databody">
								<xsl:value-of select="@ID"/>
							</td>
							<td class="databody">
								<xsl:value-of select="@equinox"/>
							</td>
							<td class="databody">
								<xsl:value-of select="@epoch"/>
							</td>
							<td class="databody">
								<xsl:value-of select="@system"/>
							</td>
						</tr>
					</xsl:for-each>
				</xsl:for-each>
			</table>
		</xsl:if>
	</xsl:template>
	<!-- Common Module for "PARAM" elements  -->
	<xsl:template name="PARAMETERS">
		<tr>
			<th class="header">
					ID
				</th>
			<th class="header">
					name
				</th>
			<th class="header">
					value
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
					Description
				</th>
			<th class="header">
					Link
				</th>
		</tr>
		<xsl:for-each select="PARAM">
			<tr>
				<td class="databody">
					<xsl:value-of select="@ID"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@name"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@value"/>
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
	</xsl:template>
	<!-- Common Module for "INFO" elements -->
	<xsl:template name="INFORMATION">
		<tr>
			<td class="header">
					ID
				</td>
			<td class="header">
					name
				</td>
			<td class="header">
					value
				</td>
		</tr>
		<xsl:for-each select="INFO">
			<tr>
				<td class="databody">
					<xsl:value-of select="@ID"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@name"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@value"/>
				</td>
			</tr>
		</xsl:for-each>
	</xsl:template>
	<!-- Generate names for different sheets -->
	<xsl:template name="table_name">
		<xsl:choose>
			<xsl:when test="@ID">
				<xsl:variable name="TAB_ID">
					<xsl:value-of select="concat('_',@ID)"/>
				</xsl:variable>
				<xsl:call-template name="resource_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="@name">
				<xsl:variable name="TAB_ID">
					<xsl:value-of select="concat('_',@name)"/>
				</xsl:variable>
				<xsl:call-template name="resource_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="TAB_ID">
					<xsl:value-of select="concat('_',name())"/>
				</xsl:variable>
				<xsl:call-template name="resource_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="resource_name">
		<xsl:param name="TAB_ID"/>
		<xsl:choose>
			<xsl:when test="../@ID">
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',../@ID)"/>
				</xsl:variable>
				<xsl:call-template name="final_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="../@name">
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',../@name)"/>
				</xsl:variable>
				<xsl:call-template name="final_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',name(..))"/>
				</xsl:variable>
				<xsl:call-template name="final_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="RES_name">
		<xsl:choose>
			<xsl:when test="@ID">
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',@ID)"/>
				</xsl:variable>
				<xsl:call-template name="final_name">
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="@name">
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',@name)"/>
				</xsl:variable>
				<xsl:call-template name="final_name">
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',name())"/>
				</xsl:variable>
				<xsl:call-template name="final_name">
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="final_name">
		<xsl:param name="RES_ID"/>
		<xsl:param name="TAB_ID"/>
		<xsl:choose>
			<xsl:when test="/VOTABLE/@ID">
				<xsl:variable name="VOT_ID">
					<xsl:value-of select="/VOTABLE/@ID"/>
				</xsl:variable>
				<xsl:value-of select="concat($VOT_ID,$RES_ID,$TAB_ID)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="VOT_ID">
					<xsl:value-of select="string('VOTABLE')"/>
				</xsl:variable>
				<xsl:value-of select="concat($VOT_ID,$RES_ID,$TAB_ID)"/>
			</xsl:otherwise>
		</xsl:choose>
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
		<!-- Transformation for each RESOURCE -->
		<xsl:for-each select="//VOT:RESOURCE">
			<xsl:call-template name="vot_Cresource"/>
		</xsl:for-each>
		<!-- Transformation for the root VOTABLE -->
		<xsl:for-each select="/VOT:VOTABLE">
			<xsl:call-template name="vot_VOTABLE"/>
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
		<xsl:if test=".//VOT:PARAM">
			<xsl:call-template name="vot_Ctableparam"/>
		</xsl:if>
		<xsl:if test=".//VOT:GROUP">
			<xsl:call-template name="vot_Ctablegroup"/>
		</xsl:if>
		<xsl:call-template name="vot_Ctableother"/>
	</xsl:template>
	<xsl:template name="vot_Ctabledata">
		<p class="topHeader">Data in Table:
		<xsl:call-template name="vot_table_name">
			</xsl:call-template>
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
		<p class="topHeader">Fields in Table:
					<xsl:call-template name="vot_table_name">
			</xsl:call-template>
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
	<xsl:template name="vot_Ctablegroup">
		<p class="topHeader">Groups Defined in Table: 
			<xsl:call-template name="vot_table_name">
			</xsl:call-template>
		</p>
		<table border="1">
			<xsl:for-each select="VOT:GROUP">
				<tr>
					<xsl:choose>
						<xsl:when test="@ID">
							<td class="groupHeader">
								Group Name
							</td>
							<td class="databody">
								<xsl:value-of select="@ID"/>
							</td>
						</xsl:when>
						<xsl:otherwise>
							<td class="groupHeader">
								Group Name
							</td>
							<td class="databody">
								<xsl:value-of select="@name"/>
							</td>
						</xsl:otherwise>
					</xsl:choose>
				</tr>
				<xsl:if test="./VOT:FIELDref">
					<tr>
						<td class="header">
							FIELDref
						</td>
						<xsl:for-each select="VOT:FIELDref">
							<td class="databody">
								<xsl:value-of select="@ref"/>
							</td>
						</xsl:for-each>
					</tr>
				</xsl:if>
				<xsl:if test="./VOT:PARAMref">
					<tr>
						<td class="header">
							PARAMref
						</td>
						<xsl:for-each select="VOT:PARAMref">
							<td class="databody">
								<xsl:value-of select="@ref"/>
							</td>
						</xsl:for-each>
					</tr>
				</xsl:if>
				<tr>
					<td class="header">
						Attributes
					</td>
					<td class="databody">
						ID
					</td>
					<td class="databody">
						name
					</td>
					<td class="databody">
						ref
					</td>
					<td class="databody">
						ucd
					</td>
					<td class="databody">
						utype
					</td>
					<td class="databody">
						Description
					</td>
				</tr>
				<tr>
					<td/>
					<td class="databody">
						<xsl:value-of select="@ID"/>
					</td>
					<td class="databody">
						<xsl:value-of select="@name"/>
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
						<xsl:value-of select="VOT:DESCRIPTION"/>
					</td>
				</tr>
				<xsl:if test="./VOT:PARAM">
					<tr>
						<td class="header">
							PARAMETERS
						</td>
					</tr>
					<xsl:call-template name="vot_PARAMETERS"/>
				</xsl:if>
				<tr></tr>
			</xsl:for-each>
		</table>
	</xsl:template>
	<xsl:template name="vot_Ctableparam">
		<p class="topHeader">Parameters for Table: <xsl:call-template name="vot_table_name">
			</xsl:call-template>
		</p>
		<xsl:if test="VOT:PARAM">
			<table border="1">
				<xsl:call-template name="vot_PARAMETERS"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="vot_Ctableother">
		<xsl:if test="(@*|VOT:DESCRIPTION|VOT:LINK)">
			<p class="topHeader">Other Metadata for Table: <xsl:call-template name="vot_table_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:if test="@*">
					<tr>
						<td class="header">
							Attributes
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							name
						</td>
						<td class="databody">
							ref
						</td>
						<td class="databody">
							ucd
						</td>
						<td class="databody">
							utype
						</td>
						<td class="databody">
							nrows
						</td>
					</tr>
					<tr>
						<td/>
						<td class="databody">
							<xsl:value-of select="@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@name"/>
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
							<xsl:value-of select="@nrows"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="VOT:DESCRIPTION">
					<tr>
						<td class="header">
							Description
						</td>
						<td class="databody">
							<xsl:value-of select="VOT:DESCRIPTION"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:for-each select="VOT:LINK">
					<tr>
						<td class="databody">
							Link
						
						</td>
						<tr>
							<td/>
							<td class="databody">
								<xsl:variable name="flink">
									<xsl:value-of select="@href"/>
								</xsl:variable>
								<a href="{$flink}">
									<xsl:value-of select="$flink"/>
								</a>
							</td>
						</tr>
					</tr>
				</xsl:for-each>
			</table>
		</xsl:if>
	</xsl:template>
	<!-- "RESOURCE" level transformation -->
	<xsl:template name="vot_Cresource">
		<xsl:call-template name="vot_Cresourceparam"/>
		<xsl:call-template name="vot_Cresourceinfo"/>
		<xsl:call-template name="vot_Cresourceother"/>
	</xsl:template>
	<xsl:template name="vot_Cresourceparam">
		<xsl:if test="VOT:PARAM">
			<p class="topHeader">Parameters for Resource: 	<xsl:call-template name="RES_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="vot_PARAMETERS"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="vot_Cresourceinfo">
		<xsl:if test="VOT:INFO">
			<p class="topHeader">Information for Resource:<xsl:call-template name="RES_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="vot_INFORMATION"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="vot_Cresourceother">
		<xsl:if test="(@*|VOT:DESCRIPTION|VOT:COOSYS|VOT:LINK)">
			<p class="topHeader">Other Metadata for Resource: 		<xsl:call-template name="RES_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:if test="@*">
					<tr>
						<td class="header">
							Attributes
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							name
						</td>
						<td class="databody">
							utype
						</td>
						<td class="databody">
							type
						</td>
					</tr>
					<tr>
						<td/>
						<td class="databody">
							<xsl:value-of select="@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@name"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@utype"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@type"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="VOT:DESCRIPTION">
					<tr>
						<td class="header">
							Description
						</td>
						<td class="databody">
							<xsl:value-of select="VOT:DESCRIPTION"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="VOT:COOSYS">
					<tr>
						<td class="header">
							Coordinates System
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							equinox
						</td>
						<td class="databody">
							epoch
						</td>
						<td class="databody">
							system
						</td>
					</tr>
					<tr>
						<td class="databody">
							<p/>
						</td>
						<td class="databody">
							<xsl:value-of select="VOT:COOSYS/@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="VOT:COOSYS/@equinox"/>
						</td>
						<td class="databody">
							<xsl:value-of select="VOT:COOSYS/@epoch"/>
						</td>
						<td class="databody">
							<xsl:value-of select="VOT:COOSYS/@system"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:for-each select="VOT:LINK">
					<tr>
						<td class="header">
							Link
						
						</td>
						<tr>
							<td/>
							<td class="databody">
								<xsl:variable name="flink">
									<xsl:value-of select="@href"/>
								</xsl:variable>
								<a href="{$flink}">
									<xsl:value-of select="$flink"/>
								</a>
							</td>
						</tr>
					</tr>
				</xsl:for-each>
			</table>
		</xsl:if>
	</xsl:template>
	<!-- "VOTABLE" or ROOT level transformation -->
	<xsl:template name="vot_VOTABLE">
		<xsl:call-template name="vot_VOTABLEparam"/>
		<xsl:call-template name="vot_VOTABLEinfo"/>
		<xsl:call-template name="vot_VOTABLEother"/>
	</xsl:template>
	<xsl:template name="vot_VOTABLEparam">
		<xsl:if test="VOT:PARAM">
			<p class="topHeader">Parameters for VOTable: 		<xsl:call-template name="vot_final_name">
				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="vot_PARAMETERS"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="vot_VOTABLEinfo">
		<!-- There is a bug in previous version here -->
		<xsl:if test="VOT:INFO">
			<p class="topHeader">Information for VOTable:<xsl:call-template name="vot_final_name">

				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:call-template name="vot_INFORMATION"/>
			</table>
		</xsl:if>
	</xsl:template>
	<xsl:template name="vot_VOTABLEother">
		<xsl:if test="(/VOT:VOTABLE[@ID]|/VOT:VOTABLE[@version]|/VOT:VOTABLE/VOT:DESCRIPTION|/VOT:VOTABLE/VOT:COOSYS|/VOT:VOTABLE/VOT:DEFINITIONS)">
			<p class="topHeader">Other Metadata for VOTable:<xsl:call-template name="vot_final_name">

				</xsl:call-template>
			</p>
			<table border="1">
				<xsl:if test="/VOT:VOTABLE[@ID]">
					<tr>
						<td class="header">
							Document ID
						</td>
						<td class="databody">
							<xsl:value-of select="/VOT:VOTABLE/@ID"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="/VOT:VOTABLE[@version]">
					<tr>
						<td class="header">
							Version
						</td>
						<td class="databody">
							<xsl:value-of select="/VOT:VOTABLE/@version"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="/VOT:VOTABLE/VOT:DESCRIPTION">
					<tr>
						<td class="header">
							Description
						</td>
						<td class="databody">
							<xsl:value-of select="/VOT:VOTABLE/VOT:DESCRIPTION"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:if test="/VOT:VOTABLE/VOT:COOSYS">
					<tr>
						<td class="header">
							Coordinates System
						</td>
						<td class="databody">
							ID
						</td>
						<td class="databody">
							equinox
						</td>
						<td class="databody">
							epoch
						</td>
						<td class="databody">
							system
						</td>
					</tr>
					<tr>
						<td class="databody">
							<p/>
						</td>
						<td class="databody">
							<xsl:value-of select="@ID"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@equinox"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@epoch"/>
						</td>
						<td class="databody">
							<xsl:value-of select="@system"/>
						</td>
					</tr>
					<tr></tr>
				</xsl:if>
				<xsl:for-each select="/VOT:VOTABLE/VOT:DEFINITIONS">
					<xsl:for-each select="VOT:COOSYS">
						<tr>
							<td class="header">
								Definition: Coordinates System
							</td>
							<td class="databody">
								ID
							</td>
							<td class="databody">
								equinox
							</td>
							<td class="databody">
								epoch
							</td>
							<td class="databody">
								system
							</td>
						</tr>
						<tr>
							<td class="databody">
								<p/>
							</td>
							<td class="databody">
								<xsl:value-of select="@ID"/>
							</td>
							<td class="databody">
								<xsl:value-of select="@equinox"/>
							</td>
							<td class="databody">
								<xsl:value-of select="@epoch"/>
							</td>
							<td class="databody">
								<xsl:value-of select="@system"/>
							</td>
						</tr>
					</xsl:for-each>
				</xsl:for-each>
			</table>
		</xsl:if>
	</xsl:template>
	<!-- Common Module for "PARAM" elements  -->
	<xsl:template name="vot_PARAMETERS">
		<tr>
			<th class="header">
					ID
				</th>
			<th class="header">
					name
				</th>
			<th class="header">
					value
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
					Description
				</th>
			<th class="header">
					Link
				</th>
		</tr>
		<xsl:for-each select="VOT:PARAM">
			<tr>
				<td class="databody">
					<xsl:value-of select="@ID"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@name"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@value"/>
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
	</xsl:template>
	<!-- Common Module for "INFO" elements -->
	<xsl:template name="vot_INFORMATION">
		<tr>
			<td class="header">
					ID
				</td>
			<td class="header">
					name
				</td>
			<td class="header">
					value
				</td>
		</tr>
		<xsl:for-each select="VOT:INFO">
			<tr>
				<td class="databody">
					<xsl:value-of select="@ID"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@name"/>
				</td>
				<td class="databody">
					<xsl:value-of select="@value"/>
				</td>
			</tr>
		</xsl:for-each>
	</xsl:template>
	<!-- Generate names for different sheets -->
	<xsl:template name="vot_table_name">
		<xsl:choose>
			<xsl:when test="@ID">
				<xsl:variable name="TAB_ID">
					<xsl:value-of select="concat('_',@ID)"/>
				</xsl:variable>
				<xsl:call-template name="vot_resource_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="@name">
				<xsl:variable name="TAB_ID">
					<xsl:value-of select="concat('_',@name)"/>
				</xsl:variable>
				<xsl:call-template name="vot_resource_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="TAB_ID">
					<xsl:value-of select="concat('_',name())"/>
				</xsl:variable>
				<xsl:call-template name="vot_resource_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="vot_resource_name">
		<xsl:param name="TAB_ID"/>
		<xsl:choose>
			<xsl:when test="../@ID">
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',../@ID)"/>
				</xsl:variable>
				<xsl:call-template name="vot_final_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:when test="../@name">
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',../@name)"/>
				</xsl:variable>
				<xsl:call-template name="vot_final_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="RES_ID">
					<xsl:value-of select="concat('_',name(..))"/>
				</xsl:variable>
				<xsl:call-template name="vot_final_name">
					<xsl:with-param name="TAB_ID" select="$TAB_ID"/>
					<xsl:with-param name="RES_ID" select="$RES_ID"/>
				</xsl:call-template>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="vot_final_name">
		<xsl:param name="RES_ID"/>
		<xsl:param name="TAB_ID"/>
		<xsl:choose>
			<xsl:when test="/VOT:VOTABLE/@ID">
				<xsl:variable name="VOT_ID">
					<xsl:value-of select="/VOT:VOTABLE/@ID"/>
				</xsl:variable>
				<xsl:value-of select="concat($VOT_ID,$RES_ID,$TAB_ID)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="VOT_ID">
					<xsl:value-of select="string('VOTABLE')"/>
				</xsl:variable>
				<xsl:value-of select="concat($VOT_ID,$RES_ID,$TAB_ID)"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
