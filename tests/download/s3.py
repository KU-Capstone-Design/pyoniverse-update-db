import os
from datetime import datetime

import pytest

from chalicelib.model.message import Message


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
def message():
    return Message(
        date=datetime.utcnow(),
        origin="test",
        rel_name="test",
        db_name="test",
        data=["test/products_0.json"],
    )


def test_download_json(env, message: Message):
    from chalicelib.download.s3 import S3Downloader

    # given
    s3_downloader = S3Downloader()
    # when
    res = s3_downloader.download(message.data)
    # then
    assert len(res) > 0
