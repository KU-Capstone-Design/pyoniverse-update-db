import logging
from dataclasses import asdict

from pymongo import MongoClient, WriteConcern
from pymongo.results import UpdateResult

from chalicelib.core.interface.processor import QueryProcessorIfs
from chalicelib.core.model.query import Query
from chalicelib.core.model.result import Result
from chalicelib.entity.product import ProductEntity


class ApiQueryProcessor(QueryProcessorIfs):
    def __init__(self, client: MongoClient):
        self.__client = client
        self.logger = logging.getLogger(__name__)

    def execute(self, query: Query) -> Result:
        """
        :param query: {"bucket": s3-bucket, "keys": [key list]}
        """
        data = self.__validate(query.data, query.rel_name)
        match query.action:
            case "UPDATE":
                result: Result = self.__update(query=query, data=data)
            case _:
                raise RuntimeError(f"{query.action} should be in ['UPDATE']")
        return result

    def __validate(self, data: dict, rel_name: str) -> dict:
        match rel_name:
            case "products":
                entity = ProductEntity.from_dict(data)
            case "events":
                entity = ProductEntity.from_dict(data)
            case _:
                raise RuntimeError(f"{rel_name} should be in ['products', 'events']")
        tmp = asdict(entity)
        result = {}
        for key, val in tmp.items():
            if val is not None:
                result[key] = val
        if not result:
            # empty result
            raise RuntimeError(f"{rel_name} Schema doesn't support {data}")
        return result

    def __update(self, query: Query, data: dict) -> Result:
        """
        filter와 일치하는 "모든" 데이터를 업데이트한다.
        """
        db = self.__client.get_database(
            query.db_name, write_concern=WriteConcern(w="majority", j=True)
        )
        res: UpdateResult = db[query.rel_name].update_many(
            filter=query.filter, update={"$set": data}, upsert=False
        )
        result = Result(
            origin=query.origin,
            db_name=query.db_name,
            rel_name=query.rel_name,
            filter=query.filter,
            action=query.action,
            data=query.data,
            modified_count=res.modified_count,
        )
        return result
