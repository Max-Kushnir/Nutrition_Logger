import datetime
from typing import List, Optional
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username:Mapped[str] = mapped_column(unique=True, nullable=False)

    logs: Mapped[List["Log"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Log(Base):
    __tablename__ = 'logs'

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    date:Mapped[datetime.date] = mapped_column(Date, primary_key=True) 

    user:Mapped[User] = relationship(back_populates="logs")
    foods:Mapped[List["Food"]] = relationship(back_populates="log", cascade="all, delete-orphan")
    
class Food(Base):
    __tablename__ = 'foods'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('logs.user_id'), primary_key=True)
    log_date:Mapped[datetime.date] = mapped_column(ForeignKey('logs.date'), primary_key=True)
    food_db_id:Mapped[int] = mapped_column(ForeignKey('food_database.id'), nullable=False)
    quantity:Mapped[float] = mapped_column(nullable = False)

    log:Mapped[Log] = relationship(back_populates="foods")
    food_db:Mapped["FoodDatabase"] = relationship()

class FoodDatabase(Base):
    __tablename__ = 'food_database'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False)
    manufacturer: Mapped[Optional[str]] = mapped_column(nullable=True)
    calories: Mapped[float] = mapped_column(nullable=False)
    protein: Mapped[float] = mapped_column(nullable=True)
    carbs: Mapped[float] = mapped_column(nullable=True)
    fat: Mapped[float] = mapped_column(nullable=True)

    foods: Mapped[List[Food]] = relationship(back_populates="food_db")

