from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.engine import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    subscription_ends = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    finances = relationship("Finance", back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(Integer, default=1)  # 1-5 приоритет
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="tasks")

class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    frequency = Column(String(50), default="daily")  # daily, weekly, monthly
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    target_days = Column(Integer, default=30)  # Цель в днях
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_completed = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    # Relationship for habit completions
    completions = relationship("HabitCompletion", back_populates="habit", cascade="all, delete-orphan")
    user = relationship("User", back_populates="habits")

class HabitCompletion(Base):
    __tablename__ = 'habit_completions'
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"))
    completed_date = Column(Date, nullable=False, default=func.current_date())
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    habit = relationship("Habit", back_populates="completions")

class Finance(Base):
    __tablename__ = 'finances'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String(100), nullable=False, default="other")
    description = Column(Text, nullable=True)
    type = Column(String(20), nullable=False)  # 'income' или 'expense'
    payment_method = Column(String(50), nullable=True)  # cash, card, etc.
    date = Column(DateTime(timezone=True), server_default=func.now())
    recurring = Column(Boolean, default=False)  # Регулярный платеж
    recurring_interval = Column(String(20), nullable=True)  # monthly, weekly
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="finances")