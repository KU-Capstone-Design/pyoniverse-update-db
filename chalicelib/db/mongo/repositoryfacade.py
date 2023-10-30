import logging
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Tuple

from chalice import BadRequestError
from pymongo import MongoClient, UpdateOne, WriteConcern
from pymongo.errors import ConfigurationError
from pymongo.results import BulkWriteResult, UpdateResult

from chalicelib.db.model.filter import Filter
from chalicelib.db.mongo.brand import BrandRepository
from chalicelib.db.mongo.converter import MongoFilterConverter
from chalicelib.db.mongo.event import EventRepository
from chalicelib.db.mongo.product import ProductRepository
from chalicelib.db.repositoryfacade_ifs import RepositoryFacade_ifs


class MongoRepositoryFacade(RepositoryFacade_ifs):
    def __init__(self):
        self.__client = MongoClient(os.getenv("MONGO_URI"))
        try:
            self.__client.admin.command("ping")
        except ConfigurationError:
            logging.error("Cannot connect to client")
            exit(1)

        self.__filter_converter = MongoFilterConverter()

    def upsert(
        self, rel_name: str, db_name: str, data: Sequence[Dict[str, Any]]
    ) -> Mapping[str, int]:
        """
        각 데이터마다 필터가 있고, 하나씩 업데이트된다.
        """
        match rel_name:
            case "products":
                filters = ProductRepository()._make_filter(data=data)
                hint = ProductRepository()._make_hint()
            case "events":
                filters = EventRepository()._make_filter(data=data)
                hint = EventRepository()._make_hint()
            case "brands":
                filters = BrandRepository()._make_filter(data=data)
                hint = BrandRepository()._make_hint()
            case _:
                raise BadRequestError(f"{rel_name} not in [products, events, brands")
        res = self.__bulk_write(
            db_name=db_name,
            rel_name=rel_name,
            filters=filters,
            data=data,
            hint=hint,
        )
        return res

    def __bulk_write(
        self,
        db_name: str,
        rel_name: str,
        hint: Sequence[Tuple[str, int]],
        filters: Sequence[Dict[str, Any]],
        data: Sequence[Dict[str, Any]],
    ) -> Mapping[str, int]:
        """
        :return: 실행 결과 반환
        """
        buffer = []
        for _filter, _datum in zip(filters, data):
            _datum["updated_at"] = datetime.utcnow()
            buffer.append(
                UpdateOne(
                    filter=_filter,
                    update={"$set": _datum},
                    upsert=True,
                    hint=hint,
                )
            )
        result = defaultdict(int)
        if buffer:
            db = self.__client.get_database(
                db_name, write_concern=WriteConcern(w="majority", wtimeout=5000)
            )
            for p in range(0, len(buffer), 100):
                tmp = buffer[p : p + 100]
                res: BulkWriteResult = db[rel_name].bulk_write(tmp, ordered=False)
                result["matched_count"] += res.matched_count
                result["updated_count"] += res.modified_count
                result["inserted_count"] += res.upserted_count
                result["deleted_count"] += res.deleted_count
        result["total_count"] = len(buffer)
        return result

    def update_many(
        self,
        rel_name: str,
        db_name: str,
        _filter: Dict[str, Filter],
        datum: Dict[str, Any],
    ) -> Mapping[str, int]:
        _filter = {k: self.__filter_converter.convert(v) for k, v in _filter.items()}
        db = self.__client.get_database(
            db_name, write_concern=WriteConcern(w="majority", wtimeout=5000)
        )
        datum["updated_at"] = datetime.utcnow()
        res: UpdateResult = db[rel_name].update_many(
            filter=_filter,
            update={"$set": datum},
        )
        result = {
            "matched_count": res.matched_count,
            "updated_count": res.modified_count,
        }
        return result
