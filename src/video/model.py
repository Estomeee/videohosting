from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, func, BigInteger
from src.user.authorization.model import User

metadata = MetaData()

video = Table(
    "video",
    metadata,
    Column("id", String(length=40), primary_key=True),
    Column("title", String(60)),
    Column("description", String),
    Column("count_likes", Integer, default=0),
    Column("count_comments", Integer, default=0),
    Column("count_views", Integer, server_default='0'),
    Column("id_auther", Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False),
    Column("nickname", String, server_default='defualt', nullable=False),
    Column('video_link', String, nullable=False),
    Column('poster_link', String, nullable=False),
    Column('published_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
)
