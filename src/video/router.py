from fastapi import APIRouter

from fastapi_users import FastAPIUsers

from .model import User


from fastapi import Depends

from src.user.authorization.current_user import current_active_user
from src.user.authorization.current_user import fastapi_users


router = APIRouter(
    prefix='/video',
    tags=['Video']
)


@router.post("/protected-route/load")
def load_video(user: User = Depends(current_active_user)):
    return f"Типа залили видео"


@router.get("/protected-route")
def get_video(user: User = Depends(current_active_user)):
    pass

#Какие-то запросы