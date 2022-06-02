from pydantic import BaseModel, Field
from typing import List

class Faculty_create(BaseModel):
    nameFaculty:str = Field(...,max_length=255,example='Филологический')
    book_ids:List[int] 
    class Config:
        orm_mode=True 

class Faculty_get(BaseModel):
    id:int
    nameFaculty:str = Field(...,max_length=255,example='Филологический')

    class Config:
        orm_mode=True 
