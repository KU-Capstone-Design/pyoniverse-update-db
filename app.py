import json
import os
from typing import Mapping

from chalice import Chalice
from chalice.app import BadRequestError, SQSEvent

from chalicelib.db.mongo.repositoryfacade import MongoRepositoryFacade
from chalicelib.dependency_injector.resource import ResourceInjector
from chalicelib.download.s3 import S3Downloader
from chalicelib.model.message import Message
from chalicelib.processor.domain.transform_processor import TransformProcessor


app = Chalice(app_name="pyoniverse-update-db", debug=False)
resource_injector = ResourceInjector()
resource_injector.init_resources()

repository = MongoRepositoryFacade(client=resource_injector.client)
downloader = S3Downloader()
transform_processor = TransformProcessor(downloader, repository)


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"), batch_size=1)
def upsert(event: SQSEvent):
    result = {}
    for record in event:
        message = Message.load(json.loads(record.body))
        app.log.info(message)
        match message.origin:
            case "transform":
                res: Mapping[str, int] = transform_processor.process(message)
            case _:
                raise BadRequestError(f"{message.origin} Not Supported")
        result[f"{message.db_name}.{message.rel_name}({message.origin})"] = res
    app.log.info(result)
    return result
