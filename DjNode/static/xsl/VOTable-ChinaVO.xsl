<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >
  <xsl:output method="html"/>
  <xsl:template match="/">
    <html>
      <head/>
      <link rel="stylesheet" type="text/css" href="http://www.lamost.org/~sang/rlamost.css" title="style"/>
      <body>
        <table name="VOTable" bgcolor="#000000">
        <xsl:for-each select="VOTABLE">
          <xsl:for-each select="RESOURCE">
            <h1>Resource Name: <xsl:value-of select="@name"/></h1>
            <h2>Resource Description:</h2>
            <table name="Resource Description" width="800">
            <h6><font size="0" color="white"><xsl:value-of select="DESCRIPTION"/></font></h6>
            </table>
            
            <h2>Resource Parameters:</h2>
            <table name="Resource Parameters" border="1" frame="box">
              <tr>
                <td bgcolor="#666666"><en><b>name</b></en></td>
                <td bgcolor="#666666"><en><b>ID</b></en></td>
                <td bgcolor="#666666"><en><b>unit</b></en></td>
                <td bgcolor="#666666"><en><b>ucd</b></en></td>
                <td bgcolor="#666666"><en><b>datatype</b></en></td>
                <td bgcolor="#666666"><en><b>Value</b></en></td>
                <td bgcolor="#666666"><en><b>arraysize</b></en></td>
                <td bgcolor="#666666"><en><b>precision</b></en></td>
                <td bgcolor="#666666"><en><b>width</b></en></td>
                <td bgcolor="#666666"><en><b>ref</b></en></td>
                <td bgcolor="#666666"><en><b>type</b></en></td>
                <td bgcolor="#666666"><en><b>description</b></en></td> 
              </tr>
              <xsl:for-each select="PARAM">
                <tr>
                  <td bgcolor="#337777"><em><xsl:value-of select="@name"/></em></td>
                  <td bgcolor="#337777"> <xsl:value-of select="@ID"/> </td>
                  <td bgcolor="#337777"> <xsl:value-of select="@unit"/> </td>
                  <td bgcolor="#337777"><font color="red"><xsl:value-of select="@ucd"/></font></td>
                  <td bgcolor="#337777"> <xsl:value-of select="@datatype"/> </td>
                  <td bgcolor="#337777"> <xsl:value-of select="@value"/> </td>
                  <td bgcolor="#337777"> <xsl:value-of select="@precision"/> </td>
                  <td bgcolor="#337777"> <xsl:value-of select="@arraysize"/> </td>
                  <td bgcolor="#337777"> <xsl:value-of select="@width"/> </td>
                  <td bgcolor="#337777"> <xsl:value-of select="@ref"/> </td>
                  <td bgcolor="#337777"> <xsl:value-of select="@type"/> </td>
                  <td bgcolor="#337777"><b><xsl:value-of select="DESCRIPTION"/></b></td>
                </tr>
              </xsl:for-each>
              </table>
              
                <xsl:for-each select="TABLE">
                  <h2>Table Data:</h2>
                  <table name="Table Data" border="1" frame="box">
                     <tr>
                     <xsl:for-each select="FIELD">           
                          <td bgcolor="#666666"><em><b><xsl:value-of select="@name"/></b></em></td>
                     </xsl:for-each>
                     </tr>
                     <tr> 
                     <xsl:for-each select="FIELD"> 
                          <td bgcolor="Green"><b><xsl:value-of select="@unit"/></b></td>
                     </xsl:for-each>
                     </tr>
                   <xsl:for-each select="DATA">
                        <xsl:for-each select="TABLEDATA">
                            <xsl:for-each select="TR">
                                <tr>
                                <xsl:for-each select="TD">
                                        <td  bgcolor="#333377" ><xsl:value-of select="."/></td>
                                </xsl:for-each>
                                </tr>
                            </xsl:for-each>
                       </xsl:for-each>
                 </xsl:for-each>
                 </table>
                 <h2>Table Fields:</h2>
                 <table  name="Table Fields" width="90%" border="1" frame="box"> 
                 <tr>
                        <td bgcolor="#666666"><en><b>name</b></en></td>
                        <td bgcolor="#666666"><en><b>ID</b></en></td>
                        <td bgcolor="#666666"><en><b>unit</b></en></td>
                        <td bgcolor="#666666"><en><b>ucd</b></en></td>
                        <td bgcolor="#666666"><en><b>datatype</b></en></td>
                        <td bgcolor="#666666"><en><b>arraysize</b></en></td>
                        <td bgcolor="#666666"><en><b>precision</b></en></td>
                        <td bgcolor="#666666"><en><b>width</b></en></td>
                        <td bgcolor="#666666"><en><b>ref</b></en></td>
                        <td bgcolor="#666666"><en><b>type</b></en></td>
                        <td bgcolor="#666666"><en><b>description</b></en></td> 
                </tr>
                <xsl:for-each select="FIELD"> 
                <tr>
                        <td bgcolor="#337777"><em><xsl:value-of select="@name"/></em></td>
                        <td bgcolor="#337777"> <xsl:value-of select="@ID"/> </td>
                        <td bgcolor="#337777"> <xsl:value-of select="@unit"/> </td>
                        <td bgcolor="#337777"><font color="red"><xsl:value-of select="@ucd"/></font></td>
                        <td bgcolor="#337777"> <xsl:value-of select="@datatype"/> </td>
                        <td bgcolor="#337777"> <xsl:value-of select="@arraysize"/> </td>
                        <td bgcolor="#337777"> <xsl:value-of select="@precision"/> </td>
                        <td bgcolor="#337777"> <xsl:value-of select="@width"/> </td>
                        <td bgcolor="#337777"> <xsl:value-of select="@ref"/> </td>
                        <td bgcolor="#337777"> <xsl:value-of select="@type"/> </td>
                        <td bgcolor="#337777"><b><xsl:value-of select="DESCRIPTION"/></b></td>
                </tr>
                </xsl:for-each> 
                </table>              
                </xsl:for-each>
          </xsl:for-each>
        </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
