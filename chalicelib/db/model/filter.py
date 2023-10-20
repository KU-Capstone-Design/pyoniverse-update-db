import typing
from dataclasses import dataclass
from typing import Any, Literal

from marshmallow import Schema, fields, types


@dataclass
class Filter:
    op: Literal["eq", "le", "lt", "ge", "gt", "ne"]
    value: Any

    class __FilterSchema(Schema):
        op = fields.Str(
            required=True, validate=lambda x: x in {"eq", "le", "l", "ge", "g", "neq"}
        )
        value = fields.Raw(required=True)

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
            return Filter(**res)

    @classmethod
    def load(cls, data) -> "Filter":
        return cls.__FilterSchema().load(data)
