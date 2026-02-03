# Замените весь файл на этот код:
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings
import os

# Для SQLite нужно использовать aiosqlite
if settings.DATABASE_URL.startswith("sqlite"):
    # Для SQLite убираем +asyncpg и добавляем aiosqlite
    db_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
else:
    db_url = settings.DATABASE_URL

engine = create_async_engine(
    db_url,
    echo=True,  # Показывает SQL запросы в консоли
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def create_database():
    """Создает все таблицы в базе данных"""
    from database.models import Base  # Импортируем здесь, чтобы избежать циклических импортов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных создана успешно!")

async def get_session() -> AsyncSession:
    """Получаем сессию для работы с БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()