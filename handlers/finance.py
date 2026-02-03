from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram import F
from aiogram.enums import ParseMode  # Импортируем ParseMode из aiogram.enums

router = Router()

class FinanceForm(StatesGroup):
    amount = State()
    category = State()
    type = State()
    description = State()

@router.message(Command("finance"))
@router.message(F.text == "💰 Финансы")
async def cmd_finance(message: Message):
    """Главное меню финансов"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="➕ Добавить расход")],
            [types.KeyboardButton(text="💰 Добавить доход")],
            [types.KeyboardButton(text="📊 Статистика")],
            [types.KeyboardButton(text="📈 Графики")],
            [types.KeyboardButton(text="↩️ На главную")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "💰 <b>Финансовый трекер</b>\n\n"
        "Отслеживайте доходы и расходы, анализируйте свои финансы!",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML  # Используем ParseMode.HTML
    )