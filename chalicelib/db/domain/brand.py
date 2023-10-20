from typing import Any, Dict, Sequence, Tuple

from chalicelib.db.repository_ifs import RepositoryIfs


class BrandRepository(RepositoryIfs):
    def __init__(self):
        super().__init__()
        self.__name = "brands"

    def _make_filter(self, data: Sequence[Dict[str, Any]]) -> Sequence[Dict[str, Any]]:
        filters = []
        for datum in data:
            filters.append({"id": datum["id"]})
        return filters

    def _make_hint(self) -> Sequence[Tuple[str, int]]:
        return [("id", 1)]
