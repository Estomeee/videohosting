from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import NAME_DB, HOST_DB, PASS_DB, PORT_DB, USER_DB

DATABASE_URL = f"postgresql+asyncpg://{USER_DB}:{PASS_DB}@{HOST_DB}:{PORT_DB}/{NAME_DB}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)