import json
import os
from typing import Any, Dict, Sequence

import boto3


class S3Downloader:
    def __init__(self):
        self.__bucket = os.getenv("S3_BUCKET")

    def download(self, data: Sequence[str]) -> Sequence[Dict[str, Any]]:
        s3 = boto3.resource("s3")
        res = []
        for file in data:
            response = s3.Object(self.__bucket, file).get()
            res += json.loads(response["Body"].read().decode())
        return res
