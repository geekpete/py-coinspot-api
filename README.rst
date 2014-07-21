Python Coinspot API Library
===========================

A python library for the Coinspot API.

Copyright (C) 2014 Peter Dyson pete@geekpete.com

Source: http://github.com/geekpete/py-coinspot-api

Please see https://www.coinspot.com.au/api for documentation on the
CoinSpot API.

**NOTE:** All requests and responses will be JSON

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

TODO
====

-  Add exception handling.

Example Usage
=============

::

    from coinspot import Coinspot

    api_key = 'xxxxx'
    api_secret = 'yyyyyyyyyyyyyyy'

    client = Coinspot(api_key, api_secret)

    print client.orders('LTC')

    print client.myorders()

    print client.spot()

    print client.buy('BTC', 0.3, 529)

    print client.sell('DOGE', 0.3, 0.00024)

    # Donate a craptonne of Dogecoins to the author of this library! Much Appreciate!!!
    print client.send('DOGE', 'DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs', 10000)

