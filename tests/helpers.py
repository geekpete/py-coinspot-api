#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Peter Dyson <pete@geekpete.com>'
__version__ = '0.2.1'
__license__ = 'GPLv3'
__source__ = 'http://github.com/geekpete/py-coinspot-api/coinspot.py'

"""helpers.py: These are helper mock functions for testing this module."""

from mock import Mock
import fixtures
import json

def mock_api_request(path=None, *args, **kwargs):
    resp = Mock()
    data = fixtures.calls().get(path)
    resp.content = json.dumps(data)
    resp.headers = kwargs.get('headers')
    return resp
