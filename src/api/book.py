from fastapi import APIRouter

router = APIRouter(prefix="/book", tags=["book"])

@router.get("/home")
def read_root():
    return {"Hello": "World"}


@router.get("/{book_id}",
            summary="Get book by id",
            description="Retrieves a book by its ID"
            )
async def get_book_by_id(book_id: int):
    return {"book_id": book_id}


@router.post("", 
          summary="Create book", 
          description="Adds a new book to the collection"
          )
async def create_book():
    ...
    