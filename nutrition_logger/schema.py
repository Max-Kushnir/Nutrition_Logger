from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

#User classes
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    logs: List["DailyLogResponse"] = []

class UserUpdate(BaseModel):
    username: str
    email: EmailStr

#Food database classes
class FoodBase(BaseModel):
    name: str
    manufacturer: str
    serving_size: float
    unit: str
    calories: float
    protein: float
    carbs: float
    fat: float

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    id: int

class FoodUpdate(BaseModel):
    name: Optional[str]
    manufacturer: Optional[str]
    serving_size: Optional[float]
    unit: Optional[str]
    calories: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fat: Optional[float]

#DailyLog classes
class DailyLogBase(BaseModel):
    date: datetime.date
    user_id: int
    
class DailyLogCreate(DailyLogBase):
    pass

class DailyLogResponse(DailyLogBase):
    id: int
    user: "UserResponse"
    food_Entries: List["FoodEntryResponse"] = []

#FoodEntry classes
class FoodEntryBase(BaseModel):
    daily_log_id: int
    food_id: int
    quantity: float
    
class FoodEntryCreate(FoodEntryBase):
    pass

class FoodEntryResponse(FoodEntryBase):
    id: int
    daily_log: "DailyLogResponse"
    food: "FoodResponse"

class FoodEntryUpdate(BaseModel):
    quantity: Optional[int]