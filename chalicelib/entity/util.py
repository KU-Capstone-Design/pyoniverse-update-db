from typing import Dict, Type

from chalicelib.entity.base import BaseEntity
from chalicelib.entity.brand import BrandEntity
from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity


ENTITY_MAP: Dict[str, Dict[str, Type[BaseEntity]]] = {
    "constant": {
        "brands": ConstantBrandEntity,
    },
    "service": {
        "brands": BrandEntity,
        "events": EventEntity,
        "products": ProductEntity,
    },
}


class ConstantConverter:
    """
    Convert id to name and vice versa
    """

    __brand_map = {
        1: {"name": "GS25", "slug": "gs25"},
        2: {"name": "CU", "slug": "cu"},
        3: {"name": "7-Eleven", "slug": "seven-eleven"},
        4: {"name": "Emart24", "slug": "emart24"},
        5: {"name": "CSpace", "slug": "c-space"},
    }

    __category_map = {
        1: {"name": "Drink", "slug": "drink"},
        2: {"name": "Alcohol", "slug": "alcohol"},
        3: {"name": "Snack", "slug": "snack"},
        4: {"name": "Ice Cream", "slug": "icecream"},
        5: {"name": "Noodle", "slug": "noodle"},
        6: {"name": "Lunch Box", "slug": "lunchbox"},
        7: {"name": "Salad", "slug": "salad"},
        8: {"name": "Kimbab", "slug": "kimbab"},
        9: {"name": "Sandwich", "slug": "sandwich"},
        10: {"name": "Bread", "slug": "bread"},
        11: {"name": "Food", "slug": "food"},
        12: {"name": "Household Goods", "slug": "household-goods"},
    }

    __event_map = {
        1: {"name": "1+1", "slug": "1+1"},
        2: {"name": "2+1", "slug": "2+1"},
        3: {"name": "GIFT", "slug": "gift"},
        4: {"name": "NEW", "slug": "new"},
        5: {"name": "MONOPOLY", "slug": "monopoly"},
        6: {"name": "RESERVATION", "slug": "reservation"},
        7: {"name": "DISCOUNT", "slug": "discount"},
        8: {"name": "3+1", "slug": "3+1"},
    }

    __currency_map = {1: {"name": "KRW", "slug": "krw"}}

    @classmethod
    def convert_brand_id(cls, brand_id: int) -> dict:
        return cls.__brand_map[brand_id]

    @classmethod
    def convert_brand_slug(cls, brand_slug: str) -> int | None:
        for _id, val in cls.__brand_map.items():
            if val["slug"] == brand_slug:
                return _id
        return None

    @classmethod
    def convert_category_id(cls, category_id: int) -> dict:
        return cls.__category_map[category_id]

    @classmethod
    def convert_event_id(cls, event_id: int) -> dict:
        return cls.__event_map[event_id]

    @classmethod
    def convert_currency(cls, currency_id: int) -> dict:
        return cls.__currency_map[currency_id]
