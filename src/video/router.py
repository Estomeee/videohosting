from fastapi import APIRouter, Request, Depends, UploadFile, HTTPException
from fastapi_users import FastAPIUsers

from sqlalchemy import select, inspect, join, delete, values, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .model import User
from src.video.model import video as video_table
from src.video.schemas import Video as video_class

from src.entrypoint_db import get_async_session
from src.user.authorization.current_user import current_active_user, current__user
from src.user.authorization.current_user import fastapi_users
from src.user.authorization.router import get_user
from src.interactions.model import like as like_table
from src.interactions.model import view as view_table
from src.interactions.utils import add_view

from boto3_my.boto3_ import s3 as s3client
import boto3

MAX_COUNT_GET_ROWS = 100


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
async def delete_video(user: User = Depends(current_active_user)):
    '''query = select(video_table).where(video_table.c.id == id_video)

    video = await db_session.execute(query)
    video = [x._asdict() for x in video.all()]
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    print(video)
    print(type(video))
    return video'''


@router.get("/get_video")
async def get_video(id_video: int,
                    user=Depends(current__user),
                    db_session: AsyncSession = Depends(get_async_session)):
    query = select(video_table).where(video_table.c.id == id_video)

    video = await db_session.execute(query)
    video = video.one_or_none()
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    if user is not None:
        await add_view(id_video, user, db_session)

    return video._asdict()


@router.get("/get_last_videos")
async def get_last_videos(count: int, offset: int, db_session: AsyncSession = Depends(get_async_session)):

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500, detail="У вас большие запросы, попробуйте использовать меньшее значение")

    query = select(video_table).where().order_by(video_table.c.published_at).offset(offset).limit(count)

    videos = await db_session.execute(query)
    videos = [row._asdict() for row in videos]

    return videos


@router.get("/get_video_this_user")
async def get_videos_this_user(id_user: int, count: int, offset: int,
                               db_session: AsyncSession = Depends(get_async_session)):
    await get_user(id_user, db_session)

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500, detail="У вас большие запросы, попробуйте использовать меньшее значение")

    query = select(video_table)\
        .where(video_table.c.id_auther == id_user)\
        .order_by(video_table.c.published_at)\
        .offset(offset)\
        .limit(count)

    videos = [row._asdict() for row in await db_session.execute(query)]

    return videos


@router.get("/protected-route/get_viewed_videos")
async def get_viewed_videos(count: int, offset: int,
                            user: User = Depends(current_active_user),
                            db_session: AsyncSession = Depends(get_async_session)):
    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500,
                            detail="У вас большие запросы, попробуйте использовать меньшее значение")

    query = select(video_table) \
        .join(view_table) \
        .where(view_table.c.id_user == user.id) \
        .order_by(like_table.c.published_at) \
        .offset(offset) \
        .limit(count)

    videos = [row._asdict() for row in await db_session.execute(query)]

    return videos


@router.get("/protected-route/get_liked_videos")
async def get_liked_videos(count: int, offset: int,
                           user: User = Depends(current_active_user),
                           db_session: AsyncSession = Depends(get_async_session)):

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500,
                            detail="У вас большие запросы, попробуйте использовать меньшее значение")

    query = select(like_table) \
        .where(like_table.c.id_auther == user.id) \
        .order_by(like_table.c.published_at) \
        .offset(offset) \
        .limit(count)

    likes = [row._asdict() for row in await db_session.execute(query)]

    videos = [await get_video(i['id_video'], db_session) for i in likes]

    return videos

@router.get("/protected-route/get_liked_videos_main")
async def get_liked_videos_main(count: int, offset: int,
                           user: User = Depends(current_active_user),
                           db_session: AsyncSession = Depends(get_async_session)):

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500,
                            detail="У вас большие запросы, попробуйте использовать меньшее значение")

    query = select(video_table) \
        .join(like_table) \
        .where(like_table.c.id_auther == user.id) \
        .order_by(like_table.c.published_at) \
        .offset(offset) \
        .limit(count)


    videos = [row._asdict() for row in await db_session.execute(query)]

    return videos
