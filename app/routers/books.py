# app/routers/books.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)],  # Use Bearer Token for all routes
)
@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create book: {str(e)}")

@router.get("/search", response_model=List[schemas.Book])
def search_books(
    title: str = None,
    author_name: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        books = crud.search_books(db, title=title, author_name=author_name, skip=skip, limit=limit)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching books: {str(e)}")


@router.delete("/", response_model=List[schemas.Book])
def delete_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        books = crud.search_books(db, skip=skip, limit=limit)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting books: {str(e)}")

@router.put("/", response_model=List[schemas.Book])
def update_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        books = crud.search_books(db, skip=skip, limit=limit)
        if not books:
            raise HTTPException(status_code=404, detail="No books found")
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating books: {str(e)}")
