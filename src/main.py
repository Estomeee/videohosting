import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import sqlalchemy as db

from src.user.user import router as user_router
from src.user.authorization.router import router_auth, router_reg
from src.user.authorization.router import router as user_au_router
from src.video.router import router as router_video
from src.interactions.router import router as router_interact
from src.pages.router import router as router_pages


metadata = db.MetaData()


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(user_router)
app.include_router(router_auth,
                   prefix="/auth",
                   tags=["Auth"],
                   )
app.include_router(router_reg,
                   prefix="/auth",
                   tags=["Auth"]
                   )
app.include_router(user_au_router)
app.include_router(router_video)
app.include_router(router_interact)
app.include_router(router_pages)


@app.get('/')
def how():
    return 'Привет, Егор'


if __name__ == '__main__':
    uvicorn.run('main:app')
