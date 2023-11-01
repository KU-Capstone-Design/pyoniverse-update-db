import logging
from typing import Any, Dict, Mapping, Sequence

from chalicelib.io.downloader import S3Downloader
from chalicelib.model.message import Message
from chalicelib.persistant.repository import MongoRepository


class TransformProcessor:
    def __init__(self, repository: MongoRepository, downloader: S3Downloader):
        self.__repository = repository
        self.__downloader = downloader
        self.logger = logging.getLogger(__name__)

    def process(self, message: Message) -> Mapping[str, Mapping[str, int]]:
        data: Sequence[Dict[str, Any]] = self.__downloader.download(message.data)
        res = self.__repository.upsert(
            rel_name=message.rel_name, db_name=message.db_name, data=data
        )
        # status 바꾸기
        invalid_result = self.__repository.update_many(
            rel_name=message.rel_name,
            db_name=message.db_name,
            _filter={"status": {"$lt": 2}},
            datum={"status": -1},
        )
        valid_result = self.__repository.update_many(
            rel_name=message.rel_name,
            db_name=message.db_name,
            _filter={"status": {"$eq": 2}},
            datum={"status": 1},
        )
        self.logger.info(f"invalid: {invalid_result}, valid: {valid_result}")
        result = {"invalid": invalid_result, "valid": valid_result}
        return result
