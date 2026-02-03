WELCOME_MESSAGE = """
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

HELP_MESSAGE = """
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

SUBSCRIPTION_PLANS = """
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

# Промпты для генерации аватара
AVATAR_PROMPTS = [
    "Minimalist flat design bot avatar, productivity tracker theme",
    "Black background with red and green accents, abstract graph design",
    "Telegram bot icon style, clean lines, tech aesthetic",
    "Productivity assistant character, friendly but professional",
    "Geometric shapes forming upward arrow, gradient black to red"
]