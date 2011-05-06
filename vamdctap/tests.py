"""
This is the VAMDC node software test suite. It is normally run together with
a node's specific tests using manage.py test, but can also be run by executing 
this file manually. 

"""

# safely import test framework (django-version non-specific)
try:
    from django.utils.unittest import TestCase
except ImportError:
    from django.test import TestCase
try:    
    from django.utils import unittest
except ImportError:
    import unittest
from django.test.client import Client


#
# Setting up the testing client
#
TCLIENT = Client()

class TapSyncTest(TestCase):
    """
    This class tests the return data from a VAMDC /tap/sync/ request using
    the test client. It makes sure to weed out all the superfluos
    data to make it easy to define and determine mismatches.
    """
    def setUp(self):
        "Creates the base config for the test class."
        self.url_prefix = "/tap/sync/"
    
    
    def call(self, requeststring, tag=None, desired=""):
        """
        Attempts a fake "call" from the test client to the handler. If
        gigen, the result is checked against desired,
        otherwise it just checked so that the return is not empty.

        requeststring - a string coming in through the GET statement. The full URL
                        should not be given, only the active part after /tap/sync/.
        """        
        requeststring = self.url_prefix + requeststring.strip()        
        request = TCLIENT.get(requeststring)        
        if desired:
            result = request.content
            if tag:
                # obtain only the wanted tag to check
                pass            
            self.assertEqual(result, desired)        
        
#
# TAPservice test suite 
#

class EmptyTest(TapSyncTest):
    def test_call(self):
        self.call("") # test an empty call. This should fail gracefully.

#
# Bibtex perser test suite
#

class TestBibTex(TestCase):
    def test_callBibTex2XML(self):
        import bibtextools
        tbibtex = """@article{BDMQ,\n        Author = {{Bi{\\'e}mont}, E. and {Dutrieux}, {J.-F.} and {Martin}, I. and {Quinet}, P.},\n        Date-Modified = {2010-09-27 17:27:07 +0200},\n        Doi = {10.1088/0953-4075/31/15/006},\n        Journal = {Journal of Physics B Atomic Molecular Physics},\n        Month = aug,\n        Note = {(BDMQ)},\n        Pages = {3321-3333},\n        Title = {{Lifetime calculations in Yb II}},\n        Volume = 31,\n        Year = 1998,\n        Bdsk-Url-1 = {http://dx.doi.org/10.1088/0953-4075/31/15/006}}\n"""
        txml = u"""<Source sourceID="BExampleNode-BDMQ">\n<Authors>\n<Author><Name>E. Bi{\\\'e}mont</Name></Author><Author><Name>J.-F. Dutrieux</Name></Author><Author><Name>I. Martin</Name></Author><Author><Name>P. Quinet</Name></Author>\n</Authors><Title>Lifetime calculations in Yb II</Title>\n<Category>journal</Category>\n<Year>1998</Year>\n<SourceName>Journal of Physics B Atomic Molecular Physics</SourceName>\n<Volume>31</Volume>\n<PageBegin>3321</PageBegin>\n<PageEnd>3333</PageEnd>\n<UniformResourceIdentifier>http://dx.doi.org/10.1088/0953-4075/31/15/006</UniformResourceIdentifier>\n<DigitalObjectIdentifier>10.1088/0953-4075/31/15/006</DigitalObjectIdentifier>\n<BibTeX>@article{BDMQ,&#10;        Author = {{Bi{\\\'e}mont}, E. and {Dutrieux}, {J.-F.} and {Martin}, I. and {Quinet}, P.},&#10;        Date-Modified = {2010-09-27 17:27:07 +0200},&#10;        Doi = {10.1088/0953-4075/31/15/006},&#10;        Journal = {Journal of Physics B Atomic Molecular Physics},&#10;        Month = aug,&#10;        Note = {(BDMQ)},&#10;        Pages = {3321-3333},&#10;        Title = {{Lifetime calculations in Yb II}},&#10;        Volume = 31,&#10;        Year = 1998,&#10;        Bdsk-Url-1 = {http://dx.doi.org/10.1088/0953-4075/31/15/006}}&#10;</BibTeX></Source>"""
        self.maxDiff = None
        self.assertEquals(txml, bibtextools.BibTeX2XML(tbibtex))





if __name__ == "__main__":    
    print "You must run this module from a node with 'manage.py test'."
