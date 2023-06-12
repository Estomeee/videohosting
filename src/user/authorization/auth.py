from typing import AsyncGenerator

from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from .model import User
from src.entrypoint_db import get_async_session
from config import SECRET as secret
from src.entrypoint_db import async_session_maker

cookie_transport = CookieTransport(cookie_max_age=3600)

SECRET = secret


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
