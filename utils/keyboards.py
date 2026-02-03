from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Основное меню (ReplyKeyboard)
def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Задачи"), KeyboardButton(text="💰 Финансы")],
            [KeyboardButton(text="🔄 Привычки"), KeyboardButton(text="📊 Статистика")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="🤖 Помощь")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Клавиатура для задач (InlineKeyboard)
def get_tasks_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Новая задача", callback_data="new_task")],
            [InlineKeyboardButton(text="📋 Мои задачи", callback_data="list_tasks")],
            [InlineKeyboardButton(text="✅ Выполненные", callback_data="completed_tasks")],
            [InlineKeyboardButton(text="🗑️ Удалить задачу", callback_data="delete_task")]
        ]
    )
    return keyboard

# Клавиатура для финансов (InlineKeyboard)
def get_finance_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить расход", callback_data="add_expense")],
            [InlineKeyboardButton(text="💰 Добавить доход", callback_data="add_income")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="finance_stats")],
            [InlineKeyboardButton(text="📁 Категории", callback_data="finance_categories")]
        ]
    )
    return keyboard

# Клавиатура для привычек (InlineKeyboard)
def get_habits_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Новая привычка", callback_data="new_habit")],
            [InlineKeyboardButton(text="📋 Мои привычки", callback_data="list_habits")],
            [InlineKeyboardButton(text="✅ Отметить выполнение", callback_data="check_habit")],
            [InlineKeyboardButton(text="📈 Прогресс", callback_data="habit_progress")]
        ]
    )
    return keyboard

# Клавиатура с категориями расходов (ReplyKeyboard)
def get_expense_categories_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍔 Еда"), KeyboardButton(text="🚗 Транспорт")],
            [KeyboardButton(text="🏠 Жилье"), KeyboardButton(text="👕 Одежда")],
            [KeyboardButton(text="💊 Здоровье"), KeyboardButton(text="🎲 Развлечения")],
            [KeyboardButton(text="📚 Образование"), KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard