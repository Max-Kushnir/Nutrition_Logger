from pydantic import BaseModel, Field, ConfigDict
from typing import List

class DailyLogBase(BaseModel):
    user_id: int = Field(gt=0)
    
class DailyLogCreate(DailyLogBase):
    pass

class DailyLogResponse(DailyLogBase):
    id: int = Field(gt=0)
    user: UserResponse 
    food_entries: List[FoodEntryResponse] = []

    model_config = ConfigDict(from_attributes=True)
