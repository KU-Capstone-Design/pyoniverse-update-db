import logging
from typing import List

from chalicelib.core.interface.parser import MessageParser
from chalicelib.core.model.message import Data, Filter, Message
from chalicelib.core.model.query import Query


class MongoMessageParser(MessageParser):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse(self, message: Message) -> Query:
        query = Query(
            db_name=message.db_name,
            rel_name=message.rel_name,
            action=message.action,
            filter=self.__get_filter(message.filters),
            data=self.__get_data(message.data),
        )
        return query

    def __get_filter(self, filters: List[Filter]) -> dict | None:
        """
        한 필드에 해당하는 여러 Filter가 있다면 가장 마지막 것만 선택된다.
        """
        if not filters:
            return None
        result = {}
        for _filter in filters:
            tmp = self.__make_filter(_filter)
            result.update(tmp)
        return result

    def __make_filter(self, _filter: Filter) -> dict:
        match _filter.op:
            case "lt":
                result = {_filter.column: {"$lt": _filter.value}}
            case "eq":
                result = {_filter.column: {"$eq": _filter.value}}
            case "gt":
                result = {_filter.column: {"$gt": _filter.value}}
            case "le":
                result = {_filter.column: {"lte": _filter.value}}
            case "ge":
                result = {_filter.column: {"gte": _filter.value}}
            case "in":
                result = {_filter.column: {"in": _filter.value}}
            case _:
                self.logger.error(f"Fail to parse message's filter: {_filter}")
                raise RuntimeError(f"Fail to parse message's filter: {_filter}")
        return result

    def __get_data(self, data: List[Data]) -> dict | None:
        """
        한 필드에 해당하는 여러 Data가 있다면 마지막 것만 취한다.
        """
        if not data:
            return None
        result = {}
        for datum in data:
            tmp = self.__make_datum(datum)
            result.update(tmp)
        return result

    def __make_datum(self, datum: Data) -> dict:
        result = {datum.column: datum.value}
        return result
