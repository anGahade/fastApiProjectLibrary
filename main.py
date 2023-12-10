from typing import Annotated, Any

from fastapi import FastAPI, Body, Path, Query, Cookie, Header, HTTPException
from schemas import Book, BookWithPrice, Employees, EmployeeListResponse
from typing import Optional


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
employees_data = [
    {
        "first_name": "Kate",
        "last_name": "Pysarenko",
        "date_joined": 20141120,
        "age": 25,
        "city": "Kharkiv",
        "library_id": 1,
        "is_active": True,
        "salary": 200,
    },
    {
        "first_name": "John",
        "last_name": "Krasinski",
        "date_joined": 20041205,
        "age": 29,
        "city": "Odessa",
        "library_id": 2,
        "is_active": False,
        "salary": 2000,
    }
]


@app.get("/books/")
async def get_book_list(q: Annotated[str | None, Query()] = None, content_type: Annotated[str | None, Header()] = None):
    # if pricegt is not None:
    #     books = list(filter(lambda x: x["price"] > pricegt, books_data))
    #     return {"books": books}
    return {"books": books_data, "q": q, "content_type": content_type}


@app.get("/books/{book_id}")
async def get_book(book_id: Annotated[int, Path(title="ID for book im my store", ge=1)], q: str | None = None):
    book = list(filter(lambda x: x["id"] == book_id, books_data))[0]
    book["q"] = q
    return book


@app.post("/books/{book_id}", response_model=Book)
async def create_book(book: BookWithPrice) -> Book:
    return book


def filter_employees(q: Optional[str] = None, min_age: Optional[int] = None, max_salary: Optional[int] = None):
    filtered_employees = employees_data

    if q:
        filtered_employees = [emp for emp in filtered_employees if q.lower() in emp["first_name"].lower() or q.lower() in emp["last_name"].lower()]

    if min_age is not None:
        filtered_employees = [emp for emp in filtered_employees if emp["age"] >= min_age]

    if max_salary is not None:
        filtered_employees = [emp for emp in filtered_employees if emp["salary"] <= max_salary]

    return filtered_employees


@app.get("/employees/", response_model=EmployeeListResponse, tags=["employees"])
async def get_employees_list(
    q: Optional[str] = Query(None, title="Filter employees by name", description="Enter a name to filter employees."),
    min_age: Optional[int] = Query(None, title="Filter employees by minimum age", description="Enter the minimum age."),
    max_salary: Optional[int] = Query(None, title="Filter employees by maximum salary", description="Enter the "
                                                                                                    "maximum salary.")
):
    filtered_employees = filter_employees(q, min_age, max_salary)
    return {"employees": filtered_employees, "q": q, "min_age": min_age, "max_salary": max_salary}


@app.post("/employees/", response_model=Employees, tags=["employees"])
async def create_employee(employee: Employees):
    validate_employee(employee)
    employees_data.append(employee.dict())
    return employee


def validate_employee(employee: Employees):
    if employee.age < 18:
        raise HTTPException(status_code=406, detail="Employee must be at least 18 years old.")

    if employee.salary < 0:
        raise HTTPException(status_code=400, detail="Salary must be a positive value.")
