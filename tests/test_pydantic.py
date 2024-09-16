import pytest
from pydantic import ValidationError
from nutrition_logger.models import User, Food, DailyLog, FoodEntry
from nutrition_logger.schema import (
    UserCreate, UserResponse, UserUpdate, 
    FoodCreate, FoodResponse, FoodUpdate, 
    DailyLogCreate, DailyLogResponse, 
    FoodEntryCreate, FoodEntryResponse, FoodEntryUpdate
)

