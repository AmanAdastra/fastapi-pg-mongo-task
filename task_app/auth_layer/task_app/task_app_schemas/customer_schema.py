from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, BigInteger
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
    phone: Mapped[int] = mapped_column(BigInteger())
    profile_picture: Mapped[str] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, fullname={self.fullname!r})"