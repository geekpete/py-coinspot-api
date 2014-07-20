#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.1.0'

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

"""

import hmac,hashlib
import httplib, urllib
import json
from pprint import pprint
from time import time, sleep

#api_key = '' # Add your Coinspot API Key
#api_secret = '' # Add your Coinspot API Secret

class Coinspot:
    """
    Coinspot class implementing API calls for the Coinspot API
    """
    def __init__(self, api_key, api_secret, endpoint='www.coinspot.com.au'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint

    def get_signed_request(self, data):
        return hmac.new(self.api_secret, data, hashlib.sha512).hexdigest()

    def request(self, path, postdata):
        nonce = int(time())
        postdata['nonce'] = nonce
        params = json.dumps(postdata, separators=(',', ':'))
        signedMessage = self.get_signed_request(params)
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
        data = response.read()
        conn.close()
        return data

    def spot(self):
        self.request('/api/spot', {})

    def balances(self):
		self.request('/api/my/balances', {})

    def myorders(self):
        self.request('/api/my/orders', {})

    def orders(self, cointype):
        """
        List Open Orders

        Url:
        /orders

        :param cointype:
            the coin shortname in uppercase, example value 'BTC', 'LTC', 'DOGE'
        :type cointype:
            String

        Response:
            status - ok, error
            buyorders - array containing all the open buy orders
            sellorders - array containing all the open sell orders


        """
        data = {'cointype':cointype}
        return self.request('/api/orders', data )

    def buy(self, cointype, amount, rate):
        data = {'cointype':cointype, 'amount':amount, 'rate':rate}
        #print data
        self.request('/api/my/buy', data)

    def sell(self, cointype, amount, rate):
        data = {'cointype':cointype, 'amount':amount, 'rate':rate}
        #print data
        self.request('/api/my/sell', data)