from typing import Any, Dict, Sequence, Tuple

from chalicelib.db.repository_ifs import RepositoryIfs


class EventRepository(RepositoryIfs):
    def _make_filter(self, data: Sequence[Dict[str, Any]]) -> Sequence[Dict[str, Any]]:
        filters = []
        for datum in data:
            filters.append(
                {
                    "crawled_infos.spider": {
                        "$in": [d["spider"] for d in datum["crawled_infos"]]
                    },
                    "crawled_infos.id": {
                        "$in": [d["id"] for d in datum["crawled_infos"]]
                    },
                }
            )
        return filters

    def _make_hint(self) -> Sequence[Tuple[str, int]]:
        return [("crawled_infos.spider", 1), ("crawled_infos.id", 1)]
