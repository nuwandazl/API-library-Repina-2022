from typing import List
import models
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
import pyd
from database import get_db
from auth import AuthHandler

router = APIRouter(
    prefix="/user",
    tags=["user"], 
)

auth_handler = AuthHandler()

@router.post("/",response_model=pyd.User_get)
async def register_users(user_input:pyd.User_create,db: Session = Depends(get_db)):
  user_db=db.query(models.User).filter(models.User.username == user_input.username).first()

  if user_db:
      raise HTTPException(400,'Такой пользователь уже есть')
  hash_pass = auth_handler.get_password_hash(user_input.password)
  user_db=models.User(
      username = user_input.username,
      password = hash_pass
  )
  db.add(user_db)
  db.commit()
  return user_db

@router.post('/login')
def user_login(user_input:pyd.User_create, db: Session = Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == user_input.username).first()
    if not user_db:
        raise HTTPException(404, 'Вас не существует =(')

    if auth_handler.verify_password(user_input.password,user_db.password):
        token=auth_handler.encode_token(user_db.username)
        return {'token':token}
    else:
        raise HTTPException(403, 'Пароль неверен')