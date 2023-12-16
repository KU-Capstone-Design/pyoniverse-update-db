import logging
from dataclasses import asdict

from pymongo import MongoClient, UpdateOne, WriteConcern

from chalicelib.core.interface.processor import QueryProcessorIfs
from chalicelib.core.model.query import Query
from chalicelib.core.model.result import Result
from chalicelib.entity.product import ProductEntity


class MigratorQueryProcessor(QueryProcessorIfs):
    def __init__(self, client: MongoClient):
        self.__client = client
        self.logger = logging.getLogger(__name__)

    def execute(self, query: Query) -> Result:
        match query.action:
            case "UPDATE":
                data = list(
                    map(lambda x: self.__validate(x, query.rel_name), query.data)
                )
                result: Result = self.__update(query=query, data=data)
            case _:
                raise RuntimeError(f"{query.action} should be in ['UPDATE', 'ADD']")
        return result

    def __validate(self, data: dict, rel_name: str) -> dict:
        match rel_name:
            case "products":
                entity = ProductEntity.from_dict(data)
            case _:
                raise RuntimeError(f"{rel_name} should be in ['products', 'events']")
        tmp = asdict(entity)
        result = {}
        for key, val in tmp.items():
            if key in data:
                result[key] = val
        if not result:
            # empty result
            raise RuntimeError(f"{rel_name} Schema doesn't support {data}")
        return result

    def __update(self, query: Query, data: list) -> Result:
        db = self.__client.get_database(
            query.db_name, write_concern=WriteConcern(w="majority", j=True)
        )
        buffer = [UpdateOne(filter={"id": d["id"]}, update={"$set": d}) for d in data]
        modified_count = 0
        for idx in range(0, len(buffer), 100):
            tmp = db[query.rel_name].bulk_write(buffer[idx : idx + 100])
            modified_count += tmp.modified_count
        result = Result(
            origin=query.origin,
            db_name=query.db_name,
            rel_name=query.rel_name,
            filter=query.filter,
            action=query.action,
            data=query.data,
            modified_count=modified_count,
        )
        return result
