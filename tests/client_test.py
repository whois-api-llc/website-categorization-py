import os
import unittest
from websitecategorization import Client
from websitecategorization import ParameterError, ApiAuthError

DOMAIN = 'whoisxmlapi.com'


class TestClient(unittest.TestCase):
    """
    Final integration tests without mocks.

    Active API_KEY is required.
    """
    def setUp(self) -> None:
        self.client = Client(os.getenv('API_KEY'))

    def test_get_correct_data(self):
        response = self.client.data(DOMAIN)
        self.assertIsNot(response.domain_name, '', "Empty domain in response")

    def test_extra_parameters(self):
        response = self.client.data(domain=DOMAIN, min_confidence=1.0)
        self.assertLessEqual(len(response.categories), 1)

    def test_empty_terms(self):
        with self.assertRaises(ParameterError):
            self.client.data('')

    def test_incorrect_api_key(self):
        client = Client('at_00000000000000000000000000000')
        with self.assertRaises(ApiAuthError):
            client.data(domain=DOMAIN)

    def test_raw_data(self):
        response = self.client.raw_data(
            domain=DOMAIN, output_format=Client.XML_FORMAT)
        self.assertTrue(response.startswith('<?xml'))


if __name__ == '__main__':
    unittest.main()
