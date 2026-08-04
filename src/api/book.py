from fastapi import APIRouter

from src.schemas.book import BookSchema, BookAdd
from src.dependencies.database import DBDep
from src.dependencies.pagination import PaginationDep


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


@router.get("",
            summary="Get list of all books",
            description="Retrieves a list of all books"
            )
async def get_list_of_books(
    db: DBDep,
    pagination: PaginationDep
):
    return await db.book.get_all(limit=pagination.per_page, offset=pagination.page-1)


@router.get("/{book_id}",
            summary="Get book by id",
            description="Retrieves a book by its ID"
            )
async def get_book_by_id(
    db: DBDep,
    book_id: int
):
    return await db.book.get_one_or_none(book_id=book_id)