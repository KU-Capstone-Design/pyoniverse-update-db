from chalicelib.db.model.filter import Filter
from chalicelib.db.mongo.converter import MongoFilterConverter


def test_filter_converter():
    # given
    converter = MongoFilterConverter()
    _filter = Filter(op="lt", value=3)
    # when
    res = converter.convert(_filter)
    # then
    assert res == {"$lt": 3}
