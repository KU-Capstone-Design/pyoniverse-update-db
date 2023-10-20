import os
from collections import defaultdict
from typing import Any, Dict, NoReturn, Sequence, Tuple

from chalice import BadRequestError
from pymongo import MongoClient, UpdateOne, WriteConcern
from pymongo.results import BulkWriteResult

from chalicelib.db.domain.brand import BrandRepository
from chalicelib.db.domain.event import EventRepository
from chalicelib.db.domain.product import ProductRepository


class RepositoryFacade:
    def __init__(self):
        self.__client = MongoClient(os.getenv("MONGO_URI"))

    def upsert(
        self, rel_name: str, db_name: str, data: Sequence[Dict[str, Any]]
    ) -> NoReturn:
        match rel_name:
            case "products":
                filters = ProductRepository()._make_filter(data=data)
                hint = ProductRepository()._make_hint()
            case "events":
                filters = EventRepository()._make_filter(data=data)
                hint = ProductRepository()._make_hint()
            case "brands":
                filters = BrandRepository()._make_filter(data=data)
                hint = ProductRepository()._make_hint()
            case _:
                raise BadRequestError(f"{rel_name} not in [products, events, brands")
        res = self._bulk_write(
            db_name=db_name,
            rel_name=rel_name,
            filters=filters,
            data=data,
            hint=hint,
        )
        return {rel_name: res}

    def _bulk_write(
        self,
        db_name: str,
        rel_name: str,
        hint: Sequence[Tuple[str, int]],
        filters: Sequence[Dict[str, Any]],
        data: Sequence[Dict[str, Any]],
    ) -> Dict[str, int]:
        """
        :return: 실행 결과 반환
        """
        buffer = []
        for _filter, _datum in zip(filters, data):
            buffer.append(
                UpdateOne(
                    filter=_filter,
                    update=_datum,
                    upsert=True,
                    hint=hint,
                )
            )

        result = defaultdict(int)
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
        return result
