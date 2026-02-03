
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

# Используем синхронный движок для SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()

def create_database():
    """Создает все таблицы в базе данных"""
    from database.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ База данных создана успешно!")

def get_session():
    """Получаем сессию для работы с БД"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

SessionLocal = AsyncSessionLocal