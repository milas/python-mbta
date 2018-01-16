import enum
import typing

import jsonapi_requests

import mbta.api
from .common import MbtaModel
from .mixin import DirectionMixin
from .orm import EnumField


class Route(jsonapi_requests.orm.ApiModel, MbtaModel, DirectionMixin):
    class Meta:
        type = 'route'
        path = 'routes'
        api = mbta.api.config

    class Type(enum.Enum):
        LightRail = 0
        HeavyRail = 1
        CommuterRail = 2
        Bus = 3
        Ferry = 4

    route_type: Type = EnumField('type', enum_cls=Type, serialize_as_name=False)
    sort_order: int = jsonapi_requests.orm.AttributeField('sort_order')
    short_name: str = jsonapi_requests.orm.AttributeField('short_name')
    long_name: str = jsonapi_requests.orm.AttributeField('long_name')
    direction_names: typing.List[str] = jsonapi_requests.orm.AttributeField('direction_names')
    description: str = jsonapi_requests.orm.AttributeField('description')

    def __str__(self):
        return f'{self.name}'

    @property
    def name(self):
        return self.long_name or self.short_name

    @classmethod
    def find(cls, *args):
        return cls.get_list(params=cls.build_params(*args))
