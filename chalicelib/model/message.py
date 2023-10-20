import typing
from dataclasses import dataclass
from datetime import datetime
from typing import List

from marshmallow import EXCLUDE, Schema, fields, types


@dataclass
class Message:
    date: datetime
    origin: str
    rel_name: str
    db_name: str
    data: List[str]

    class __MessageSchema(Schema):
        date = fields.Date(required=True, format="iso")
        origin = fields.Str(required=True)
        rel_name = fields.Str(required=True)
        db_name = fields.Str(required=True)
        data = fields.List(fields.Str(required=True), required=True)

        class Meta:
            unknown = EXCLUDE

        def load(
            cls,
            data: (
                typing.Mapping[str, typing.Any]
                | typing.Iterable[typing.Mapping[str, typing.Any]]
            ),
            *,
            many: bool | None = None,
            partial: bool | types.StrSequenceOrSet | None = None,
            unknown: str | None = None,
        ):
            res = super().load(data, many=many, partial=partial, unknown=unknown)
            return Message(**res)

    @classmethod
    def load(cls, data: dict) -> "Message":
        return cls.__MessageSchema().load(data)
