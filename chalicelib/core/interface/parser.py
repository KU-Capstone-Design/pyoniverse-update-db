from abc import ABCMeta, abstractmethod

from chalicelib.core.model.message import Message
from chalicelib.core.model.query import Query


class MessageParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, message: Message) -> Query:
        pass
