#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'

"""
Script to test the coinspot-api module.
"""

from coinspot import Coinspot


#api_key = '' # Add your Coinspot API Key
#api_secret = '' # Add your Coinspot API Secret


api_key = '6a8bd271d0ee89598c01ffd93fe27788'
api_secret = 'MLD8F9WT4M7Q4RAKY5121A967TBG3LFJMMHF5XFDGVLT1JL2B5575XYHRV6YGKLTYRC9LL4QY4TPY4W97'

# Test it out:
client = Coinspot(api_key, api_secret)

# get the spot prices
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()
print client.spot()

# get your coin wallet balances
#print client.balances()

# get the last 1000 orders for Dogecoins
#print client.orderhistory('DOGE')

# get a list of all the current buy and sell orders
#print client.orders('DOGE')

# put an order in to sell 20 Dogecoins at 0.000280 per coin
#print client.sell('DOGE', '20', '0.000280')

# Get a quote on buying a billion Dogecoins, with estimation of timeframe
#print client.quotebuy('DOGE', 1000000000)

# Donate a craptonne of Dogecoins to the author of this library! Much Appreciate!!!
#print client.send('DOGE', 'DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs', 10000)