import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from src.models import Base, User, Log, Food, FoodDatabase
import os

load_dotenv()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PW")
db = os.environ.get("POSTGRES_TEST_DB")
host = os.environ.get("POSTGRES_HOST", "localhost") #postgres running from docker image
port = os.environ.get("POSTGRES_PORT", 5432)

url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(url)

