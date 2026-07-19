from src.repos.base import BaseRepository
from src.models.book import BookModel
from src.schemas.book import BookSchema


class BookRepository(BaseRepository):
    model = BookModel
    schema = BookSchema