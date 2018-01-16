import unittest

import requests_mock

from mbta.models import route, stop
from mbta.models.common import Point, WheelchairAccess

from tests.base_test import MbtaApiTestCase


class StopTest(MbtaApiTestCase):
    @requests_mock.Mocker()
    def test_get_stop_by_id(self, m):
        m.get('https://api-v3.mbta.com/stops/70015',
              text=self.get_sample_resp('stop-70015.json'))

        m.get('https://api-v3.mbta.com/stops/place-bbsta',
              text=self.get_sample_resp('stop-place-bbsta.json'))

        s = stop.Stop.from_id('70015')
        self.assertEqual('Back Bay - Inbound', s.name)
        self.assertIs(WheelchairAccess.Accessible, s.wheelchair)
        self.assertEqual(Point(latitude=42.34735, longitude=-71.075727), s.location)

        self.assertEqual('place-bbsta', s.parent_station.id)
        self.assertEqual('Back Bay', s.parent_station.name)

    @requests_mock.Mocker()
    def test_nearby(self, m):
        m.get('https://api-v3.mbta.com/stops?filter[route_type]=3&filter[radius]=0.001&filter[latitude]=42.302298&filter[longitude]=-71.1111743',
              text=self.get_sample_resp('stop-nearby.json'),
              complete_qs=True)

        loc = Point(latitude=42.302298, longitude=-71.1111743)
        stops = stop.Stop.nearby(loc, 0.001, route_type=route.Route.Type.Bus)

        self.assertEqual(1, len(stops))
        s = stops[0]
        self.assertEqual('Washington St opp Burnett St', s.name)
        self.assertEqual(Point(latitude=42.302682, longitude=-71.111044), s.location)
        self.assertEqual(WheelchairAccess.Unknown, s.wheelchair)

