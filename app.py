import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import settings
from database.engine import create_database
from handlers import start, tasks, habits, finance, admin, subscription
from middlewares.subscription import SubscriptionMiddleware

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Основная функция запуска бота"""
    
    # Проверяем настройки
    try:
        settings.validate()
    except ValueError as e:
        logger.error(f"Ошибка настроек: {e}")
        return
    
    # Создаем базу данных
    create_database()
    
    # Инициализируем бота и диспетчер
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Подключаем middleware
    dp.update.outer_middleware(SubscriptionMiddleware())
    
    # Регистрируем роутеры
    dp.include_router(start.router)
    dp.include_router(tasks.router)
    dp.include_router(habits.router)
    dp.include_router(finance.router)
    dp.include_router(admin.router)
    dp.include_router(subscription.router)
    
    # Запускаем бота
    logger.info("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())