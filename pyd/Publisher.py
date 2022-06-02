from pydantic import BaseModel, Field
from typing import List

class Publisher_create(BaseModel):
    namePublisher:str = Field(...,max_length=255,example='АСТ')
    city:str = Field(...,max_length=255,example='Санкт - Петербург')
    book_ids:List[int] 
    class Config:
        orm_mode=True 

class Publisher_get(BaseModel):
    id:int
    namePublisher:str = Field(...,max_length=255,example='АСТ')
    city:str = Field(...,max_length=255,example='Санкт - Петербург')

    class Config:
        orm_mode=True 
