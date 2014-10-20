#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""__init__.py: Init for unit testing this module."""

__author__ = "monkee"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "monk-ee"
__email__ = "magic.monkee.magic@gmail.com"
__status__ = "Development"

import unittest

from coinspot.tests.coinspotTestCase import TheStretcherTestCase


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TheStretcherTestCase))
    return suite
