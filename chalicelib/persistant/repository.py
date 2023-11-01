import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Tuple

from pymongo import MongoClient, UpdateOne, WriteConcern
from pymongo.results import BulkWriteResult, UpdateResult


class MongoRepository:
    def __init__(self, client: MongoClient):
        self.logger = logging.getLogger(__name__)
        self.__client = client

    def upsert(
        self, rel_name: str, db_name: str, data: Sequence[Dict[str, Any]]
    ) -> Mapping[str, int]:
        """
        각 데이터마다 필터가 있고, 하나씩 업데이트된다.
        """
        if rel_name not in {"products", "events"}:
            self.logger.error(f"{rel_name} should be in [products, events]")
            raise RuntimeError(f"{rel_name} should be in [products, events]")
        filters = []
        for d in data:
            _filter = {
                "crawled_infos.spider": {
                    "$in": [c["spider"] for c in d["crawled_infos"]]
                },
                "crawled_infos.id": {"$in": [c["id"] for c in d["crawled_infos"]]},
            }
            filters.append(_filter)
        hint = [("crawled_infos.spider", 1), ("crawled_infos.id", 1)]
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
                db_name, write_concern=WriteConcern(w="majority", j=True)
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
        _filter: dict,
        datum: Dict[str, Any],
    ) -> Mapping[str, int]:
        db = self.__client.get_database(
            db_name, write_concern=WriteConcern(w="majority", j=True)
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
        self.logger.info(f"Upsert result: {result}")
        return result
