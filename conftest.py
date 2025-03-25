import os
import dotenv
import pytest
from sqlmodel import create_engine

from app.database.users_db_service import UserDBService
from client.api.login_api import LoginApi
from client.api.user_api import UsersApi
from model.envs import Envs


@pytest.fixture(scope="session")
def envs() -> Envs:
    dotenv.load_dotenv()
    envs_instance = Envs(
        app_url=os.getenv("APP_URL"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
        db_engine=os.getenv("DATABASE_ENGINE"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )
    return envs_instance


@pytest.fixture(scope="session")
def _db_engine_(envs):
    return create_engine(envs.db_engine, pool_size=os.getenv("DATABASE_POOL_SIZE", 10))


@pytest.fixture
def db_service(_db_engine_):
    return UserDBService(_db_engine_)


@pytest.fixture
def users_api(envs):
    return UsersApi(f"{envs.app_url}/api")


@pytest.fixture
def login_api(envs):
    return LoginApi(f"{envs.app_url}/api")
