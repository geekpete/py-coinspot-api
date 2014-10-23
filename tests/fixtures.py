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
        '/api/quote/buy':{
            "status": "ok",
            "quote": "0.0004",
            "timeframe": "4"
        }
    }
