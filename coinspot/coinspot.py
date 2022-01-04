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

    def _request(self, path, postdata):
        nonce = int(time() * 1000000)
        postdata["nonce"] = nonce
        params = json.dumps(postdata, separators=(",", ":"))
        signedMessage = self._get_signed_request(params)
        headers = {}
        headers["Content-type"] = "application/json"
        headers["Accept"] = "text/plain"
        headers["key"] = self._api_key
        headers["sign"] = signedMessage
        headers["User-Agent"] = (
            "py-coinspot-api/%s (https://github.com/geekpete/py-coinspot-api)"
            % __version__
        )
        if self._debug:
            logging.warning(self.timestamp + " " + str(headers))
        conn = http.client.HTTPSConnection(self._endpoint)
        if self._debug:
            conn.set_debuglevel(1)
        response_data = '{"status":"invalid","error": "Did not make request"}'
        try:
            conn.request("POST", path, params, headers)
            response = conn.getresponse()
            if self._debug:
                logging.warning(self.timestamp + " " + str(response))
                logging.warning(self.timestamp + " " + str(response.msg))
            # print response.status, response.reason
            response_data = response.read()
            if self._debug:
                logging.warning(self.timestamp + " " + str(response_data))
            conn.close()
        except IOError as error:
            if self._debug:
                error_text = "Attempting to make request I/O error({0}): {1}".format(
                    error.errno, error.strerror
                )
                logging.warning(self.timestamp + " " + error_text)
                response_data = '{"status":"invalid","error": "' + error_text + '"}'
        except:
            exit("Unexpected error: {0}".format(sys.exc_info()[0]))

        return response_data
