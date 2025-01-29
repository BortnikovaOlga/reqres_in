import os
import dotenv
import pytest
from sqlmodel import create_engine


@pytest.fixture(scope="session", autouse=True)
def load_envs():
    """Загрузка переменных окружения из файла .env"""
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def _app_url_():
    return os.getenv("APP_URL")


@pytest.fixture
def app_url(request, _app_url_):
    request.cls.app_url = _app_url_


@pytest.fixture(scope="session")
def _db_engine_():
    return create_engine(os.getenv("DATABASE_ENGINE"), pool_size=os.getenv("DATABASE_POOL_SIZE", 10))

# @pytest.fixture(scope="session")
# def _app_url_(request):
#     return request.config.getoption("--app-url")

# def pytest_addoption(parser):
#     parser.addoption(
#         "--app-url",
#         action="store",
#         help="enter app url",
#         default="http://127.0.0.1:8008",
#     ),
