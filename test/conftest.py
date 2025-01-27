import os
import dotenv
import pytest

from json_loader import load_json


@pytest.fixture(scope="session")
def db_users():
    data = load_json("users.json")
    assert len(data)
    return data


@pytest.fixture(autouse=True)
def load_envs():
    """Загрузка переменных окружения из файла .env"""
    dotenv.load_dotenv()


# todo
# @pytest.fixture(scope="session")
# def _app_url_():
#     return os.getenv("APP_URL")

@pytest.fixture(scope="session")
def _app_url_(request):
    return request.config.getoption("--app-url")


@pytest.fixture
def app_url(request, _app_url_):
    request.cls.app_url = _app_url_


def pytest_addoption(parser):
    parser.addoption(
        "--app-url",
        action="store",
        help="enter app url",
        default="http://127.0.0.1:8008",
    ),
