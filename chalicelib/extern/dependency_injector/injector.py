from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Dependency, Singleton
from pymongo import MongoClient

from chalicelib.alarm.slack.alarm import SlackAlarm
from chalicelib.core.parser.mongo_parser import MongoMessageParser
from chalicelib.core.processor.transform_processor import TransformQueryProcessor


class Injector(DeclarativeContainer):
    config = Configuration()
    client = Dependency(MongoClient)

    # alarm
    slack_alarm = Singleton(
        SlackAlarm,
        slack_queue_name=config.slack_queue_name,
    )
    # query processor
    transform_query_processor = Singleton(TransformQueryProcessor, client=client)
    # parser
    message_parser = Singleton(MongoMessageParser)
