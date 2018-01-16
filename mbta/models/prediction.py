import datetime
import enum
import typing

import jsonapi_requests

import mbta.api
from .common import MbtaModel, Point
from .mixin import DirectionMixin
from .orm import EnumField, TimestampField


class Prediction(jsonapi_requests.orm.ApiModel, MbtaModel, DirectionMixin):
    class Meta:
        type = 'prediction'
        path = 'predictions'
        api = mbta.api.config

    class Status(enum.Enum):
        Added = 'ADDED'
        Cancelled = 'CANCELLED'
        NoData = 'NO_DATA'
        Skipped = 'SKIPPED'
        Unscheduled = 'UNSCHEDULED'

    track: str = jsonapi_requests.orm.AttributeField('track')
    stop_sequence: int = jsonapi_requests.orm.AttributeField('stop_sequence')
    status: Status = EnumField('status', enum_cls=Status, serialize_as_name=False)
    schedule_relationship = jsonapi_requests.orm.AttributeField('schedule_relationship')
    direction_id: int = jsonapi_requests.orm.AttributeField('direction_id')
    departure_time: datetime.datetime = TimestampField('departure_time')
    arrival_time: datetime.datetime = TimestampField('arrival_time')

    trip: 'mbta.Trip' = jsonapi_requests.orm.RelationField('trip')
    stop: 'mbta.Stop' = jsonapi_requests.orm.RelationField('stop')
    route: 'mbta.Route' = jsonapi_requests.orm.RelationField('route')
    vehicle: 'mbta.Vehicle' = jsonapi_requests.orm.RelationField('vehicle')

    def __str__(self):
        return f'{self.id}: arrives @ {self.arrival_time} / departs @ {self.departure_time}'

    @classmethod
    def find(cls, *,
             stop: typing.Union[str, typing.Iterable[str]] = None,
             route: typing.Union[str, typing.Iterable[str]] = None,
             trip: typing.Union[str, typing.Iterable[str]] = None,
             direction: typing.Union[str, typing.Iterable[str]] = None,
             location: Point = None,
             **kwargs) -> typing.Iterable['Prediction']:
        filters = [
            cls.make_multifilter('stop', stop),
            cls.make_multifilter('route', route),
            cls.make_multifilter('trip', trip),
            cls.make_multifilter('direction_id', direction)
        ]

        params = cls.build_params(
            *filters,
            location=location,
            include=kwargs.pop('include', ['trip', 'route']),
            **kwargs
        )
        return cls.get_list(params=params)
