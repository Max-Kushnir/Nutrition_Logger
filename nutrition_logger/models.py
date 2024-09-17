from __future__ import annotations
from typing import List
import datetime

from sqlalchemy import ForeignKey, UniqueConstraint, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

#table of users
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    logs: Mapped[List[DailyLog]] = relationship(back_populates="user", cascade="all, delete-orphan")

#database for food
class Food(Base):
    __tablename__ = 'foods'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    manufacturer: Mapped[str] = mapped_column(unique=True, nullable=False)
    serving_size: Mapped[float] = mapped_column(nullable=False)
    unit: Mapped[str] = mapped_column(nullable=False)
    calories: Mapped[float] = mapped_column(nullable=False)
    protein: Mapped[float] = mapped_column(nullable=False)
    carbs: Mapped[float] = mapped_column(nullable=False)
    fat: Mapped[float] = mapped_column(nullable=False)

#table of logs, user can only have one log per date
class DailyLog(Base):
    __tablename__ = 'daily_logs'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, default=datetime.date.today)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user: Mapped[User] = relationship(back_populates="logs")
    food_entries: Mapped[List[FoodEntry]] = relationship(back_populates="daily_log", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('user_id', 'date', name='_user_date_uc'),)

#table of food entries associated with individual logs
class FoodEntry(Base):
    __tablename__ = 'food_entries'

    id: Mapped[int] = mapped_column(primary_key=True)
    daily_log_id: Mapped[int] = mapped_column(ForeignKey('daily_logs.id'), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey('foods.id'), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False, default=1.0)

    daily_log: Mapped[DailyLog] = relationship(back_populates="food_entries")
    food: Mapped[Food] = relationship()

