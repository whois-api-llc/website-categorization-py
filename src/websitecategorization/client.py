from json import loads, JSONDecodeError
import re

from .net.http import ApiRequester
from .models.response import Response
from .exceptions.error import ParameterError, EmptyApiKeyError, \
    UnparsableApiResponseError


class Client:
    __default_url = "https://website-categorization.whoisxmlapi.com/api/v2"
    _api_requester: ApiRequester or None
    _api_key: str

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)
    _re_domain_name = re.compile(
        r'^(?:[0-9a-z_](?:[0-9a-z-_]{0,62}(?<=[0-9a-z-_])[0-9a-z_])?\.)+'
        + r'[0-9a-z][0-9a-z-]{0,62}[a-z0-9]$', re.IGNORECASE)
    _SUPPORTED_FORMATS = ['json', 'xml']

    _PARSABLE_FORMAT = 'json'

    JSON_FORMAT = 'json'
    XML_FORMAT = 'xml'
    CSV_FORMAT = 'csv'

    __DATETIME_OR_NONE_MSG = 'Value should be None or an instance of ' \
                             'datetime.date'

    def __init__(self, api_key: str, **kwargs):
        """
        :param api_key: str: Your API key.
        :key base_url: str: (optional) API endpoint URL.
        :key timeout: float: (optional) API call timeout in seconds
        """

        self._api_key = ''

        self.api_key = api_key

        if 'base_url' not in kwargs:
            kwargs['base_url'] = Client.__default_url

        self.api_requester = ApiRequester(**kwargs)

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = Client._validate_api_key(value)

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def base_url(self) -> str:
        return self._api_requester.base_url

    @base_url.setter
    def base_url(self, value: str or None):
        if value is None:
            self._api_requester.base_url = Client.__default_url
        else:
            self._api_requester.base_url = value

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def data(self, domain: str,
             min_confidence: float or None = None) -> Response:
        """
        Get parsed API response as a `Response` instance.

        :param domain: Domain name, string
        :param min_confidence: Minimal confidence value. The higher this
            value the fewer false-positive results will be returned, float
        :return: `Response` instance
        :raises ConnectionError:
        :raises WebsiteCategorizationApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        output_format = Client._PARSABLE_FORMAT

        response = self.raw_data(domain, min_confidence, output_format)
        try:
            parsed = loads(str(response))
            if 'domainName' in parsed:
                return Response(parsed)
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError("Could not parse API response", error)

    def raw_data(self, domain: str, min_confidence: float or None = None,
                 output_format: str or None = None) -> str:
        """
        Get raw API response.

        :param domain: Domain name, string
        :param min_confidence: Minimal confidence value. The higher this
            value the fewer false-positive results will be returned, float
        :param output_format: Use Client.JSON_FORMAT, Client.XML_FORMAT,
            Client.CSV_FORMAT constants
        :return: str
        :raises ConnectionError:
        :raises WebsiteCategorizationApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        if self.api_key == '':
            raise EmptyApiKeyError('')

        _domain = Client._validate_domain_name(domain)
        _confidence = Client._validate_confidence(min_confidence) \
            if min_confidence is not None else None
        _output_format = Client._validate_output_format(output_format) \
            if output_format is not None else None

        return self._api_requester.get(self._build_payload(
            self.api_key,
            _domain,
            _confidence,
            _output_format
        ))

    @staticmethod
    def _validate_api_key(api_key) -> str:
        if Client._re_api_key.search(
                str(api_key)
        ) is not None:
            return str(api_key)
        else:
            raise ParameterError("Invalid API key format.")

    @staticmethod
    def _validate_domain_name(value) -> str:
        if Client._re_domain_name.search(str(value)) is not None:
            return str(value)

        raise ParameterError("Invalid domain name")

    @staticmethod
    def _validate_output_format(value: str):
        if value.lower() in {Client.JSON_FORMAT,
                             Client.XML_FORMAT, Client.CSV_FORMAT}:
            return value.lower()

        raise ParameterError(
            f"Response format must be {Client.JSON_FORMAT} "
            f"or {Client.XML_FORMAT} or {Client.CSV_FORMAT}")

    @staticmethod
    def _validate_confidence(value: float):
        if type(value) is float and 0.0 < value <= 1.0:
            return value

        raise ParameterError("min_confidence should be a float "
                             "number in range (0; 1)")

    @staticmethod
    def _build_payload(
            api_key,
            domain,
            min_confidence,
            output_format
    ) -> dict:
        tmp = {
            'apiKey': api_key,
            'domainName': domain,
            'minConfidence': min_confidence,
            'outputFormat': output_format
        }

        return {k: v for (k, v) in tmp.items() if v is not None}
