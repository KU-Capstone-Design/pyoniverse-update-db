import os

from chalice import Chalice
from chalice.app import SQSEvent


app = Chalice(app_name="pyoniverse-update-db")


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"), batch_size=1)
def upsert(event: SQSEvent):
    return {"hello": "world2"}
