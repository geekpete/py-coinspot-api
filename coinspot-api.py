#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'

import hmac
import hashlib
from pprint import pprint

api_key = '' # Add your Coinspot API Key
api_secret = '' # Add your Coinspot API Secret

my_hmac = hmac.new(api_secret,'',hashlib.sha256)
my_hmac.update('message')
print my_hmac.hexdigest()

#dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
#binascii.hexlify(dk)

#pprint(vars(hashlib))
