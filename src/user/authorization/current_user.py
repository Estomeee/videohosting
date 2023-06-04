from fastapi_users.authentication import AuthenticationBackend, CookieTransport, JWTStrategy
from fastapi_users import FastAPIUsers

from .user_manager import get_user_manager
from .model import User
from src.user.authorization.auth import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
