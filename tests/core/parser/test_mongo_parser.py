from chalicelib.core.model.message import Data, Filter, Message
from chalicelib.core.model.query import Query
from chalicelib.core.parser.mongo_parser import MongoMessageParser
from tests.mock import env


def test_mongo_parser(env):
    # given
    parser = MongoMessageParser()
    message = Message(
        db_name="test_db",
        rel_name="test_rel",
        action="UPDATE",
        filters=[Filter(column="status", op="lt", value=2)],
        data=[Data(column="status", value=-1)],
    )
    # when
    query: Query = parser.parse(message)
    # then
    assert query.db_name == message.db_name
    assert query.rel_name == message.rel_name
    assert query.action == message.action
    assert query.filter == {"status": {"$lt": 2}}
    assert query.data == {"status": -1}
