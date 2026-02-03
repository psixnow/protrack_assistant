import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Settings:
    """Настройки приложения без pydantic-settings"""
    
    # Бот
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Админ
    ADMIN_ID: int = int(os.getenv("ADMIN_ID", 0))
    
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///database.db")
    
    # Платежи (опционально)
    PAYMENTS_TOKEN: str = os.getenv("PAYMENTS_TOKEN", "")
    
    # Логирование
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self):
        """Проверка обязательных настроек"""
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не установлен в .env файле")
        if not self.ADMIN_ID:
            raise ValueError("ADMIN_ID не установлен в .env файле")
        
        print("✅ Настройки загружены корректно")
        return True

# Создаем экземпляр настроек
settings = Settings()