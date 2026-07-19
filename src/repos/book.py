from src.repos.base import BaseRepository
from src.models.book import BookModel

class BookRepository(BaseRepository):
    model = BookModel