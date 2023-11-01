import typing
from dataclasses import dataclass, field
from typing import List

from marshmallow import EXCLUDE, Schema, fields, types

from chalicelib.io.slack.model.enum.message_enum import MessageTypeEnum


@dataclass(kw_only=True)
class SlackMessage:
    type: MessageTypeEnum
    source: str
    text: str
    cc: list
    ps: dict = field(default_factory=dict)

    class __MessageSchema(Schema):
        type: str = fields.Enum(required=True, enum=MessageTypeEnum)
        source: str = fields.Str(required=True)
        text: str = fields.Str(required=True)
        ps: dict = fields.Dict(
            allow_none=True,
            keys=fields.Str(),
            values=fields.Str(),
            load_default={},
        )
        cc: List[str] = fields.List(
            fields.Str(), required=True, validate=lambda x: len(x) > 0
        )

        class Meta:
            unknown = EXCLUDE

        def load(
            self,
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
            return SlackMessage(**res)

    @classmethod
    def load(cls, data: dict) -> "SlackMessage":
        return cls.__MessageSchema().load(data)
