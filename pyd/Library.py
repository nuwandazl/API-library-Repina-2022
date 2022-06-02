from pydantic import BaseModel, Field
import pyd 
from typing import List

class Library_create(BaseModel):
    nameLibrary:str = Field(...,max_length=255,example='Кони и лоси')
    address:str = Field(...,max_length=255,example='Мирная, 40')
    book_ids:List[int] 
    class Config:
        orm_mode=True 

class Library_get(BaseModel):
    id:int
    nameLibrary:str = Field(...,max_length=255,example='Кони и лоси')
    address:str = Field(...,max_length=255,example='Мирная, 40')
    class Config:
        orm_mode=True 