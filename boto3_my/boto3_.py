import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

#s3.put_object(Bucket='urfube-emegor', Key='object_name', Body='TEST', StorageClass='COLD')
s3.upload_file('_DSC1067.JPG', 'urfube-emegor', '_DSC1067.JPG')
