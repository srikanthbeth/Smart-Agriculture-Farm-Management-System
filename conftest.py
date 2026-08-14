import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

import models


# ============================================================
# TEST DATABASE
# ============================================================

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://postgres:Srik8499@localhost:5433/smart_agriculture_test_db"
)


engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ============================================================
# CREATE TEST DATABASE TABLES
# ============================================================

@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    Base.metadata.create_all(
        bind=engine
    )

    yield

    Base.metadata.drop_all(
        bind=engine
    )


# ============================================================
# DATABASE SESSION
# ============================================================

@pytest.fixture
def db():

    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection
    )

    try:
        yield session

    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ============================================================
# FASTAPI TEST CLIENT
# ============================================================

@pytest.fixture
def client(db):

    def override_get_db():

        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ============================================================
# AUTHENTICATION HELPER
# ============================================================

def get_auth_headers(
    client,
    username,
    role="Farmer"
):
    """
    Register a test user and return Authorization headers.

    Parameters:
        client:
            FastAPI TestClient

        username:
            Unique username for the test

        role:
            User role.
            Default = Farmer

    Returns:
        Authorization headers dictionary
    """

    email = f"{username}@example.com"
    password = "Test@12345"

    # --------------------------------------------------------
    # REGISTER USER
    # --------------------------------------------------------

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
    )

    print(
        "\nREGISTER STATUS:",
        register_response.status_code
    )

    # --------------------------------------------------------
    # Allow user to already exist
    # --------------------------------------------------------

    if register_response.status_code not in (201, 400, 409):

        print(
            "REGISTER RESPONSE:",
            register_response.text
        )

        raise AssertionError(
            f"Registration failed: "
            f"{register_response.status_code} - "
            f"{register_response.text}"
        )

    # --------------------------------------------------------
    # LOGIN USER
    # --------------------------------------------------------

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    print(
        "LOGIN STATUS:",
        login_response.status_code
    )

    if login_response.status_code != 200:

        print(
            "LOGIN RESPONSE:",
            login_response.text
        )

    assert login_response.status_code == 200, (
        f"Login failed: "
        f"{login_response.status_code} - "
        f"{login_response.text}"
    )

    # --------------------------------------------------------
    # GET ACCESS TOKEN
    # --------------------------------------------------------

    login_data = login_response.json()

    assert "access_token" in login_data, (
        f"access_token missing from login response: "
        f"{login_response.text}"
    )

    token = login_data["access_token"]

    # --------------------------------------------------------
    # RETURN AUTHORIZATION HEADER
    # --------------------------------------------------------

    return {
        "Authorization": f"Bearer {token}"
    }