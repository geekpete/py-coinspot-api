Python Coinspot API Library
===========================
A python library for the Coinspot API.

Source: [http://github.com/geekpete/py-coinspot-api](http://github.com/geekpete/py-coinspot-api)

Please see [https://www.coinspot.com.au/api](https://www.coinspot.com.au/api) for documentation on the CoinSpot API.

Example Usage
=============
```
import py-coinspot-api

key = 'xxxxx'
secret = 'yyyyyyyyyyyyyyy'

client = py-coinspot-api(key, secret)

client.orders('LTC')

client.myorders()

client.spot()

client.buy('BTC', 0.3, 529)

client.sell('DOGE', 0.3, 0.00024)
```