from datetime import datetime

from src.entrypoint_db import get_async_session
from src.user.authorization.model import User, AsyncSession
from fastapi import Depends, HTTPException
from src.user.authorization.current_user import current_active_user
#from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert
from src.interactions.model import view as view_table
from src.interactions.schemas import View


async def add_view(id_video: int,
             user: User,
             db_session: AsyncSession = Depends(get_async_session)):
    query = insert(view_table).values(id_video=id_video, id_user=user.id, published_at=datetime.utcnow())
    await db_session.execute(query.on_conflict_do_nothing(index_elements=['id_video', 'id_user']))

    #db_session.add(View(id_video=id_video, id_user=user.id, published_at=datetime.datetime.utcnow()))
    print('Есть попытка')
    print(user.id)
    await db_session.commit()
