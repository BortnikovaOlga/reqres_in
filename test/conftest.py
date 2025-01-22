import pytest

from json_loader import load_json


@pytest.fixture(scope="session")
def users():
    return load_json("../users.json")
