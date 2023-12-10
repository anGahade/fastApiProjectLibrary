from pydantic import BaseModel
from typing import List, Optional


class Book(BaseModel):
    id: int
    title: str
    description: str | None = None
    author: str
    published_year: int


class BookWithPrice(Book):
    price: int


class Employees(BaseModel):
    first_name: str
    last_name: str
    date_joined: int
    age: int
    city: str
    library_id: int
    is_active: bool
    salary: int


class EmployeeListResponse(BaseModel):
    employees: List[Employees]
    q: Optional[str] = None
    content_type: Optional[str] = None
