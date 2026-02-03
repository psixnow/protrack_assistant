from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import F
from aiogram.enums import ParseMode  # Добавляем импорт ParseMode

from utils.keyboards import get_main_keyboard, get_task_keyboard

router = Router()

class TaskForm(StatesGroup):
    title = State()
    description = State()
    priority = State()
    deadline = State()

@router.message(Command("tasks"))
async def cmd_tasks(message: Message):
    """Главное меню задач"""
    await message.answer(
        "🖤 <b>Управление задач</b>\n\n"
        "Выберите действие:",
        reply_markup=get_task_keyboard(),
        parse_mode=ParseMode.HTML
    )

@router.message(F.text == "➕ Новая задача")
@router.message(Command("newtask"))
async def new_task_start(message: Message, state: FSMContext):
    """Начало создания новой задачи"""
    await message.answer(
        "✏️ <b>Создание новой задачи</b>\n\n"
        "Введите название задачи:",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(TaskForm.title)

@router.message(TaskForm.title)
async def process_title(message: Message, state: FSMContext):
    """Обработка названия задачи"""
    await state.update_data(title=message.text)
    await message.answer(
        "📝 Введите описание задачи (или пропустите, отправив '0'):"
    )
    await state.set_state(TaskForm.description)

@router.message(TaskForm.description)
async def process_description(message: Message, state: FSMContext):
    """Обработка описания задачи"""
    description = message.text if message.text != '0' else None
    await state.update_data(description=description)
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🔴 Высокий")],
            [types.KeyboardButton(text="🟡 Средний")],
            [types.KeyboardButton(text="🟢 Низкий")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        "⚡ Выберите приоритет задачи:",
        reply_markup=keyboard
    )
    await state.set_state(TaskForm.priority)

@router.message(TaskForm.priority)
async def process_priority(message: Message, state: FSMContext):
    """Обработка приоритета задачи"""
    priority_map = {
        "🔴 Высокий": "high",
        "🟡 Средний": "medium", 
        "🟢 Низкий": "low"
    }
    
    priority = priority_map.get(message.text, "medium")
    await state.update_data(priority=priority)
    
    await message.answer(
        "📅 Введите дедлайн (в формате ДД.ММ.ГГГГ или '0' для пропуска):",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(TaskForm.deadline)

@router.message(TaskForm.deadline)
async def process_deadline(message: Message, state: FSMContext):
    """Завершение создания задачи"""
    from datetime import datetime
    
    data = await state.get_data()
    
    # Парсим дедлайн
    deadline = None
    if message.text != '0':
        try:
            deadline = datetime.strptime(message.text, "%d.%m.%Y")
        except ValueError:
            await message.answer("❌ Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return
    
    # Сохраняем задачу в базу данных
    try:
        from database.models import Task, User
        from sqlalchemy import select
        
        from database.engine import engine
        from sqlalchemy.ext.asyncio import async_sessionmaker
        
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        
        async with async_session() as session:
            # Находим пользователя
            result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                # Создаем пользователя, если его нет
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name
                )
                session.add(user)
                await session.flush()
            
            # Создаем задачу
            task = Task(
                user_id=user.id,
                title=data['title'],
                description=data.get('description'),
                priority=data['priority'],
                deadline=deadline
            )
            
            session.add(task)
            await session.commit()
            await session.refresh(task)
            
            deadline_text = deadline.strftime('%d.%m.%Y') if deadline else 'Не установлен'
            
            await message.answer(
                f"✅ <b>Задача создана!</b>\n\n"
                f"<b>Название:</b> {task.title}\n"
                f"<b>Приоритет:</b> {data['priority']}\n"
                f"<b>Дедлайн:</b> {deadline_text}\n\n"
                f"ID задачи: <code>{task.id}</code>",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
    except Exception as e:
        await message.answer(
            f"❌ Ошибка при создании задачи: {str(e)}",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
    
    await state.clear()

@router.message(Command("mytasks"))
@router.message(F.text == "📋 Список задач")
async def list_tasks(message: Message):
    """Показать список активных задач"""
    try:
        from database.models import Task, User
        from sqlalchemy import select
        
        from database.engine import engine
        from sqlalchemy.ext.asyncio import async_sessionmaker
        
        async_session = async_sessionmaker(engine, expire_on_commit=False)
        
        async with async_session() as session:
            # Находим пользователя
            user_result = await session.execute(
                select(User).where(User.telegram_id == message.from_user.id)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                await message.answer(
                    "📭 У вас пока нет активных задач.\n"
                    "Создайте первую: /newtask"
                )
                return
            
            # Получаем задачи пользователя
            query = select(Task).where(Task.user_id == user.id).where(Task.status != 'done')
            result = await session.execute(query)
            tasks = result.scalars().all()
            
            if not tasks:
                await message.answer(
                    "📭 У вас пока нет активных задач.\n"
                    "Создайте первую: /newtask"
                )
                return
            
            tasks_text = "📋 <b>Ваши задачи:</b>\n\n"
            for task in tasks:
                status_emoji = "✅" if task.status == "done" else "⏳"
                priority_emoji = {
                    "high": "🔴",
                    "medium": "🟡", 
                    "low": "🟢"
                }.get(task.priority, "⚪")
                
                tasks_text += f"{status_emoji} <b>{task.title}</b>\n"
                tasks_text += f"   {priority_emoji} Приоритет: {task.priority}\n"
                if task.deadline:
                    tasks_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
                tasks_text += f"   ID: <code>{task.id}</code>\n\n"
            
            await message.answer(
                tasks_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_task_keyboard()
            )
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении задач: {str(e)}")