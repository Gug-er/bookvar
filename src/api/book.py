from fastapi import APIRouter

from src.schemas.book import Book, BookAdd
from src.repos.book import BookRepository

router = APIRouter(prefix="/book", tags=["book"])


@router.get("/{book_id}",
            summary="Get book by id",
            description="Retrieves a book by its ID"
            )
async def get_book_by_id(book_id: int):
    return await BookRepository().get_one_or_none(id=book_id)


@router.post("", 
          summary="Create book", 
          description="Adds a new book to the collection"
          )
async def create_book():
    ...
    