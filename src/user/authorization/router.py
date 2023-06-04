from fastapi import APIRouter

from fastapi_users import FastAPIUsers

from .model import User
from .user_manager import get_user_manager
from .schemas import UserCreate, UserRead, UserUpdate
from .auth import auth_backend

from fastapi import Depends

from src.user.authorization.current_user import current_active_user
from src.user.authorization.current_user import fastapi_users

router_reg = fastapi_users.get_register_router(UserRead, UserCreate)
router_auth = fastapi_users.get_auth_router(auth_backend)

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.get("/protected-route")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}"
