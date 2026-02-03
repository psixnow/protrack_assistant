import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from datetime import datetime
import random

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = "8035264884:AAH81CBGe44-nrT3GjVQg0J6pUu0AwHy944"

# Инициализация
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ========== СОСТОЯНИЯ (FSM) ==========
class TaskForm(StatesGroup):
    title = State()
    description = State()
    priority = State()

class ExpenseForm(StatesGroup):
    amount = State()
    category = State()
    description = State()

class IncomeForm(StatesGroup):
    amount = State()
    category = State()
    description = State()

class HabitForm(StatesGroup):
    title = State()
    frequency = State()

# ========== БАЗА ДАННЫХ (упрощенная в памяти) ==========
users_db = {}
tasks_db = {}
habits_db = {}
transactions_db = {}
task_counter = 0
habit_counter = 0
transaction_counter = 0

def get_or_create_user(user_id: int, username: str = None, first_name: str = None):
    """Создает или получает пользователя"""
    if user_id not in users_db:
        users_db[user_id] = {
            'id': user_id,
            'username': username,
            'first_name': first_name,
            'subscription': 'free',
            'created_at': datetime.now(),
            'daily_tasks': 0,
            'daily_habits': 0
        }
    return users_db[user_id]

# ========== КОМАНДЫ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Начало работы"""
    user = get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📝 Задачи"), types.KeyboardButton(text="🔄 Привычки")],
            [types.KeyboardButton(text="💰 Финансы"), types.KeyboardButton(text="📊 Статистика")],
            [types.KeyboardButton(text="🤖 AI Помощник"), types.KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f"🖤 <b>Привет, {message.from_user.first_name}!</b>\n\n"
        "Я твой личный помощник ProTrack. Помогу с:\n\n"
        "✅ <b>Задачи</b> - ставь цели и отслеживай прогресс\n"
        "🔄 <b>Привычки</b> - формируй полезные ритуалы\n"
        "💰 <b>Финансы</b> - контролируй доходы и расходы\n"
        "🤖 <b>AI Помощник</b> - получай советы и мотивацию\n\n"
        "Используй кнопки ниже или команды:\n"
        "/tasks - задачи\n"
        "/habits - привычки\n"
        "/finance - финансы\n"
        "/ai - AI помощник",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Справка"""
    help_text = """
🖤 <b>ProTrack Assistant - Полный список команд</b>

<b>Основные команды:</b>
/start - Начало работы
/help - Эта справка
/menu - Главное меню

<b>Задачи:</b>
/tasks - Управление задачами
/newtask - Новая задача
/mytasks - Мои задачи
/done [id] - Завершить задачу

<b>Привычки:</b>
/habits - Трекер привычек
/newhabit - Новая привычка
/myhabits - Мои привычки
/loghabit [id] - Отметить выполнение

<b>Финансы:</b>
/finance - Финансовый обзор
/addexpense - Добавить расход
/addincome - Добавить доход
/expenses - Мои расходы
/incomes - Мои доходы

<b>AI помощник:</b>
/ai - AI советы
/aimotivate - Мотивация
/aiquote - Цитата дня

<b>Подписка и статистика:</b>
/subscriptions - Тарифные планы
/mystats - Моя статистика
/settings - Настройки
"""
    await message.answer(help_text, parse_mode=ParseMode.HTML)

# ========== ЗАДАЧИ ==========
@dp.message(Command("tasks"))
@dp.message(F.text == "📝 Задачи")
async def cmd_tasks(message: types.Message):
    """Меню задач"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="➕ Новая задача"), types.KeyboardButton(text="📋 Мои задачи")],
            [types.KeyboardButton(text="✅ Завершенные"), types.KeyboardButton(text="🗑️ Удалить задачу")],
            [types.KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "📝 <b>Управление задачами</b>\n\n"
        "Что вы хотите сделать?",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.message(F.text == "➕ Новая задача")
@dp.message(Command("newtask"))
async def new_task_start(message: types.Message, state: FSMContext):
    """Начало создания задачи"""
    user = get_or_create_user(message.from_user.id)
    
    # Проверка лимита для free плана
    if user['subscription'] == 'free' and user['daily_tasks'] >= 10:
        await message.answer(
            "❌ <b>Достигнут дневной лимит!</b>\n\n"
            "Бесплатный план: 10 задач в день\n"
            "Обновите план: /subscriptions",
            parse_mode=ParseMode.HTML
        )
        return
    
    await message.answer(
        "✏️ <b>Создание новой задачи</b>\n\n"
        "Введите название задачи:",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(TaskForm.title)

@dp.message(TaskForm.title)
async def process_task_title(message: types.Message, state: FSMContext):
    """Обработка названия задачи"""
    await state.update_data(title=message.text)
    await message.answer(
        "📝 Введите описание задачи (или '0' для пропуска):"
    )
    await state.set_state(TaskForm.description)

@dp.message(TaskForm.description)
async def process_task_description(message: types.Message, state: FSMContext):
    """Обработка описания задачи"""
    description = message.text if message.text != '0' else ""
    await state.update_data(description=description)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🔴 Высокий"), types.KeyboardButton(text="🟡 Средний")],
            [types.KeyboardButton(text="🟢 Низкий")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "⚡ Выберите приоритет задачи:",
        reply_markup=keyboard
    )
    await state.set_state(TaskForm.priority)

@dp.message(TaskForm.priority)
async def process_task_priority(message: types.Message, state: FSMContext):
    """Завершение создания задачи"""
    data = await state.get_data()
    
    global task_counter
    task_counter += 1
    
    # Сохраняем задачу
    tasks_db[task_counter] = {
        'id': task_counter,
        'user_id': message.from_user.id,
        'title': data['title'],
        'description': data['description'],
        'priority': message.text[0],  # Первый символ эмодзи
        'status': 'active',
        'created_at': datetime.now()
    }
    
    # Обновляем счетчик пользователя
    users_db[message.from_user.id]['daily_tasks'] += 1
    
    await message.answer(
        f"✅ <b>Задача создана!</b>\n\n"
        f"<b>Название:</b> {data['title']}\n"
        f"<b>Приоритет:</b> {message.text}\n"
        f"<b>Описание:</b> {data['description'] or 'Нет'}\n\n"
        f"ID задачи: <code>{task_counter}</code>\n\n"
        "Для завершения: /done {id}",
        parse_mode=ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()

@dp.message(F.text == "📋 Мои задачи")
@dp.message(Command("mytasks"))
async def show_tasks(message: types.Message):
    """Показать задачи пользователя"""
    user_tasks = [t for t in tasks_db.values() if t['user_id'] == message.from_user.id and t['status'] == 'active']
    
    if not user_tasks:
        await message.answer("📭 У вас пока нет активных задач.")
        return
    
    tasks_text = "📋 <b>Ваши задачи:</b>\n\n"
    for task in user_tasks:
        status_emoji = "⏳" if task['status'] == 'active' else "✅"
        tasks_text += f"{status_emoji} <b>{task['title']}</b>\n"
        tasks_text += f"   Приоритет: {task['priority']}\n"
        tasks_text += f"   ID: <code>{task['id']}</code>\n\n"
    
    await message.answer(tasks_text, parse_mode=ParseMode.HTML)

@dp.message(Command("done"))
async def complete_task(message: types.Message):
    """Завершить задачу"""
    try:
        task_id = int(message.text.split()[1])
        
        if task_id not in tasks_db:
            await message.answer("❌ Задача не найдена.")
            return
        
        task = tasks_db[task_id]
        if task['user_id'] != message.from_user.id:
            await message.answer("❌ Это не ваша задача.")
            return
        
        task['status'] = 'completed'
        task['completed_at'] = datetime.now()
        
        await message.answer(
            f"🎉 <b>Задача завершена!</b>\n\n"
            f"<b>{task['title']}</b>\n"
            f"Время выполнения: {datetime.now().strftime('%H:%M')}",
            parse_mode=ParseMode.HTML
        )
    except (IndexError, ValueError):
        await message.answer("Использование: /done [ID задачи]")

# ========== ФИНАНСЫ ==========
@dp.message(Command("finance"))
@dp.message(F.text == "💰 Финансы")
async def cmd_finance(message: types.Message):
    """Меню финансов"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📉 Добавить расход"), types.KeyboardButton(text="📈 Добавить доход")],
            [types.KeyboardButton(text="💳 Мои расходы"), types.KeyboardButton(text="💰 Мои доходы")],
            [types.KeyboardButton(text="📊 Статистика"), types.KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True
    )
    
    # Рассчитываем баланс
    user_transactions = [t for t in transactions_db.values() if t['user_id'] == message.from_user.id]
    expenses = sum(t['amount'] for t in user_transactions if t['type'] == 'expense')
    incomes = sum(t['amount'] for t in user_transactions if t['type'] == 'income')
    balance = incomes - expenses
    
    await message.answer(
        f"💰 <b>Финансовый обзор</b>\n\n"
        f"📈 Доходы: <b>{incomes}₽</b>\n"
        f"📉 Расходы: <b>{expenses}₽</b>\n"
        f"💵 Баланс: <b>{balance}₽</b>\n\n"
        "Выберите действие:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.message(F.text == "📉 Добавить расход")
@dp.message(Command("addexpense"))
async def add_expense_start(message: types.Message, state: FSMContext):
    """Начало добавления расхода"""
    await message.answer(
        "📉 <b>Добавление расхода</b>\n\n"
        "Введите сумму расхода (например: 500):",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(ExpenseForm.amount)

@dp.message(ExpenseForm.amount)
async def process_expense_amount(message: types.Message, state: FSMContext):
    """Обработка суммы расхода"""
    try:
        amount = float(message.text)
        await state.update_data(amount=amount)
        
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="🍔 Еда"), types.KeyboardButton(text="🚗 Транспорт")],
                [types.KeyboardButton(text="🏠 Жилье"), types.KeyboardButton(text="🎮 Развлечения")],
                [types.KeyboardButton(text("👕 Одежда"), types.KeyboardButton(text="💊 Здоровье"))],
                [types.KeyboardButton(text="📚 Образование"), types.KeyboardButton(text="✈️ Путешествия")]
            ],
            resize_keyboard=True
        )
        
        await message.answer("Выберите категорию или введите свою:", reply_markup=keyboard)
        await state.set_state(ExpenseForm.category)
    except ValueError:
        await message.answer("❌ Введите число (например: 500)")

@dp.message(ExpenseForm.category)
async def process_expense_category(message: types.Message, state: FSMContext):
    """Обработка категории расхода"""
    await state.update_data(category=message.text)
    await message.answer("Введите описание (или '0' для пропуска):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ExpenseForm.description)

@dp.message(ExpenseForm.description)
async def process_expense_description(message: types.Message, state: FSMContext):
    """Завершение добавления расхода"""
    data = await state.get_data()
    description = message.text if message.text != '0' else ""
    
    global transaction_counter
    transaction_counter += 1
    
    transactions_db[transaction_counter] = {
        'id': transaction_counter,
        'user_id': message.from_user.id,
        'amount': data['amount'],
        'category': data['category'],
        'type': 'expense',
        'description': description,
        'created_at': datetime.now()
    }
    
    await message.answer(
        f"📉 <b>Расход добавлен!</b>\n\n"
        f"<b>Сумма:</b> {data['amount']}₽\n"
        f"<b>Категория:</b> {data['category']}\n"
        f"<b>Описание:</b> {description or 'Нет'}",
        parse_mode=ParseMode.HTML
    )
    await state.clear()

@dp.message(F.text == "📈 Добавить доход")
@dp.message(Command("addincome"))
async def add_income_start(message: types.Message, state: FSMContext):
    """Начало добавления дохода"""
    await message.answer(
        "📈 <b>Добавление дохода</b>\n\n"
        "Введите сумму дохода (например: 50000):",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(IncomeForm.amount)

@dp.message(IncomeForm.amount)
async def process_income_amount(message: types.Message, state: FSMContext):
    """Обработка суммы дохода"""
    try:
        amount = float(message.text)
        await state.update_data(amount=amount)
        
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="💰 Зарплата"), types.KeyboardButton(text="💼 Фриланс")],
                [types.KeyboardButton(text="📈 Инвестиции"), types.KeyboardButton(text="🎁 Подарок")],
                [types.KeyboardButton(text="🔄 Возврат"), types.KeyboardButton(text="💸 Подработка")]
            ],
            resize_keyboard=True
        )
        
        await message.answer("Выберите категорию или введите свою:", reply_markup=keyboard)
        await state.set_state(IncomeForm.category)
    except ValueError:
        await message.answer("❌ Введите число (например: 50000)")

@dp.message(IncomeForm.category)
async def process_income_category(message: types.Message, state: FSMContext):
    """Обработка категории дохода"""
    await state.update_data(category=message.text)
    await message.answer("Введите описание (или '0' для пропуска):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(IncomeForm.description)

@dp.message(IncomeForm.description)
async def process_income_description(message: types.Message, state: FSMContext):
    """Завершение добавления дохода"""
    data = await state.get_data()
    description = message.text if message.text != '0' else ""
    
    global transaction_counter
    transaction_counter += 1
    
    transactions_db[transaction_counter] = {
        'id': transaction_counter,
        'user_id': message.from_user.id,
        'amount': data['amount'],
        'category': data['category'],
        'type': 'income',
        'description': description,
        'created_at': datetime.now()
    }
    
    await message.answer(
        f"📈 <b>Доход добавлен!</b>\n\n"
        f"<b>Сумма:</b> {data['amount']}₽\n"
        f"<b>Категория:</b> {data['category']}\n"
        f"<b>Описание:</b> {description or 'Нет'}",
        parse_mode=ParseMode.HTML
    )
    await state.clear()

@dp.message(F.text == "💳 Мои расходы")
@dp.message(Command("expenses"))
async def show_expenses(message: types.Message):
    """Показать расходы"""
    user_expenses = [t for t in transactions_db.values() 
                    if t['user_id'] == message.from_user.id and t['type'] == 'expense']
    
    if not user_expenses:
        await message.answer("📭 У вас пока нет расходов.")
        return
    
    total = sum(e['amount'] for e in user_expenses)
    expenses_text = f"📉 <b>Ваши расходы:</b>\nВсего: {total}₽\n\n"
    
    for expense in user_expenses[-10:]:  # Последние 10
        expenses_text += f"• {expense['amount']}₽ - {expense['category']}\n"
        if expense['description']:
            expenses_text += f"  ({expense['description']})\n"
    
    await message.answer(expenses_text, parse_mode=ParseMode.HTML)

@dp.message(F.text == "💰 Мои доходы")
@dp.message(Command("incomes"))
async def show_incomes(message: types.Message):
    """Показать доходы"""
    user_incomes = [t for t in transactions_db.values() 
                   if t['user_id'] == message.from_user.id and t['type'] == 'income']
    
    if not user_incomes:
        await message.answer("📭 У вас пока нет доходов.")
        return
    
    total = sum(i['amount'] for i in user_incomes)
    incomes_text = f"📈 <b>Ваши доходы:</b>\nВсего: {total}₽\n\n"
    
    for income in user_incomes[-10:]:  # Последние 10
        incomes_text += f"• {income['amount']}₽ - {income['category']}\n"
        if income['description']:
            incomes_text += f"  ({income['description']})\n"
    
    await message.answer(incomes_text, parse_mode=ParseMode.HTML)

# ========== ПРИВЫЧКИ ==========
@dp.message(Command("habits"))
@dp.message(F.text == "🔄 Привычки")
async def cmd_habits(message: types.Message):
    """Меню привычек"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🆕 Новая привычка"), types.KeyboardButton(text="📋 Мои привычки")],
            [types.KeyboardButton(text="✅ Отметить сегодня"), types.KeyboardButton(text="🔥 Моя серия")],
            [types.KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🔄 <b>Трекер привычек</b>\n\n"
        "Формируйте полезные ритуалы и отслеживайте прогресс!",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.message(F.text == "🆕 Новая привычка")
@dp.message(Command("newhabit"))
async def new_habit_start(message: types.Message, state: FSMContext):
    """Новая привычка"""
    user = get_or_create_user(message.from_user.id)
    
    # Проверка лимита
    if user['subscription'] == 'free' and len([h for h in habits_db.values() if h['user_id'] == message.from_user.id]) >= 5:
        await message.answer(
            "❌ <b>Достигнут лимит привычек!</b>\n\n"
            "Бесплатный план: 5 привычек\n"
            "Обновите план: /subscriptions",
            parse_mode=ParseMode.HTML
        )
        return
    
    await message.answer(
        "🔄 <b>Создание новой привычки</b>\n\n"
        "Введите название привычки (например: 'Утренняя зарядка'):",
        parse_mode=ParseMode.HTML
    )
    await state.set_state(HabitForm.title)

@dp.message(HabitForm.title)
async def process_habit_title(message: types.Message, state: FSMContext):
    """Обработка названия привычки"""
    await state.update_data(title=message.text)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📅 Ежедневно"), types.KeyboardButton(text="📆 Еженедельно")],
            [types.KeyboardButton(text="🗓️ Ежемесячно")]
        ],
        resize_keyboard=True
    )
    
    await message.answer("Выберите частоту выполнения:", reply_markup=keyboard)
    await state.set_state(HabitForm.frequency)

@dp.message(HabitForm.frequency)
async def process_habit_frequency(message: types.Message, state: FSMContext):
    """Завершение создания привычки"""
    data = await state.get_data()
    
    global habit_counter
    habit_counter += 1
    
    habits_db[habit_counter] = {
        'id': habit_counter,
        'user_id': message.from_user.id,
        'title': data['title'],
        'frequency': message.text[1:],  # Убираем эмодзи
        'streak': 0,
        'best_streak': 0,
        'last_completed': None,
        'created_at': datetime.now()
    }
    
    await message.answer(
        f"✅ <b>Привычка создана!</b>\n\n"
        f"<b>{data['title']}</b>\n"
        f"Частота: {message.text}\n"
        f"ID: <code>{habit_counter}</code>\n\n"
        "Отмечайте выполнение: /loghabit {id}",
        parse_mode=ParseMode.HTML,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()

@dp.message(F.text == "📋 Мои привычки")
@dp.message(Command("myhabits"))
async def show_habits(message: types.Message):
    """Показать привычки"""
    user_habits = [h for h in habits_db.values() if h['user_id'] == message.from_user.id]
    
    if not user_habits:
        await message.answer("🔄 У вас пока нет привычек.")
        return
    
    habits_text = "🔄 <b>Ваши привычки:</b>\n\n"
    for habit in user_habits:
        habits_text += f"• <b>{habit['title']}</b>\n"
        habits_text += f"  Частота: {habit['frequency']}\n"
        habits_text += f"  Серия: {habit['streak']} дней (рекорд: {habit['best_streak']})\n"
        habits_text += f"  ID: <code>{habit['id']}</code>\n\n"
    
    await message.answer(habits_text, parse_mode=ParseMode.HTML)

@dp.message(Command("loghabit"))
async def log_habit(message: types.Message):
    """Отметить выполнение привычки"""
    try:
        habit_id = int(message.text.split()[1])
        
        if habit_id not in habits_db:
            await message.answer("❌ Привычка не найдена.")
            return
        
        habit = habits_db[habit_id]
        if habit['user_id'] != message.from_user.id:
            await message.answer("❌ Это не ваша привычка.")
            return
        
        # Простая логика: увеличиваем серию
        habit['streak'] += 1
        if habit['streak'] > habit['best_streak']:
            habit['best_streak'] = habit['streak']
        
        habit['last_completed'] = datetime.now()
        
        await message.answer(
            f"🔥 <b>Отличная работа!</b>\n\n"
            f"Привычка <b>{habit['title']}</b> выполнена!\n"
            f"Текущая серия: {habit['streak']} дней\n"
            f"Рекорд: {habit['best_streak']} дней",
            parse_mode=ParseMode.HTML
        )
    except (IndexError, ValueError):
        await message.answer("Использование: /loghabit [ID привычки]")

# ========== AI ПОМОЩНИК ==========
@dp.message(Command("ai"))
@dp.message(F.text == "🤖 AI Помощник")
async def cmd_ai(message: types.Message):
    """AI помощник"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="💬 Мотивация"), types.KeyboardButton(text="💡 Совет дня")],
            [types.KeyboardButton(text="📝 План на день"), types.KeyboardButton(text="🎯 Цитата")],
            [types.KeyboardButton(text="🏠 Главное меню")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🤖 <b>AI Помощник</b>\n\n"
        "Выберите, что вам нужно:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.message(F.text == "💬 Мотивация")
@dp.message(Command("aimotivate"))
async def ai_motivation(message: types.Message):
    """Мотивация"""
    motivations = [
        "Каждый день — это новый шанс стать лучше, чем вчера.",
        "Успех — это сумма маленьких усилий, повторяемых изо дня в день.",
        "Не откладывай на завтра то, что можно сделать сегодня. Завтра начнется новая жизнь.",
        "Дисциплина — это мост между целями и их достижением.",
        "Малые шаги каждый день приводят к большим результатам."
    ]
    
    await message.answer(f"💬 <b>Мотивация:</b>\n\n{random.choice(motivations)}", parse_mode=ParseMode.HTML)

@dp.message(F.text == "🎯 Цитата")
@dp.message(Command("aiquote"))
async def ai_quote(message: types.Message):
    """Цитата"""
    quotes = [
        "Дорогу осилит идущий.",
        "Лучше сделать и пожалеть, чем пожалеть, что не сделал.",
        "Упасть — не страшно. Страшно не подняться.",
        "Верь в себя, и ты будешь непобедим.",
        "Мечты сбываются, если приложить усилия."
    ]
    
    await message.answer(f"🎯 <b>Цитата дня:</b>\n\n{random.choice(quotes)}", parse_mode=ParseMode.HTML)

@dp.message(F.text == "💡 Совет дня")
async def ai_advice(message: types.Message):
    """Совет дня"""
    advice = [
        "Составьте список из 3 самых важных дел на сегодня и выполните их в первую очередь.",
        "Разбейте большую задачу на маленькие шаги по 15 минут каждый.",
        "Планируйте следующий день с вечера, чтобы утром сразу приступить к работе.",
        "Делайте 5-минутные перерывы каждый час для поддержания продуктивности.",
        "Записывайте все идеи, которые приходят в голову, чтобы не забыть."
    ]
    
    await message.answer(f"💡 <b>Совет дня:</b>\n\n{random.choice(advice)}", parse_mode=ParseMode.HTML)

# ========== СТАТИСТИКА ==========
@dp.message(Command("mystats"))
@dp.message(F.text == "📊 Статистика")
async def show_stats(message: types.Message):
    """Статистика пользователя"""
    user = get_or_create_user(message.from_user.id)
    
    # Задачи
    user_tasks = [t for t in tasks_db.values() if t['user_id'] == message.from_user.id]
    active_tasks = len([t for t in user_tasks if t['status'] == 'active'])
    completed_tasks = len([t for t in user_tasks if t['status'] == 'completed'])
    
    # Привычки
    user_habits = [h for h in habits_db.values() if h['user_id'] == message.from_user.id]
    total_streak = sum(h['streak'] for h in user_habits)
    
    # Финансы
    user_transactions = [t for t in transactions_db.values() if t['user_id'] == message.from_user.id]
    expenses = sum(t['amount'] for t in user_transactions if t['type'] == 'expense')
    incomes = sum(t['amount'] for t in user_transactions if t['type'] == 'income')
    
    stats_text = f"""
📊 <b>Ваша статистика</b>

<b>Общая информация:</b>
👤 Пользователь: {user['first_name']}
🎯 План: {user['subscription'].upper()}
📅 В системе с: {user['created_at'].strftime('%d.%m.%Y')}

<b>Задачи:</b>
📝 Всего задач: {len(user_tasks)}
✅ Выполнено: {completed_tasks}
⏳ Активных: {active_tasks}

<b>Привычки:</b>
🔄 Количество: {len(user_habits)}
🔥 Общая серия: {total_streak} дней

<b>Финансы:</b>
📈 Доходы: {incomes}₽
📉 Расходы: {expenses}₽
💵 Баланс: {incomes - expenses}₽

<b>Дневные лимиты:</b>
📝 Задачи: {user['daily_tasks']}/10
🔄 Привычки: {len(user_habits)}/5
"""
    
    await message.answer(stats_text, parse_mode=ParseMode.HTML)

# ========== ПОДПИСКИ ==========
@dp.message(Command("subscriptions"))
async def cmd_subscriptions(message: types.Message):
    """Тарифные планы"""
    subscription_text = """
🖤 <b>Тарифные планы ProTrack</b>

<b>🎯 БЕСПЛАТНЫЙ</b>
• 10 задач в день
• 5 активных привычек  
• Базовый финансовый трекер
• 3 AI-запроса в день

<b>🔥 PRO — 299₽/месяц</b>
• Неограниченные задачи и привычки
• Расширенная аналитика
• 50 AI-запросов в день
• Экспорт данных
• Приоритетная поддержка

<b>⚡ PREMIUM — 599₽/месяц</b>
• Всё из PRO
• Неограниченные AI-запросы
• Автоматизация отчетов
• Личный AI-коуч
• Доступ к бета-функциям

<i>Для оплаты используйте команду /buy [план]</i>
Например: /buy pro
"""
    
    await message.answer(subscription_text, parse_mode=ParseMode.HTML)

@dp.message(Command("buy"))
async def cmd_buy(message: types.Message):
    """Покупка подписки"""
    args = message.text.split()
    if len(args) < 2:
        await message.answer(
            "Использование: /buy [план]\n"
            "Доступные планы: pro, premium\n\n"
            "Пример: /buy pro",
            parse_mode=ParseMode.HTML
        )
        return
    
    plan = args[1].lower()
    if plan not in ["pro", "premium"]:
        await message.answer("❌ Неверный план. Доступно: pro, premium", parse_mode=ParseMode.HTML)
        return
    
    price = "299₽" if plan == "pro" else "599₽"
    
    # В реальном боте здесь была бы интеграция с платежной системой
    await message.answer(
        f"🛒 <b>Оплата подписки {plan.upper()}</b>\n\n"
        f"Сумма: {price}\n"
        f"Период: 30 дней\n\n"
        f"<i>Система оплаты в разработке...</i>\n"
        f"Для теста подписка активирована в демо-режиме.",
        parse_mode=ParseMode.HTML
    )
    
    # Активируем подписку для пользователя
    if message.from_user.id in users_db:
        users_db[message.from_user.id]['subscription'] = plan

# ========== НАСТРОЙКИ ==========
@dp.message(Command("settings"))
@dp.message(F.text == "⚙️ Настройки")
async def cmd_settings(message: types.Message):
    """Настройки"""
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="🔔 Уведомления", callback_data="notifications")],
            [types.InlineKeyboardButton(text="🌍 Язык", callback_data="language")],
            [types.InlineKeyboardButton(text="🗑️ Очистить данные", callback_data="clear_data")],
            [types.InlineKeyboardButton(text="📞 Поддержка", callback_data="support")]
        ]
    )
    
    await message.answer(
        "⚙️ <b>Настройки</b>\n\n"
        "Выберите параметр для настройки:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

# ========== ОБРАБОТКА ВСЕХ СООБЩЕНИЙ ==========
@dp.message(F.text == "🏠 Главное меню")
async def main_menu(message: types.Message):
    """Главное меню"""
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📝 Задачи"), types.KeyboardButton(text="🔄 Привычки")],
            [types.KeyboardButton(text="💰 Финансы"), types.KeyboardButton(text="📊 Статистика")],
            [types.KeyboardButton(text="🤖 AI Помощник"), types.KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите раздел:",
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )

@dp.message(Command("menu"))
async def cmd_menu(message: types.Message):
    """Команда меню"""
    await main_menu(message)

# ========== ЗАПУСК БОТА ==========
async def main():
    """Запуск бота"""
    logger.info("🚀 ProTrack Assistant запущен!")
    
    # Удаляем вебхук
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем поллинг
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())