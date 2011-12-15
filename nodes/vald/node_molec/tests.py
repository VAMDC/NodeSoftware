"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

import sys
try:
    from django.utils.unittest import TestCase
except ImportError:
    from django.test import TestCase
try:    
    from django.utils import unittest
except ImportError:
    import unittest
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
    """
    tsuite = unittest.TestSuite()
    tsuite.addTest(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    tsuite.addTest(unittest.defaultTestLoader.loadTestsFromModule(vamdctests))
    return tsuite
