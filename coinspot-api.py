#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.1.0'

import hmac,hashlib
import httplib, urllib
import json
from pprint import pprint
from time import time, sleep

#api_key = '' # Add your Coinspot API Key
#api_secret = '' # Add your Coinspot API Secret

class Coinspot:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = "www.coinspot.com.au"

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
        print response.status, response.reason
        data = response.read()
        conn.close()
        print data

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

        Inputs:
        cointype - the coin shortname, example value 'BTC', 'LTC', 'DOGE'

        Response:
        status - ok, error
        buyorders - array containing all the open buy orders
        sellorders - array containing all the open sell orders
        """
        data = {'cointype':cointype}
        self.request('/api/orders', data )

    def buy(self, cointype, amount, rate):
        data = {'cointype':cointype, 'amount':amount, 'rate':rate}
        print data
        self.request('/api/my/buy', data)

    def sell(self, cointype, amount, rate):
        data = {'cointype':cointype, 'amount':amount, 'rate':rate}
        print data
        self.request('/api/my/sell', data)


# Test it out:
client = Coinspot(api_key, api_secret)
#client.spot()
#sleep(2)
#client.balances()
#sleep(2)
client.myorders()
#client.orders('DOGE')
#client.sell('DOGE', '20', '0.000280')