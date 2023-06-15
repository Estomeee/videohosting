from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, DateTime, func

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(30))
    nickname = Column("fullname", String, server_default='defualt')
    link_img = Column("link_img", String, server_default='https://storage.yandexcloud.net/urfube-emegor/default_user.png')
    count_subs = Column("count_subs", Integer, default=0)
    created_at = Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
    '''
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    '''