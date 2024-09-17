from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional

#User classes
class UserBase(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr 

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int = Field(gt=0)
    username: str = Field(min_length=1)
    email: EmailStr
    logs: List[DailyLogResponse] = []

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username:Optional[str] = Field(min_length=1)
    email: Optional[EmailStr]

#Food database classes
class FoodBase(BaseModel):
    name: str = Field(min_length=1)
    manufacturer: str = Field(min_length=1)
    serving_size: float = Field(gt=0, default=1.0)
    unit: str = Field(min_length=1)
    calories: float = Field(ge=0, default=0)
    protein: float = Field(ge=0, default=0)
    carbs: float = Field(ge=0, default=0)
    fat: float = Field(ge=0, default=0)

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    id: int = Field(gt=0)
    
    model_config = ConfigDict(from_attributes=True)


class FoodUpdate(BaseModel):
    name: Optional[str] = Field(min_length=1)
    manufacturer: Optional[str] = Field(min_length=1)
    serving_size: Optional[float] = Field(gt=0, default=1.0)
    unit: Optional[str] = Field(min_length=1)
    calories: Optional[float] = Field(ge=0, default=0)
    protein: Optional[float] = Field(ge=0, default=0)
    carbs: Optional[float] = Field(ge=0, default=0)
    fat: Optional[float] = Field(ge=0, default=0)

#DailyLog classes
class DailyLogBase(BaseModel):
    user_id: int = Field(gt=0)
    
class DailyLogCreate(DailyLogBase):
    pass

class DailyLogResponse(DailyLogBase):
    id: int = Field(gt=0)
    user: UserResponse 
    food_entries: List[FoodEntryResponse] = []

    model_config = ConfigDict(from_attributes=True)



#FoodEntry classes
class FoodEntryBase(BaseModel):
    daily_log_id: int = Field(gt=0)
    food_id: int = Field(gt=0)
    quantity: float = Field(gt=0, default=1)
     
class FoodEntryCreate(FoodEntryBase):
    pass

class FoodEntryResponse(FoodEntryBase):
    id: int = Field(gt=0)
    daily_log: DailyLogResponse
    food: FoodResponse 

    model_config = ConfigDict(from_attributes=True)


class FoodEntryUpdate(BaseModel):
    quantity: Optional[float] = Field(gt=0)