from io import BytesIO
from typing import Union
from fastapi import UploadFile
import aioboto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

BUCKET = 'urfube-emegor'


config = {
            "service_name": 's3',
            "endpoint_url": "https://storage.yandexcloud.net",
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "aws_access_key_id": AWS_ACCESS_KEY_ID
        }


async def upload_object(key: str, file: Union[UploadFile, bytes]):
    if type(file) == bytes:
        file = BytesIO(file)
    async with aioboto3.Session().client(**config) as s3:
        await s3.upload_fileobj(file, BUCKET, key)
