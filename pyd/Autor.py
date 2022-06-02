from pydantic import BaseModel, Field
from typing import List

class Autor_create(BaseModel):
    name:str = Field(...,max_length=255,example='Лев')
    middleName:str = Field(...,max_length=255,example='Николаевич')
    surname:str = Field(...,max_length=255,example='Толстой')
    book_ids:List[int] 
    class Config:
        orm_mode=True 

class Autor_get(BaseModel):
    id:int
    name:str = Field(...,max_length=255,example='Лев')
    middleName:str = Field(...,max_length=255,example='Николаевич')
    surname:str = Field(...,max_length=255,example='Толстой')
    class Config:
        orm_mode=True 
