import logging
from abc import ABCMeta, abstractmethod
from typing import Mapping

from chalicelib.model.message import Message


class ProcessorIfs(metaclass=ABCMeta):
    def __init__(self, downloader, repository):
        self._downloader = downloader
        self._repository = repository
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def process(self, message: Message) -> Mapping[str, Mapping[str, int]]:
        """
        :param message: Message
        :return: 실행 결과 반환. Ex) {"products": {"matched_count": 10, "modified_count": 1, ...}}
        """
        pass
