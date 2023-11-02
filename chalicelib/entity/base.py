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


EntityType = TypeVar("EntityType", bound=BaseEntity)
