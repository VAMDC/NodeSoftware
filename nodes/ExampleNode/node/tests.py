"""
This file demonstrates tests that willpass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import unittest
from django.test import TestCase

from vamdctap import tests as vamdctests

# add database-specific tests here. See example below.

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


# Don't edit the following. It allows this module and the vamdc
# software tests to be run through the Django test runner.

def suite():
    """
    This function is called automatically by the django test runner.
    This also runs the command tests defined in src/commands/default/tests.py.
    """
    tsuite = unittest.TestSuite()
    tsuite.addTest(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    tsuite.addTest(unittest.defaultTestLoader.loadTestsFromModule(vamdctests))

    return tsuite
