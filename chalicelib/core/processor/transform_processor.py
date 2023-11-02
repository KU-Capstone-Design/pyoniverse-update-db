import json
import logging
import traceback
from collections import defaultdict
from dataclasses import asdict
from typing import Any, Dict, List, Sequence

import boto3
from pymongo import MongoClient, UpdateOne, WriteConcern
from pymongo.results import BulkWriteResult, UpdateResult

from chalicelib.core.interface.processor import QueryProcessorIfs
from chalicelib.core.model.query import Query
from chalicelib.core.model.result import Result
from chalicelib.entity.base import EntityType
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity


class TransformQueryProcessor(QueryProcessorIfs):
    def __init__(self, client: MongoClient):
        self.__client = client
        self.logger = logging.getLogger(__name__)

    def execute(self, query: Query) -> Result:
        """
        :param query: {"bucket": s3-bucket, "keys": [key list]}
        """
        bucket, keys = query.data["bucket"], query.data["keys"]
        data: Sequence[Dict[str, Any]] = self.__download(bucket=bucket, keys=keys)
        entities: Sequence[EntityType] = [
            self.__convert_to_entity(rel_name=query.rel_name, datum=d) for d in data
        ]
        result: Result = self.__write(entities=entities, query=query)
        return result

    def __download(self, bucket: str, keys: List[str]) -> Sequence[Dict[str, Any]]:
        s3 = boto3.resource("s3")
        res = []
        for key in keys:
            try:
                response = s3.Object(bucket, key).get()
                res += json.loads(response["Body"].read().decode())
                self.logger.info(f"Download data from s3://{bucket}{key}")
            except Exception as e:
                if "NoSuchKey" in traceback.format_exc():
                    self.logger.error(f"s3://{bucket}{key} NOT FOUND")
                else:
                    self.logger.error(traceback.format_exc())
                continue
        return res

    def __convert_to_entity(self, rel_name: str, datum: Dict[str, Any]) -> EntityType:
        match rel_name:
            case "products":
                return ProductEntity.from_dict(datum)
            case "events":
                return EventEntity.from_dict(datum)
            case _:
                self.logger.error(f"{rel_name} should be in [products, events]")
                raise RuntimeError(f"{rel_name} should be in [products, events]")

    def __write(
        self, query: Query, entities: Sequence[ProductEntity | EventEntity]
    ) -> Result:
        db = self.__client.get_database(
            query.db_name, write_concern=WriteConcern(w="majority", j=True)
        )
        filters = []
        data = []
        for entity in entities:
            _filter = {
                "crawled_infos.spider": {
                    "$in": [c.spider for c in entity.crawled_infos]
                },
                "crawled_infos.id": {"$in": [c.id for c in entity.crawled_infos]},
            }
            filters.append(_filter)

            datum = {}
            tmp = asdict(entity)
            for key, val in tmp.items():
                if val is not None:
                    datum[key] = val
            data.append(datum)

        buffer = [
            UpdateOne(filter=_filter, update={"$set": datum}, upsert=True)
            for _filter, datum in zip(filters, data)
        ]

        tmp_result = defaultdict(int)
        for p in range(0, len(buffer), 100):
            res: BulkWriteResult = db[query.rel_name].bulk_write(buffer[p : p + 100])
            tmp_result["matched_count"] += res.matched_count
            tmp_result["modified_count"] += res.modified_count
            tmp_result["inserted_count"] += res.inserted_count
            tmp_result["upserted_count"] += res.upserted_count
            tmp_result["deleted_count"] += res.deleted_count

        # change status
        # status 바꾸기
        updated_res: UpdateResult = db[query.rel_name].update_many(
            filter={"status": {"$lt": 2}}, update={"$set": {"status": -1}}
        )
        tmp_result["modified_count"] = updated_res.modified_count
        updated_res: UpdateResult = db[query.rel_name].update_many(
            filter={"status": 2}, update={"$set": {"status": 1}}
        )
        tmp_result["modified_count"] = updated_res.modified_count

        result = Result(
            origin=query.origin,
            db_name=query.db_name,
            rel_name=query.rel_name,
            filter=query.filter,
            action=query.action,
            data=query.data,
            modified_count=tmp_result["modified_count"]
            + tmp_result["inserted_count"]
            + tmp_result["upserted_count"]
            + tmp_result["deleted_count"],
        )
        return result
