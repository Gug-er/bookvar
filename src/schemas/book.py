from pydantic import BaseModel

class BookAdd(BaseModel):
    title: str
    author: str
    year: int
    annotation: str
    genre: str

class Book(BookAdd):
    id: int