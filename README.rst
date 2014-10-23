Python Coinspot API Library
===========================

|Build Status|

A python library for the Coinspot cryptocurrency trading API.

Copyright (C) 2014 Peter Dyson pete@geekpete.com

Source: http://github.com/geekpete/py-coinspot-api

PyPi Package: https://pypi.python.org/pypi/py-coinspot-api/

Please see https://www.coinspot.com.au/api for documentation on the
CoinSpot API.

**NOTE:** All requests and responses will be JSON

Installation
============
Install with pip via

::

    
      pip install py-coinspot-api --user

or

::

      
      sudo pip install py-coinspot-api
      
Configuration
=============

The library requires credentials to access the API.
These can be stored in your script or for more separation in a YAML config file.

The config.yml.sample needs to be copied to config.yml and your unique
api key and secret values need to be inserted.

::

  api:
    key: 'PUT_YOUR_KEY_HERE'
    secret: 'PUT_YOUR_SECRET_HERE'
    endpoint: 'www.coinspot.com.au'
  logfile: 'coinspot.log'

Your python program would then be configured to load the YAML config file on start up,
to get the credentials to provide to the library without the credentials being hard coded
in your script.

For example::

  #!/usr/bin/env python



Class Documentation
===================

http://py-coinspot-api.readthedocs.org/en/latest/

TODO
====

-  Extend test cases and requirements.

Example Usage
=============

::

    from coinspot import CoinSpot
    
    # initialise the library with credentials
    client = CoinSpot(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

    # get the spot prices
    print client.spot()

    # get your coin wallet balances
    print client.balances()

    # get the last 1000 orders for Dogecoins
    print client.orderhistory('DOGE')

    # get a list of all the current buy and sell orders
    print client.orders('DOGE')

    # put an order in to sell 20 Dogecoins at 0.000280 per coin
    print client.sell('DOGE', '20', '0.000280')

    # Get a quote on buying a billion Dogecoins, with estimation of timeframe
    print client.quotebuy('DOGE', 1000000000)

    # Donate a craptonne of Dogecoins 
    # to the author of this library! Much Appreciate!!!
    print client.send('DOGE', 'DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs', 1000)

Send Dogecoins of appreciation
==============================

If you like this software, you can always send cold hard cryptocoin my
way

::

    Dogecoin: DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs
    Bitcoin: 1LybpYphZJqSAxjNFqjfYHB8pWxKcBmFkf

You can do this using the library like this:
::

    # Donate a craptonne of Dogecoins to the author of this library! 
    # Much Appreciate!!!
    print client.send('DOGE', 'DJrHRxurwQoBUe7r9RsMkMrTxj92wXd5gs', 10000)

or send Bitcoins:
::

    # Donate a craptonne of Bitcoins to the author of this library!
    print client.send('BTC', '1LybpYphZJqSAxjNFqjfYHB8pWxKcBmFkf', 1)

License
=======

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

Change Log
==========

-  0.1.1 Initial Release
-  0.2.2 Logging Support, Initial Test Cases, Exception Handling, Travis
   Support, Configuration File Example

.. |Build Status| image:: https://travis-ci.org/monk-ee/py-coinspot-api.png?branch=master
   :target: https://travis-ci.org/monk-ee/py-coinspot-api
