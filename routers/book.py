from typing import List
from auth import AuthHandler
import models
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
import pyd
from database import get_db
from enum import Enum

router = APIRouter(
    prefix="/book",
    tags=["book"], 
)

auth_handler=AuthHandler()

class ModalClass(str,Enum):
    asc = "asc"
    desc = "desc"

# 2) сортировка книг по алфавиту 
# вывод всех существующих в базе книг
@router.get("/2/{sortirovka}",response_model=List[pyd.BookSchema])
async def get_books( sortirovka: ModalClass,db: Session = Depends(get_db)):
    if sortirovka == ModalClass.asc:
        return db.query(models.Book).order_by(models.Book.nameBook.asc()).all()
    if sortirovka == ModalClass.desc:
           return db.query(models.Book).order_by(models.Book.nameBook.desc()).all() 

# вывод книги по айди
@router.get("/{book_id}",response_model=pyd.BookSchema)
async def get_book(book_id:int,db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

# 3) предоставить возможность добавления и изменения информации о книгах в библиотеке
# заполнение таблицы с проверкой на уникальность имени
@router.post("/3/",response_model=pyd.BookSchema)
async def post_books(book_input:pyd.Book_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
   book_db=db.query(models.Book).filter(models.Book.nameBook == book_input.nameBook).first()
   if book_db:
       raise HTTPException(400, 'Имя занято, попробуйте другое')

   book_db=models.Book()
   book_db.nameBook = book_input.nameBook
   book_db.price = book_input.price
   book_db.number_of_pages = book_input.number_of_pages
   book_db.number_of_copies = book_input.number_of_pages
   book_db.yearPublished = book_input.yearPublished
   book_db.idPublisher = book_input.idPublisher
   book_db.idFaculty = book_input.idFaculty

   for library_id in book_input.libraryIds:
        library_db = db.query(models.Library).filter(models.Library.id==library_id).first()
        if library_db:
           book_db.librarys.append(library_db)
        else:
            raise HTTPException(status_code=404, detail="Не найдено")

   db.add(book_db)
   db.commit()
   return book_db

#3) предоставить возможность добавления и изменения информации о книгах в библиотеке
# обновление книги 
@router.put("/3/{book_id}",response_model=pyd.BookSchema)
async def update_book(book_id:int,book_input:pyd.Book_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    book_db = db.query(models.Book).filter(models.Book.id == book_id).first()
    book_db.nameBook = book_input.nameBook
    book_db.yearPublished = book_input.yearPublished
    book_db.price = book_input.price
    db.commit()
    return book_db


# удаление книги
@router.delete("/{book_id}")
async def delete_book(book_id:int,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    deleted_rows = db.query(models.Book).filter(models.Book.id == book_id).delete()
    if deleted_rows == 0:
        raise HTTPException(404, 'Книга не найдена')
    db.commit()
    return 'Удалено'

# 2) сортировка книг по алфавиту 

