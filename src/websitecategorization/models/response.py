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


class Tier(BaseModel):
    confidence: float
    id: str
    name: str

    def __init__(self, values):
        super().__init__()
        self.confidence = 0.0
        self.name = ""
        self.id = ""

        if values is not None:
            self.confidence = _float_value(values, 'confidence')
            self.id = _string_value(values, 'id')
            self.name = _string_value(values, 'name')


class Category(BaseModel):
    tier1: Tier or None
    tier2: Tier or None

    def __init__(self, values):
        super().__init__()

        self.tier1 = None
        self.tier2 = None

        if values is not None:
            if 'tier1' in values and values['tier1']:
                self.tier1 = Tier(values['tier1'])
            if 'tier2' in values and values['tier2']:
                self.tier2 = Tier(values['tier2'])


class Response(BaseModel):
    domain_name: str
    website_responded: bool
    if sys.version_info < (3, 9):
        categories: typing.List[Category]
    else:
        categories: [Category]

    def __init__(self, values):
        super().__init__()

        self.domain_name = ""
        self.website_responded = False
        self.categories = []

        if values is not None:
            self.domain_name = _string_value(values, 'domainName')
            self.website_responded = _bool_value(values, 'websiteResponded')
            self.categories = _list_of_objects(
                values, 'categories', 'Category')


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
