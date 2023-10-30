import copy

from .base import BaseModel
import sys

if sys.version_info < (3, 9):
    import typing


def _string_value(values: dict, key: str) -> str:
    if key in values and values[key]:
        return str(values[key])
    return ''


def _float_value(values: dict, key: str) -> float:
    if key in values and values[key]:
        return float(values[key])
    return 0.0


def _int_value(values: dict, key: str) -> int:
    if key in values and values[key]:
        return int(values[key])
    return 0


def _list_value(values: dict, key: str) -> list:
    if key in values and type(values[key]) is list:
        return copy.deepcopy(values[key])
    return []


def _list_of_objects(values: dict, key: str, classname: str) -> list:
    r = []
    if key in values and type(values[key]) is list:
        r = [globals()[classname](x) for x in values[key]]
    return r


def _bool_value(values: dict, key: str) -> bool:
    if key in values and values[key]:
        return bool(values[key])
    return False


class Category(BaseModel):
    confidence: float
    id: int
    name: str

    def __init__(self, values):
        super().__init__()
        self.confidence = 0.0
        self.name = ""
        self.id = 0

        if values is not None:
            self.confidence = _float_value(values, 'confidence')
            self.id = _int_value(values, 'id')
            self.name = _string_value(values, 'name')


class AS(BaseModel):
    asn: int
    domain: str
    name: str
    route: str
    type: str

    def __init__(self, values):
        super().__init__()
        self.asn = 0
        self.domain = ""
        self.name = ""
        self.route = ""
        self.type = ""

        if values is not None:
            self.asn = _int_value(values, 'asn')
            self.domain = _string_value(values, 'domain')
            self.name = _string_value(values, 'name')
            self.route = _string_value(values, 'route')
            self.type = _string_value(values, 'type')


class Response(BaseModel):
    as_field: AS or None
    domain_name: str
    if sys.version_info < (3, 9):
        categories: typing.List[Category]
    else:
        categories: [Category]
    created_date: str or None
    website_responded: bool

    def __init__(self, values):
        super().__init__()

        self.as_field = None
        self.domain_name = ""
        self.categories = []
        self.created_date = None
        self.website_responded = False

        if values is not None:
            if 'as' in values and values['as']:
                self.as_field = AS(values['as'])
            self.domain_name = _string_value(values, 'domainName')
            self.categories = _list_of_objects(values, 'categories', 'Category')
            self.created_date = _string_value(values, 'createdDate')
            self.website_responded = _bool_value(values, 'websiteResponded')


class ErrorMessage(BaseModel):
    code: int
    message: str

    def __init__(self, values):
        super().__init__()

        self.int = 0
        self.message = ''

        if values is not None:
            self.code = _int_value(values, 'code')
            self.message = _string_value(values, 'messages')
