from enum import auto
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='password') #, cursor_factory=RealDictCursor)

        cursor = conn.cursor()

        print("Database connection was successful!")
        break

    except Exception as error:
        print("connecting to database failed")
        print("Error: ", error)
        time.sleep(2)



# request Get method url "/"
@app.get("/")
def root():
    return {"message": "Welcome to API!!!"}