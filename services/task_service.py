from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select

from database.models import Task, User
from database.repository import get_db

class TaskService:
    def __init__(self):
        pass
    
    async def create_task(self, user_id: int, title: str, description: Optional[str] = None,
                         priority: str = "medium", deadline: Optional[datetime] = None) -> Task:
        """Создать новую задачу"""
        async for session in get_db():
            # Находим пользователя по telegram_id
            user_result = await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                # Создаем пользователя, если его нет
                user = User(telegram_id=user_id)
                session.add(user)
                await session.flush()  # Получаем id пользователя
            
            task = Task(
                user_id=user.id,
                title=title,
                description=description,
                priority=priority,
                deadline=deadline
            )
            
            session.add(task)
            await session.commit()
            await session.refresh(task)
            
            return task
    
    async def get_user_tasks(self, user_id: int, status: str = None) -> List[Task]:
        """Получить задачи пользователя"""
        async for session in get_db():
            # Находим пользователя
            user_result = await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                return []
            
            query = select(Task).where(Task.user_id == user.id)
            
            if status:
                query = query.where(Task.status == status)
            
            result = await session.execute(query)
            tasks = result.scalars().all()
            
            return tasks
    
    async def complete_task(self, user_id: int, task_id: int) -> Task:
        """Завершить задачу"""
        async for session in get_db():
            # Находим пользователя
            user_result = await session.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise ValueError("Пользователь не найден")
            
            query = select(Task).where(
                Task.id == task_id,
                Task.user_id == user.id,
                Task.status != "done"
            )
            
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            
            if not task:
                raise ValueError("Задача не найдена или уже завершена")
            
            task.status = "done"
            task.completed_at = datetime.now()
            
            await session.commit()
            await session.refresh(task)
            
            return task