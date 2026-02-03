import logging
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

# Создаем папку для данных
os.makedirs("data", exist_ok=True)

# URL для SQLite
DATABASE_URL = "sqlite+aiosqlite:///data/bot.db"

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

Base = declarative_base()

# Создаем фабрику сессий
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def create_db():
    """Создание таблиц в базе данных"""
    # Импортируем модели здесь, чтобы избежать циклических импортов
    from database.models import User, Task, Habit, HabitCompletion, Transaction, Payment
    
    async with engine.begin() as conn:
        # Просто создаем таблицы без сложных проверок
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ База данных создана успешно")

async def get_db():
    """Получение сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()