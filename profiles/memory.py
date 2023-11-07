"""
python -m memory_profiler [script].py
[Visualization]
mprof run [script].py
mprof plot -o [output].png

[Result]
140 - 150 MiB를 다운로드 및 변환에 사용한다.
여기에 추가로 DB update 시 필요한 Filter 등을 만드는데 필요한 메모리를 더하면 현재 설정된 150MiB보다 크다.
-> Memory Kill 발생
-> 192MiB로 설정
"""
import json
from typing import Any, Dict, List, Sequence

import boto3
from memory_profiler import profile

from chalicelib.entity.base import EntityType
from chalicelib.entity.event import EventEntity
from chalicelib.entity.product import ProductEntity


@profile
def download(bucket: str, keys: List[str]) -> Sequence[Dict[str, Any]]:
    """
    10,000개의 데이터를 다운로드하고 dictionary로 변경할 때, 115MiB가 소비됨
    """
    s3 = boto3.resource("s3")
    res = []
    for key in keys:
        try:
            response = s3.Object(bucket, key).get()
            res += json.loads(response["Body"].read().decode())
        except Exception as e:
            continue
    return res


def convert_to_entity(rel_name: str, datum: Dict[str, Any]) -> EntityType:
    match rel_name:
        case "products":
            return ProductEntity.from_dict(datum)
        case "events":
            return EventEntity.from_dict(datum)
        case _:
            raise RuntimeError(f"{rel_name} should be in [products, events]")


@profile
def convert(result: list):
    res = []
    for r in result:
        res.append(convert_to_entity("products", r))
    return res


if __name__ == "__main__":
    bucket = "pyoniverse-tmp"
    keys = [f"etl-transform/dev/service/products_{idx}.json" for idx in range(103)]
    result = download(bucket, keys)
    entities = convert(result)
