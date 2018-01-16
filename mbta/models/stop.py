import typing

import jsonapi_requests

import mbta.api
from .common import MbtaModel, Point, WheelchairAccess
from .mixin import LocationMixin
from .orm import EnumField


class Stop(jsonapi_requests.orm.ApiModel, MbtaModel, LocationMixin):
    class Meta:
        type = 'stop'
        path = 'stops'
        api = mbta.api.config

    wheelchair: WheelchairAccess = EnumField('wheelchair_boarding', enum_cls=WheelchairAccess, serialize_as_name=False)
    name: str = jsonapi_requests.orm.AttributeField('name')
    longitude: float = jsonapi_requests.orm.AttributeField('longitude')
    latitude: float = jsonapi_requests.orm.AttributeField('latitude')

    parent_station: 'mbta.Stop' = jsonapi_requests.orm.RelationField('parent_station')

    def __str__(self):
        return f'{self.name} ({self.latitude}, {self.longitude})'

    @classmethod
    def find(cls, *args):
        params = cls.build_params(*args)
        return cls.get_list(params=params)

    @classmethod
    def nearby(cls,
               loc: Point,
               radius: typing.Optional[float]=None,
               route_type: typing.Optional['mbta.Route.Type']=None):

        params = cls.build_params(
            cls.make_multifilter('route_type', route_type.value if route_type else None),
            cls.make_multifilter('radius', radius),
            location=loc
        )

        return cls.get_list(params=params)
