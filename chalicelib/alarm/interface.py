from abc import ABCMeta, abstractmethod

from chalicelib.core.model.result import Result


class AlarmIfs(metaclass=ABCMeta):
    @abstractmethod
    def notice(self, result: Result):
        pass
