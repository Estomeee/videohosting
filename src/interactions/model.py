from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, func

from src.user.authorization.model import User
from src.video.model import metadata as md

metadata = MetaData()


comment = Table(
    "comment",
    md,
    Column("id", String(length=40), primary_key=True),
    Column("text", String),
    Column("id_video", String(length=40), ForeignKey("video.id", ondelete='CASCADE'), nullable=False),
    Column("id_auther", Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False),
    Column('published_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
)

like = Table(
    "like",
    md,
    Column("id_video", String(length=40), ForeignKey("video.id", ondelete='CASCADE'), nullable=False, primary_key=True),
    Column("id_auther", Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('published_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
)

view = Table(
    "view",
    md,
    Column("id_video", String(length=40), ForeignKey("video.id", ondelete='CASCADE'), nullable=False, primary_key=True),
    Column("id_user", Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('published_at', DateTime(timezone=True), server_default=func.now(), nullable=False)
)

sub = Table(
    "sub",
    metadata,
    Column("id_maker", Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False, primary_key=True),
    Column("id_subscriber", Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False, primary_key=True),
    Column('datatime', DateTime(timezone=True), server_default=func.now(), nullable=False)
)
