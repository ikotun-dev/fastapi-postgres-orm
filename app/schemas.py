from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    title : str
    content : str
    published : bool
 #   description : str

class User(BaseModel):
    email : str
    password : str 

class UserOut(BaseModel): 
    email : str
    created_at : datetime

    class Config:
        orm_mode = True