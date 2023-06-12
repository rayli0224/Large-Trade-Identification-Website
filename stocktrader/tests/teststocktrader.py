from django.test import TestCase
from handler import large_trade_identifier

class TestGoodInputs(TestCase):
    def test_lower_case(self):
        json, csv = large_trade_identifier.get_large_trades("aapl")
        self.assertNotEqual(json, {})
    def test_upper_case(self):
        json, csv = large_trade_identifier.get_large_trades("AAPL")
        self.assertNotEqual(json, {})
    def test_random_case(self):
        json, csv = large_trade_identifier.get_large_trades("aApl")
        self.assertNotEqual(json, {})

