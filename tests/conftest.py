# coding: utf-8
"""
Pytest configuration for generator tests

This disables Django integration for non-Django tests
"""

import pytest


def pytest_configure(config):
    """Configure pytest to skip Django setup for these tests"""
    # Disable Django for unit tests
    config.option.no_django = True
