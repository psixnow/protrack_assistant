from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from utils.keyboards import get_subscription_keyboard

router = Router()

@router.message(Command("subscriptions"))
async def cmd_subscriptions(message: Message):
    """Показать тарифные планы"""
    subscription_text = """
🖤 <b>Тарифные планы ProTrack</b>

<b>🎯 БЕСПЛАТНЫЙ</b>
• 10 задач в день
• 5 активных привычек  
• Базовый финансовый трекер

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
    
    await message.answer(
        subscription_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_subscription_keyboard()
    )

@router.message(Command("buy"))
async def cmd_buy(message: Message):
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
    
    await message.answer(
        f"🛒 <b>Оплата подписки {plan.upper()}</b>\n\n"
        f"Сумма: {price}\n"
        f"Период: 30 дней\n\n"
        f"<i>Система оплаты в разработке...</i>\n"
        f"Для теста админ может выдать подписку вручную.",
        parse_mode=ParseMode.HTML
    )

@router.callback_query(lambda c: c.data.startswith('plan_'))
async def process_plan_callback(callback_query: CallbackQuery):
    """Обработка нажатия на кнопку с планом"""
    await callback_query.answer("Функция в разработке")
    await callback_query.message.answer(
        "Функция выбора плана через кнопки в разработке.\n"
        "Используйте команду /buy [план]",
        parse_mode=ParseMode.HTML
    )