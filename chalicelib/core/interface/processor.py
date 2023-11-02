from abc import ABCMeta, abstractmethod

from chalicelib.core.model.query import Query
from chalicelib.core.model.result import Result


class QueryProcessorIfs(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, query: Query) -> Result:
        pass
