import re

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from pybtex.database.input import bibtex
from .caselessdict import CaselessDict
from xml.sax.saxutils import quoteattr

# get the NodeID to put it in the source key
from django.conf import settings
from django.utils.importlib import import_module
DICTS=import_module(settings.NODEPKG+'.dictionaries')
try: NODEID = DICTS.RETURNABLES['NodeID']
except: NODEID = 'PleaseFillTheNodeID'

DUMMY='@article{DUMMY, Author = {No Body}, Title = {This is a dummy entry. If you see it in your XSAMS output it means that at there was a malformed BibTex entry.}, annote = {%s}}'

def getEntryFromString(s):
    parser = bibtex.Parser()
    try:
        parser.parse_stream(StringIO(s))
        key,entry = parser.data.entries.items()[0]
    except Exception:
        parser.parse_stream(StringIO(DUMMY))
        key,entry = parser.data.entries.items()[0]
    return entry

TYPE2CATEGORY=CaselessDict({\
'article':'journal',
'book':'book',
'techreport':'report',
'misc':'private communication',
'inproceedings':'proceedings',
'phdthesis':'thesis',
'unpublished':'private communication'
})

def BibTeX2XML(bibtexstring, key=None):
    """
    Derives an XSAMS source element from the given BibTeX and returns the XML text.
    The ID of the Source is set in the form B(node)-(key) where (node) is replaced
    by the ID string for this node and (key) is replaced by the unique key for this
    Source. If the key argument is given, this value is used for the key; otherwise,
    a key is generated from the BibTeX content.
    """
    e = getEntryFromString(bibtexstring)
    if key:
        xml = u'<Source sourceID="B%s-%s">\n<Authors>\n'%(NODEID,key)
    else:
        xml = u'<Source sourceID="B%s-%s">\n<Authors>\n'%(NODEID,e.key)
    for a in e.persons['author']:
        name = a.first() + a.middle() + a.last() + a.lineage()
        name = name.strip()
        name = name.strip(['{}']*len(name))
        xml += '<Author><Name>%s</Name></Author>'%' '.join(name)
    xml += '\n</Authors>'

    category = TYPE2CATEGORY.get(e.type)

    f = CaselessDict(e.fields)
    url = f.get('bdsk-url-1')
    title = f.get('title', "").strip().strip('{}')
    sourcename = f.get('journal','unknown')
    doi = f.get('doi', "")
    year = f.get('year', "")
    volume = f.get('volume', "")
    pages = f.get('pages', "")
    p1, p2 = '', ''
    pages = re.findall(r'[0-9][0-9]*', pages)
    if pages:
        p1 = pages[0]
        if len(pages) > 1:
            p2 = pages[-1]

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

    xml += '<BibTeX>%s</BibTeX></Source>' % quoteattr(bibtexstring)[1:-1]

    return xml
