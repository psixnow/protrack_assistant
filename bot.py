import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from config.settings import settings
from database.engine import create_database, get_session
from database.models import User, Task, Habit, Finance
from utils.keyboards import get_main_keyboard, get_tasks_keyboard, get_finance_keyboard, get_habits_keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем хранилище и диспетчер
storage = MemoryStorage()
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=storage)

# Состояния для FSM (машины состояний)
class ExpenseState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_category = State()

# Хендлер команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    try:
        session = next(get_session())
        
        # Проверяем, есть ли пользователь в БД
        user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        if not user:
            # Создаем нового пользователя
            user = User(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            session.add(user)
            session.commit()
            await message.answer(f"👋 Привет, {message.from_user.first_name}!\nЯ бот для отслеживания задач, привычек и финансов.")
        else:
            await message.answer(f"👋 С возвращением, {message.from_user.first_name}!")
        
        # Показываем основное меню
        await message.answer("Выберите действие:", reply_markup=get_main_keyboard())
        
        session.close()
    except Exception as e:
        logger.error(f"Ошибка в cmd_start: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")

# Хендлер для кнопки "Финансы"
@dp.message(F.text == "💰 Финансы")
async def finances_menu(message: types.Message):
    """Меню финансов"""
    await message.answer(
        "💼 Управление финансами:",
        reply_markup=get_finance_keyboard()
    )

# Хендлер для кнопки "Задачи"
@dp.message(F.text == "📝 Задачи")
async def tasks_menu(message: types.Message):
    """Меню задач"""
    await message.answer(
        "✅ Управление задачами:",
        reply_markup=get_tasks_keyboard()
    )

# Хендлер для кнопки "Привычки"
@dp.message(F.text == "🔄 Привычки")
async def habits_menu(message: types.Message):
    """Меню привычек"""
    await message.answer(
        "🔄 Управление привычками:",
        reply_markup=get_habits_keyboard()
    )

# Хендлер для кнопки "Добавить расход" (inline кнопка)
@dp.callback_query(F.data == "add_expense")
async def add_expense_callback(callback: types.CallbackQuery, state: FSMContext):
    """Начинаем добавление расхода"""
    await callback.message.answer("💸 Введите сумму расхода (например: 500):")
    await state.set_state(ExpenseState.waiting_for_amount)
    await callback.answer()

# Хендлер для ввода суммы расхода
@dp.message(ExpenseState.waiting_for_amount)
async def process_expense_amount(message: types.Message, state: FSMContext):
    """Обработка суммы расхода"""
    try:
        amount = float(message.text)
        await state.update_data(amount=amount)
        
        # Создаем клавиатуру с категориями
        categories_keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="🍔 Еда"), types.KeyboardButton(text="🚗 Транспорт")],
                [types.KeyboardButton(text="🏠 Жилье"), types.KeyboardButton(text="👕 Одежда")],
                [types.KeyboardButton(text="💊 Здоровье"), types.KeyboardButton(text="🎲 Развлечения")],
                [types.KeyboardButton(text="📚 Образование"), types.KeyboardButton(text="🔙 Назад")],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        
        await message.answer("📂 Выберите категорию:", reply_markup=categories_keyboard)
        await state.set_state(ExpenseState.waiting_for_category)
        
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректную сумму (например: 500 или 99.99):")

# Хендлер для выбора категории
@dp.message(ExpenseState.waiting_for_category)
async def process_expense_category(message: types.Message, state: FSMContext):
    """Обработка категории расхода"""
    if message.text == "🔙 Назад":
        await message.answer("Действие отменено.", reply_markup=get_main_keyboard())
        await state.clear()
        return
    
    # Получаем данные из состояния
    data = await state.get_data()
    amount = data.get('amount')
    category = message.text
    
    try:
        session = next(get_session())
        
        # Получаем пользователя
        user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        if user:
            # Создаем запись о расходе
            expense = Finance(
                amount=amount,
                category=category.replace(" ", "").lower(),
                description=f"Расход: {category}",
                type="expense",
                payment_method="cash",
                user_id=user.id
            )
            session.add(expense)
            session.commit()
            
            await message.answer(
                f"✅ Расход успешно добавлен!\n"
                f"💸 Сумма: {amount} руб.\n"
                f"📂 Категория: {category}",
                reply_markup=get_main_keyboard()
            )
        else:
            await message.answer("❌ Пользователь не найден.")
        
        session.close()
    except Exception as e:
        logger.error(f"Ошибка при добавлении расхода: {e}")
        await message.answer("❌ Произошла ошибка при добавлении расхода.")
    
    await state.clear()

