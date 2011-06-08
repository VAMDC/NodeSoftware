<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	version="1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:cap="http://www.ivoa.net/xml/VOSICapabilities/v1.0" xmlns:vr="http://www.ivoa.net/xml/VOResource/v1.0">

	<xsl:template match="/cap:capabilities">
		<html>
			<head>
				<title>Service capabilities</title>
			</head>
			<body>
				<h1>Service capabilities</h1>
				<xsl:apply-templates />
			</body>
		</html>
	</xsl:template>

	<xsl:template match="capability">
		<h2>
			<xsl:value-of select="@standardID" />
		</h2>
		<xsl:apply-templates />
	</xsl:template>

	<xsl:template match="versionOfStandards">
		<p><xsl:text>Version of VAMDC standards: </xsl:text><xsl:value-of select="."/></p>
	</xsl:template>

	<xsl:template match="versionOfSoftware">
		<p><xsl:text>Version of Node Software: </xsl:text><xsl:value-of select="."/></p>
	</xsl:template>

	<xsl:template match="sampleQuery">
		<p><xsl:text>Sample query: </xsl:text><xsl:value-of select="."/></p>
	</xsl:template>

	<xsl:template match="returnable">
		<p>
			Returnable
			<xsl:value-of select="." />
		</p>
	</xsl:template>

	<xsl:template match="restrictable">
		<p>
			Restrictable
			<xsl:value-of select="." />
		</p>

	</xsl:template>

	<xsl:template match="interface">
		<h3>Interface</h3>
		<dl>
			<dt>Type</dt>
			<dd>
				<xsl:value-of select="@xsi:type" />
			</dd>
			<dt>Version</dt>
			<dd>
				<xsl:value-of select="@version" />
			</dd>
			<dt>Role</dt>
			<dd>
				<xsl:value-of select="@role" />
			</dd>
			<xsl:for-each select="accessURL">
				<dt>Access URL</dt>
				<dd>
					<xsl:value-of select="." />
				</dd>
			</xsl:for-each>
			<xsl:for-each select="securityMethod">
				<dt>Access URL</dt>
				<dd>
					<xsl:value-of select="." />
				</dd>
			</xsl:for-each>
			<xsl:for-each select="wsdlURL">
				<dt>Access URL</dt>
				<dd>
					<xsl:value-of select="." />
				</dd>
			</xsl:for-each>
			<dt>HTTP verb</dt>
			<dd>
				<xsl:value-of select="queryType" />
			</dd>
			<dt>MIME type of HTTP response</dt>
			<dd>
				<xsl:value-of select="resultType" />
			</dd>
		</dl>
	</xsl:template>

	<xsl:template match="managedApplications">
		<h3>Applications</h3>
		<ul>
			<xsl:for-each select="ApplicationReference">
				<li>
					<xsl:value-of select="." />
				</li>
			</xsl:for-each>
		</ul>
	</xsl:template>
</xsl:stylesheet>
