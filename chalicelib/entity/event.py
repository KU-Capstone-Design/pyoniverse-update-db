from dataclasses import dataclass, field
from typing import List

from chalicelib.entity.base import BaseEntity


@dataclass(kw_only=True)
class EventImageEntity:
    thumb: str = field(default=None)
    others: List[str] = field(default_factory=list)


@dataclass(kw_only=True)
class EventEntity(BaseEntity):
    brand: int = field(default=None)
    description: str = field(default=None)
    start_at: int = field(default=None)
    end_at: int = field(default=None)
    image: EventImageEntity = field(default_factory=EventImageEntity)
    name: str = field(default=None)
    good_count: int = field(default=None)
    view_count: int = field(default=None)

    @classmethod
    def from_dict(cls, data: dict) -> "EventEntity":
        return cls(
            id=data.get("id"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            brand=data.get("brand"),
            description=data.get("description"),
            start_at=data.get("start_at"),
            end_at=data.get("end_at"),
            image=EventImageEntity(
                thumb=data.get("image", {}).get("thumb"),
                others=data.get("image", {}).get("others", []),
            ),
            name=data.get("name"),
            good_count=data.get("good_count"),
            view_count=data.get("view_count"),
        )
