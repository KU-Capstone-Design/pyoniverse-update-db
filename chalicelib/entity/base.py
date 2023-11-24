from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar


@dataclass(kw_only=True)
class BaseEntity:
    id: int = field(default=None)
    status: int = field(default=None)
    created_at: datetime = field(default=None)
    updated_at: datetime = field(default=None)

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "BaseEntity":
        pass


@dataclass(kw_only=True)
class CrawledInfoEntity:
    spider: str = field(default=None)
    id: str = field(default=None)
    url: str = field(default=None)
    brand: int = field(default=None)

    @classmethod
    def from_dict(cls, data: dict) -> "CrawledInfoEntity":
        return cls(
            spider=data.get("spider"),
            id=data.get("id"),
            url=data.get("url"),
            brand=data.get("brand"),
        )


EntityType = TypeVar("EntityType", bound=BaseEntity)
