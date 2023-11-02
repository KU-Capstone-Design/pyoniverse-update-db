from dataclasses import dataclass, field


@dataclass(kw_only=True, frozen=True)
class Result:
    origin: str = field(default=None)
    db_name: str = field(default=None)
    rel_name: str = field(default=None)
    action: str = field(default=None)
    filter: dict | None = field(default=None)
    data: dict | None = field(default=None)
    modified_count: int = field(default=None)
