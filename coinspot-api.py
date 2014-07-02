#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'

import hmac
import hashlib
from pprint import pprint

api_key = '' # Add your Coinspot API Key
api_secret = '' # Add your Coinspot API Secret

class Complex:
    def __init__(self, api_key, api_secret):
        self.key = api_key
        self.secret = api_secret
        self.endpoint = "https://www.coinspot.com.au/api"

    def hmac_encode(self, ):

        return
my_hmac = hmac.new(api_secret, '', hashlib.sha256)
my_hmac.update('message')
print my_hmac.hexdigest()

#dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
#binascii.hexlify(dk)

#pprint(vars(hashlib))
