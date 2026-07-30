from __future__ import annotations

from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from datetime import date, datetime

book_authors = Table(
    "book_authors", 
    Base.metadata,
    Column("book_id", ForeignKey("books.book_id", ondelete="CASCADE"), primary_key=True), 
    Column("author_id", ForeignKey("authors.author_id", ondelete="CASCADE"), primary_key=True), 
    )


class Series(Base):
    __tablename__ = "series"

    series_id: Mapped[int] = mapped_column(primary_key=True)
    series_title: Mapped[str] = mapped_column(index=True)
    series_description: Mapped[str | None] = mapped_column(default=None)

    books: Mapped[list[Book]] = relationship(back_populates="series")


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    book_title: Mapped[str] = mapped_column(index=True, nullable=False)
    book_description: Mapped[str | None] = mapped_column(default=None)
    book_year: Mapped[int]
    book_isbn: Mapped[str] = mapped_column(index=True, unique=True)
    book_original_language: Mapped[str]
    book_series_id: Mapped[int | None] = mapped_column(ForeignKey("series.series_id", ondelete="SET NULL"), default=None)

    series: Mapped[Series | None] = relationship(back_populates="books")
    authors: Mapped[list[Author]] = relationship(
        secondary=book_authors, 
        back_populates="books"
    )


class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    author_name: Mapped[str] = mapped_column(index=True)
    author_date_of_birth: Mapped[date | None] = mapped_column(default=None)
    author_citizenship: Mapped[str | None] = mapped_column(default=None)
    author_biography: Mapped[str | None] = mapped_column(default=None)

    books: Mapped[list[Book]] = relationship(
        secondary=book_authors,
        back_populates="authors"
    )


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(unique=True, index=True)
    user_email: Mapped[str] = mapped_column(unique=True, index=True)
    user_hash_password: Mapped[str]
    user_about: Mapped[str | None]
    user_register_date: Mapped[datetime] = mapped_column(default=datetime.now)
