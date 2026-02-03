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
        from database.models import User, Task, Habit, Finance
        print("✅ Все модели импортируются корректно")
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return
    
    # Проверяем создание БД
    try:
        await create_database()
        print("✅ База данных создана")
    except Exception as e:
        print(f"❌ Ошибка создания БД: {e}")
        return
    
    # Проверяем клавиатуры
    try:
        from utils.keyboards import get_main_keyboard, get_tasks_keyboard
        kb1 = get_main_keyboard()
        kb2 = get_tasks_keyboard()
        print("✅ Клавиатуры создаются корректно")
    except Exception as e:
        print(f"❌ Ошибка создания клавиатур: {e}")
        return
    
    print("\n🎉 Все основные компоненты работают!")
    print("\n📋 Следующие шаги:")
    print("1. Создайте бота через @BotFather")
    print("2. Получите токен и добавьте в .env")
    print("3. Запустите: python app.py")
    print("4. Откройте Telegram и найдите своего бота")

if __name__ == "__main__":
    asyncio.run(test_setup())