import unittest
from json import loads
from websitecategorization import Response, ErrorMessage


_json_response_ok = '''{
  "as": {
    "asn": 13335,
    "domain": "https://www.cloudflare.com",
    "name": "CLOUDFLARENET",
    "route": "172.67.64.0/20",
    "type": "Content"
  },
  "domainName": "whoisxmlapi.com",
  "categories": [
    {
      "confidence": 0.85,
      "id": 5,
      "name": "Computer and Internet Info"
    }
  ],
  "createdDate": "2009-03-19T21:47:17+00:00",
  "websiteResponded": true
}'''

_json_response_error = '''{
    "code": 403,
    "messages": "Access restricted. Check credits balance or enter the correct API key."
}'''


class TestModel(unittest.TestCase):

    def test_response_parsing(self):
        response = loads(_json_response_ok)
        parsed = Response(response)
        self.assertEqual(parsed.domain_name, response['domainName'])
        self.assertEqual(
            parsed.website_responded, response['websiteResponded'])
        self.assertIsInstance(parsed.categories, list)
        self.assertEqual(
            parsed.categories[0].id,
            response['categories'][0]['id'])
        self.assertEqual(
            parsed.categories[0].name,
            response['categories'][0]['name'])
        self.assertEqual(
            parsed.categories[0].confidence,
            response['categories'][0]['confidence'])

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        self.assertEqual(parsed_error.code, error['code'])
        self.assertEqual(parsed_error.message, error['messages'])