# Хендлер для команды /newhabit (создание привычки)
@dp.message(Command("newhabit"))
async def cmd_new_habit(message: types.Message):
    """Создание новой привычки через команду"""
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            await message.answer("❌ Использование: /newhabit [название] [частота]\nПример: /newhabit Утренняя зарядка ежедневно")
            return
        
        _, title, frequency = parts
        
        session = next(get_session())
        user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        if user:
            habit = Habit(
                title=title,
                frequency=frequency,
                user_id=user.id
            )
            session.add(habit)
            session.commit()
            
            await message.answer(
                f"✅ Привычка создана!\n\n"
                f"📝 Название: {title}\n"
                f"🔄 Частота: {frequency}\n"
                f"🆔 ID: {habit.id}\n\n"
                f"Отмечайте выполнение: /loghabit {habit.id}"
            )
        else:
            await message.answer("❌ Пользователь не найден. Используйте /start")
        
        session.close()
    except Exception as e:
        logger.error(f"Ошибка в cmd_new_habit: {e}")
        await message.answer("❌ Произошла ошибка при создании привычки.")

# Хендлер для команды /loghabit
@dp.message(Command("loghabit"))
async def cmd_log_habit(message: types.Message):
    """Отметка выполнения привычки"""
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.answer("❌ Использование: /loghabit [ID привычки]\nПример: /loghabit 1")
            return
        
        habit_id = int(parts[1])
        
        session = next(get_session())
        user = session.query(User).filter(User.telegram_id == message.from_user.id).first()
        
        if user:
            habit = session.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.id).first()
            
            if habit:
                # Увеличиваем счетчик
                habit.current_streak += 1
                if habit.current_streak > habit.longest_streak:
                    habit.longest_streak = habit.current_streak
                habit.last_completed = func.now()
                
                session.commit()
                
                await message.answer(
                    f"✅ Привычка отмечена как выполненная!\n\n"
                    f"📝 Название: {habit.title}\n"
                    f"🔥 Текущая серия: {habit.current_streak} дней\n"
                    f"🏆 Лучшая серия: {habit.longest_streak} дней"
                )
            else:
                await message.answer("❌ Привычка не найдена.")
        else:
            await message.answer("❌ Пользователь не найден. Используйте /start")
        
        session.close()
    except ValueError:
        await message.answer("❌ ID привычки должен быть числом.")
    except Exception as e:
        logger.error(f"Ошибка в cmd_log_habit: {e}")
        await message.answer("❌ Произошла ошибка при отметке привычки.")

# Хендлер для команды /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Помощь по командам"""
    help_text = """
🤖 **Доступные команды:**

**Основные:**
/start - Запустить бота
/help - Показать это сообщение

**Привычки:**
/newhabit [название] [частота] - Создать привычку
/loghabit [ID] - Отметить выполнение привычки
/habits - Список привычек

**Финансы:**
/addincome [сумма] [описание] - Добавить доход
/addexpense [сумма] [категория] - Добавить расход
/finance - Статистика финансов

**Задачи:**
/newtask [название] - Создать задачу
/tasks - Список задач
/done [ID] - Отметить задачу выполненной

📱 **Или используйте кнопки меню!**
"""
    await message.answer(help_text, parse_mode="Markdown")

# Основная функция запуска
async def main():
    """Основная функция запуска бота"""
    try:
        # Проверяем настройки
        if not settings.BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не установлен в .env файле")
            return
        
        # Создаем базу данных
        create_database()
        
        logger.info("🤖 Бот запускается...")
        logger.info(f"👤 Админ ID: {settings.ADMIN_ID}")
        
        # Запускаем бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())