from fastapi import APIRouter, Request, Depends, UploadFile, UploadFile

from fastapi_users import FastAPIUsers

from .model import User

from src.entrypoint_db import async_session_maker
from src.user.authorization.current_user import current_active_user
from src.user.authorization.current_user import fastapi_users

from boto3_my.boto3_ import s3 as s3client
import boto3

router = APIRouter(
    prefix='/video',
    tags=['Video']
)

@router.post("/protected-route/load")
async def load_video(request: Request):

    key = 'new3'

    # Открыл поток для записи файла
    multipart_upload = s3client.create_multipart_upload(
        Bucket='urfube-emegor', Key=key)

    bb = []
    parts = []
    part_number = 1
    async for data in request.stream():

        if part_number == 0:
            part_number += 1
            continue

        bb.append(data)
        data = b''.join(bb)
        bb = []
        if len(data) < 6000000:
            bb.append(data)
            continue


        upload_part_response = s3client.upload_part(Body=data,
                                                    Bucket="urfube-emegor",
                                                    UploadId=multipart_upload['UploadId'],
                                                    PartNumber=part_number,
                                                    Key=key)

        parts.append({
            'PartNumber': part_number,
            'ETag': upload_part_response['ETag']
        })
        print(parts[part_number-1])
        print(len(data))
        #print(chunk)

        part_number += 1

    if len(bb) > 0:
        data = b''.join(bb)
        bb = []

        upload_part_response = s3client.upload_part(Body=data,
                                                    Bucket="urfube-emegor",
                                                    UploadId=multipart_upload['UploadId'],
                                                    PartNumber=part_number,
                                                    Key=key)

        parts.append({
            'PartNumber': part_number,
            'ETag': upload_part_response['ETag']
        })


    # Закрываем поток
    completeResult = s3client.complete_multipart_upload(
        Bucket='urfube-emegor',
        Key=key,
        MultipartUpload={'Parts': parts},
        UploadId=multipart_upload['UploadId']
    )

'''
@router.post("/protected-route/load")
async def load_video(request: Request,

                     ):
    key = '9999'

    # Открыл поток для записи файла
    multipart_upload = s3client.create_multipart_upload(
        Bucket='urfube-emegor', Key=key)

    bb = []
    parts = []
    part_number = 1
    with open('99.mp4', 'rb') as f:
        while True:
            data = f.read(1024*1024*5)
            if not len(data):
                break
            upload_part_response = s3client.upload_part(Body=data,
                                                        Bucket="urfube-emegor",
                                                        UploadId=multipart_upload['UploadId'],
                                                        PartNumber=part_number,
                                                        Key=key)

            parts.append({
                'PartNumber': part_number,
                'ETag': upload_part_response['ETag']
            })
            print(parts[part_number-1])
            print(len(data))
            #print(chunk)

            part_number += 1


    # Закрываем поток
    completeResult = s3client.complete_multipart_upload(
        Bucket='urfube-emegor',
        Key=key,
        MultipartUpload={'Parts': parts},
        UploadId=multipart_upload['UploadId']
    )
'''

@router.get("/protected-route")
def get_video(user: User = Depends(current_active_user)):
    pass

#Какие-то запросы