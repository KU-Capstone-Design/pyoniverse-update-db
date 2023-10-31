import os

import pytest

from chalicelib.slack.model.enum.message_enum import MessageTypeEnum
from chalicelib.slack.model.message import SlackMessage
from chalicelib.slack.sender import SlackSender


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


def test_slack_sender(env):
    # given
    sender = SlackSender()
    message = SlackMessage(
        type=MessageTypeEnum.TEST,
        source="pyoniverse-update-db",
        text="test message",
        ps={"test_key": "test_val"},
        cc=["윤영로"],
    )
    # when & then
    try:
        sender.send(message)
        assert True
    except Exception:
        assert False
