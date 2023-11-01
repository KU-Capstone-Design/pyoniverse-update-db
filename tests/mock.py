import pytest


@pytest.fixture
def env():
    import os
    import json
    import dotenv

    while "app.py" not in os.listdir():
        os.chdir("..")
    dotenv.load_dotenv()

    with open(".chalice/config.json", "r") as fd:
        config = json.load(fd)
    env = config.get("environment_variables", {})
    env.update(
        config.get("stages", {}).get("dev_v1", {}).get("environment_variables", {})
    )
    os.environ.update(env)


@pytest.fixture
def client(env):
    from chalice.test import Client
    from app import app

    with Client(app, stage_name="dev_v1") as client:
        yield client
