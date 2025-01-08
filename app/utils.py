import requests
from fastapi import HTTPException

def fetch_book_details_by_name(book_name: str):
    """
    Fetch book details from Open Library API using the book name.
    """
    url = f"https://openlibrary.org/search.json?q={book_name}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to fetch data from Open Library API")
    
    data = response.json()
    if not data.get("docs"):
        raise HTTPException(status_code=404, detail="No books found with the given name")
    
    # Fetch the first book's details
    first_book = data["docs"][0]
    return {
        "title": first_book.get("title"),
        "author_names": first_book.get("author_name", []),
        "publish_year": first_book.get("first_publish_year"),
        "isbn_list": first_book.get("isbn", [])
    }
