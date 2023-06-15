from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Request, Depends, UploadFile, HTTPException, File, UploadFile

from sqlalchemy import select, delete, insert, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.authorization.model import User
from src.video.model import video as video_table

from src.entrypoint_db import get_async_session
from src.user.authorization.current_user import current_active_user, current_user
from src.interactions.model import like as like_table
from src.interactions.model import view as view_table
from src.interactions.utils import add_view

from streaming_form_data.targets import ValueTarget, FileTarget, NullTarget
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.validators import MaxSizeValidator
from starlette.concurrency import run_in_threadpool
from src.video.streaming import VideoTarget
from starlette.requests import ClientDisconnect
from boto3_my.boto3_ import upload_object, remove_object
from boto3_my.boto3_ import BUCKET
from src.video.streaming import MaxBodySizeValidator, MaxBodySizeException


MAX_COUNT_GET_ROWS = 100
MAX_FILE_SIZE = 1024 * 1024 * 1024 * 4  # = 4GB
MAX_REQUEST_BODY_SIZE = MAX_FILE_SIZE + 1024
MIN_SIZE_CHUNK = 1024 * 1024 * 6
MAX_VIDEO_SIZE = 1024 * 1024 * 512
PREFIX_VIDEO = 'video$'
PREFIX_IMAGE = 'image$'


router = APIRouter(
    prefix='/video',
    tags=['Video']
)


@router.post("/protected-route/load")
async def load_video(request: Request,
                     user: User = Depends(current_active_user),
                     db_session: AsyncSession = Depends(get_async_session)):

    body_validator = MaxBodySizeValidator(MAX_REQUEST_BODY_SIZE)
    filename = request.headers.get('Filename')
    print(filename)

    key = str(uuid4())
    print(f'key: {key}')
    # key_video = f'video${user.id}${title}${key}'
    key_video = f'{PREFIX_VIDEO}{key}'

    default_image_link = f'https://storage.yandexcloud.net/{BUCKET}/_DSC1067.JPG'
    image_link = default_image_link
    video_link = ''

    video_file = VideoTarget(MaxSizeValidator(MAX_VIDEO_SIZE), bucket=BUCKET, pre_key=key_video)
    image_file = ValueTarget()
    title_value = ValueTarget()
    descr_value = ValueTarget()

    title = 'default'
    description = 'default'

    if not filename:
        #raise HTTPException(status_code=422, detail='Filename header is missing')
        pass

    try:
        parser = StreamingFormDataParser(headers=request.headers)
        print(request.headers)
        print(request.body)
        print(request)
        parser.register('file', video_file)
        parser.register('image', image_file)
        parser.register('title', title_value)
        parser.register('description', descr_value)

        async for chunk in request.stream():
            body_validator(chunk)
            await run_in_threadpool(parser.data_received, chunk)

        await video_file.uploader.close_stream()
        video_type, video_extension = video_file.multipart_content_type.split('/')

        video_link = f'https://storage.yandexcloud.net/{BUCKET}/{key_video}.{video_extension}'
        image = image_file.value
        title = title_value.value.decode()
        description = descr_value.value.decode()
        print(title)
        print(description)

        if len(image) != 0:
            preview_type, preview_extension = image_file.multipart_content_type.split('/')
            print(preview_type)
            if preview_type != 'image':
                raise HTTPException(status_code=418, detail='Preview isn`t image')

            key_image = f'{PREFIX_IMAGE}{key}.{preview_extension}'

            image_link = f'https://storage.yandexcloud.net/{BUCKET}/{key_image}'
            await upload_object(key_image, image)


    except ClientDisconnect:
        print("Client Disconnected")
        await video_file.uploader.abort_multipart_upload()
    except MaxBodySizeException as e:
        await video_file.uploader.abort_multipart_upload()
        raise HTTPException(status_code=413,
                            detail=f'Maximum request body size limit ({MAX_REQUEST_BODY_SIZE} bytes) exceeded ({e.body_len} bytes read)')
    except Exception:
        await video_file.uploader.abort_multipart_upload()
        raise HTTPException(status_code=512, detail=Exception)

    try:
        await add_video_db(key, user.id, title,
                           description,
                           video_link, image_link, 'Можно убрать это поле))',db_session)
    except Exception:
        await video_file.uploader.remove_object()
        raise Exception

    return {"message": f"Successfuly uploaded {filename}"}


