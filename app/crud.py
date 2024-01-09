from sqlalchemy.orm import Session
from models import Book, Author
from schemas import CreateBook, CreateAuthor


# Книги
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


def book_update(db: Session, book_id: int, book: CreateBook):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        for key, value in book.model_dump(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def book_delete(db: Session, book_id: int):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book


# Автори
def author_list_crud(db: Session):
    return db.query(Author).all()


def author_create(db: Session, author: CreateAuthor):
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def author_retrieve(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()
