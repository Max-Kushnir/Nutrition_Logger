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
    engine = create_engine(TEST_DB_URL)
    yield engine

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
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
