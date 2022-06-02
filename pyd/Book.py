from pydantic import BaseModel, Field
from typing import List

class Book_create(BaseModel):
    nameBook:str = Field(...,max_length=255,example='Клара Милич')
    price:int = Field(..., gt=0, example=99.95)
    number_of_pages:int = Field(None, gt=0, example=1)
    number_of_copies:int = Field(None, gt=0, example=1)
    yearPublished:int = Field(None, example=1863)
    idPublisher:int = Field(None, gt=0, example=1)
    idFaculty:int = Field(None, gt=0, example=1)
    libraryIds:List[int]
    class Config:
        orm_mode=True 

class Book_get(BaseModel):
    id:int
    nameBook:str = Field(...,max_length=255,example='Клара Милич')
    price:int = Field(..., gt=0, example=99.95)
    number_of_pages:int = Field(None, gt=0, example=1)
    number_of_copies:int = Field(None, gt=0, example=1)
    yearPublished:int = Field(None, example=1863)
    idPublisher:int = Field(None, gt=0, example=1)
    idFaculty:int = Field(None, gt=0, example=1)
    class Config:
        orm_mode=True 
