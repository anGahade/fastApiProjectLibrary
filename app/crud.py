from sqlalchemy.orm import Session

from .models import Book
from .schemas import CreateBook


def book_list_crud(db: Session):
    return db.query(Book).all()


def book_create(db: Session, book: CreateBook):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def book_retrieve(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

