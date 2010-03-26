from lxml import etree as e
from lxml.etree import XPath

text_list=XPath("//text()")
parser=e.XMLParser(remove_blank_text=True)

# XML schemata
xsl_job2html_url='http://vamdc.fysast.uu.se:8080/DSAcat/TAP/uws-job-to-html.xsl'
xsl_job2html = e.parse(xsl_job2html_url)
job2html= e.XSLT(xsl_job2html)

xsl_data2html_url='http://vamdc.fysast.uu.se:8080/DSAcat/TAP/uws-results-to-html.xsl'
xsl_data2html = e.parse(xsl_data2html_url)
data2html= e.XSLT(xsl_data2html)

xsl_xsams_url='http://vamdc.fysast.uu.se:8080/DSAcat/xsams-0.1.xsd'
xsl_xsams= e.parse(xsl_xsams_url)
