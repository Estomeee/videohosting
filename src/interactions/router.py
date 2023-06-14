from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Body

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, desc

from fastapi_users import FastAPIUsers

from .model import User
from src.user.authorization.current_user import current_active_user
from src.entrypoint_db import get_async_session
from src.interactions.model import like as like_table
from src.video.model import video as video_table
from src.interactions.model import view as view_table
from src.interactions.utils import check_view, check_sub, check_like
from src.interactions.model import comment as comment_table
from src.interactions.model import sub as sub_table
from src.video.utils import check_video
from src.interactions.schemas import Comment

MAX_COUNT_GET_ROWS = 100

router = APIRouter(
    prefix='/interactions',
    tags=['Interactions']
)

# Адреса поменять добавить по необходимости

'''
@router.get("/protected-route/like")
async def like(id_video: str,
               user: User = Depends(current_active_user),
               db_session: AsyncSession = Depends(get_async_session)):

    if not await check_view(id_video, user, db_session):
        raise HTTPException(status_code=500, detail="Вы не можете поставить лайк на видео, которые не посмотрели")

    query_like = select(like_table).where(like_table.c.id_video == id_video, like_table.c.id_auther == user.id)
    like = await db_session.execute(query_like)

    if like.one_or_none() is None:
        query_like = insert(like_table).values(id_video=id_video, id_auther=user.id, published_at=datetime.utcnow())
        await db_session.execute(query_like)
        print('Action: add')
        count_change = 1
    else:
        query_like = delete(like_table).where(like_table.c.id_video == id_video, like_table.c.id_auther == user.id)
        await db_session.execute(query_like)
        print('Action: remove')
        count_change = -1

    query_video = update(video_table).where(video_table.c.id == id_video).values(count_likes=video_table.c.count_likes + count_change)
    await db_session.execute(query_video)

    await db_session.commit()
    return
'''


@router.get("/protected-route/put_like")
async def put_like(id_video: str,
                   user: User = Depends(current_active_user),
                   db_session: AsyncSession = Depends(get_async_session)):

    if not await check_view(id_video, user, db_session):
        raise HTTPException(status_code=500, detail="Вы не можете поставить лайк на видео, которые не посмотрели")

    if await check_like(id_video, user, db_session):
        raise HTTPException(status_code=500, detail="Лайк уже поставлен")
    else:
        query_like = insert(like_table).values(id_video=id_video, id_auther=user.id, published_at=datetime.utcnow())
        await db_session.execute(query_like)
        print('Action: add')

    query_video = update(video_table)\
        .where(video_table.c.id == id_video)\
        .values(count_likes=video_table.c.count_likes+1)
    await db_session.execute(query_video)

    await db_session.commit()
    return


@router.get("/protected-route/remove_like")
async def remove_like(id_video: str,
                      user: User = Depends(current_active_user),
                      db_session: AsyncSession = Depends(get_async_session)):

    if await check_like(id_video, user, db_session):
        query_like = delete(like_table).where(like_table.c.id_video == id_video, like_table.c.id_auther == user.id)
        await db_session.execute(query_like)
        print('Action: remove')
    else:
        raise HTTPException(status_code=500, detail="Вы не ставили лайк на это видео")

    query_video = update(video_table)\
        .where(video_table.c.id == id_video)\
        .values(count_likes=video_table.c.count_likes - 1)
    await db_session.execute(query_video)

    await db_session.commit()
    return


@router.post("/protected-route/comment/add")
async def add_comment(id_video: str,
                      request: Comment,
                      user: User = Depends(current_active_user),
                      db_session: AsyncSession = Depends(get_async_session)):

    if not await check_view(id_video, user, db_session):
        raise HTTPException(status_code=500, detail="Видео ещё не просмотренно")

    # Првоерка и обработка содержимого комментария
    text = request.text
    if text == '':
        raise HTTPException(status_code=500, detail="Что-то не так с тектом(Допилить проверку текста)")
    ######

    query = insert(comment_table).values(id=str(uuid4()), text=text, id_video=id_video, id_auther=user.id, published_at=datetime.utcnow())
    await db_session.execute(query)

    query_video = update(video_table).where(video_table.c.id == id_video).values(
        count_comments=video_table.c.count_comments + 1)
    await db_session.execute(query_video)

    await db_session.commit()
    return 'Комментарий успешно добавлен'


