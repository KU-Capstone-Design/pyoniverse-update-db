from typing import Any, Dict, Mapping, Sequence

from chalicelib.model.message import Message
from chalicelib.processor.processor_ifs import ProcessorIfs


class TransformProcessor(ProcessorIfs):
    def process(self, message: Message) -> Mapping[str, int]:
        data: Sequence[Dict[str, Any]] = self._downloader.download(message.data)
        res = self._repository.upsert(
            rel_name=message.rel_name, db_name=message.db_name, data=data
        )
        return res
