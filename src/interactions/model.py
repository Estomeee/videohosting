from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from src.user.authorization.model import User
from src.video.model import video

from src.video.model import metadata as md

metadata = MetaData()

comment = Table(
    "comment",
    md,
    Column("id", Integer, primary_key=True),
    Column("text", String),
    Column("id_video", Integer, ForeignKey("video.id"), nullable=False),
    Column("id_auther", Integer, ForeignKey(User.id), nullable=False)
)

like = Table(
    "like",
    md,
    Column("id", Integer, primary_key=True),
    Column("id_video", Integer, ForeignKey("video.id"), nullable=False),
    Column("id_auther", Integer, ForeignKey(User.id), nullable=False)
)

sub = Table(
    "sub",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_maker", Integer, ForeignKey(User.id), nullable=False),
    Column("id_subscriber", Integer, ForeignKey(User.id), nullable=False)
)
