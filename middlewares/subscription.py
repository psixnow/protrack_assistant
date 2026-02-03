from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from services.subscription import SubscriptionService

class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        """Middleware для проверки подписки перед обработкой команды"""
        
        # Команды, которые не требуют проверки подписки
        free_commands = ['/start', '/help', '/subscriptions', '/buy', 
                        '/feedback', '/donate', '/settings']
        
        # Если команда бесплатная - пропускаем
        if event.text and any(event.text.startswith(cmd) for cmd in free_commands):
            return await handler(event, data)
        
        # Для остальных команд проверяем подписку
        user_id = event.from_user.id
        
        # Определяем, к какой функции относится команда
        feature = self._get_feature_from_command(event.text)
        
        if feature:
            subscription_service = SubscriptionService(user_id)
            if not await subscription_service.check_access(feature):
                await self._send_limit_message(event, feature)
                return
        
        return await handler(event, data)
    
    def _get_feature_from_command(self, command: str) -> str:
        """Определяет функцию из команды"""
        if not command:
            return None
        
        command = command.lower()
        
        if any(cmd in command for cmd in ['/newtask', '/tasks', '/done']):
            return 'tasks'
        elif any(cmd in command for cmd in ['/newhabit', '/habits', '/loghabit']):
            return 'habits'
        elif any(cmd in command for cmd in ['/addexpense', '/addincome', '/finance']):
            return 'finance'
        elif any(cmd in command for cmd in ['/ai', '/aimotivate']):
            return 'ai'
        
        return None
    
    async def _send_limit_message(self, event: Message, feature: str):
        """Отправляет сообщение о достижении лимита"""
        feature_names = {
            'tasks': 'задач',
            'habits': 'привычек',
            'finance': 'финансового трекера',
            'ai': 'AI-запросов'
        }
        
        feature_name = feature_names.get(feature, 'функции')
        
        await event.answer(
            f"❌ <b>Лимит {feature_name} исчерпан!</b>\n\n"
            f"Ваш текущий план: 🎯 БЕСПЛАТНЫЙ\n\n"
            f"Обновите план для полного доступа:\n"
            f"/subscriptions — посмотреть тарифы\n"
            f"/buy pro — купить PRO версию\n\n"
            f"<i>Или дождитесь завтра, лимиты обновятся.</i>",
            parse_mode='HTML'
        )