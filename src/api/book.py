from fastapi import APIRouter

from src.schemas.book import BookSchema, BookAdd
from src.dependencies.database import DBDep


router = APIRouter(prefix="/book", tags=["book"])


@router.post("", 
          summary="Create book", 
          description="Adds a new book to the collection"
          )
async def create_book(
    db: DBDep,
    book: BookAdd
):
  await db.book.add(book)
  await db.commit()
  return {"status": "OK", "data": book}


@router.get("/{book_id}",
            summary="Get book by id",
            description="Retrieves a book by its ID"
            )
async def get_book_by_id(
    db: DBDep,
    book_id: int
):
    return await db.get_one_or_none(id=book_id)    