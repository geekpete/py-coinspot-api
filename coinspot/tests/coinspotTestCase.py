#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CoinSpotTestCase.py: A bunch of unittests for testing this module."""

__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.2.1'
__license__ = 'GPLv3'
__source__ = 'http://github.com/geekpete/py-coinspot-api/coinspot.py'


import unittest
import os
from coinspot import CoinSpot

class CoinSpotTestCase(unittest.TestCase):
    def setUp(self):
        self._client = CoinSpot()

    def tearDown(self):
        pass


