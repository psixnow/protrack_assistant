from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, Any

class SubscriptionPlan(Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"

class SubscriptionLimits:
    """Лимиты для каждого плана подписки"""
    
    PLANS = {
        SubscriptionPlan.FREE: {
            "daily_tasks": 10,
            "daily_ai_requests": 3,
            "max_habits": 5,
            "features": ["basic_tasks", "basic_habits", "basic_finance"]
        },
        SubscriptionPlan.PRO: {
            "daily_tasks": float('inf'),  # неограниченно
            "daily_ai_requests": 50,
            "max_habits": float('inf'),
            "features": ["unlimited_tasks", "unlimited_habits", "advanced_finance", 
                        "ai_requests", "export_data", "priority_support"]
        },
        SubscriptionPlan.PREMIUM: {
            "daily_tasks": float('inf'),
            "daily_ai_requests": float('inf'),
            "max_habits": float('inf'),
            "features": ["unlimited_tasks", "unlimited_habits", "advanced_finance",
                        "unlimited_ai", "export_data", "priority_support",
                        "auto_reports", "ai_coach", "beta_access"]
        }
    }
    
    @classmethod
    def get_plan_limits(cls, plan: SubscriptionPlan) -> Dict[str, Any]:
        """Получить лимиты для плана"""
        return cls.PLANS.get(plan, cls.PLANS[SubscriptionPlan.FREE])
    
    @classmethod
    def can_access_feature(cls, plan: SubscriptionPlan, feature: str) -> bool:
        """Проверить доступ к функции"""
        limits = cls.get_plan_limits(plan)
        return feature in limits["features"]

class SubscriptionService:
    """Сервис управления подписками"""
    
    def __init__(self, user_id: int):  # Изменил: принимаем user_id вместо db_session
        self.user_id = user_id
        # Для тестирования, без базы данных
        self.user_plan = SubscriptionPlan.FREE  # По умолчанию бесплатный план
    
    async def check_access(self, feature: str) -> bool:
        """Проверить доступ к функции (реализация для middleware)"""
        # Преобразуем feature из middleware в названия функций в плане
        feature_mapping = {
            'tasks': ['basic_tasks', 'unlimited_tasks'],
            'habits': ['basic_habits', 'unlimited_habits'],
            'finance': ['basic_finance', 'advanced_finance'],
            'ai': ['ai_requests', 'unlimited_ai']
        }
        
        # Получаем список функций, которые соответствуют запрошенной
        required_features = feature_mapping.get(feature, [])
        
        # Получаем план пользователя (пока заглушка)
        user_plan = await self._get_user_plan()
        
        # Получаем лимиты плана
        plan_limits = SubscriptionLimits.get_plan_limits(user_plan)
        
        # Проверяем, есть ли у пользователя хотя бы одна из требуемых функций
        for required_feature in required_features:
            if required_feature in plan_limits["features"]:
                # Если функция есть, дополнительно проверяем лимиты для задач и AI
                if feature == 'tasks':
                    return await self.check_task_limit()
                elif feature == 'ai':
                    return await self.check_ai_limit()
                else:
                    return True
        
        return False
    
    async def _get_user_plan(self) -> SubscriptionPlan:
        """Получить план пользователя (заглушка)"""
        # В реальном приложении здесь будет запрос к базе данных
        return self.user_plan
    
    async def check_task_limit(self) -> bool:
        """Проверить лимит задач на сегодня (заглушка)"""
        # Временная заглушка: всегда возвращаем True для тестирования
        # В реальном приложении здесь будет логика проверки daily_task_count
        return True
    
    async def check_ai_limit(self) -> bool:
        """Проверить лимит AI запросов (заглушка)"""
        # Временная заглушка: всегда возвращаем True для тестирования
        return True
    
    async def upgrade_subscription(self, plan: SubscriptionPlan, 
                                  duration_days: int = 30):
        """Обновить подписку пользователя"""
        # Здесь будет логика обновления подписки
        self.user_plan = plan
        # В реальном приложении: сохранение в базу данных
        pass
    
    async def get_user_subscription_info(self) -> Dict[str, Any]:
        """Получить информацию о подписке пользователя"""
        user_plan = await self._get_user_plan()
        plan_limits = SubscriptionLimits.get_plan_limits(user_plan)
        
        return {
            "plan": user_plan.value,
            "until": None,
            "tasks_today": 0,
            "tasks_limit": plan_limits["daily_tasks"],
            "ai_requests_today": 0,
            "ai_requests_limit": plan_limits["daily_ai_requests"],
            "habits_count": 0,
            "habits_limit": plan_limits["max_habits"]
        }