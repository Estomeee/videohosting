from fastapi import FastAPI

import sqlalchemy as db

from src.user.user import router as user_router


metadata = db.MetaData()


app = FastAPI()

app.include_router(user_router)

@app.get('/')
def how():
    return '<ly'
