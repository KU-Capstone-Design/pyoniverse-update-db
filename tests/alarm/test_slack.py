import os

from chalicelib.alarm.slack.alarm import SlackAlarm
from chalicelib.core.model.result import Result
from tests.mock import env


# def test_slack_alarm(env):
#     # given
#     alarm = SlackAlarm(slack_queue_name=os.getenv("SLACK_QUEUE_NAME"))
#     result = Result(
#         origin="test",
#         db_name="test",
#         rel_name="test_rel",
#         filter={"x": 1},
#         data={"a": "b"},
#         action="UPDATE",
#         modified_count=0,
#     )
#     try:
#         alarm.notice(result)
#         assert True
#     except Exception:
#         assert False
