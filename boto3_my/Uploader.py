from fastapi import HTTPException
import aioboto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from boto3_my.boto3_ import config as boto3_config


class Uploader:
    def __init__(self, bucket: str, key: str = None):
        self.bucket = bucket
        self.key = key
        self.parts = []
        self.part_number = 0
        self.mpu = None
        self.config = boto3_config
        self.chunks = []
        self.chunks_size = 0

    async def get_part_number(self):
        self.part_number += 1
        return self.part_number

    async def open_stream(self):
        try:
            async with aioboto3.Session().client(**self.config) as s3client:
                multipart_upload = await s3client.create_multipart_upload(Bucket=self.bucket, Key=self.key)
                self.mpu = multipart_upload
                print('Open stream')
        except HTTPException:
            raise HTTPException(status_code=488, detail="Не получилось открыть поток")
        finally:
            pass

    async def upload_chunk(self, chunk, force=False):

        if self.mpu is None:
            await self.open_stream()

        self.chunks_size += len(chunk)
        self.chunks.append(chunk)
        if self.chunks_size < 1024*1024*6 and not force:
            return

        chunk = b''.join(self.chunks)
        self.chunks = []
        self.chunks_size = 0

        part_number = await self.get_part_number()
        multipart_upload = self.mpu
        print('Uploader')
        try:
            async with aioboto3.Session().client(**self.config) as s3client:
                upload_part_response = await s3client.upload_part(Body=chunk,
                                                                  Bucket=self.bucket,
                                                                  UploadId=multipart_upload['UploadId'],
                                                                  PartNumber=part_number,
                                                                  Key=self.key)

                self.parts.append({
                    'PartNumber': part_number,
                    'ETag': upload_part_response['ETag']
                })
                print(self.parts[part_number - 1])
                print(len(chunk))

        except HTTPException:
            raise HTTPException(status_code=488, detail="Не получилось отправить фрагмент")
        finally:
            pass

    async def close_stream(self):
        if self.mpu is None:
            raise HTTPException(status_code=488, detail="Поток не открыт")

        if self.chunks_size > 0:
            await self.upload_chunk(b'', True)


        async with aioboto3.Session().client(**self.config) as s3client:
            multipart_upload = self.mpu
            completeResult = await s3client.complete_multipart_upload(
                Bucket=self.bucket,
                Key=self.key,
                MultipartUpload={'Parts': self.parts},
                UploadId=multipart_upload['UploadId'])

    async def abort_multipart_upload(self):
        async with aioboto3.Session().client(**self.config) as s3client:
            await s3client.abort_multipart_upload(
                Bucket=self.bucket,
                Key=self.key,
                UploadId=self.mpu['UploadId'])

    async def remove_object(self):
        async with aioboto3.Session().client(**self.config) as s3:
            res = await s3.delete_object(Bucket=self.bucket, Key=self.key)
            print(res)
