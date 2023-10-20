import json
import os
from typing import Any, Dict, Sequence

from chalice import Chalice
from chalice.app import SQSEvent

from chalicelib.db.repository import Repository
from chalicelib.download.s3 import S3Downloader
from chalicelib.model.message import Message


app = Chalice(app_name="pyoniverse-update-db")
repository = Repository()
downloader = S3Downloader()


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"), batch_size=1)
def upsert(event: SQSEvent):
    result = {}
    for record in event:
        message = Message.load(json.loads(record.body))
        data: Sequence[Dict[str, Any]] = downloader.download(message.data)
        res = repository.upsert(
            rel_name=message.rel_name, db_name=message.db_name, data=data
        )
        app.log.info(f"{message.db_name}.{message.rel_name}: {dict(res)}")
        result[f"{message.db_name}.{message.rel_name}"] = res
    return result
