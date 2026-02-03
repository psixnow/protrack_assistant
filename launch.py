import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_setup():
    """Быстрая проверка всех компонентов"""
    print("🧪 Тестирование компонентов проекта...")
    
    # Проверяем импорты
    try:
        from database.engine import create_database, engine
        from database.models import User, Task, Habit, Finance, HabitCompletion
        print("✅ Все модели импортируются корректно")
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Проверяем создание БД
    try:
        await create_database()
        print("✅ База данных создана")
        
        # Проверяем подключение к БД
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        print("✅ Подключение к БД работает")
    except Exception as e:
        print(f"❌ Ошибка создания/подключения к БД: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Проверяем клавиатуры
    try:
        from utils.keyboards import get_main_keyboard, get_tasks_keyboard
        kb1 = get_main_keyboard()
        kb2 = get_tasks_keyboard()
        print("✅ Клавиатуры создаются корректно")
    except Exception as e:
        print(f"❌ Ошибка создания клавиатур: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Проверяем конфигурацию
    try:
        from config.settings import settings
        print(f"✅ Конфигурация загружена")
        print(f"   DATABASE_URL: {settings.DATABASE_URL[:30]}...")
    except Exception as e:
        print(f"❌ Ошибка загрузки конфигурации: {e}")
        return
    
    # Проверяем хендлеры
    try:
        from handlers.start import router as start_router
        from handlers.tasks import router as tasks_router
        from handlers.habits import router as habits_router
        from handlers.finance import router as finance_router
        print("✅ Все хендлеры импортируются корректно")
    except Exception as e:
        print(f"⚠️ Предупреждение при импорте хендлеров: {e}")
    
    print("\n" + "="*50)
    print("🎉 Все основные компоненты работают!")
    print("="*50)
    print("\n📋 Следующие шаги:")
    print("1. Создайте бота через @BotFather (если еще не создан)")
    print("2. Получите токен и добавьте в .env файл:")
    print("   BOT_TOKEN=ваш_токен_здесь")
    print("3. Добавьте ваш Telegram ID в .env:")
    print("   ADMIN_ID=ваш_id_здесь")
    print("4. Запустите: python app.py")
    print("5. Откройте Telegram и найдите своего бота")
    print("\n⚠️  Убедитесь, что файл .env существует и содержит токен!")

if __name__ == "__main__":
    asyncio.run(test_setup())