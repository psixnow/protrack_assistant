import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all():
    print("🧪 Финальный тест проекта...")
    
    # 1. Проверка Python версии
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # 2. Проверка настроек
    try:
        from config.settings import settings
        print("✅ Настройки загружены")
    except Exception as e:
        print(f"❌ Ошибка настроек: {e}")
        return
    
    # 3. Проверка БД (синхронная!)
    try:
        from database.engine import create_database
        create_database()  # БЕЗ await!
        print("✅ База данных создана")
    except Exception as e:
        print(f"❌ Ошибка БД: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Проверка хендлеров
    try:
        from handlers.start import router as start_router
        print("✅ Хендлеры импортируются")
    except Exception as e:
        print(f"⚠️  Предупреждение хендлеров: {e}")
    
    # 5. Проверка клавиатур
    try:
        from utils.keyboards import get_main_keyboard
        keyboard = get_main_keyboard()
        print("✅ Клавиатуры создаются")
    except Exception as e:
        print(f"❌ Ошибка клавиатур: {e}")
        return
    
    print("\n" + "="*50)
    print("🎉 Проект готов к запуску!")
    print("="*50)
    print("\n📋 Следующие шаги:")
    print("1. Создайте файл .env с токеном бота")
    print("2. Запустите бота: python app.py")
    print("3. Откройте Telegram и найдите своего бота")

if __name__ == "__main__":
    test_all()  # БЕЗ asyncio!