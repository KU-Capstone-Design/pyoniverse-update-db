from dataclasses import dataclass, field
from typing import List, Optional

from chalicelib.entity.base import BaseEntity


@dataclass(kw_only=True)
class ProductBestEntity:
    price: float = field(default=None)
    brand: int = field(default=None)
    events: List[int] = field(default_factory=list)


@dataclass(kw_only=True)
class ProductPriceEntity:
    value: float = field()
    currency: int = field()
    discounted_value: Optional[float] = field(default=None)


@dataclass(kw_only=True)
class ProductBrandEntity:
    id: int = field()
    price: ProductPriceEntity = field()
    events: List[int] = field()


@dataclass(kw_only=True)
class ProductRecommendationEntity:
    products: list = field(default_factory=list)
    events: list = field(default_factory=list)


@dataclass(kw_only=True)
class ProductHistoryEntity:
    date: str = field(default=True)
    brands: List[ProductBrandEntity] = field(default_factory=list)


@dataclass(kw_only=True)
class ProductEntity(BaseEntity):
    best: ProductBestEntity = field(default_factory=ProductBestEntity)
    brands: List[ProductBrandEntity] = field(default_factory=list)
    category: int = field(default=None)
    description: str = field(default=None)
    image: str = field(default=None)
    name: str = field(default=None)
    price: float = field(default=None)
    recommendation: ProductRecommendationEntity = field(
        default_factory=ProductRecommendationEntity
    )
    good_count: int = field(default=None)
    view_count: int = field(default=None)
    histories: List[ProductHistoryEntity] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ProductEntity":
        return cls(
            id=data.get("id"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            best=ProductBestEntity(
                price=data.get("best", {}).get("price"),
                brand=data.get("best", {}).get("brand"),
                events=data.get("best", {}).get("events", []),
            ),
            brands=[
                ProductBrandEntity(
                    id=b.get("id"),
                    price=ProductPriceEntity(
                        value=b.get("price", {}).get("value"),
                        currency=b.get("price", {}).get("currency"),
                        discounted_value=b.get("price", {}).get("discounted_value"),
                    ),
                    events=b.get("events", []),
                )
                for b in data.get("brands", [])
            ],
            category=data.get("category"),
            description=data.get("description"),
            image=data.get("image"),
            name=data.get("name"),
            price=data.get("price"),
            recommendation=ProductRecommendationEntity(
                events=data.get("recommendation", {}).get("events"),
                products=data.get("recommendation", {}).get("products"),
            ),
            good_count=data.get("good_count"),
            view_count=data.get("view_count"),
            histories=[
                ProductHistoryEntity(
                    date=h.get("date"),
                    brands=[
                        ProductBrandEntity(
                            id=b.get("id"),
                            price=ProductPriceEntity(
                                value=b.get("price", {}).get("value"),
                                currency=b.get("price", {}).get("currency"),
                                discounted_value=b.get("price", {}).get(
                                    "discounted_value"
                                ),
                            ),
                            events=b.get("events", []),
                        )
                        for b in h.get("brands")
                    ],
                )
                for h in data.get("histories", [])
            ],
        )
