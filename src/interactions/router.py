from fastapi import APIRouter

from fastapi_users import FastAPIUsers

from .model import User


from fastapi import Depends

from src.user.authorization.current_user import current_active_user


router = APIRouter(
    prefix='/interactions',
    tags=['Interactions']
)

# Адреса поменять добавить по необходимости
@router.get("/protected-route")
def put_like(user: User = Depends(current_active_user)):
    pass

@router.get("/protected-route")
def remove_like(user: User = Depends(current_active_user)):
    pass

@router.get("/protected-route")
def add_comment(user: User = Depends(current_active_user)):
    pass

@router.get("/protected-route")
def remove_comment(user: User = Depends(current_active_user)):
    pass

@router.get("/protected-route")
def subscribe(user: User = Depends(current_active_user)):
    pass

@router.get("/protected-route")
def unsubscribe(user: User = Depends(current_active_user)):
    pass
