from dataclasses import asdict
from datetime import datetime


def test_message():
    # given
    msg = {
        "date": "2022-11-11",
        "origin": "test",
        "rel_name": "test_rel",
        "db_name": "test_db",
        "data": ["file1.json", "file2.json", "file3.json"],
    }
    # when
    from chalicelib.model.message import Message

    res = Message.load(msg)

    # then
    assert datetime.strftime(res.date, "%Y-%m-%d") == msg["date"]
    assert res.origin == msg["origin"]
    assert res.rel_name == msg["rel_name"]
    assert res.db_name == msg["db_name"]
    assert res.data == msg["data"]
