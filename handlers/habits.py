from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode  # Импортируем ParseMode из aiogram.enums
from aiogram import F

router = Router()

@router.message(Command("habits"))
@router.message(F.text == "🔄 Привычки")
async def cmd_habits(message: Message):
    """Главное меню привычек"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="➕ Новая привычка")],
            [types.KeyboardButton(text="📋 Мои привычки")],
            [types.KeyboardButton(text="🔥 Сегодня")],
            [types.KeyboardButton(text="📊 Статистика привычек")],
            [types.KeyboardButton(text="↩️ На главную")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🔄 <b>Трекер привычек</b>\n\n"
        "Формируйте полезные ритуалы и отслеживайте прогресс!",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML  # Используем ParseMode.HTML
    )