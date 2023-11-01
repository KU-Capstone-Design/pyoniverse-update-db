import json
import os
from dataclasses import asdict
from datetime import datetime

from chalice.test import Client

from chalicelib.model.message import Message
from tests.mock import client, env


def test_transform_origin(env, client: Client):
    # given
    message = asdict(
        Message(
            date=datetime.now(),
            origin="transform",
            rel_name="products",
            db_name="service_dev",
            data=[],
        )
    )
    message["data"] = [
        f"etl-transform/dev/crawling/products_{idx}.json" for idx in range(200)
    ]
    message["date"] = message["date"].strftime("%Y-%m-%d")
    try:
        client.lambda_.invoke(
            "upsert",
            client.events.generate_sqs_event(
                queue_name=os.getenv("QUEUE_NAME"),
                message_bodies=[json.dumps(message, ensure_ascii=False)],
            ),
        )
        assert True
    except Exception as e:
        assert False
