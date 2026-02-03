from datetime import datetime, timedelta
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database.models import Habit, HabitCompletion

class HabitService:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def create_habit(self, user_id: int, title: str, description: str = None,
                          frequency: str = "daily") -> Habit:
        """Создать новую привычку"""
        habit = Habit(
            user_id=user_id,
            title=title,
            description=description,
            frequency=frequency
        )
        
        self.db.add(habit)
        await self.db.commit()
        await self.db.refresh(habit)
        
        return habit
    
    async def get_user_habits(self, user_id: int) -> list[Habit]:
        """Получить привычки пользователя"""
        query = select(Habit).where(Habit.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def log_completion(self, user_id: int, habit_id: int) -> Dict[str, Any]:
        """Записать выполнение привычки"""
        # Получаем привычку
        query = select(Habit).where(
            Habit.id == habit_id,
            Habit.user_id == user_id
        )
        result = await self.db.execute(query)
        habit = result.scalar_one_or_none()
        
        if not habit:
            raise ValueError("Привычка не найдена")
        
        # Проверяем, была ли привычка выполнена сегодня
        today = datetime.now().date()
        completion_query = select(HabitCompletion).where(
            HabitCompletion.habit_id == habit_id,
            func.date(HabitCompletion.completed_at) == today
        )
        completion_result = await self.db.execute(completion_query)
        existing_completion = completion_result.scalar_one_or_none()
        
        if existing_completion:
            raise ValueError("Привычка уже отмечена сегодня")
        
        # Записываем выполнение
        completion = HabitCompletion(habit_id=habit_id)
        self.db.add(completion)
        
        # Обновляем серию
        yesterday = today - timedelta(days=1)
        
        # Проверяем, была ли привычка выполнена вчера
        yesterday_query = select(HabitCompletion).where(
            HabitCompletion.habit_id == habit_id,
            func.date(HabitCompletion.completed_at) == yesterday
        )
        yesterday_result = await self.db.execute(yesterday_query)
        completed_yesterday = yesterday_result.scalar_one_or_none() is not None
        
        if completed_yesterday:
            # Продолжаем серию
            habit.streak += 1
            is_streak_extended = True
        else:
            # Начинаем новую серию
            habit.streak = 1
            is_streak_extended = False
        
        # Обновляем рекорд
        if habit.streak > habit.best_streak:
            habit.best_streak = habit.streak
        
        await self.db.commit()
        
        return {
            "habit_title": habit.title,
            "new_streak": habit.streak,
            "best_streak": habit.best_streak,
            "is_streak_extended": is_streak_extended
        }