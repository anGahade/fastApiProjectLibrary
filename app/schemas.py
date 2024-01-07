from pydantic import BaseModel

from typing import List


class BaseBook(BaseModel):
    title: str
    description: str | None = None
    published_year: int
    price: int
    author_id: int


class CreateBook(BaseBook):
    pass


class Book(BaseBook):
    id: int

    class Config:
        orm_mode = True


class BaseAuthor(BaseModel):
    first_name: str
    last_name: str


class CreateAuthor(BaseAuthor):
    pass


class Author(BaseAuthor):
    id: int

    class Config:
        orm_mode = True
