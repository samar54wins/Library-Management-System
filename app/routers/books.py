# app/routers/books.py

from fastapi import APIRouter, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)],  # Use Bearer Token for all routes
)

@router.post("/create a book", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_book(db, book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create book: {str(e)}")

OPEN_LIBRARY_API_URL = "https://openlibrary.org/search.json"

@router.get("/search", response_model=List[schemas.Book])
def search_books(
    title: Optional[str] = None,
    author_name: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        # Search locally in the database
        books = crud.search_books(db, title=title, author_name=author_name, skip=skip, limit=limit)
        if books:
            return books

        # If no results are found locally, query the Open Library API
        query_params = {}
        if title:
            query_params["title"] = title
        if author_name:
            query_params["author"] = author_name
        query_params["page"] = skip // limit + 1  # Open Library uses page-based pagination

        response = requests.get(OPEN_LIBRARY_API_URL, params=query_params)
        response.raise_for_status()

        data = response.json()
        if not data.get("docs"):
            raise HTTPException(status_code=404, detail="No books found")

        # Map Open Library API response to your schema
        open_library_books = []
        for doc in data["docs"][:limit]:
            # Extracting book details and cleaning the data
            title = doc.get("title", "Unknown Title")
            authors = ", ".join(doc.get("author_name", ["Unknown Author"]))
            first_publish_year = (
                int(doc["first_publish_year"]) if doc.get("first_publish_year") else None
            )
            isbn = doc["isbn"][0] if "isbn" in doc and doc["isbn"] else None
            genre = doc.get("subject", ["Unknown"])[0] if "subject" in doc else "Unknown"

            # Map data to schema
            book = schemas.Book(
                title=title,
                author_name=authors,
                published_year=first_publish_year,
                isbn=isbn,
                genre=genre,
                type="External",  # Indicate that this data comes from Open Library
            )
            open_library_books.append(book)

        return open_library_books

    except HTTPException as http_err:
        raise http_err
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
        raise HTTPException(status_code=500, 
        detail=f"Error updating books: {str(e)}")
