import logging
import os
import sys

import dotenv
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Resource
from pymongo import MongoClient


def init_client() -> MongoClient:
    client = MongoClient(os.getenv("MONGO_URI"))
    client.admin.command("ping")
    yield client
    # shutdown
    client.close()


class ResourceInjector(DeclarativeContainer):
    logging = Resource(
        logging.basicConfig,
        force=True,
        level=logging.INFO,
        stream=sys.stdout,
        datefmt="%Y-%m-%dT%H:%M:%S",
        format="%(asctime)s %(name)s[%(levelname)s]:%(message)s",
    )
    client = Resource(init_client)

    def init_resources(self):
        dotenv.load_dotenv()
        return super().init_resources()
