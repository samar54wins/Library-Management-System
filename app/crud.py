# app/crud.py
from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas
from .auth import get_password_hash
from fastapi import HTTPException


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.UserResponse(
        id=db_user.id.__int__(),
        username=str(db_user.username),
        email=str(db_user.email)
    )

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def search_books(db: Session, title: Optional[str] = None, author_name: Optional[str] = None, skip: int = 0, limit: int = 10):
    query = db.query(models.Book, models.Author.author_name).join(models.Author, models.Book.author_id == models.Author.author_id)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author_name:
        query = query.filter(models.Author.author_name.ilike(f"%{author_name}%"))

    books = query.offset(skip).limit(limit).all()

    # Map query result into Book schema
    return [
        {
            "book_id": book.book_id,
            "title": book.title,
            "author_id": book.author_id,
            "author_name": author_name,
            "isbn": book.isbn,
            "published_year": book.published_year,
            "genre": book.genre,
            "type": "Local",
        }
        for book, author_name in books
    ]



def create_author(db: Session, author: schemas.AuthorBase):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()


def update_author(db: Session, author_id: int, author_update: schemas.AuthorBase):
    # Fetch the author record by author_id
    db_author = db.query(models.Author).filter(models.Author.author_id == author_id).first()
    
    # If author is not found, raise an exception
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    # Update the fields of the author record
    for key, value in author_update.dict(exclude_unset=True).items():
        setattr(db_author, key, value)

    # Commit changes to the database
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    # Fetch the author record by author_id
    db_author = db.query(models.Author).filter(models.Author.author_id == author_id).first()

    # If author is not found, raise an exception
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
      
      

    # Delete the author record
    db.delete(db_author)
    db.commit()
    return {"message": "Author deleted successfully"}