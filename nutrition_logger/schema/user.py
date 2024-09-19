from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional

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