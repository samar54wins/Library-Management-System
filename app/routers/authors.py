from fastapi import APIRouter, Depends, HTTPException  
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
    dependencies=[Depends(get_current_user)], 
     responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorBase, db: Session = Depends(get_db)):
    try:
        return crud.create_author(db, author)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create author: {str(e)}")

@router.get("/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        authors = crud.get_authors(db, skip=skip, limit=limit)
        if not authors:
            raise HTTPException(status_code=404, detail="No authors found")
        return authors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving authors: {str(e)}")


@router.put("/", response_model=schemas.Author)
def update_authors(author: schemas.AuthorBase, author_id: int = None, db: Session = Depends(get_db)):
    try:
        authors = crud.update_author(db, author_id, author)
        return authors
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update author: {str(e)}")


@router.delete("/", response_model=schemas.Author)
def delete_authors(author_id: int = None, db: Session = Depends(get_db)):
    try:
        authors = crud.delete_author(db, author_id)
        return authors
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete author: {str(e)}")


