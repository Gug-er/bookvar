from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.db_engine import Base

class BookModel(Base):
    __tablename__ = "books"
    
    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    annotation: Mapped[str] = mapped_column()
    genre: Mapped[str] = mapped_column()