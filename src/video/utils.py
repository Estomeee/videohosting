from fastapi import APIRouter, Request, Depends, UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.video.model import video as video_table
from src.entrypoint_db import get_async_session


async def check_video(id_video: str,
                db_session: AsyncSession = Depends(get_async_session)):

    query = select(video_table).where(video_table.c.id == id_video)
    video = await db_session.execute(query)

    return video.one_or_none() is not None
