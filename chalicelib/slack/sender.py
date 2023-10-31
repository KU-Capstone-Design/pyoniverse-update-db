import json
import logging
import os
from dataclasses import asdict
from typing import NoReturn

import boto3

from chalicelib.slack.model.message import SlackMessage


class SlackSender:
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)

    def send(self, message: SlackMessage) -> NoReturn:
        try:
            sqs_client = boto3.client("sqs")
            sqs_queue_url: str = sqs_client.get_queue_url(
                QueueName=os.getenv("SLACK_QUEUE_NAME")
            )["QueueUrl"]
            sqs_client.send_message(
                QueueUrl=sqs_queue_url,
                MessageBody=json.dumps(asdict(message)),
            )
        except Exception as e:
            self.logger.error(e)
            raise RuntimeError(e)
