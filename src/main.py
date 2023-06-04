from fastapi import FastAPI

import sqlalchemy as db

from src.user.user import router as user_router
from src.user.authorization.router import router_auth, router_reg
from src.user.authorization.router import router as user_au_router

from fastapi import FastAPI


metadata = db.MetaData()


app = FastAPI()

app.include_router(user_router)
app.include_router(router_auth,
                   prefix="/auth",
                   tags=["auth"],
                   )
app.include_router(router_reg,
                   prefix="/auth",
                   tags=["auth"]
                   )
app.include_router(user_au_router)

@app.get('/')
def how():
    return '<ly'
