from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entrypoint_db import get_async_session
from src.user.authorization.model import User
from src.user.authorization.current_user import current_active_user
from src.interactions.model import view as view_table
from src.video.model import video as video_table
from src.interactions.model import like as like_table
from src.interactions.model import sub as sub_table


async def add_view(id_video: str,
                   user: User,
                   db_session: AsyncSession = Depends(get_async_session)):

    query_bool = select(view_table).where(view_table.c.id_video == id_video, view_table.c.id_user == user.id)
    _bool = (await db_session.execute(query_bool)).one_or_none()
    if _bool is None:
        query_video = update(video_table).where(video_table.c.id == id_video).values(
            count_views=video_table.c.count_views + 1)
        await db_session.execute(query_video)

    query = insert(view_table).values(id_video=id_video, id_user=user.id, published_at=datetime.utcnow())
    await db_session.execute(query.on_conflict_do_update(index_elements=['id_video', 'id_user'],
                                                         set_={'published_at': datetime.utcnow()}))

    await db_session.commit()


async def check_view(id_video: str,
                     user: User = Depends(current_active_user),
                     db_session: AsyncSession = Depends(get_async_session)):

    query = select(view_table).where(view_table.c.id_video == id_video, view_table.c.id_user == user.id)
    view = await db_session.execute(query)

    return view.one_or_none() is not None


async def check_like(id_video: str,
                     user: User = Depends(current_active_user),
                     db_session: AsyncSession = Depends(get_async_session)):
    if user is None:
        return False

    query = select(like_table).where(like_table.c.id_video == id_video, like_table.c.id_auther == user.id)

    like = await db_session.execute(query)

    return like.one_or_none() is not None


async def check_sub(id_maker: id,
                    user: User = Depends(current_active_user),
                    db_session: AsyncSession = Depends(get_async_session)):
    if user is None:
        return False

    query = select(sub_table).where(sub_table.c.id_maker == id_maker, sub_table.c.id_subscriber == user.id)

    sub = await db_session.execute(query)

    return sub.one_or_none() is not None
