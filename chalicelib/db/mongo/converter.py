from chalice import BadRequestError

from chalicelib.db.filter_converter_ifs import FilterConverterIfs
from chalicelib.db.model.filter import Filter


class MongoFilterConverter(FilterConverterIfs):
    def convert(self, _filter: Filter):
        match _filter.op:
            case "eq":
                return {"$eq": _filter.value}
            case "le":
                return {"$le": _filter.value}
            case "lt":
                return {"$lt": _filter.value}
            case "ge":
                return {"$ge": _filter.value}
            case "gt":
                return {"$gt": _filter.value}
            case "neq":
                return {"$ne": _filter.value}
            case _:
                BadRequestError(f"{_filter.op} not supported")
