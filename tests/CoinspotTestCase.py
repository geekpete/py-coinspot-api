#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CoinSpotTestCase.py: A bunch of unittests for testing this module."""

__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.2.1'
__license__ = 'GPLv3'
__source__ = 'http://github.com/geekpete/py-coinspot-api/coinspot.py'


import unittest
from coinspot import CoinSpot
from mock import patch
import helpers
import fixtures


class CoinSpotTestCase(unittest.TestCase):
    def setUp(self):
        self._coinspot = CoinSpot()

    def tearDown(self):
        pass

    #@patch('CoinSpot._request')
    def test_get_spot(self, get):
        #get.side_effect = helpers.mock_api_request
        #resp = self._coinspot.spot()
        pass
