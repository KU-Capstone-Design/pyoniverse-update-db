import logging
import os

from pymongo import MongoClient

from chalicelib.extern.dependency_injector.injector import Injector
from chalicelib.extern.dependency_injector.resource import ResourceInjector
from tests.mock import env


def test_resource_injector(env):
    # given
    injector = ResourceInjector()
    # when
    injector.init_resources()
    # then
    assert isinstance(injector.client(), MongoClient)
    assert injector.client() is injector.client()

    assert logging.getLogger().level == logging.INFO
    logging.getLogger().info("Success")


def test_injector(env):
    # given
    resource_injector = ResourceInjector()
    resource_injector.init_resources()
    injector = Injector(client=resource_injector.client())
    injector.config.slack_queue_name.from_env("SLACK_QUEUE_NAME", required=True)
    # when
    assert injector.config.slack_queue_name() == os.getenv("SLACK_QUEUE_NAME")
    try:
        injector.check_dependencies()
        assert True
    except Exception:
        assert False
