import json
import os
import traceback

from chalice import Chalice
from chalice.app import BadRequestError, SQSEvent

from chalicelib.extern.dependency_injector.resource import ResourceInjector
from chalicelib.downloader import S3Downloader
from chalicelib.alarm.slack.model.enum.message_enum import MessageTypeEnum
from chalicelib.alarm.slack.model.message import SlackMessage
from chalicelib.alarm.slack.alarm import SlackAlarm
from chalicelib.model.message import Message
from chalicelib.persistant.repository import MongoRepository
from chalicelib.core.processor.transform_processor import TransformQueryProcessor


app = Chalice(app_name="pyoniverse-update-db", debug=False)
resource_injector = ResourceInjector()
resource_injector.init_resources()

repository = MongoRepository(client=resource_injector.client())
downloader = S3Downloader(bucket=os.getenv("S3_BUCKET"))
transform_processor = TransformQueryProcessor(
    downloader=downloader, repository=repository
)
slack_sender = SlackAlarm(slack_queue_name=os.getenv("SLACK_QUEUE_NAME"))


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"), batch_size=1)
def upsert(event: SQSEvent):
    try:
        result = {}
        for record in event:
            message = Message.load(json.loads(record.body))
            app.log.info(message)
            match message.origin:
                case "transform":
                    res = transform_processor.process(message)
                case _:
                    raise BadRequestError(f"{message.origin} Not Supported")
            result[f"{message.db_name}.{message.rel_name}({message.origin})"] = res
            slack_sender.send(
                message=SlackMessage(
                    type=MessageTypeEnum.SUCCESS,
                    source=app.app_name,
                    text=f"{message.db_name}.{message.rel_name}({message.origin})",
                    cc=["윤영로"],
                )
            )
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
