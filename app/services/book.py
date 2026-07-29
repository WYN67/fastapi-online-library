from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book, Author
from app.schemas.book import BookCreate

class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_book_by_id(self, book_id: int) -> Book | None:
        stmt = select(Book).where(Book.book_id == book_id).options(selectinload(Book.authors), selectinload(Book.series))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def get_book_by_isbn(self, book_isbn: str) -> Book | None:
        stmt = select(Book).where(Book.book_isbn == book_isbn).options(selectinload(Book.authors), selectinload(Book.series))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def create_book(self, book_data: BookCreate) -> Book:
        stmt = select(Author).where(Author.author_id.in_(book_data.author_ids))
        result = await self.db.execute(stmt)
        authors = result.scalars().all()
        book_clear_data = book_data.model_dump(exclude={"author_ids"})
        new_book = Book(**book_clear_data)
        new_book.authors = authors
        self.db.add(new_book)
        await self.db.commit()
        return await self.get_book_by_id(new_book.book_id)


    async def delete_book(self, book_id: int) -> bool:
        book = await self.get_book_by_id(book_id)
        if not book:
            return None
        else:
            await self.db.delete(book)
            await self.db.commit()
            return True
