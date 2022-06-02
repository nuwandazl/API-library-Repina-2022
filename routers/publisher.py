from typing import List
from auth import AuthHandler
import models
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
import pyd
from database import get_db

router = APIRouter(
    prefix="/publisher",
    tags=["publisher"], 
)

auth_handler=AuthHandler()

# вывод всех существующих в базе авторов
@router.get("/",response_model=List[pyd.PublisherSchema])
async def get_publishers(db: Session = Depends(get_db)):
    return db.query(models.Publisher).all()

# вывод автора по айди
@router.get("/{publisher_id}",response_model=pyd.PublisherSchema)
async def get_publisher(publisher_id:int,db: Session = Depends(get_db)):
    return db.query(models.Publisher).filter(models.Publisher.id == publisher_id).first()

# заполнение таблицы с проверкой на уникальность имени
@router.post("/",response_model=pyd.PublisherSchema)
async def post_autors(publisher_input:pyd.Publisher_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
   publisher_db=db.query(models.Publisher).filter(models.Publisher.namePublisher == publisher_input.namePublisher).first()
   if publisher_db:
       raise HTTPException(400, 'Имя издательства занято, попробуйте другое')

   publisher_db=models.Publisher()
   publisher_db.namePublisher = publisher_input.namePublisher
   publisher_db.city = publisher_input.city
   
   for book_id in publisher_input.book_ids:
        book_db = db.query(models.Book).filter(models.Book.id==book_id).first()
        if book_db:
            # ЧОТ НАДО ПОДУМАТЬ ПРО АУТОРС (ПАБЛИШЕРС)
           publisher_db.books.append(book_db)
        else:
            raise HTTPException(status_code=404, detail="Не найдено")
   db.add(publisher_db)
   db.commit()
   return publisher_db

# обновление автора
@router.put("/{publisher_id}",response_model=pyd.PublisherSchema)
async def update_publisher(publisher_id:int,publisher_input:pyd.Publisher_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    publisher_db = db.query(models.Publisher).filter(models.Book.id == publisher_id).first()
    publisher_db.namePublisher = publisher_input.namePublisher
    publisher_db.city = publisher_input.city
    db.commit()
    return publisher_db


# удаление автора
@router.delete("/{publisher_id}")
async def delete_publisher(publisher_id:int,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    deleted_rows = db.query(models.Publisher).filter(models.Publisher.id == publisher_id).delete()
    if deleted_rows == 0:
        raise HTTPException(404, 'Издательство не найдено')
    db.commit()
    return 'Удалено'

