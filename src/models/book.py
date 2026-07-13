from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import Base

class BookModel(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
   