from dataclasses import dataclass, field

from chalicelib.entity.base import BaseEntity


@dataclass(kw_only=True)
class ConstantBrandEntity(BaseEntity):
    name: str = field(default=None)
    slug: str = field(default=None)
    image: str = field(default=None)

    @classmethod
    def from_dict(cls, data: dict) -> "ConstantBrandEntity":
        return cls(
            id=data.get("id"),
            status=data.get("status"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            name=data.get("name"),
            slug=data.get("slug"),
            image=data.get("image"),
        )
