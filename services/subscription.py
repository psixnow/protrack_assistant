from enum import Enum
from datetime import datetime, timedelta
import pytz
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
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def check_task_limit(self, user_id: int) -> bool:
        """Проверить лимит задач на сегодня"""
        # Здесь будет логика проверки daily_task_count
        # Пока заглушка
        return True
    
    async def check_ai_limit(self, user_id: int) -> bool:
        """Проверить лимит AI запросов"""
        # Заглушка
        return True
    
    async def upgrade_subscription(self, user_id: int, plan: SubscriptionPlan, 
                                  duration_days: int = 30):
        """Обновить подписку пользователя"""
        # Здесь будет логика обновления подписки
        # Пока заглушка
        pass
    
    async def get_user_subscription_info(self, user_id: int) -> Dict[str, Any]:
        """Получить информацию о подписке пользователя"""
        return {
            "plan": "free",
            "until": None,
            "tasks_today": 0,
            "tasks_limit": 10,
            "ai_requests_today": 0,
            "ai_requests_limit": 3,
            "habits_count": 0,
            "habits_limit": 5
        }