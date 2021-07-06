import unittest
from json import loads
from websitecategorization import Response, ErrorMessage


_json_response_ok = '''{
    "categories": [
        {
            "tier1": {
                "confidence": 0.9499015947838411,
                "id":"IAB-596",
                "name":"Technology & Computing"
            },
            "tier2": {
                "confidence":0.8420597541031617,
                "id":"IAB-618",
                "name":"Information and Network Security"
            }
        },
        {
            "tier1": {
                "confidence":0.9499015947838411,
                "id":"IAB-596",
                "name":"Technology & Computing"
            },
            "tier2": {
                "confidence":0.6916495127489835,
                "id":"IAB-623",
                "name":"Email"
            }
        },
        {
            "tier1": {
                "confidence":0.9499015947838411,
                "id":"IAB-52",
                "name":"Business and Finance"
            },
            "tier2": {
                "confidence":0.6916495127489835,
                "id":"IAB-99",
                "name":"Information Services Industry"
            }
        },
        {
            "tier1": {
                "confidence":0.9499015947838411,
                "id":"IAB-52",
                "name":"Business and Finance"
            },
            "tier2": {
                "confidence":0.6916495127489835,
                "id":"IAB-115",
                "name":"Technology Industry"
            }
        },
        {
            "tier1": {
                "confidence":0.9499015947838411,
                "id":"IAB-52",
                "name":"Business and Finance"
            },
            "tier2": {
                "confidence":0.6916495127489835,
                "id":"IAB-116",
                "name":"Telecommunications Industry"
            }
        },
        {
            "tier1": {
                "confidence":0.9499015947838411,
                "id":"IAB-596",
                "name":"Technology & Computing"
            },
            "tier2": {
                "confidence":0.6087944770670476,
                "id":"IAB-619",
                "name":"Internet"
            }
        }
    ],
    "domainName": "whoisxmlapi.com",
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
            parsed.categories[0].tier1.id,
            response['categories'][0]['tier1']['id'])
        self.assertEqual(
            parsed.categories[0].tier1.name,
            response['categories'][0]['tier1']['name'])
        self.assertEqual(
            parsed.categories[0].tier1.confidence,
            response['categories'][0]['tier1']['confidence'])

        self.assertEqual(
            parsed.categories[0].tier2.id,
            response['categories'][0]['tier2']['id'])
        self.assertEqual(
            parsed.categories[0].tier2.name,
            response['categories'][0]['tier2']['name'])
        self.assertEqual(
            parsed.categories[0].tier2.confidence,
            response['categories'][0]['tier2']['confidence'])

        self.assertEqual(
            parsed.categories[1].tier1.id,
            response['categories'][1]['tier1']['id'])
        self.assertEqual(
            parsed.categories[1].tier1.name,
            response['categories'][1]['tier1']['name'])
        self.assertEqual(
            parsed.categories[1].tier1.confidence,
            response['categories'][1]['tier1']['confidence'])

    def test_error_parsing(self):
        error = loads(_json_response_error)
        parsed_error = ErrorMessage(error)
        self.assertEqual(parsed_error.code, error['code'])
        self.assertEqual(parsed_error.message, error['messages'])
