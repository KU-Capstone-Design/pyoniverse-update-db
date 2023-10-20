from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Mapping, Sequence

from chalicelib.db.model.filter import Filter


class RepositoryFacade_ifs(metaclass=ABCMeta):
    @abstractmethod
    def upsert(
        self, rel_name: str, db_name: str, data: Sequence[Dict[str, Any]]
    ) -> Mapping[str, int]:
        pass

    @abstractmethod
    def update_many(
        self,
        rel_name: str,
        db_name: str,
        _filter: Dict[str, Filter],
        datum: Dict[str, Any],
    ) -> Mapping[str, int]:
        pass
