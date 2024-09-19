import pytest, json, os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from pydantic import ValidationError
from nutrition_logger.database.db import Base
from nutrition_logger.models import User
from nutrition_logger.schema.daily_log import DailyLogCreate
from nutrition_logger.schema.user import UserCreate, UserResponse
from nutrition_logger.schema.food import FoodCreate
from nutrition_logger.schema.food_entry import FoodEntryCreate
UserResponse.model_rebuild()

# testing validation

def test_valid_user():
    valid_user = UserCreate(username="Maxime_Kushnir", email="maxekushnir@gmail.com")
    assert valid_user.model_dump() == {
        "username": "Maxime_Kushnir",
        "email": "maxekushnir@gmail.com"
    }
    
@pytest.mark.parametrize("field,invalid_value,error_message", [("username", "", "String should have at least 1 character"), ("email", "Maxime_Kushnir", "value is not a valid email address")])
def test_invalid_user(field, invalid_value, error_message):
    valid_data = {"username":"Maxime_Kushnir", "email":"maxekushnir@gmail.com"}
    invalid_data = valid_data.copy()
    invalid_data[field] = invalid_value

    with pytest.raises(ValidationError) as error:
        UserCreate(**invalid_data)

    assert error_message in str(error)

def test_valid_food():
    valid_food = FoodCreate(
        name="Banana",
        manufacturer="example_shop",
        serving_size=1,
        unit="Banana",
        calories=80,
        protein=1.3,
        carbs=27,
        fat=0.4
    )
    
    assert valid_food.model_dump() == {
        "name":"Banana",
        "manufacturer":"example_shop",
        "serving_size":1,
        "unit":"Banana",
        "calories":80,
        "protein":1.3,
        "carbs":27,
        "fat":0.4
    }

@pytest.mark.parametrize("field,invalid_value,error_message", [
    ("name", "", "String should have at least 1 character"),
    ("manufacturer", "", "String should have at least 1 character"),
    ("serving_size", "-1", "Input should be greater than 0"),
    ("unit", "", "String should have at least 1 character"),
    ("calories", "-1", "Input should be greater than or equal to 0"),
    ("protein", "-1", "Input should be greater than or equal to 0"),
    ("carbs", "-1", "Input should be greater than or equal to 0"),
    ("fat", "-1", "Input should be greater than or equal to 0"),
])
def test_invalid_food(field, invalid_value, error_message):
    valid_data = {
        "name":"Banana",
        "manufacturer":"example_shop",
        "serving_size":1,
        "unit":"Banana",
        "calories":80,
        "protein":1.3,
        "carbs":27,
        "fat":0.4
    }
    invalid_data = valid_data.copy()
    invalid_data[field] = invalid_value

    with pytest.raises(ValidationError) as error:
        FoodCreate(**invalid_data)

    assert error_message in str(error)

def test_valid_dailylog():
    valid_dailylog = DailyLogCreate(user_id=1)

    assert valid_dailylog.model_dump() == {
        "user_id":1
    }

def test_invalid_dailylog():
    invalid_data = {"user_id":-1}
    
    with pytest.raises(ValidationError) as error:
        DailyLogCreate(**invalid_data)

    assert "Input should be greater than 0" in str(error)

def test_valid_foodentry():
    valid_foodentry = FoodEntryCreate(daily_log_id=1, food_id=1, quantity=1)

    assert valid_foodentry.model_dump() == {
        "daily_log_id":1,
        "food_id":1,
        "quantity":1.0
    }

@pytest.mark.parametrize("field,invalid_value,error_message", [
    ("daily_log_id", "-1", "Input should be greater than 0"),
    ("food_id", "-1", "Input should be greater than 0"),
    ("quantity", "-1", "Input should be greater than 0"),
])
def test_invalid_foodentry(field, invalid_value, error_message):
    valid_data = {
        "daily_log_id":1,
        "food_id":1,
        "quantity":1.0
    }
    invalid_data = valid_data.copy()
    invalid_data[field] = invalid_value

    with pytest.raises(ValidationError) as error:
        FoodEntryCreate(**invalid_data)

    assert error_message in str(error)

# testing serialization and deserialization integration with sqlalchemy

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

# connect to database
@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DB_URL, echo=True)
    yield engine

# construct engine
@pytest.fixture(scope="function")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

# create session
@pytest.fixture(scope="function")
def db_session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_serialize(db_session):
    user = User(username="testuser", email="testuser@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    db_user = db_session.query(User).first()
    json_user = (UserResponse.model_validate(db_user)).model_dump_json()

    parsed_json = json.loads(json_user)

    assert set(parsed_json.keys()) == {"id", "username", "email", "logs"}

    assert parsed_json["id"] == db_user.id
    assert parsed_json["username"] == db_user.username
    assert parsed_json["email"] == db_user.email
    assert parsed_json["logs"] == db_user.logs

def test_deserialize(db_session):
    user = {
        "id":1,
        "username":"testuser",
        "email":"testuser@example.com",
        "logs":[]
    }

    user_json = json.dumps(user)

    data = json.loads(user_json)
    pydantic_obj = UserCreate(**data)
    db_user = User(**pydantic_obj.model_dump())
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh

    db_user = db_session.query(User).first()

    assert db_user.id == user["id"]
    assert db_user.username == user["username"]
    assert db_user.email == user["email"]
    assert db_user.logs == user["logs"]
