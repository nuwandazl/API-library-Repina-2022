# REST КОНТРОЛЕР

from unicodedata import numeric
from fastapi import FastAPI, Depends
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import pyd
import routers
# создание БД из нашей модели
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.book_router)
app.include_router(routers.library_router)
app.include_router(routers.user_router)
app.include_router(routers.autor_router)
app.include_router(routers.publisher_router)
app.include_router(routers.faculty_router)