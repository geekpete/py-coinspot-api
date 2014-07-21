#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.1.0'
__license__ = 'GPLv3'
__source__ = 'http://github.com/geekpete/py-coinspot-api/coinspot.py'

"""
coinspot.py - A python library for the Coinspot API.

Copyright (C) 2014 Peter Dyson <pete@geekpete.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

.. note:: Please see https://www.coinspot.com.au/api for documentation on the CoinSpot API.
.. note:: All requests and responses will be JSON

"""

import hmac
import hashlib
import httplib
import json
from time import time


class Coinspot:
    """
    Coinspot class implementing API calls for the Coinspot API
    """
    def __init__(self, api_key, api_secret, endpoint='www.coinspot.com.au'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint

    def _get_signed_request(self, data):
        return hmac.new(self.api_secret, data, hashlib.sha512).hexdigest()

    def _request(self, path, postdata):
        nonce = int(time())
        postdata['nonce'] = nonce
        params = json.dumps(postdata, separators=(',', ':'))
        signedMessage = self._get_signed_request(params)
        headers = {}
        headers['Content-type'] = 'application/json'
        headers['Accept'] = 'text/plain'
        headers['key'] = self.api_key
        headers['sign'] = signedMessage
        headers['User-Agent'] = 'py-coinspot-api/%s (https://github.com/geekpete/py-coinspot-api)' % __version__

        conn = httplib.HTTPSConnection(self.endpoint)
        #conn.set_debuglevel(1)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()
        #print response.status, response.reason
        response_data = response.read()
        conn.close()
        return response_data

    def sendcoin(self, cointype, address, amount):
        """
        Send coins

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :param address:
            the address to send the coins to
        :param amount:
            the amount of coins to send
        :return:
            - **status** - ok, error

        """
        request_data = {'cointype':cointype, 'address':address, 'amount':amount}
        return self._request('/api/my/coin/send', request_data)

    def coindeposit(self, cointype):
        """
        Deposit coins

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **address** - your deposit address for the coin

        """
        request_data = {'cointype':cointype}
        return self._request('/api/my/coin/deposit', request_data)

    def quotebuy(self, cointype, amount):
        """
        Quick buy quote

        Fetches a quote on rate per coin and estimated timeframe to buy an amount of coins

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            the amount of coins to sell
        :return:
            - **status** - ok, error
            - **quote** - the rate per coin
            - **timeframe** - estimate of hours to wait for trade to complete (0 = immediate trade)

        """
        request_data = {'cointype':cointype, 'amount':amount}
        return self._request('/api/quote/buy', request_data)

    def quotesell(self, cointype, amount):
        """
        Quick sell quote

        Fetches a quote on rate per coin and estimated timeframe to sell an amount of coins

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            the amount of coins to sell
        :return:
            - **status** - ok, error
            - **quote** - the rate per coin
            - **timeframe** - estimate of hours to wait for trade to complete (0 = immediate trade)

        """
        request_data = {'cointype':cointype, 'amount':amount}
        return self._request('/api/quote/sell', request_data)


    def spot(self):
        """
        Fetch the latest spot prices

        :return:
            - **status** - ok, error
            - **spot**  - a list of the current spot price for each coin type

        """
        return self._request('/api/spot', {})

    def balances(self):
        """
        List my balances

        :return:
            - **status** - ok, error
            - **balances** - object containing one property for each coin with your balance for that coin.

        """
        return self._request('/api/my/balances', {})

    def orderhistory(self, cointype):
        """
        Lists the last 1000 completed orders

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **orders** - list of the last 1000 completed orders

        """
        request_data = {'cointype':cointype}
        return self._request('/api/orders/history', request_data)

    def orders(self, cointype):
        """
        Lists all open orders

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **buyorders** - array containing all the open buy orders
            - **sellorders** - array containing all the open sell orders

        """
        request_data = {'cointype':cointype}
        return self._request('/api/orders', request_data)

    def myorders(self):
        """
        List my buy and sell orders

        :return:
            - **status** - ok, error
            - **buyorders** - array containing all your buy orders
            - **sellorders** - array containing all your sell orders

        """
        return self._request('/api/my/orders', {})

    def buy(self, cointype, amount, rate):
        """
        Place buy orders

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            the amount of coins you want to buy, max precision 8 decimal places
        :param rate:
            the rate in AUD you are willing to pay, max precision 6 decimal places
        :return:
            - **status** - ok, error

        """
        request_data = {'cointype':cointype, 'amount':amount, 'rate':rate}
        return self._request('/api/my/buy', request_data)

    def sell(self, cointype, amount, rate):
        """
        Place sell orders

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            the amount of coins you want to sell, max precision 8 decimal places
        :param rate:
            the rate in AUD you are willing to sell for, max precision 6 decimal places
        :return:
            - **status** - ok, error

        """
        request_data = {'cointype':cointype, 'amount':amount, 'rate':rate}
        self._request('/api/my/sell', request_data)