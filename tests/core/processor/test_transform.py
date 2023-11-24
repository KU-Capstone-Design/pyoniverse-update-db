import pytest

from chalicelib.core.model.query import Query
from chalicelib.core.model.result import Result
from chalicelib.core.processor.transform_processor import TransformQueryProcessor
from chalicelib.extern.dependency_injector.resource import ResourceInjector
from tests.mock import env


@pytest.fixture
def resource_injector(env):
    injector = ResourceInjector()
    injector.init_resources()
    return injector


def test_transform_processor(resource_injector):
    # given
    processor = TransformQueryProcessor(client=resource_injector.client())
    query = Query(
        db_name="test",
        rel_name="products",
        action="UPSERT",
        filter=None,
        data={
            "bucket": "pyoniverse-tmp",
            "keys": ["etl-transform/dev/crawling/products_0.json"],
        },
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
