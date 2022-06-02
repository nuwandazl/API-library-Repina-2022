from pydantic import BaseModel, Field
from typing import List

class User_create(BaseModel):
    username:str = Field(...,max_length=255,example='SleepySailor534')
    password :str = Field(...,max_length=255,example='')
  
    class Config:
        orm_mode=True 

class User_get(BaseModel):
    id:int = Field(None ,gt=0, example=1)
    username:str = Field(...,max_length=255,example='SleepySailor534')
    
    class Config:
        orm_mode=True 
