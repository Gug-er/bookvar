from src.schemas.book import BookAdd
from src.utils.db_manager import DBManager
from src.db_engine import async_session_maker


async def test_create_book():
    book_data = BookAdd(
                    title='Crime and Punishment', 
                    author='Fyodor Dostoevsky', 
                    year=1866, 
                    annotation='A destitute former student commits murder to test his own theory of moral exceptionalism, then unravels under guilt.', 
                    genre='novel'
                )
    async with DBManager(session_factory=async_session_maker) as db:
        await db.book.add(book_data)
        await db.commit()
    