import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def main():
    print(f"Пробуем подключиться к: {settings.DATABASE_URL}")
    engine = create_async_engine(settings.DATABASE_URL)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ УСПЕХ! Ответ базы:", result.scalar())
    except Exception as e:
        print("❌ ОШИБКА ПОДКЛЮЧЕНИЯ:")
        print(type(e), e)

asyncio.run(main())