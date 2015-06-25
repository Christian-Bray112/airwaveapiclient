# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import unittest
from airwaveapiclient import AirWaveAPIClient


class UnitTests(unittest.TestCase):

    """Class UnitTests.

    Unit test for airwaveapiclient.

    """

    def setUp(self):
        """Setup."""
        self.obj = AirWaveAPIClient(username='admin',
                                    password='password',
                                    address='192.168.1.1')
