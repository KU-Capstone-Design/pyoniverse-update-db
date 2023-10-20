from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Sequence, Tuple


class RepositoryIfs(metaclass=ABCMeta):
    @abstractmethod
    def _make_filter(self, data: Sequence[Dict[str, Any]]) -> Sequence[Dict[str, Any]]:
        pass

    @abstractmethod
    def _make_hint(self) -> Sequence[Tuple[str, int]]:
        pass
