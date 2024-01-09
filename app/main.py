from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException

from database import SessionLocal
from schemas import Book, CreateBook, Author, CreateAuthor
from crud import book_list_crud, book_create, book_retrieve, book_update, book_delete, author_create, author_list_crud, author_retrieve


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Книги
@app.get("/books/", response_model=List[Book])
async def get_book_list(db: Session = Depends(get_db)) -> List[Book]:
    books = book_list_crud(db)
    return books


@app.get("/books/{book_id}", response_model=Book)
async def get_book(
        book_id: int,
        db: Session = Depends(get_db)
):
    book = book_retrieve(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books/", response_model=Book, status_code=201)
async def create_book(book: CreateBook, db: Session = Depends(get_db)) -> Book:
    return book_create(db, book)


@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: CreateBook, db: Session = Depends(get_db)) -> Book:
    updated_book = book_update(db, book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@app.delete("/books/{book_id}", response_model=Book)
async def delete_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    deleted_book = book_delete(db, book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book


# Автори
@app.get("/authors/", response_model=List[Author])
async def get_author_list(db: Session = Depends(get_db)) -> List[Author]:
    authors = author_list_crud(db)
    return authors


@app.get("/authors/{author_id}", response_model=Author)
async def get_author(
        author_id: int,
        db: Session = Depends(get_db)
):
    author = author_retrieve(db, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.post("/authors/", response_model=Author, status_code=201)
async def create_author(author: CreateAuthor, db: Session = Depends(get_db)) -> Author:
    return author_create(db, author)
