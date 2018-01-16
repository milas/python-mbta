import jsonapi_requests

import mbta.api
from .common import MbtaModel, WheelchairAccess
from .mixin import DirectionMixin
from .orm import EnumField


class Trip(jsonapi_requests.orm.ApiModel, MbtaModel, DirectionMixin):
    class Meta:
        type = 'trip'
        path = 'trips'
        api = mbta.api.config

    wheelchair = EnumField('wheelchair_accessible', enum_cls=WheelchairAccess, serialize_as_name=False)
    name = jsonapi_requests.orm.AttributeField('name')
    headsign = jsonapi_requests.orm.AttributeField('headsign')
    direction_id = jsonapi_requests.orm.AttributeField('direction_id')
    block_id = jsonapi_requests.orm.AttributeField('block_id')

    # shape = jsonapi_requests.orm.RelationField('shape')
    route = jsonapi_requests.orm.RelationField('route')
    service = jsonapi_requests.orm.RelationField('service')

    def __repr__(self):
        return f'{self.name} ({self.headsign})'
