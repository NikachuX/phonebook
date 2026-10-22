from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class PhoneBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    mobile: Mapped[str] = mapped_column(String(20))