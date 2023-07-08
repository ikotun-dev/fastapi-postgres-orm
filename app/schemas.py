from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    email : str
    password : str 

class UserOut(BaseModel): 
    email : str
    created_at : datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Post(BaseModel):
    title : str
    content : str
    published : bool
 #   description : str

class PostOut(Post):
    user_id : int
    owner : UserOut

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
