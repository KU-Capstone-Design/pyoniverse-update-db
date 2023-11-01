import json
import logging
from dataclasses import asdict
from typing import NoReturn

import boto3

from chalicelib.io.slack.model.message import SlackMessage


class SlackSender:
    def __init__(self, slack_queue_name: str, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        if not slack_queue_name:
            self.logger.error(f"{slack_queue_name} shouldn't be none")
            raise RuntimeError(f"{slack_queue_name} shouldn't be none")
        self.__sqs_client = boto3.client("sqs")
        try:
            self.__sqs_queue_url: str = self.__sqs_client.get_queue_url(
                QueueName=slack_queue_name
            )["QueueUrl"]
        except Exception as e:
            self.logger.error(f"There's no queue: {slack_queue_name}")
            raise RuntimeError(f"There's no queue: {slack_queue_name}")

    def send(self, message: SlackMessage) -> NoReturn:
        try:
            self.__sqs_client.send_message(
                QueueUrl=self.__sqs_queue_url,
                MessageBody=json.dumps(asdict(message)),
            )
        except Exception as e:
            self.logger.error(e)
            raise RuntimeError(e)
