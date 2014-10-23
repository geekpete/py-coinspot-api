#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""fixtures.py: These are fixture functions for returning mocked api data."""

__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.2.1'
__license__ = 'GPLv3'
__source__ = 'http://github.com/geekpete/py-coinspot-api/coinspot.py'


def calls():
    return {
        '/api/spot': {
            "status": "ok",
             "spot": [
                 {"ltcspot": "4.891671"},
                 {"btcspot": "474.920000"},
                 {"dogespot": "0.000294"},
                 {"lotspot": "0.000005"},
                 {"ppcspot": "1.258258"},
                 {"wdcspot": "0.012348"},
                 {"qrkspot": "0.007371"},
                 {"moonspot": "0.000001"},
                 {"ftcspot": "0.042548"},
                 {"xpmspot": "0.233181"},
                 {"maxspot": "0.021371"}
            ]
        },
        '/api/quote/buy': {
            "status": "ok",
            "quote": 0.0004,
            "timeframe": 4
        },
        '/api/my/balances': {
            "status": "ok",
            "balance": [
                {"btc": 0},
                {"ltc": 0},
                {"doge": 0},
                {"ppc": 0},
                {"wdc": 0},
                {"xpm": 0},
                {"max": 0},
                {"lot": 0},
                {"qrk": 0},
                {"moon": 0},
                {"ftc": 0}
            ]
        },
        '/api/orders/history': {
            "status": "ok",
            "orders": [
                {"amount":108070,"rate":0.00036,"total":38.9052,"coin":"DOGE","solddate":1414029447346},
                {"amount":400000,"rate":0.00036,"total":144,"coin":"DOGE","solddate":1414028078529},
                {"amount":63328,"rate":0.00033,"total":20.89824,"coin":"DOGE","solddate":1414026957966},
                {"amount":44100,"rate":0.00036,"total":15.876,"coin":"DOGE","solddate":1414018270934},
                {"amount":2194.444444,"rate":0.00036,"total":0.79,"coin":"DOGE","solddate":1414017655259},
                {"amount":26094.893,"rate":0.000356,"total":9.289782,"coin":"DOGE","solddate":1414015639276},
                {"amount":16000,"rate":0.000356,"total":5.696,"coin":"DOGE","solddate":1413996783991},
                {"amount":30000,"rate":0.00032,"total":9.6,"coin":"DOGE","solddate":1413984643120},
                {"amount":17784.42905305,"rate":0.00032,"total":5.691017,"coin":"DOGE","solddate":1413973077259},
                {"amount":806.94430267,"rate":0.00031,"total":0.250153,"coin":"DOGE","solddate":1413971283577},
                {"amount":332,"rate":0.00035,"total":0.1162,"coin":"DOGE","solddate":1413968733430},
                {"amount":145322.6,"rate":0.00031,"total":45.050006,"coin":"DOGE","solddate":1413968754860},
                {"amount":57500,"rate":0.0003475,"total":19.98125,"coin":"DOGE","solddate":1413944365197},
                {"amount":150,"rate":0.0003475,"total":0.052125,"coin":"DOGE","solddate":1413944359771}
            ]
        }
    }
