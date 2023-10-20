from typing import Any, Dict

from chalice import BadRequestError

from chalicelib.db.repository import Repository


class BrandRepository(Repository):
    def __init__(self):
        super().__init__()
        self.__name = "brands"

    def upsert(self, rel_name: str, db_name: str, data: list) -> Dict[str, Any]:
        """
        :param rel_name: relation name
        :param db_name: db_name
        :param data: List[Dict] <- Fully Document
        :return: 성공 여부
        """
        if rel_name != self.__name:
            raise BadRequestError(f"{rel_name} != {self.__name}")
        # filter 만들기
        filters = self._make_filter(data)
        # data update
        res = self._bulk_write(
            db_name=db_name,
            rel_name=rel_name,
            filters=filters,
            data=data,
            hint=[("id", 1)],
        )
        return {self.__name: res}

    def _make_filter(self, data: list) -> list:
        filters = []
        for datum in data:
            filters.append({"id": datum["id"]})
        return filters
