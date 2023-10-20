import json
import os

from chalice import Chalice
from chalice.app import SQSEvent

from chalicelib.model.message import Message


app = Chalice(app_name="pyoniverse-update-db")


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"), batch_size=1)
def upsert(event: SQSEvent):
    for record in event:
        message = Message.load(json.loads(record.body))
