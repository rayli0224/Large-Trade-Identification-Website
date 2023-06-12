from django.test import TestCase


class LoadsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200)
    def test_signup_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000/search')
        self.assertEqual(response.status_code, 200)
    def test_search_loads_properly(self):
        response = self.client.get('http://127.0.0.1:8000/signup')
        self.assertEqual(response.status_code, 200)
