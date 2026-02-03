from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode  # Импортируем ParseMode из aiogram.enums

from utils.keyboards import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = """
🖤 <b>Добро пожаловать в ProTrack Assistant!</b>

Я ваш личный помощник для продуктивности. Давайте начнем!

<b>Основные возможности:</b>
✅ <b>Задачи</b> — ставьте цели и отслеживайте прогресс
🔄 <b>Привычки</b> — формируйте полезные ритуалы  
💰 <b>Финансы</b> — контролируйте доходы и расходы
🤖 <b>AI-помощник</b> — получайте персональные советы

<b>Ваш текущий план:</b> 🎯 <b>БЕСПЛАТНЫЙ</b>
• 10 задач в день
• 5 активных привычек  
• Базовый финансовый трекер
• 3 AI-запроса в день

<b>Начните с команды:</b> /tasks — добавить первую задачу
<b>Все команды:</b> /help

<i>Обновите план для большего!</i> /subscriptions
"""
    
    await message.answer(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )
    
    # Регистрируем пользователя в базе данных
    try:
        from database.models import User
        from sqlalchemy.ext.asyncio import AsyncSession
        from sqlalchemy import select
        
        from database.engine import engine
        from sqlalchemy.ext.asyncio import async_sessionmaker
        
        # Создаем сессию
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        
        async with async_session() as session:
            # Проверяем, есть ли пользователь уже в базе
            result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            existing_user = result.scalar_one_or_none()
            
            if not existing_user:
                # Создаем нового пользователя
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name
                )
                session.add(user)
                await session.commit()
                print(f"User {message.from_user.id} registered successfully")
    except Exception as e:
        print(f"Error registering user: {e}")

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = """
🖤 <b>ProTrack Assistant — Помощь</b>

<b>Основные команды:</b>
/start — Начало работы
/help — Эта справка

<b>Задачи:</b>
/tasks — Список задач
/newtask — Новая задача
/done [id] — Завершить задачу

<b>Привычки:</b>
/habits — Мои привычки
/newhabit — Новая привычка
/loghabit [id] — Отметить выполнение

<b>Финансы:</b>
/finance — Финансовый обзор
/addexpense [сумма] [категория] — Добавить расход
/addincome [сумма] [категория] — Добавить доход

<b>AI помощник:</b>
/ai — AI советы и мотивация
/aimotivate — Мотивационная цитата

<b>Подписка:</b>
/subscriptions — Тарифы и оплата
/mystats — Моя статистика
/settings — Настройки

<b>Поддержка:</b>
/feedback — Обратная связь
/donate — Поддержать проект
"""
    
    await message.answer(
        help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )