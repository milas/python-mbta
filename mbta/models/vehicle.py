import datetime
import enum

import jsonapi_requests

import mbta.api
from .common import MbtaModel
from .mixin import DirectionMixin, LocationMixin
from .orm import EnumField, TimestampField


class Vehicle(jsonapi_requests.orm.ApiModel, MbtaModel, DirectionMixin, LocationMixin):
    class Status(enum.Enum):
        IncomingAt = 'INCOMING_AT'
        StoppedAt = 'STOPPED_AT'
        InTransitTo = 'IN_TRANSIT_TO'

    class Meta:
        type = 'vehicle'
        path = 'vehicles'
        api = mbta.api.config

    speed: float = jsonapi_requests.orm.AttributeField('speed')
    longitude: float = jsonapi_requests.orm.AttributeField('longitude')
    latitude: float = jsonapi_requests.orm.AttributeField('latitude')
    last_updated: datetime.datetime = TimestampField('last_updated')
    label: str = jsonapi_requests.orm.AttributeField('label')
    direction_id: int = jsonapi_requests.orm.AttributeField('direction_id')
    current_stop_sequence: int = jsonapi_requests.orm.AttributeField('current_stop_sequence')
    status: Status = EnumField('current_status', enum_cls=Status, serialize_as_name=False)
    bearing: int = jsonapi_requests.orm.AttributeField('bearing')

    trip: 'mbta.Trip' = jsonapi_requests.orm.RelationField('trip')
    stop: 'mbta.Stop' = jsonapi_requests.orm.RelationField('stop')
    route: 'mbta.Route' = jsonapi_requests.orm.RelationField('route')

    def __str__(self):
        return f'{self.label} ({self.status})'
