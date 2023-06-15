from pydantic.main import BaseModel
from datetime import datetime


class View(BaseModel):
    id_video: int
    id_user: int
    published_at: datetime


class Comment(BaseModel):
    text: str

