#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Peter Dyson <pete@geekpete.com>"
__version__ = "0.3.0"
__license__ = "GPLv3"
__source__ = "http://github.com/geekpete/py-coinspot-api/coinspot.py"

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

try:
    import httplib
except:
    import http.client
import json
import yaml
import os
import sys
import logging
from time import time, strftime
import requests


class CoinSpot:
    """
    set some defaults
    """

    _api_key = ""
    _api_secret = ""
    _endpoint = "https://www.coinspot.com.au"
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
            self._api_key = os.environ["COINSPOT_API_KEY"]
            self._api_secret = os.environ["COINSPOT_SECRET_KEY"]
            # ok got enough to run
            return
        except:
            pass

        """
        Step 2  Second we look for the localest yaml file - closest to executing code
        """
        try:
            config = yaml.load(
                open(
                    os.path.realpath(os.path.dirname(sys.argv[0])) + "/config.yml", "r"
                ),
                Loader=yaml.SafeLoader,
            )
            # these must be set
            self._api_key = config["api"]["key"]
            self._api_secret = config["api"]["secret"]
            # these are optional  - wrap some code around this
            self._endpoint = config["api"]["endpoint"]
            self._logging = config["logfile"]
            self._debug = config["debug"]
            # ok we are good to run
            print(self)
            return
        except IOError as error:
            pass
        except:
            pass

        """
        Step 3 Carry on - we dont care if there is no config file - we might be testing
        """

    def start_logging(self):
        logging.basicConfig(
            filename=os.path.realpath(os.path.dirname(sys.argv[0]))
            + "/"
            + self._logging,
            level=logging.DEBUG,
        )

    def _get_signed_request(self, data):
        print(self)
        # print(hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest()
        return hmac.new(
            str((self._api_secret)).encode("utf-8"),
            data.encode("utf-8"),
            hashlib.sha512,
        ).hexdigest()

    def _request_public(self, path, postdata):
        """
        The public API uses a GET method, while the Private API uses a POST method.
            _request_public - is for the public API, requires no nonce, key or hash or data.
        """

        # Create base URL
        path = self._endpoint + path

        # Add each parameter into the URL
        for parameter in postdata:
            path = path + postdata[parameter] + "/"

        # Request
        response_data = requests.get(path)
        return response_data

    def _request(self, path, postdata):
        # Create URL
        path = self._endpoint + path

        # Post data
        nonce = int(time() * 1000000)
        postdata["nonce"] = nonce
        params = json.dumps(postdata, separators=(",", ":"))
        signedMessage = self._get_signed_request(params)

        # Header
        headers = {}
        headers["Content-type"] = "application/json"
        headers["Accept"] = "text/plain"
        headers["key"] = self._api_key
        headers["sign"] = signedMessage

        # Request
        response_data = requests.post(path, data=params, headers=headers)
        return response_data


    def latestprices(self):
        """
        Latest Prices

        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **prices** - array of objects with one set of properties for each coin with latest buy and sell prices, non aud markets are symbolised by (e.g.) 'btc_usdt'

        """
        request_data = {}
        return self._request_public("/pubapi/v2/latest/", request_data)

    def coinprices(self, cointype):
        """
        Latest Coin Prices

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **prices** - object with set of properties for coin with latest buy, ask and last prices

        """
        request_data = {"cointype":cointype}
        return self._request_public("/pubapi/v2/latest/", request_data)

    def coinmarketprices(self, cointype, markettype):
        """
        Latest Coin / Market Prices

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            market coin short name, example value 'USDT' (only for available markets)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **prices** - object with set of properties for coin with latest buy, ask and last prices

        """
        request_data = {"cointype":cointype, "markettype":markettype}
        return self._request_public("/pubapi/v2/latest/", request_data)

    def buyprice(self, cointype):
        """
        Latest Buy Price

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **rate** - latest buy price for that coin
            - **market** - market coin is trading in

        """
        request_data = {"cointype":cointype}
        return self._request_public("/pubapi/v2/buyprice/", request_data)

    def buymarketprice(self, cointype, markettype):
        """
        Latest Buy Price / Market

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            coin market you wish to use to buy it, example value: USDT' (only for available markets)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **rate** - latest buy price for that coin
            - **market** - market coin is trading in

        """
        request_data = {"cointype":cointype, "markettype":markettype}
        return self._request_public("/pubapi/v2/buyprice/", request_data)

    def sellprice(self, cointype):
        """
        Latest Sell Price

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **rate** - latest sell price for that coin
            - **market** - market coin is trading in

        """
        request_data = {"cointype":cointype}
        return self._request_public("/pubapi/v2/sellprice/", request_data)

    def sellmarketprice(self, cointype, markettype):
        """
        Latest Sell Price / Market

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            coin market you wish to sell it for, example value: 'USDT' (note: only for available markets)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **rate** - latest sell price for that coin
            - **market** - market coin is trading in

        """
        request_data = {"cointype":cointype, "markettype":markettype}
        return self._request_public("/pubapi/v2/sellprice/", request_data)

    def openorders(self, cointype):
        """
        Open Orders By Coin

        :param cointype:
            the coin short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - list of top 100 open AUD buy orders for the given coin
            - **sellorders** - list of top 100 open AUD sell orders for the given coin

        """
        request_data = {"cointype":cointype}
        return self._request_public("/pubapi/v2/orders/open/", request_data)

    def openmarketorders(self, cointype, markettype):
        """
        Open Orders By Coin / Market

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            coin market, example values 'USDT' (note: only for available markets)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - list of top 20 open buy order rates for the given coin / market
            - **sellorders** - list of top 20 open sell order rates for the given coin / market

        """
        request_data = {"cointype":cointype, "markettype":markettype}
        return self._request_public("/pubapi/v2/orders/open/", request_data)

    def completedorders(self, cointype):
        """
        Completed Orders By Coin

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - list of top 100 completed AUD buy orders for the given coin
            - **sellorders** - list of top 100 completed AUD sell orders for the given coin

        """
        request_data = {"cointype":cointype}
        return self._request_public("/pubapi/v2/orders/completed/", request_data)

    def completedmarketorders(self, cointype, markettype):
        """
        Completed Orders By Coin / Market

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            coin market, example values 'USDT' (note: only for available markets)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - list of top 100 completed buy orders for the given coin / market
            - **sellorders** - list of top 100 completed sell orders for the given coin / market

        """
        request_data = {"cointype":cointype, "markettype":markettype}
        return self._request_public("/pubapi/v2/orders/completed/", request_data)

    def statuscheck(self):
        """
        Full Access Status Check

        :return:
            - **status** - ok

        """
        request_data = {}
        return self._request("/api/v2/status/", request_data)

    def depositaddress(self, cointype):
        """
        My Coin Deposit Address

        :param cointype:
            short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **networks** - list of available networks (fields below)

        """
        request_data = {"cointype":cointype}
        return self._request("/api/v2/my/coin/deposit/", request_data)

    def buynowquote(self, cointype, amount, amounttype):
        """
        Buy Now Quote

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            amount to buy
        :param amounttype:
            'coin' or 'aud' - whether the amount above is coin amount or AUD amount
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **rate** - rate per specified coin

        """
        request_data = {"cointype":cointype, "amount":amount, "amounttype":amounttype}
        return self._request("/api/v2/quote/buy/now/", request_data)

    def sellnowquote(self, cointype, amount, amounttype):
        """
        Sell Now Quote

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            amount of coins to sell
        :param amounttype:
            'coin' or 'aud' - whether the amount below is coin amount or AUD amount
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **rate** - rate per specified coin inclusive of fee

        """
        request_data = {"cointype":cointype, "amount":amount, "amounttype":amounttype}
        return self._request("/api/v2/quote/sell/now/", request_data)

    def swapnowquote(self, cointypesell, cointypebuy, amount):
        """
        Swap Now Quote

        :param cointypesell:
            coin short name you would like to swap, example value 'BTC', 'LTC', 'DOGE'
        :param cointypebuy:
            coin short name you wuld like to swap it for, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            amount of coins to swap
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **rate** - rate per coin swapped exclusive of fee

        """
        request_data = {"cointypesell":cointypesell, "cointypebuy":cointypebuy, "amount":amount}
        return self._request("/api/v2/quote/swap/now/", request_data)

    def buymarket(self, cointype, amount, rate, markettype="AUD", **kwargs):
        """
        Place Markey Buy Order

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            mount of coins you want to buy, max precision 8 decimal places
        :param rate:
            rate in market currency (e.g. AUD or USDT) you are willing to pay, max precision 8 decimal places
        :param markettype:
            (optional, available markets only, default 'AUD') market coin short name to use to buy the coin, example value 'USDT'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **coin** - coin short name, example value 'BTC', 'LTC', 'DOGE'
            - **market** - market used to place buy order for the coin
            - **amount** - coin amount that was placed
            - **rate** - rate that order was placed at
            - **id** - id of buy order created which can be used to cancel the order if desired

        """
        # Required parameters
        request_data = {"cointype":cointype, "amount":amount, "rate":rate, "markettype":markettype}
        
        # Optional parameter
        for key, value in kwargs.items():
            if key == "markettype":
                request_data[key] = value
        
        return self._request("/api/v2/my/buy/", request_data)

    def buynow(self, cointype, amounttype, amount, **kwargs):
        """
        Place Buy Now Order

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param amounttype:
            'coin' or 'aud' - whether the amount below is coin amount or AUD amount
        :param amount:
            amount to buy, max precision for coin is 8 decimal places and 2 decimal places for AUD
        :param rate:
            (optional) rate in AUD received from using Buy Now Quote or otherwise
        :param threshold:
            (optional) 0 to 1000 - buy request will terminate if not within percentage threshold for current rate to vary from submitted rate, max precision for percentage is 8 decimal places
        :param direction:
            (optional) UP, DOWN, or BOTH (default is UP) - direction the price has moved for the percentage threshold to apply
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **coin** - coin short name, example value 'BTC', 'LTC', 'DOGE'
            - **market** - market used to place buy order for the coin
            - **amount** - amount that was bought
            - **total** - total amount in market currency

        """
        # Required parameter
        request_data = {"cointype":cointype, "amounttype":amounttype, "amount":amount}
        
        # Optional parameter
        for key, value in kwargs.items():
            if key == "rate" or key == "threshold" or key == "direction":
                request_data[key] = value
        
        return self._request("/api/v2/my/buy/now/", request_data)

    def sellmarket(self, cointype, amount, rate, **kwargs):
        """
        Place Market Sell Order

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            amount of coins you want to sell, max precision 8 decimal places
        :param rate:
            rate in AUD you are willing to sell for, max precision 8 decimal places
        :param markettype:
            OPTIONAL use markettype='market', example: sellmarket('BTC', 10, 10, markettype='USDT') (optional, available markets only, default 'AUD') market coin short name to use to sell the coin into, example value 'USDT'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **coin** - coin short name
            - **market** - market used to place sell order for the coin
            - **amount** - coin amount that was placed in order
            - **rate** - rate that order was placed at
            - **id** - id of sell order created which can be used to cancel the order if desired

        """
        # Required parameters
        request_data = {"cointype":cointype, "amount":amount, "rate":rate, "markettype":markettype}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "markettype":
                request_data[key] = value

        return self._request("/api/v2/my/sell/", request_data)

    def sellnow(self, cointype, amounttype, amount, **kwargs):
        """
        Place Sell Now Order

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param amounttype:
            'coin' or 'aud' - whether the amount below is coin amount or AUD amount
        :param amount:
            amount of coins you want to sell, max precision 8 decimal places
        :param rate:
            (optional) rate in AUD received from using Sell Now Quote or otherwise
        :param threshold:
            (optional) 0 to 1000 - sell request will terminate if not within percentage threshold for current rate to vary from submitted rate, max precision for percentage is 8 decimal places
        :param direction:
            (optional) UP, DOWN, or BOTH (default is DOWN) - direction the price has moved for the percentage threshold to apply
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **coin** - coin short name, example value 'BTC', 'LTC', 'DOGE'
            - **market** - market used to place sell order for the coin
            - **amount** - amount that was sold
            - **rate** - rate that order was placed at
            - **total** - total amount in market currency

        """
        # Required parameters
        request_data = {"cointype":cointype, "amounttype":amounttype, "amount":amount}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "rate" or key == "threshold" or key == "direction":
                request_data[key] = value

        return self._request("/api/v2/my/sell/now/", request_data)

    def swapnow(self, cointypesell, cointypebuy, amount, **kwargs):
        """
        Place Swap Now Order

        :param cointypesell:
            coin short name you would like to swap, example value 'BTC', 'LTC', 'DOGE'
        :param cointypebuy:
            coin short name you wuld like to swap it for, example value 'BTC', 'LTC', 'DOGE'
        :param amount:
            amount of (cointypesell) to swap, max precision for coin is 8 decimal places
        :param rate:
            (optional) rate received from using Swap Now Quote or otherwise
        :param threshold:
            (optional) 0 to 1000 - Swap request will terminate if not within percentage threshold for current rate to vary from submitted rate, max precision for percentage is 8 decimal places
        :param direction:
            (optional) UP, DOWN, or BOTH (default is DOWN) - direction the price has moved for the percentage threshold to apply
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **coin** - coin short name, example value 'BTC', 'LTC', 'DOGE'
            - **market** - coin swapped and and coin it was swapped for
            - **amount** - coin amount that was swapped
            - **rate** - rate that order was placed at
            - **total** - total amount in swapped coin currency

        """
        # Required parameters
        request_data = {"cointypesell":cointypesell, "cointypebuy":cointypebuy, "amount":amount}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "rate" or key == "threshold" or key == "direction":
                request_data[key] = value

        return self._request("/api/v2/my/swap/now/", request_data)

    def cancelbuy(self, id):
        """
        Cancel My Buy Order

        :param id:
            id of the buy order to cancel
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred

        """
        request_data = {"id":id}
        return self._request("/api/v2/my/buy/cancel/", request_data)

    def cancelsell(self, id):
        """
        Cancel My Sell Order

        :param id:
            id of the sell order to cancel
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred

        """
        request_data = {"id":id}
        return self._request("/api/v2/my/sell/cancel/", request_data)

    def withdrawdetails(self, cointype):
        """
        Get Coin Withdrawal Details


        :param cointype:
            coin short name you would like to withdraw, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **networks** - list of available send networks

        """
        request_data = {"cointype":cointype}
        return self._request("/api/v2/my/coin/withdraw/senddetails/", request_data)

    def withdraw(self, cointype, amount, address, **kwargs):
        """
        Coin Withdrawal

        :param cointype:
            coin short name you would like to withdraw, example values 'BTC', 'LTC', 'DOGE'
        :param amount:
            the amount (in coin currency) of coin you would like to withdraw
        :param address:
            the destination address for the coin amount'
        :param emailconfirm:
            (optional, default is 'NO') if 'YES' an email confirmation will be sent and withdraw will not complete until confirmation link within email is clicked, values: 'YES', 'NO'
        :param network:
            (optional) - network you would like to send using e.g. 'BNB', 'ETH' - omit for 'default' network
        :param paymentid:
            (optional) - the appropriate payment id/memo for the withdrawal where permitted
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred

        """
        # Required parameters
        request_data = {"cointype": cointype, "amount": amount, "address": address}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "emailconfirm" or key == "network" or key == "paymentid":
                request_data[key] = value

        return self._request("/api/v2/my/coin/withdraw/send/", request_data)

    def rostatuscheck(self):
        """
        Read Only Status Check

        :return:
            - **status** - ok

        """
        request_data = {}
        return self._request("/api/v2/ro/status/", request_data)

    def marketorders(self, cointype, markettype='AUD'):
        """
        Open Market Orders

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            (optional, available markets only)) market coin short name, example values 'AUD', 'USDT'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - list of top 20 open buy order rates for the given coin
            - **sellorders** - list of top 20 open sell orders rates for the given coin

        """
        # Required parameter
        request_data = {"cointype":cointype, "markettype":markettype}

        return self._request("/api/v2/ro/orders/market/open/", request_data)

    def completedmarket(self, cointype, markettype='AUD', **kwargs):
        """
        Completed Market Orders

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            (optional, available markets only)) market coin short name, example values 'AUD', 'USDT'
        :param startdate:
            (optional, note: date is UTC date or UNIX EPOCH time) format 'YYYY-MM-DD' or e.g. 1614824116
        :param enddate:
            (optional, note: date is UTC date or UNIX EPOCH time) format 'YYYY-MM-DD' or e.g. 1614824116
        :param limit:
            (optional, default is 200 records, max is 500 records)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - list of top 100 completed buy orders for the given coin
            - **sellorders** - list of top 100 completed sell orders for the given coin

        """
        # Required parameter
        request_data = {"cointype":cointype, "markettype":markettype}
        
        # Optional parameters
        for key, value in kwargs.items():
            if key == "startdate" or key == "enddate" or key == "limit":
                request_data[key] = value

        return self._request("/api/v2/ro/orders/market/completed/", request_data)

    def my_balances(self):
        """
        My Coin Balances

        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **balances** - array containing one object for each coin with your balance, AUD value and rate for that coin

        """
        request_data = {}
        return self._request("/api/v2/ro/my/balances/", request_data)

    def my_coinbalance(self, cointype):
        """
        My Coin Balance

        :param cointype:
            coin short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **balance** - object containing one property with your balance, AUD value and rate for that coin

        """
        request_data = {"cointype":cointype}
        return self._request("/api/v2/ro/my/balance/", request_data)

    def my_marketorders(self, cointype, markettype='AUD'):
        """
        My Open Market Orders

        :param cointype:
            (optional) coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            (optional) market coin short name, example value 'USDT', 'AUD'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - array containing your open buy orders
            - **sellorders** - array containing your open sell orders

        """
        request_data = {"cointype":cointype, "markettype":markettype}
        return self._request("/api/v2/ro/my/orders/market/open/", request_data)

    def my_limitorders(self, cointype):
        """
        My Open Limit Orders

        :param cointype:
            (optional) coin short name, example value 'BTC', 'LTC', 'DOGE'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - array containing your open buy orders
            - **sellorders** - array containing your open sell orders

        """
        request_data = {"cointype":cointype}
        return self._request("/api/v2/ro/my/orders/limit/open/", request_data)

    def my_orderhistory(self, cointype, markettype='AUD', **kwargs):
        """
        My Order History

        :param cointype:
            (optional) coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            (optional, available markets only)) market coin short name, example values 'AUD', 'USDT'
        :param startdate:
            (optional, note: date is UTC date or UNIX EPOCH time) format 'YYYY-MM-DD' or e.g. 1614824116
        :param enddate:
            (optional, note: date is UTC date or UNIX EPOCH time) format 'YYYY-MM-DD' or e.g. 1614824116
        :param limit:
            (optional, default is 200 records, max is 500 records)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - array containing your buy order history
            - **sellorders** - array containing your sell order history

        """
        # Required Parameters
        request_data = {"cointype":cointype, "markettype":markettype}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "startdate" or key == "enddate" or key == "limit":
                request_data[key] = value

        return self._request("/api/v2/ro/my/orders/completed/", request_data)

    def my_markethistory(self, cointype, markettype="AUD", **kwargs):
        """
        My Market Order History

        :param cointype:
            (optional) coin short name, example value 'BTC', 'LTC', 'DOGE'
        :param markettype:
            (optional, available markets only)) market coin short name, example values 'AUD', 'USDT'
        :param startdate:
            (optional, note: date is UTC date or UNIX EPOCH time) format 'YYYY-MM-DD' or e.g. 1614824116
        :param enddate:
            ((optional, note: date is UTC date or UNIX EPOCH time) format 'YYYY-MM-DD' or e.g. 1614824116
        :param limit:
            (optional, default is 200 records, max is 500 records)
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **buyorders** - array containing your buy order history
            - **sellorders** - array containing your sell order history

        """
        # Required parameters
        request_data = {"cointype":cointype, "markettype":markettype}
        
        # Optional parameters
        for key, value in kwargs.items():
            if key == "startdate" or key == "enddate" or key == "limit":
                request_data[key] = value

        return self._request("/api/v2/ro/my/orders/market/completed/", request_data)

    def my_transferhistory(self, **kwargs):
        """
        My Send & Receive History

        :param startdate:
            (optional) format 'YYYY-MM-DD'
        :param enddate:
            (optional) format 'YYYY-MM-DD'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **sendtransactions** - array containing your coin send transaction history
            - **receivetransactions** - array containing your coin receive transaction history

        """
        # Required parameter
        request_data = {}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "startdate" or key == "enddate":
                request_data[key] = value

        return self._request("/api/v2/ro/my/sendreceive/", request_data)

    def my_deposithistory(self, **kwargs):
        """
        My Deposit History

        :param startdate:
            (optional) format 'YYYY-MM-DD'
        :param enddate:
            (optional) format 'YYYY-MM-DD'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **deposits** - array containing your AUD deposit history

        """
        # Required parameter
        request_data = {}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "startdate" or key == "enddate":
                request_data[key] = value

        return self._request("/api/v2/ro/my/deposits/", request_data)

    def my_withdrawhistory(self, **kwargs):
        """
        My Withdrawal History

        :param startdate:
            (optional) format 'YYYY-MM-DD'
        :param enddate:
            (optional) format 'YYYY-MM-DD'
        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **withdrawals** - array containing your AUD withdrawal history

        """
        # Required parameter
        request_data = {}

        # Optional parameters
        for key, value in kwargs.items():
            if key == "startdate" or key == "enddate":
                request_data[key] = value
        
        return self._request("/api/v2/ro/my/withdrawals/", request_data)

    def my_affiliatepayments(self):
        """
        My Affiliate Payments

        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **payments** - array containing one object for each completed affiliate payment

        """
        request_data = {}
        return self._request("/api/v2/ro/my/affiliatepayments/", request_data)

    def my_referralpayment(self):
        """
        My Referral Payments

        :return:
            - **status** - ok, error
            - **message** - ok, description of error if error occurred
            - **payments** - array containing one object for each completed referral payment

        """
        request_data = {}
        return self._request("/api/v2/ro/my/referralpayments/", request_data)