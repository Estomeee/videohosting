from fastapi import APIRouter, Request, Depends, UploadFile, HTTPException
from fastapi_users import FastAPIUsers

from sqlalchemy import select, inspect, join, delete, values, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .model import User
from src.video.model import video as video_table
from src.video.schemas import Video as video_class

from src.entrypoint_db import get_async_session
from src.user.authorization.current_user import current_active_user, current_user
from src.user.authorization.current_user import fastapi_users
from src.user.authorization.router import get_user
from src.interactions.model import like as like_table
from src.interactions.model import view as view_table
from src.interactions.utils import add_view


async def check_video(id_video: int,
                db_session: AsyncSession = Depends(get_async_session)):

    query = select(video_table).where(video_table.c.id == id_video)
    video = await db_session.execute(query)

    return video.one_or_none() is not None
