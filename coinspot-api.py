#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'

import hmac,hashlib
import httplib, urllib
import json
from pprint import pprint
from time import time

api_key = '' # Add your Coinspot API Key
api_secret = '' # Add your Coinspot API Secret


class coinspot:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = "www.coinspot.com.au"

    def get_signed_request(self, data):
        #print "data:"
        #print data
        return hmac.new(self.api_secret, data, hashlib.sha512).hexdigest()

    def request(self, path, postdata):
        nonce = int(time())
        postdata['nonce'] = nonce

        #print "postdata:"
        #print postdata
        signedMessage = self.get_signed_request(json.dumps(postdata))
        #print "signedMessage:"
        #print signedMessage

        params = urllib.urlencode(postdata)
        #print "params:"
        #print params
        headers = {}
        #headers['Content-type'] = 'application/json'
        headers['Content-type'] = 'text/json'
        headers['Accept'] = 'text/plain'
        headers['key'] = self.api_key
        headers['sign'] = signedMessage
        #headers['User-Agent'] = 'py-coinspot-api https://github.com/geekpete/py-coinspot-api'
        #print "headers:"
        #print headers
        #print self.endpoint

        conn = httplib.HTTPSConnection(self.endpoint)
        #conn.set_debuglevel(1)
        conn.request("POST", path, params, headers)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
        print data
        #print json.loads(data)

    def spot(self):
        self.request('/api/spot', {})

    def balances(self):
		self.request('/api/my/balances', {})

    def myorders(self):
        self.request('/api/my/orders', {})


# Test it out:
client = coinspot(api_key, api_secret)
client.spot()
client.balances()
client.myorders()

