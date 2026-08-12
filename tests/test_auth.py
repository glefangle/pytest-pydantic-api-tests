import allure
import pytest

from src.api.auth_api import AuthApi
from src.config.settings import get_settings
from src.schemas.users import AuthResponse, ErrorResponse


@allure.feature("Auth")
@allure.story("Login")
@pytest.mark.smoke
def test_login_success(auth_api: AuthApi) -> None:
    settings = get_settings()

    with allure.step("Login with valid credentials"):
        response, body = auth_api.login(settings.auth_username, settings.auth_password)

    with allure.step("API returns 200 with access and refresh tokens"):
        assert response.status_code == 200
        assert isinstance(body, AuthResponse)
        assert body.access_token
        assert body.refresh_token
        assert body.username == settings.auth_username


@allure.feature("Auth")
@allure.story("Login")
@pytest.mark.regression
def test_bearer_token_grants_access_to_profile(auth_api: AuthApi) -> None:
    settings = get_settings()

    with allure.step("Login to obtain a token"):
        _, auth = auth_api.login(settings.auth_username, settings.auth_password)
        assert isinstance(auth, AuthResponse)

    with allure.step("Call GET /auth/me with the Bearer token"):
        profile = auth_api.current_user(auth.access_token)

    with allure.step("Profile belongs to the logged-in user"):
        assert profile.username == settings.auth_username
        assert profile.email


@allure.feature("Auth")
@allure.story("Login")
@pytest.mark.negative
@pytest.mark.parametrize(
    ("username", "password", "case_id"),
    [
        ("emilys", "wrong-password", "wrong-password"),
        ("nosuchuser", "whatever", "unknown-user"),
        ("", "", "empty-credentials"),
    ],
)
def test_login_failure(auth_api: AuthApi, username: str, password: str, case_id: str) -> None:
    with allure.step(f"Login attempt: {case_id}"):
        response, body = auth_api.login(username, password)

    with allure.step("API rejects the request and explains why"):
        assert response.status_code == 400
        assert isinstance(body, ErrorResponse)
        assert body.message
