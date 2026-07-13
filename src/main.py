import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/home")
def read_root():
    return {"Hello": "World"}


@app.get("/{book_id}")
async def get_book_by_id(book_id: int):
    return {"book_id": book_id}


@app.post("", 
          summary="Create book", 
          description="Adds a new book to the collection"
          )
async def create_book():
    ...
    