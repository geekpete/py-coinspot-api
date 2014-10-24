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
import json

import helpers


class CoinSpotTestCase(unittest.TestCase):
    def setUp(self):
        self._coinspot = CoinSpot()

    def tearDown(self):
        pass

    @patch('coinspot.CoinSpot._request')
    def test_get_spot(self, get):
        get.side_effect = helpers.mock_api_request
        resp = self._coinspot.spot()
        data = json.loads(resp.content)
        self.assertTrue(data.has_key('status'))
        self.assertEqual(data.get('status'), 'ok')
        self.assertTrue(data.has_key('spot'))

    @patch('coinspot.CoinSpot._request')
    def test_get_quotebuy(self, get):
        get.side_effect = helpers.mock_api_request
        resp = self._coinspot.quotebuy("DOGE", 100)
        data = json.loads(resp.content)
        self.assertTrue(data.has_key('status'))
        self.assertEqual(data.get('status'), 'ok')
        self.assertTrue(data.has_key('quote'))
        self.assertTrue(data.has_key('timeframe'))

    @patch('coinspot.CoinSpot._request')
    def test_get_balances(self, get):
        get.side_effect = helpers.mock_api_request
        resp = self._coinspot.balances()
        data = json.loads(resp.content)
        self.assertTrue(data.has_key('status'))
        self.assertEqual(data.get('status'), 'ok')
        self.assertTrue(data.has_key('balance'))

    @patch('coinspot.CoinSpot._request')
    def test_get_orderhistory(self, get):
        get.side_effect = helpers.mock_api_request
        resp = self._coinspot.orderhistory('DOGE')
        data = json.loads(resp.content)
        self.assertTrue(data.has_key('status'))
        self.assertEqual(data.get('status'), 'ok')
        self.assertTrue(data.has_key('orders'))