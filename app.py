import json
import os
import traceback
from typing import Mapping

from chalice import Chalice
from chalice.app import BadRequestError, SQSEvent

from chalicelib.db.mongo.repositoryfacade import MongoRepositoryFacade
from chalicelib.dependency_injector.resource import ResourceInjector
from chalicelib.io.downloader import S3Downloader
from chalicelib.io.slack.model.enum.message_enum import MessageTypeEnum
from chalicelib.io.slack.model.message import SlackMessage
from chalicelib.io.slack.sender import SlackSender
from chalicelib.model.message import Message
from chalicelib.processor.domain.transform_processor import TransformProcessor


app = Chalice(app_name="pyoniverse-update-db", debug=False)
resource_injector = ResourceInjector()
resource_injector.init_resources()

repository = MongoRepositoryFacade(client=resource_injector.client())
downloader = S3Downloader(bucket=os.getenv("S3_BUCKET"))
transform_processor = TransformProcessor(downloader, repository)
slack_sender = SlackSender(slack_queue_name=os.getenv("SLACK_QUEUE_NAME"))


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"), batch_size=1)
def upsert(event: SQSEvent):
    try:
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
    except Exception as e:
        app.log.error(str(e))
        slack_sender.send(
            message=SlackMessage(
                type=MessageTypeEnum.ERROR,
                source=app.app_name,
                text=traceback.format_exc(),
                cc=["윤영로"],
            )
        )
