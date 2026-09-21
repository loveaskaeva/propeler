import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, get_db
from main import app
from fastapi.testclient import TestClient


TEST_DATABASE_URL = "sqlite:///./test_propeler.db"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}, future=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
