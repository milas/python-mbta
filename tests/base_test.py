import os
import unittest


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MbtaApiTestCase(unittest.TestCase):
    @staticmethod
    def get_sample_resp(name):
        with open(os.path.join(BASE_DIR, 'sample_responses', name), encoding='utf-8') as f:
            return f.read()
