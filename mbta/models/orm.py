import datetime
import enum
import typing

import iso8601
from jsonapi_requests.orm import AttributeField


class TimestampField(AttributeField):
    def deserialize(self, raw_value: str) -> datetime.datetime:
        return iso8601.parse_date(raw_value) if raw_value is not None else None

    def serialize(self, raw_value: datetime.datetime) -> str:
        return raw_value.isoformat() if raw_value is not None else None


class EnumField(AttributeField):
    E = typing.TypeVar('E', bound=enum.Enum)

    def __init__(self, source, enum_cls: typing.Type[E], serialize_as_name: bool=False):
        super().__init__(source)
        self.enum_cls = enum_cls
        self.serialize_as_name = serialize_as_name

    def deserialize(self, json_value: str) -> E:
        try:
            return self.enum_cls(json_value) if json_value is not None else None
        except ValueError:
            return self.enum_cls[json_value]

    def serialize(self, value: E):
        return value.name if self.serialize_as_name else value.value