@router.get("/protected-route/comment/remove")
async def remove_comment(id_comment: str,
                         user: User = Depends(current_active_user),
                         db_session: AsyncSession = Depends(get_async_session)):

    query = select(comment_table).where(comment_table.c.id == id_comment, comment_table.c.id_auther == user.id)
    comment = await db_session.execute(query)
    comment = comment.one_or_none()
    if comment is None:
        raise HTTPException(status_code=404, detail="Вы не можете этого сделать(Комментарий не существует или у вас нет прав)")

    query = delete(comment_table).where(comment_table.c.id == id_comment, comment_table.c.id_auther == user.id)
    await db_session.execute(query)
    print('Action: remove')

    query_video = update(video_table).where(video_table.c.id == comment.id_video).values(count_comments=video_table.c.count_comments - 1)
    await db_session.execute(query_video)


    await db_session.commit()
    return 'Комментарий удалён'


@router.get("/protected-route/comment/get_comments")
async def get_comments(count: int,
                       offset: int,
                       id_video: str,
                       db_session: AsyncSession = Depends(get_async_session)):

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500, detail="У вас большие запросы, попробуйте использовать меньшее значение")

    # Необходимо ли проверять наличие видео?
    if not await check_video(id_video, db_session):
        raise HTTPException(status_code=404, detail="Video not found")

    query = select(comment_table)\
        .where(comment_table.c.id_video == id_video)\
        .order_by(desc(comment_table.c.published_at))\
        .offset(offset).limit(count)
    comments = [row._asdict() for row in await db_session.execute(query)]

    return comments

'''
@router.get("/protected-route/subscribe")
async def subscribe(id_maker: int,
                    user: User = Depends(current_active_user),
                    db_session: AsyncSession = Depends(get_async_session)):

    if id_maker == user.id:
        raise HTTPException(status_code=500, detail="Вы не можете подписаться на себя")

    query_maker = select(User).where(User.id == id_maker)
    maker = await db_session.execute(query_maker)
    maker = maker.one_or_none()
    if maker is None:
        raise HTTPException(status_code=500, detail="User not found")

    query_sub = select(sub_table).where(sub_table.c.id_maker == id_maker, sub_table.c.id_subscriber == user.id)
    sub = await db_session.execute(query_sub)

    if sub.one_or_none() is None:
        query_sub = insert(sub_table).values(id_maker=id_maker, id_subscriber=user.id, datatime=datetime.utcnow())
        print('Action: sub')
        count_change = 1
    else:
        query_sub = delete(sub_table).where(sub_table.c.id_maker == id_maker, sub_table.c.id_subscriber == user.id)
        print('Action: unsub')
        count_change = -1
    await db_session.execute(query_sub)

    query_update_maker = update(User).where(User.id == id_maker).values(count_subs=User.count_subs + count_change)
    print(query_update_maker)
    await db_session.execute(query_update_maker)

    await db_session.commit()
    return
'''


@router.get("/protected-route/subscribe")
async def subscribe(id_maker: int,
                    user: User = Depends(current_active_user),
                    db_session: AsyncSession = Depends(get_async_session)):

    if id_maker == user.id:
        raise HTTPException(status_code=500, detail="Вы не можете подписаться на себя")

    query_maker = select(User).where(User.id == id_maker)
    maker = await db_session.execute(query_maker)
    maker = maker.one_or_none()
    if maker is None:
        raise HTTPException(status_code=500, detail="User not found")

    if await check_sub(id_maker, user, db_session):
        raise HTTPException(status_code=500, detail="Подписка уже оформлена")
    else:
        query_sub = insert(sub_table).values(id_maker=id_maker, id_subscriber=user.id, datatime=datetime.utcnow())
        print('Action: sub')

    await db_session.execute(query_sub)

    query_update_maker = update(User).where(User.id == id_maker).values(count_subs=User.count_subs + 1)
    await db_session.execute(query_update_maker)

    await db_session.commit()
    return


@router.get("/protected-route/unsubscribe")
async def unsubscribe(id_maker: int,
                      user: User = Depends(current_active_user),
                      db_session: AsyncSession = Depends(get_async_session)):

    if await check_sub(id_maker, user, db_session):
        query_sub = delete(sub_table).where(sub_table.c.id_maker == id_maker, sub_table.c.id_subscriber == user.id)
        print('Action: unsub')
    else:
        raise HTTPException(status_code=500, detail="Вы не можете отписаться, т.к. подписка не была оформлена")

    await db_session.execute(query_sub)

    query_update_maker = update(User).where(User.id == id_maker).values(count_subs=User.count_subs - 1)
    await db_session.execute(query_update_maker)

    await db_session.commit()
    return
