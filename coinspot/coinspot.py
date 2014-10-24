#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.2.2'
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
import yaml
import os
import sys
import logging
from time import time, strftime


class CoinSpot:
    """
    set some defaults
    """
    _api_key = ""
    _api_secret = ""
    _endpoint = "www.coinspot.com.au"
    _logging = "coinspot.log"
    _debug = False

    """
    coinspot class implementing API calls for the coinspot API
    """

    def __init__(self):
        self.timestamp = strftime("%d/%m/%Y %H:%M:%S")
        self.loader()
        if self._debug:
            self.start_logging()

    def loader(self):
        """
        Step 1 First we look for globals in the form:
         COINSPOT_API_KEY
         COINSPOT_SECRET_KEY
        """
        try:
            self._api_key = os.environ['COINSPOT_API_KEY']
            self._api_secret = os.environ['COINSPOT_SECRET_KEY']
            #ok got enough to run
            return
        except:
            pass

        """
        Step 2  Second we look for the localest yaml file - closest to executing code
        """
        try:
            config = yaml.load(open(os.path.realpath(os.path.dirname(sys.argv[0])) + '/config.yml', 'r'))
            #these must be set
            self._api_key = config['api']['key']
            self._api_secret = config['api']['secret']
            #these are optional  - wrap some code around this
            self._endpoint = config['api']['endpoint']
            self._logging = config['logfile']
            self._debug = config['debug']
            #ok we are good to run
            return
        except IOError as error:
            pass
        except:
            pass

        """
        Step 3 Carry on - we dont care if there is no config file - we might be testing
        """

    def start_logging(self):
        logging.basicConfig(filename=os.path.realpath(os.path.dirname(sys.argv[0])) + "/" + self._logging, level=logging.DEBUG)

    def _get_signed_request(self, data):
        return hmac.new(self._api_secret, data, hashlib.sha512).hexdigest()

    def _request(self, path, postdata):
        nonce = int(time()*1000000)
        postdata['nonce'] = nonce
        params = json.dumps(postdata, separators=(',', ':'))
        signedMessage = self._get_signed_request(params)
        headers = {}
        headers['Content-type'] = 'application/json'
        headers['Accept'] = 'text/plain'
        headers['key'] = self._api_key
        headers['sign'] = signedMessage
        headers['User-Agent'] = 'py-coinspot-api/%s (https://github.com/geekpete/py-coinspot-api)' % __version__
        if self._debug:
            logging.warning(self.timestamp + " " + str(headers))
        conn = httplib.HTTPSConnection(self._endpoint)
        if self._debug:
            conn.set_debuglevel(1)
        response_data = '{"status":"invalid","error": "Did not make request"}'
        try:
            conn.request("POST", path, params, headers)
            response = conn.getresponse()
            if self._debug:
                logging.warning(self.timestamp + " " + str(response))
                logging.warning(self.timestamp + " " + str(response.msg))
            #print response.status, response.reason
            response_data = response.read()
            if self._debug:
                logging.warning(self.timestamp + " " + str(response_data))
            conn.close()
        except IOError as error:
            if self._debug:
                error_text = "Attempting to make request I/O error({0}): {1}".format(error.errno, error.strerror)
                logging.warning(self.timestamp + " " + error_text)
                response_data = '{"status":"invalid","error": "' + error_text + '"}'
        except:
            exit("Unexpected error: {0}".format(sys.exc_info()[0]))

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
