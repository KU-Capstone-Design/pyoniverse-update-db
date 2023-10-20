from abc import ABCMeta, abstractmethod

from chalicelib.db.model.filter import Filter


class FilterConverterIfs(metaclass=ABCMeta):
    @abstractmethod
    def convert(self, _filter: Filter):
        pass
