from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

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