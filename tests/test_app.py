import json
import os
from dataclasses import asdict
from datetime import datetime

from chalice.test import Client

from chalicelib.core.model.message import Message
from tests.mock import client, env


def test_transform_origin(env, client: Client):
    # given
    message = asdict(
        Message(
            origin="transform",
            rel_name="products",
            db_name="test",
            data=[],
            filters=[],
            action="UPSERT",
        )
    )
    message["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    message["data"] = [
        {"column": "bucket", "value": os.getenv("S3_BUCKET")},
        {
            "column": "keys",
            "value": [
                f"etl-transform/dev/crawling/products_{idx}.json" for idx in range(5)
            ],
        },
    ]

    response = client.lambda_.invoke(
        "upsert",
        client.events.generate_sqs_event(
            queue_name=os.getenv("QUEUE_NAME"),
            message_bodies=[json.dumps(message, ensure_ascii=False)],
        ),
    )
    assert response.payload is True


def test_transform_origin_invalid_action(env, client: Client):
    # given
    message = asdict(
        Message(
            origin="transform",
            rel_name="products",
            db_name="test",
            data=[],
            filters=[],
            action="INVALID",
        )
    )
    message["date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    message["data"] = [
        {"column": "bucket", "value": os.getenv("S3_BUCKET")},
        {
            "column": "keys",
            "value": [
                f"etl-transform/dev/crawling/products_{idx}.json" for idx in range(5)
            ],
        },
    ]

    response = client.lambda_.invoke(
        "upsert",
        client.events.generate_sqs_event(
            queue_name=os.getenv("QUEUE_NAME"),
            message_bodies=[json.dumps(message, ensure_ascii=False)],
        ),
    )
    assert response.payload is False
