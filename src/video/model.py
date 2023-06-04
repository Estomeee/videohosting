from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from src.user.authorization.model import User

metadata = MetaData()

video = Table(
    "video",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(60)),
    Column("description", String),
    Column("count_likes", Integer),
    Column("id_auther", Integer, ForeignKey(User.id), nullable=False),
    Column('video_link', String, nullable=False),
    Column('poster_link', String, nullable=False)
)