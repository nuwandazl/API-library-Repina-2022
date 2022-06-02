from typing import List
from auth import AuthHandler
import models
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
import pyd
from database import get_db

router = APIRouter(
    prefix="/library",
    tags=["library"], 
)

auth_handler=AuthHandler()

# вывод всех существующих в базе библиотек
@router.get("/",response_model=List[pyd.LibrarySchema])
async def get_librarys(db: Session = Depends(get_db)):
    return db.query(models.Library).all()

# вывод библиотеки по айди
@router.get("/{library_id}",response_model=pyd.LibrarySchema)
async def get_library(library_id:int,db: Session = Depends(get_db)):
    return db.query(models.Library).filter(models.Library.id == library_id).first()

# 4) предоставить возможность добавления и изменения информации о филиалах
# заполнение таблицы с проверкой на уникальность имени
@router.post("/4/",response_model=pyd.LibrarySchema)
async def post_librarys(library_input:pyd.Library_create,db: Session = Depends(get_db),username=Depends(AuthHandler.auth_wrapper)):
   library_db=db.query(models.Library).filter(models.Library.nameLibrary == library_input.nameLibrary).first() 
#  делаем запрос к таблице Library, где в таблице поле имя сравнивается с полем в лабрари инпут, ищем библиотеку с таким же именем, если такая есть, то пишем, что имя заянято
   if library_db:
       raise HTTPException(400, 'Имя занято, попробуйте другое')
# заполнение каждого поля по отдельности
   library_db=models.Library()
   library_db.nameLibrary = library_input.nameLibrary
   library_db.address = library_input.address
#    получаем айди если книга сущетсвует, то добавляем, если нет, то ошибка
   for book_id in library_input.book_ids:
        book_db = db.query(models.Book).filter(models.Book.id==book_id).first()
        if book_db:
           library_db.books.append(book_db)
        else:
            raise HTTPException(status_code=404, detail="Не найдено")
   db.add(library_db)
   db.commit()
   return library_db

# 4) предоставить возможность добавления и изменения информации о филиалах
# обновление библиотеки
@router.put("/4/{library_id}",response_model=pyd.LibrarySchema)
async def update_library(library_id:int,library_input:pyd.Library_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    library_db = db.query(models.Library).filter(models.Library.id == library_id).first()
    library_db.nameLibrary = library_input.nameLibrary
    library_db.address = library_input.address
    library_db.books.clear()
    for book_id in library_input.book_ids:
        book_db = db.query(models.Book).filter(models.Book.id==book_id).first()
        if book_db:
           library_db.books.append(book_db)
        else:
            raise HTTPException(status_code=404, detail="Не найдено")
    db.commit()
    return library_db


# удаление библиотеки
@router.delete("/{library_id}")
async def delete_library(library_id:int,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    deleted_rows = db.query(models.Library).filter(models.Library.id == library_id).delete()
    if deleted_rows == 0:
        raise HTTPException(404, 'Такой филиал библиотеки не найден')
    db.commit()
    return 'Удалено'

# 1) Для указанного филиала посчитать количество экземпляров указанной книги, находящихся в нём
@router.get("/7/{library_id}/{book_id}")
async def book_count(library_id: int,  book_id: int, db:Session = Depends(get_db)):
        lib=db.query(models.Book).filter(models.Book.librarys.any(id = library_id), models.Book.id == book_id).all() 
        i = 0
        # return lib
        for j in lib:
            i+= j.number_of_copies
        return i