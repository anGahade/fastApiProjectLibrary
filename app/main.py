from typing import Annotated, List
from sqlalchemy.orm import Session

from fastapi import FastAPI, Path, Query, Depends
from .schemas import Book, CreateBook
from .database import SessionLocal
from .crud import book_list_crud, book_create, book_retrieve


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

books_data = [
    {
        "id": 1,
        "title": "Who let the dog out?",
        "description": "Who? Who? Who?",
        "author": "Anton Komarov",
        "price": 1200,
        "published_year": 2023
    }, {
        "id": 2,
        "title": "Sense of the world",
        "description": "An empty book",
        "author": "Cristian Justin",
        "price": 250,
        "published_year": 1998
    }, {
        "id": 3,
        "title": "Computer science",
        "description": "be-bo-peep",
        "author": "Vlad Drakula",
        "price": 850,
        "published_year": 2004
    }
]


def get_query_params(is_active: bool, q: Annotated[str | None, Query()] = None):
    return {"q": q, "is_active": is_active}


class GetQueryParams:
    def __init__(self, is_active: bool, foo: str, q: Annotated[str | None, Query()] = None):
        self.is_active = is_active
        self.foo = foo
        self.q = q


@app.get("/books/")
async def get_book_list(db: Session = Depends(get_db)) -> List[Book]:
    books = book_list_crud(db)
    return books


@app.get("/books/{book_id}")
async def get_book(
        book_id: Annotated[int, Path(title="ID for book im my store", ge=1)],
        db: Session = Depends(get_db)
):
    book = book_retrieve(db, book_id)
    return book


@app.post("/books/", response_model=Book, status_code=201)
async def create_book(book: CreateBook, db: Session = Depends(get_db)) -> Book:
    return book_create(db, book)
