from sqlalchemy.ext.asyncio import AsyncSession

from app.models.book import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_user_by_id(self, user_id: int) -> User | None:
        pass


    async def get_user_by_email(self, user_email: str) -> User | None:
        pass


    async def get_user_by_username(self, username: str) -> User | None:
        pass


    def create_user(self, user_data: dict) -> User:
        pass