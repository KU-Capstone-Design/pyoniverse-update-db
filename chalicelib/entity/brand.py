from dataclasses import dataclass, field
from typing import List

from chalicelib.entity.base import BaseEntity


@dataclass(kw_only=True)
class BrandProductEntity:
    id: int = field(default=None)
    image: str = field(default=None)
    image_alt: str = field(default=None)
    name: str = field(default=None)
    good_count: int = field(default=None)
    view_count: int = field(default=None)
    price: float = field(default=None)
    events: List[str] = field(default=None)
    event_price: float = field(default=None)


@dataclass(kw_only=True)
class BrandEventEntity:
    brand: str = field(default=None)
    image: str = field(default=None)
    name: str = field(default=None)
    id: int = field(default=None)
    image_alt: str = field(default=None)
    start_at: str = field(default=None)
    end_at: str = field(default=None)
    good_count: int = field(default=None)
    view_count: int = field(default=None)


@dataclass(kw_only=True)
class BrandMetaEntity:
    description: str = field(default=None)


@dataclass(kw_only=True)
class BrandEntity(BaseEntity):
    slug: str = field(default=None)
    name: str = field(default=None)
    meta: BrandMetaEntity = field(default_factory=BrandMetaEntity)
    description: str = field(default=None)
    events: List[BrandEventEntity] = field(default_factory=list)
    products: List[BrandProductEntity] = field(default_factory=list)
    image: str = field(default=None)
    image_alt: str = field(default=None)

    @classmethod
    def from_dict(cls, data: dict) -> "BrandEntity":
        return cls(
            id=data.get("id"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            slug=data.get("slug"),
            name=data.get("name"),
            meta=BrandMetaEntity(description=data.get("meta", {}).get("description")),
            description=data.get("description"),
            events=[
                BrandEventEntity(
                    brand=e.get("brand"),
                    image=e.get("image"),
                    image_alt=e.get("image_alt"),
                    name=e.get("name"),
                    id=e.get("id"),
                    start_at=e.get("start_at"),
                    end_at=e.get("end_at"),
                    good_count=e.get("good_count"),
                    view_count=e.get("view_count"),
                )
                for e in data.get("events", [])
            ],
            products=[
                BrandProductEntity(
                    id=p.get("id"),
                    image=p.get("image"),
                    image_alt=p.get("image_alt"),
                    name=p.get("name"),
                    good_count=p.get("good_count"),
                    view_count=p.get("view_count"),
                    price=p.get("price"),
                    events=p.get("events", []),
                    event_price=p.get("event_price"),
                )
                for p in data.get("products", [])
            ],
            image=data.get("image"),
            image_alt=data.get("image_alt"),
        )
