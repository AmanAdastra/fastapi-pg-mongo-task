from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String
from typing import Optional
from pydantic import EmailStr

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String(30))
    email: Mapped[EmailStr] = mapped_column(String(40))
    password: Mapped[str] = mapped_column(String(100))
    phone: Mapped[int]
    profile_picture: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, fullname={self.fullname!r})"