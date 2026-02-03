from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings
import os

# Используем синхронный движок для SQLite
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
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