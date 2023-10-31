from typing import Any, Dict, Mapping, Sequence

from chalicelib.db.model.filter import Filter
from chalicelib.model.message import Message
from chalicelib.processor.processor_ifs import ProcessorIfs


class TransformProcessor(ProcessorIfs):
    def process(self, message: Message) -> Mapping[str, int]:
        data: Sequence[Dict[str, Any]] = self._downloader.download(message.data)
        res = self._repository.upsert(
            rel_name=message.rel_name, db_name=message.db_name, data=data
        )
        # status 바꾸기
        invalid_result = self._repository.update_many(
            rel_name=message.rel_name,
            db_name=message.db_name,
            _filter={"status": Filter(op="lt", value=2)},
            datum={"status": -1},
        )
        valid_result = self._repository.update_many(
            rel_name=message.rel_name,
            db_name=message.db_name,
            _filter={"status": Filter(op="eq", value=2)},
            datum={"status": 1},
        )
        self.logger.info(f"invalid: {invalid_result}, valid: {valid_result}")
        result = {"invalid": invalid_result, "valid": valid_result}
        return result
