import os

from pymongo import MongoClient

from chalicelib.core.model.query import Query
from chalicelib.core.model.result import Result
from chalicelib.core.processor.migrator_processor import MigratorQueryProcessor


def test_migrator_processor_update_action(env):
    # given
    client = MongoClient(os.getenv("MONGO_URI"))
    client.admin.command("ping")
    processor = MigratorQueryProcessor(client=client)
    query = Query(
        db_name="test",
        rel_name="products",
        action="UPDATE",
        filter=None,
        data={"documents": [{"id": 1, "name": "Test Name"}]},
    )
    # when
    result: Result = processor.execute(query)
    # then
    assert result.origin == query.origin
    assert result.db_name == query.db_name
    assert result.rel_name == query.rel_name
    assert result.action == query.action
    assert result.filter == query.filter
    assert result.data == query.data
    assert result.modified_count > 0
