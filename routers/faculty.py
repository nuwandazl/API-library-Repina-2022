from typing import List
from auth import AuthHandler
import models
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
import pyd
from database import get_db

router = APIRouter(
    prefix="/faculty",
    tags=["faculty"], 
)

auth_handler=AuthHandler()

# вывод всех существующих в базе факультетов
@router.get("/",response_model=List[pyd.FacultySchema])
async def get_faculties(db: Session = Depends(get_db)):
    return db.query(models.Faculty).all()

# вывод факультета по айди
@router.get("/{faculty_id}",response_model=pyd.FacultySchema)
async def get_faculty(faculty_id:int,db: Session = Depends(get_db)):
    return db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()

# заполнение таблицы факультеты с проверкой на уникальность имени
@router.post("/",response_model=pyd.FacultySchema)
async def post_faculties(faculty_input:pyd.Faculty_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
   faculty_db=db.query(models.Faculty).filter(models.Faculty.nameFaculty == faculty_input.nameFaculty).first()
   if faculty_db:
       raise HTTPException(400, 'Имя занято, попробуйте другое')

   faculty_db=models.Faculty()
   faculty_db.nameFaculty = faculty_input.nameFaculty
  
   for book_id in faculty_input.book_ids:
        book_db = db.query(models.Book).filter(models.Book.id==book_id).first()
        if book_db:
            #  !!!!!!!!!!!!!!!!!!!
           faculty_db.faculty.append(book_db)
        else:
            raise HTTPException(status_code=404, detail="Не найдено")
   db.add(faculty_db)
   db.commit()
   return faculty_db

# обновление факультета
@router.put("/{faculty_id}",response_model=pyd.FacultySchema)
async def update_faculty(faculty_id:int,faculty_input:pyd.Faculty_create,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    faculty_db = db.query(models.Faculty).filter(models.Book.id == faculty_id).first()
    faculty_db.nameFaculty = faculty_input.nameFaculty
    db.commit()
    return faculty_db


# удаление факультета
@router.delete("/{faculty_id}")
async def delete_faculty(faculty_id:int,db: Session = Depends(get_db),username=Depends(auth_handler.auth_wrapper)):
    deleted_rows = db.query(models.Faculty).filter(models.Faculty.id == faculty_id).delete()
    if deleted_rows == 0:
        raise HTTPException(404, 'Факультет не найден')
    db.commit()
    return 'Удалено'



