"""Session-scoped fixtures: one HTTP session and API service objects per test run."""

import logging
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

from src.api.auth_api import AuthApi
from src.api.users_api import UsersApi
from src.clients.http_client import HttpClient
from src.config.settings import get_settings

ALLURE_RESULTS = Path("allure-results")


@pytest.fixture(scope="session", autouse=True)
def configure_logging() -> None:
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        stream=sys.stdout,
    )


@pytest.fixture(scope="session", autouse=True)
def allure_environment() -> None:
    """Fill the Allure report's Environment widget with run settings (no secrets)."""
    settings = get_settings()
    entries = {
        "Base URL": settings.base_url,
        "Auth Username": settings.auth_username,
        "Timeout": f"{settings.timeout:g}s",
        "Log Level": settings.log_level.upper(),
    }
    ALLURE_RESULTS.mkdir(exist_ok=True)
    (ALLURE_RESULTS / "environment.properties").write_text(
        "\n".join(f"{key}={value}" for key, value in entries.items()), encoding="utf-8"
    )


@pytest.fixture(scope="session")
def http_client() -> Iterator[HttpClient]:
    client = HttpClient()
    yield client
    client.session.close()


@pytest.fixture(scope="session")
def users_api(http_client: HttpClient) -> UsersApi:
    return UsersApi(http_client)


@pytest.fixture(scope="session")
def auth_api(http_client: HttpClient) -> AuthApi:
    return AuthApi(http_client)
