import json
import logging
import traceback
from datetime import datetime

from chalice import Chalice
from chalice.app import SQSEvent

from chalicelib.core.model.message import Data, Filter, Message
from chalicelib.core.model.query import Query
from chalicelib.core.model.result import Result
from chalicelib.extern.dependency_injector.injector import Injector
from chalicelib.extern.dependency_injector.resource import ResourceInjector


resource_injector = ResourceInjector()
resource_injector.init_resources()
injector = Injector(client=resource_injector.client())
injector.config.slack_queue_name.from_env("SLACK_QUEUE_NAME", required=True)
injector.config.queue_name.from_env("QUEUE_NAME", required=True)

transform_processor = injector.transform_query_processor()
message_parser = injector.message_parser()
slack_alarm = injector.slack_alarm()

app = Chalice(app_name="pyoniverse-update-db", debug=False)
logger = logging.getLogger(__name__)


@app.on_sqs_message(queue=injector.config.queue_name, batch_size=1)
def upsert(event: SQSEvent):
    try:
        for record in event:
            logger.info(f"Receive {record.body}")
            try:
                body = json.loads(record.body)
                message = Message(
                    origin=body["origin"],
                    date=datetime.strptime(body["date"], "%Y-%m-%dT%H:%M:%S"),
                    db_name=body["db_name"],
                    rel_name=body["rel_name"],
                    action=body["action"],
                    filters=[
                        Filter(
                            op=_filter["op"],
                            column=_filter["column"],
                            value=_filter["value"],
                        )
                        for _filter in body["filters"]
                    ],
                    data=[
                        Data(column=d["column"], value=d["value"]) for d in body["data"]
                    ],
                )
            except Exception as e:
                raise RuntimeError(f"Invalid message format: {record.body}")
            try:
                query: Query = message_parser.parse(message)
            except Exception as e:
                raise RuntimeError(f"Cannot parse {message}")
            try:
                match message.origin:
                    case "transform":
                        result: Result = transform_processor.execute(query=query)
                    case _:
                        raise RuntimeError(f"{message.origin} Not Supported")
            except Exception as e:
                raise RuntimeError(
                    f"Cannot process query(origin={message.origin}): {query}"
                )
            else:
                logger.info(result)
                slack_alarm.notice(result=result)
    except Exception as e:
        logger.error(traceback.format_exc())
        result = Result(
            origin=app.app_name, action="ERROR REPORT", data=traceback.format_exc()
        )
        slack_alarm.notice(result)
