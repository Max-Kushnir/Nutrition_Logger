from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, DailyLog, Food, FoodEntry

load_dotenv()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PW")
db = os.environ.get("POSTGRES_DB")
host = os.environ.get("POSTGRES_HOST", "localhost") #postgres running from docker image
port = os.environ.get("POSTGRES_PORT", 5432)

url = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(url)

#create all tables
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

#create a session
session = Session()


