from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.book import Book, Author
from app.schemas.authors import CreateAuthor


class AuthorService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_author_by_id(self, author_id: int) -> Author | None:
        stmt = select(Author).where(Author.author_id == author_id).options(selectinload(Author.books))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none


    async def create_author(self, author_data: CreateAuthor) -> Author:
        new_author = Author(**author_data.model_dump())
        self.db.add(new_author)
        await self.db.flush() 
        author_id = new_author.author_id
        await self.db.commit()
        return await self.get_author_by_id(author_id)