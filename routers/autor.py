from typing import List
from auth import AuthHandler
import models
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
import pyd
from database import get_db

router = APIRouter(
    prefix="/autor",
    tags=["autor"], 
)

auth_handler=AuthHandler()

# вывод всех существующих в базе авторов
@router.get("/",response_model=List[pyd.AutorSchema])
async def get_autors(db: Session = Depends(get_db)):
    return db.query(models.Autor).all()

# вывод автора по айди
@router.get("/{autor_id}",response_model=pyd.AutorSchema)
async def get_autor(autor_id:int,db: Session = Depends(get_db)):
    return db.query(models.Autor).filter(models.Autor.id == autor_id).first()

# заполнение таблицы с проверкой на уникальность имени
@router.post("/",response_model=pyd.AutorSchema)
async def post_autors(autor_input:pyd.Autor_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
   autor_db=db.query(models.Autor).filter(models.Autor.surname == autor_input.surname).first()
   if autor_db:
       raise HTTPException(400, 'Имя занято, попробуйте другое')

   autor_db=models.Autor()
   autor_db.name = autor_input.name
   autor_db.middleName = autor_input.middleName
   autor_db.surname = autor_input.surname
  
   for book_id in autor_input.book_ids:
        book_db = db.query(models.Book).filter(models.Book.id==book_id).first()
        if book_db:
           autor_db.books.append(book_db)
        else:
            raise HTTPException(status_code=404, detail="Не найдено")
   db.add(autor_db)
   db.commit()
   return autor_db

# обновление автора
@router.put("/{autor_id}",response_model=pyd.AutorSchema)
async def update_autor(autor_id:int,autor_input:pyd.Autor_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    autor_db = db.query(models.Autor).filter(models.Book.id == autor_id).first()
    autor_db.name = autor_input.name
    autor_db.middleName = autor_input.middleName
    autor_db.surname = autor_input.surname
    db.commit()
    return autor_db


# удаление автора
@router.delete("/{autor_id}")
async def delete_autor(autor_id:int,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    deleted_rows = db.query(models.Autor).filter(models.Autor.id == autor_id).delete()
    if deleted_rows == 0:
        raise HTTPException(404, 'Автор не найден')
    db.commit()
    return 'Удалено'

