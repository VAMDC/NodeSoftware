from StringIO import StringIO
from pybtex.database.input import bibtex
from string import strip
from caselessdict import CaselessDict
from xml.sax.saxutils import quoteattr

# get the NodeID to put it in the source key
from django.conf import settings
from django.utils.importlib import import_module
DICTS=import_module(settings.NODEPKG+'.dictionaries')
try: NODEID = DICTS.RETURNABLES['NodeID']
except: NODEID = 'PleaseFillTheNodeID'

DUMMY='@article{DUMMY, Author = {No Boby}, Title = {This is a dummy entry. If you see it in your XSAMS output it means that at there was a malformed BibTex entry.}, annote = {%s}}'

def getEntryFromString(s):
    parser = bibtex.Parser()
    try:
        parser.parse_stream(StringIO(s))
        key,entry = parser.data.entries.items()[0]
    except:
        bib = parser.parse_stream(StringIO(DUMMY))
        key,entry = parser.data.entries.items()[0]
    return entry

TYPE2CATEGORY=CaselessDict({\
'article':'journal',
'book':'book',
'techreport':'report',
'misc':'private communication',
'inproceedings':'proceedings',
})

def BibTeX2XML(bibtexstring):
    e = getEntryFromString(bibtexstring)
    xml = u'<Source sourceID="B%s-%s">\n<Authors>\n'%(NODEID,e.key)
    for a in e.persons['author']:
        name = a.first() + a.middle() + a.last() + a.lineage()
        name = map(strip,name)
        name = map(strip,name,['{}']*len(name))
        xml += '<Author><Name>%s</Name></Author>'%' '.join(name)
    xml += '\n</Authors>'

    category = TYPE2CATEGORY.get(e.type)

    f = CaselessDict(e.fields)
    url = f.get('bdsk-url-1')
    title = f.get('title').strip().strip('{}')
    sourcename = f.get('journal','unknown')
    doi = f.get('doi')
    year = f.get('year')
    volume = f.get('volume')
    pages = f.get('pages')
    if pages:
        if '-' in pages:
            p1,p2 = pages.split('-')
        else:
            p1, p2 = pages, ''
    else: 
        p1,p2 = '',''

    xml += """<Title>%s</Title>
<Category>%s</Category>
<Year>%s</Year>
<SourceName>%s</SourceName>
<Volume>%s</Volume>
<PageBegin>%s</PageBegin>
<PageEnd>%s</PageEnd>
<UniformResourceIdentifier>%s</UniformResourceIdentifier>
<DigitalObjectIdentifier>%s</DigitalObjectIdentifier>
""" % (title,category,year or 2222,sourcename,volume,p1,p2,url,doi)

    xml += '<BibTeX>%s</BibTeX></Source>'%quoteattr(bibtexstring)[1:-1]

    return xml
