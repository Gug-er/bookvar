from sqlalchemy.orm import Mapped, mapped_column

from src.db_engine import Base

class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    super_user: Mapped[bool] = mapped_column(default=False)