from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Author Schemas
class AuthorBase(BaseModel):
    author_name: str
    bio: Optional[str] = None
    date_of_birth: Optional[date] = None

    class Config:
        from_attributes = True
    #    orm_mode = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class Author(AuthorBase):
    author_id: Optional[int]

# Book Schemas
class BookBase(BaseModel):
    title: str
    author_id: Optional[int]
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None

    class Config:
        from_attributes = True
    #    orm_mode = True

class Book(BookBase):
    book_id: Optional[int]

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
    #    orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
    #    orm_mode = True

# Authentication Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True
    #    orm_mode = True

class BookCreate(BookBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str
#    orm_mode = True