async def add_video_db(id_video: str,
                       user_id: int,
                       title: str,
                       description: str,
                       video_link: str,
                       poster_link: str,
                       nickname: str,
                       db_session: AsyncSession = Depends(get_async_session)):

    print([title, description])
    query_insert = insert(video_table).values(id=id_video,
                                              title=title,
                                              description=description,
                                              id_auther=user_id,
                                              count_likes=0,
                                              count_comments=0,
                                              video_link=video_link,
                                              poster_link=poster_link,
                                              published_at=datetime.utcnow(),
                                              nickname=nickname)

    await db_session.execute(query_insert)
    await db_session.commit()


@router.get("/protected-route/delete_video")
async def delete_video(id_video: str,
                       user: User = Depends(current_active_user),
                       db_session: AsyncSession = Depends(get_async_session)):

    query = select(video_table).where(video_table.c.id == id_video, video_table.c.id_auther == user.id)
    video = await db_session.execute(query)
    video = video.one_or_none()
    if video is None:
        raise HTTPException(status_code=500,
                            detail="Вы не можете этого сделать(Видео не существует или у вас нет прав)")

    video = video._asdict()

    key_video = video['video_link'].split('/')[-1]
    key_img = video['poster_link'].split('/')[-1]

    try:
        res = await remove_object(key_video)
        print(res)
        res = await remove_object(key_img)
        print(res)
    except Exception:
        raise Exception

    query = delete(video_table).where(video_table.c.id == id_video, video_table.c.id_auther == user.id)
    await db_session.execute(query)
    print('Action: remove')

    await db_session.commit()
    return 'Видео удалён'


@router.get("/get_video")
async def get_video(id_video: str,
                    user=Depends(current_user),
                    db_session: AsyncSession = Depends(get_async_session)):

    query = select(video_table, User).join(User, User.id == video_table.c.id_auther).where(video_table.c.id == id_video)

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

    query = select(video_table, User)\
        .join(User, User.id == video_table.c.id_auther).where().order_by(desc(video_table.c.published_at))\
        .offset(offset)\
        .limit(count)

    videos = await db_session.execute(query)
    videos = [row._asdict() for row in videos]

    return videos


@router.get("/get_video_this_user")
async def get_videos_this_user(id_user: int, count: int, offset: int,
                               db_session: AsyncSession = Depends(get_async_session)):

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500, detail="У вас большие запросы, попробуйте использовать меньшее значение")

    query = select(video_table, User).join(User, User.id == video_table.c.id_auther)\
        .where(video_table.c.id_auther == id_user)\
        .order_by(desc(video_table.c.published_at))\
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

    query = select(video_table, User)\
        .join(view_table,
              (video_table.c.id_auther == view_table.c.id_user) & (video_table.c.id == view_table.c.id_video)) \
        .join(User, video_table.c.id_auther == User.id) \
        .where(view_table.c.id_user == user.id) \
        .order_by(desc(view_table.c.published_at)) \
        .offset(offset) \
        .limit(count)

    print(query)

    videos = [row._asdict() for row in await db_session.execute(query)]
    print(len(videos))
    return videos


@router.get("/protected-route/get_liked_videos_main")
async def get_liked_videos_main(count: int, offset: int,
                                user: User = Depends(current_active_user),
                                db_session: AsyncSession = Depends(get_async_session)):

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500,
                            detail="У вас большие запросы, попробуйте использовать меньшее значение")

    query = select(video_table, User) \
        .join(like_table,
              (video_table.c.id_auther == like_table.c.id_auther) & (video_table.c.id == like_table.c.id_video)) \
        .where(like_table.c.id_auther == user.id) \
        .join(User, video_table.c.id_auther == User.id) \
        .order_by(desc(like_table.c.published_at)) \
        .offset(offset) \
        .limit(count)

    videos = [row._asdict() for row in await db_session.execute(query)]

    return videos
