import json, uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nutrition_logger.database.db import get_db
from nutrition_logger.models.models import User, DailyLog, Food, FoodEntry
from nutrition_logger.schema.schema import (
    UserCreate, UserResponse, UserUpdate, 
    FoodCreate, FoodResponse, FoodUpdate, 
    DailyLogCreate, DailyLogResponse, 
    FoodEntryCreate, FoodEntryResponse, FoodEntryUpdate
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("nutrition_logger.main:app", port=5000, log_level="info")