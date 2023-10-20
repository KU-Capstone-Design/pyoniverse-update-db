import os

from chalice import Chalice
from chalice.app import SQSEvent


app = Chalice(app_name='pyoniverse-update-db')


@app.on_sqs_message(queue=os.getenv("QUEUE_NAME"), batch_size=10)
def update(event: SQSEvent):
    return {'hello': 'world2'}


@app.lambda_function
def make_and_send_msg_from_transform(event, context):
    pass
