import json
import logging
import traceback
from typing import Any, Dict, Sequence

import boto3


class S3Downloader:
    def __init__(self, bucket: str):
        self.logger = logging.getLogger(__name__)
        self.__bucket = bucket
        if not self.__bucket:
            self.logger.error(f"{bucket} shouldn't be none")
            raise RuntimeError(f"{bucket} shouldn't be none")

    def download(self, data: Sequence[str]) -> Sequence[Dict[str, Any]]:
        s3 = boto3.resource("s3")
        res = []
        for file in data:
            try:
                response = s3.Object(self.__bucket, file).get()
                res += json.loads(response["Body"].read().decode())
            except Exception as e:
                if "NoSuchKey" in traceback.format_exc():
                    self.logger.error(f"s3://{self.__bucket}{file} NOT FOUND")
                else:
                    self.logger.error(traceback.format_exc())
                continue
        return res
