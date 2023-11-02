import logging

from pymongo import MongoClient

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
