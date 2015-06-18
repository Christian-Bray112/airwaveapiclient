# -*- coding: utf-8 -*-

"""UnitTests for airwaveapiclient."""

import unittest
from airwaveapiclient.airwaveapiclient import AirWaveAPIClient


class UnitTests(unittest.TestCase):

    """Class UnitTests.

    Unit test for airwaveapiclient.

    """

    def setUp(self):
        """Setup."""
        self.obj = AirWaveAPIClient(username='admin',
                                    password='password',
                                    address='192.168.1.1')

    def test_airwaveapiclient(self):
        """test airwaveapiclient."""
        # self.assertEqual(self.obj, True)

    def test_start_time_init(self):
        """Test start time initialize."""
        start_times = (60,
                       3600,
                       7200)
        obj = AirWaveAPIClient(username='admin',
                               password='password',
                               address='192.168.1.1',
                               start_times=start_times)
        self.assertEqual(obj.start_times[0], start_times[0])
        self.assertEqual(obj.start_times[1], start_times[1])
        self.assertEqual(obj.start_times[2], start_times[2])

        obj = AirWaveAPIClient(username='admin',
                               password='password',
                               address='192.168.1.1')
        self.assertEqual(len(obj.start_times), 12)

    def test_time_label(self):
        """Test time_label."""
        label = AirWaveAPIClient.time_label(3600*24*180)
        self.assertEqual(label, '180 day(s)')

        label = AirWaveAPIClient.time_label(3600*24*2)
        self.assertEqual(label, '2 day(s)')

        label = AirWaveAPIClient.time_label(3600*24)
        self.assertEqual(label, '1 day(s)')

        label = AirWaveAPIClient.time_label(3600*12)
        self.assertEqual(label, '12 hour(s)')

        label = AirWaveAPIClient.time_label(3600)
        self.assertEqual(label, '1 hour(s)')

        label = AirWaveAPIClient.time_label(60*10)
        self.assertEqual(label, '10 minute(s)')

        label = AirWaveAPIClient.time_label(60)
        self.assertEqual(label, '1 minute(s)')

        label = AirWaveAPIClient.time_label(1)
        self.assertEqual(label, '1 second(s)')

        label = AirWaveAPIClient.time_label(0)
        self.assertEqual(label, '0 second(s)')
