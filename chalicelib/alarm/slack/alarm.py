import json
import logging
import traceback
from dataclasses import asdict

import boto3

from chalicelib.alarm.interface import AlarmIfs
from chalicelib.alarm.slack.model.enum.message_enum import MessageTypeEnum
from chalicelib.alarm.slack.model.message import SlackMessage
from chalicelib.core.model.result import Result


class SlackAlarm(AlarmIfs):
    def __init__(self, slack_queue_name: str):
        self.logger = logging.getLogger(__name__)
        if not slack_queue_name:
            raise RuntimeError(f"{slack_queue_name} shouldn't be none")
        self.__sqs_client = boto3.client("sqs")
        try:
            self.__sqs_queue_url: str = self.__sqs_client.get_queue_url(
                QueueName=slack_queue_name
            )["QueueUrl"]
        except Exception as e:
            raise RuntimeError(f"There's no queue: {slack_queue_name}")

    def notice(self, result: Result):
        ps = {}
        if result.action:
            ps["action"] = result.action
        if result.modified_count:
            ps["modified_count"] = str(result.modified_count)
        if result.filter:
            ps["filter"] = json.dumps(result.filter, ensure_ascii=False)
        if result.data:
            ps["data"] = json.dumps(result.data, ensure_ascii=False)

        text = ""
        if result.origin:
            text += result.origin
        if result.db_name:
            text += f"-{result.db_name}"
        if result.rel_name:
            text += f"-{result.rel_name}"
        message = SlackMessage(
            type=MessageTypeEnum.DEBUG,
            source="pyoniverse-update-db",
            text=text,
            cc=["윤영로"],
            ps=ps,
        )
        try:
            self.__sqs_client.send_message(
                QueueUrl=self.__sqs_queue_url,
                MessageBody=json.dumps(asdict(message)),
            )
        except Exception as e:
            self.logger.error(traceback.format_exc())
