from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    name: str
    nickname: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
