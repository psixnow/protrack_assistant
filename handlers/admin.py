from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config.settings import settings

router = Router()

# Проверка, является ли пользователь администратором
def is_admin(user_id: int) -> bool:
    return user_id in settings.get_admin_ids()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Панель администратора"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещен")
        return
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="👥 Пользователи")],
            [types.KeyboardButton(text="💰 Подписки")],
            [types.KeyboardButton(text="📊 Статистика")],
            [types.KeyboardButton(text="📢 Рассылка")],
            [types.KeyboardButton(text="⚙️ Настройки")],
            [types.KeyboardButton(text="↩️ На главную")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🛠️ <b>Панель администратора</b>\n\n"
        "Выберите раздел для управления:",
        reply_markup=keyboard,
        parse_mode=types.ParseMode.HTML
    )

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Статистика бота"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Доступ запрещен")
        return
    
    # Здесь будет реальная статистика из БД
    # Пока заглушка
    await message.answer(
        "📊 <b>Статистика бота</b>\n\n"
        "• Всего пользователей: 1\n"
        "• Активных сегодня: 1\n"
        "• Подписок PRO: 0\n"
        "• Подписок PREMIUM: 0\n"
        "• Всего задач: 0\n"
        "• Всего привычек: 0\n\n"
        "Бот запущен и работает!",
        parse_mode=types.ParseMode.HTML
    )

@router.message(lambda message: message.text == "👥 Пользователи")
async def admin_users(message: Message):
    """Управление пользователями"""
    if not is_admin(message.from_user.id):
        return
    
    await message.answer(
        "👥 <b>Управление пользователями</b>\n\n"
        "Функция в разработке.\n"
        "Скоро здесь можно будет:\n"
        "• Просматривать список пользователей\n"
        "• Изменять подписки\n"
        "• Блокировать/разблокировать\n\n"
        "Пока используйте команду /stats",
        parse_mode=types.ParseMode.HTML
    )