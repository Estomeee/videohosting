from pydantic.main import BaseModel
from datetime import datetime
from sqlalchemy import MetaData
from src.interactions.model import view as view_t

from sqlalchemy import DateTime


class View(BaseModel):
    id_video: int
    id_user: int
    published_at: datetime


class Comment(BaseModel):
    text: str

