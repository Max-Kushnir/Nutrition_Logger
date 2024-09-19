from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nutrition_logger.database.db import Base

class FoodEntry(Base):
    __tablename__ = 'food_entries'

    id: Mapped[int] = mapped_column(primary_key=True)
    daily_log_id: Mapped[int] = mapped_column(ForeignKey('daily_logs.id'), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey('foods.id'), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False, default=1.0)

    daily_log: Mapped[DailyLog] = relationship(back_populates="food_entries")
    food: Mapped[Food] = relationship()

