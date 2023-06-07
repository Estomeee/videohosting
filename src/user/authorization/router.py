from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users import FastAPIUsers
from sqlalchemy import select, inspect, join, delete, values, insert
from src.user.authorization.model import User as user_table

from .model import User
from .user_manager import get_user_manager
from .schemas import UserCreate, UserRead, UserUpdate
from .auth import auth_backend

from src.entrypoint_db import get_async_session
from src.user.authorization.current_user import current_active_user
from src.user.authorization.current_user import fastapi_users
from src.interactions.model import sub as sub_table
MAX_COUNT_GET_ROWS = 100

router_reg = fastapi_users.get_register_router(UserRead, UserCreate)
router_auth = fastapi_users.get_auth_router(auth_backend)

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"


@router.get("/get_user")
async def get_user(id: int, db_session: AsyncSession = Depends(get_async_session)):
    query = select(user_table) \
        .where(user_table.id == id)

    user = await db_session.execute(query)
    user = user.one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user._asdict()


@router.get("/protected-route/get_subscriptions")
async def get_subscriptions(count: int,
                            offset: int,
                            user: User = Depends(current_active_user),
                            db_session: AsyncSession = Depends(get_async_session)):

    if count > MAX_COUNT_GET_ROWS:
        raise HTTPException(status_code=500, detail="У вас большие запросы, попробуйте использовать меньшее значение")
    # Можно изменить вывод с помощью join.form()
    query = select(sub_table, User).join(User, User.id == sub_table.c.id_maker).where(sub_table.c.id_subscriber == user.id).order_by(sub_table.c.datatime).offset(offset).limit(count)
    print(query)
    subs = [row._asdict() for row in await db_session.execute(query)]

    return subs
