import pytest
from dotenv import load_dotenv, find_dotenv
from selene import browser


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv(find_dotenv())


@pytest.fixture(scope="session")
def api_base_url():
    return "https://api.litres.ru/foundation/api"