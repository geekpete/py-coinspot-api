#!/usr/bin/python
__author__ = 'Peter Dyson <pete@geekpete.com>'

"""
Script to test the coinspot-api module.
"""

from coinspot import Coinspot


api_key = '' # Add your Coinspot API Key
api_secret = '' # Add your Coinspot API Secret

# Test it out:
client = Coinspot(api_key, api_secret)

# get the spot prices
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