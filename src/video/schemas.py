from pydantic import BaseModel


class Video(BaseModel):
    id: int
    title: str
    description: str
    count_likes: int
    id_auther: int
    video_link: str
    poster_link: str
    #published_at: datatime