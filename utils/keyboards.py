from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✅ Задачи"),
                KeyboardButton(text="🔄 Привычки")
            ],
            [
                KeyboardButton(text="💰 Финансы"),
                KeyboardButton(text="🤖 AI Помощник")
            ],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="⚙️ Настройки")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard

def get_task_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для управления задачами"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Новая задача")],
            [KeyboardButton(text="📋 Мои задачи")],
            [KeyboardButton(text="✅ Завершенные")],
            [KeyboardButton(text="↩️ На главную")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_habit_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура для управления привычками"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Новая привычка")],
            [KeyboardButton(text="📋 Мои привычки")],
            [KeyboardButton(text="🔥 Сегодня")],
            [KeyboardButton(text="📊 Статистика привычек")],
            [KeyboardButton(text="↩️ На главную")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_subscription_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-клавиатура для подписок"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎯 Бесплатный", callback_data="plan_free"),
                InlineKeyboardButton(text="🔥 PRO - 299₽", callback_data="plan_pro")
            ],
            [
                InlineKeyboardButton(text="⚡ PREMIUM - 599₽", callback_data="plan_premium")
            ],
            [
                InlineKeyboardButton(text="ℹ️ Подробнее о планах", callback_data="plan_details")
            ],
            [
                InlineKeyboardButton(text="💳 Оплатить", callback_data="payment"),
                InlineKeyboardButton(text="📊 Моя статистика", callback_data="my_stats")
            ]
        ]
    )
    return keyboard