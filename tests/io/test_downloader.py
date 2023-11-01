import os

from chalicelib.io.downloader import S3Downloader
from tests.mock import env


def test_downloader(env):
    downloader = S3Downloader(bucket=os.getenv("S3_BUCKET"))
    data = [
        "pass",
        "even",
        "if",
        "error",
        "mixed",
        "etl-transform/dev/crawling/products_0.json",
    ]
    res = downloader.download(data)
    assert len(res) > 0
