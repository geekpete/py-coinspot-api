#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""__init__.py: Init for unit testing this module."""

__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.2.1'
__license__ = 'GPLv3'
__source__ = 'http://github.com/geekpete/py-coinspot-api/coinspot.py'

import unittest

from coinspot.tests.CoinSpotTestCase import CoinSpotTestCase


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CoinSpotTestCase))
    return suite
