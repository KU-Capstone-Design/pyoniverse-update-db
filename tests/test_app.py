import os

import pytest
from chalice.test import Client


@pytest.fixture
def env():
    while "app.py" not in os.listdir():
        os.chdir("..")
    import dotenv

    dotenv.load_dotenv()

    # Load .chalice/config.json
    import json

    with open(".chalice/config.json", "r") as fd:
        config = json.load(fd)

    env = config.get("environment_variables", {})
    env.update(
            config.get("stages", {}).get("dev_v1", {}).get("environment_variables", {})
    )
    os.environ.update(env)


@pytest.fixture
def client(env):
    from app import app

    with Client(app, stage_name="dev_v1") as client:
        yield client


def test_send(client, message):
    # response = client.lambda_.invoke(
    #     "send_message",
    #     client.events.generate_sqs_event(
    #         queue_name=os.getenv("QUEUE_NAME"),
    #         message_bodies=[json.dumps(message, ensure_ascii=False)],
    #     ),
    # )
    # assert response.payload == {"result": "1/1"}
    pass
