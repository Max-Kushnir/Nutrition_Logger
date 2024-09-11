import pytest
from dotenv import load_dotenv
import os
from datetime import date

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from nutrition_logger.models import Base, User, Food, DailyLog, FoodEntry

# Load environment variables
load_dotenv()

# Database configuration
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PW")
db = os.environ.get("POSTGRES_TEST_DB")
host = os.environ.get("POSTGRES_HOST", "localhost")
port = os.environ.get("POSTGRES_PORT", 5432)

# Construct database URL
TEST_DB_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DB_URL, echo=True)
    yield engine

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="session")
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_database_connection(engine):
    with engine.connect() as conn:
        assert conn is not None

def test_tables_exist(engine, tables):
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    expected_tables = ['users', 'foods', 'daily_logs', 'food_entries']
    assert set(expected_tables).issubset(set(existing_tables))

def test_add_user(db_session):
    user = User(username="testuser", email="testuser@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    db_session.close()

    added_user = db_session.query(User).filter_by(username="testuser").first()

    assert added_user is not None
    assert added_user.username == "testuser"
    assert added_user.email == "testuser@example.com"

def test_add_food(db_session):
    food = Food(
        name="Banana",
        manufacturer="Chiquita",
        serving_size=118,
        unit="g",
        calories=105,
        protein=1.3,
        carbs=27,
        fat=0.3
    )
    db_session.add(food)
    db_session.commit()
    db_session.refresh(food)
    db_session.close()

    added_food = db_session.query(Food).filter_by(name="Banana").first()

    assert added_food is not None
    assert added_food.name == "Banana"
    assert added_food.manufacturer == "Chiquita"
    assert added_food.serving_size == 118
    assert added_food.unit== "g"
    assert added_food.calories == 105
    assert added_food.protein == 1.3
    assert added_food.carbs == 27
    assert added_food.fat == 0.3

def test_add_log(db_session):
    log = DailyLog(user_id=1) 
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)
    db_session.close()

    added_log = db_session.query(DailyLog).filter_by(user_id=1).first()

    assert added_log.user_id == 1

def test_add_food_entry(db_session):
    food_entry = FoodEntry(daily_log_id=1, food_id=1)
    db_session.add(food_entry)
    db_session.commit()
    db_session.refresh(food_entry)
    db_session.close()

    added_food_entry = db_session.query(FoodEntry).filter_by(daily_log_id=1).first()

    assert added_food_entry.daily_log_id == 1
    assert added_food_entry.quantity == 1.0
    assert added_food_entry.food.name == "Banana"
    assert added_food_entry.daily_log.user.username == "testuser"

#children of user and list should be deleted if their parent is removed from database
def test_cascade_delete(db_session): 
    added_user = db_session.query(User).filter_by(username="testuser").first()
    db_session.delete(added_user)
    db_session.commit()
    db_session.close()

    added_user = db_session.query(User).filter_by(username="testuser").first()
    added_log = db_session.query(DailyLog).filter_by(user_id=1).first()
    added_food_entry = db_session.query(FoodEntry).filter_by(daily_log_id=1).first()
    
    assert added_user == None
    assert added_log == None
    assert added_food_entry == None

