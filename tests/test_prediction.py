import os
import unittest

import requests_mock

from mbta.models import common, prediction

from tests.base_test import MbtaApiTestCase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@requests_mock.Mocker()
# @requests_mock.Mocker(real_http=True)
class PredictionTest(MbtaApiTestCase):
    def test_get_predictions(self, m):
        m.get(
            'https://api-v3.mbta.com/predictions?filter[stop]=place-bbsta&filter[route]=Orange&filter[direction_id]=1&page[offset]=0&page[limit]=3',
            complete_qs=True,
            text=self.get_sample_resp('pred-bbsta-orange.json')
        )

        m.get(
            'https://api-v3.mbta.com/routes/Orange',
            text=self.get_sample_resp('route-orange.json')
        )

        preds = prediction.Prediction.find(
            stop='place-bbsta',
            route='Orange',
            include=[],
            direction='1',
            page=common.Page(0, 3)
        )

        self.assertEqual(3, len(preds))

        for pred in preds:
            self.assertEqual('Orange', pred.route.id)
            self.assertEqual('70015', pred.stop.id)
            self.assertEqual(1, pred.direction_id)
            # this will invoke a load of the route
            self.assertEqual('Northbound', pred.direction_name)
            self.assertEqual('Orange Line', pred.route.name)
