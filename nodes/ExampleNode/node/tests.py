"""
Tests of the ExampleNode, run with "manage.py test".

They send queries through the same code as a live node and look at the
XSAMS that comes back. Adapt them to your own data: a handful of queries
with known answers is the cheapest way to notice that a change in
models.py, dictionaries.py or queryfunc.py broke something.
"""

import builtins
from xml.etree import ElementTree

from django.test import TestCase

import load_data

NS = '{http://vamdc.org/xml/xsams/1.0}'

class QueryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        load_data.load_all()

    def query(self, query):
        response = self.client.get('/tap/sync', {'LANG': 'VSS2', 'FORMAT': 'XSAMS', 'QUERY': query})
        if response.streaming:
            response.body = b''.join(response.streaming_content)
        else:
            response.body = response.content
        return response

    def count(self, response, tag):
        return len(list(ElementTree.fromstring(response.body).iter(NS + tag)))

    def test_select_all(self):
        r = self.query("select all where AtomSymbol = 'Nb'")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['VAMDC-COUNT-RADIATIVE'], '19')
        self.assertEqual(r['VAMDC-COUNT-STATES'], '21')
        self.assertEqual(self.count(r, 'RadiativeTransition'), 19)
        self.assertEqual(self.count(r, 'AtomicState'), 21)
        # the self-reference to the query plus REF1 and REF2
        self.assertEqual(self.count(r, 'Source'), 3)

    def test_wavelength_range(self):
        r = self.query("select all where RadTransWavelength > 2700 and RadTransWavelength < 3000")
        self.assertEqual(self.count(r, 'RadiativeTransition'), 3)
        self.assertEqual(self.count(r, 'AtomicState'), 5)

    def test_logic(self):
        r = self.query("select all where AtomStateEnergy < 41000 "
                       "and (AtomIonCharge = 1 or AtomIonCharge = 5) "
                       "and not RadTransProbabilityLog10WeightedOscillatorStrength < -1")
        self.assertEqual(self.count(r, 'RadiativeTransition'), 5)

    def test_in_and_like(self):
        r = self.query("select all where AtomSymbol in ('Nb','Fe') and AtomSymbol like 'N%'")
        self.assertEqual(self.count(r, 'RadiativeTransition'), 19)

    def test_select_species(self):
        r = self.query("select species")
        self.assertEqual(self.count(r, 'Atom'), 1)
        self.assertEqual(self.count(r, 'RadiativeTransition'), 0)

    def test_no_match(self):
        r = self.query("select all where AtomSymbol = 'Fe'")
        self.assertEqual(r.status_code, 204)

    def test_unknown_restrictable(self):
        r = self.query("select all where NoSuchKeyword = 1")
        self.assertEqual(r.status_code, 400)

    def test_values_are_data(self):
        # A value must never be executed, whatever quotes it contains.
        r = self.query('''select all where AtomSymbol = 'x") or setattr(__import__("builtins"), "PWNED", 1) or Q(pk="1' ''')
        self.assertEqual(r.status_code, 204)
        self.assertFalse(hasattr(builtins, 'PWNED'))
