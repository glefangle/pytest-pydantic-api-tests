import allure
import pytest
from faker import Faker

from src.api.users_api import UsersApi
from src.schemas.users import CreateUpdateUserRequest, ErrorResponse

fake = Faker()

EXISTING_USER_ID = 1
NOT_FOUND_USER_ID = 9999


@allure.feature("Users")
@allure.story("Get user")
@pytest.mark.smoke
def test_get_existing_user(users_api: UsersApi) -> None:
    with allure.step("Request user by id"):
        user = users_api.get_user(EXISTING_USER_ID)

    with allure.step("User fields match the contract"):
        assert user.id == EXISTING_USER_ID
        assert user.first_name == "Emily"
        assert user.last_name == "Johnson"
        assert user.email is not None
        assert "@" in user.email


@allure.feature("Users")
@allure.story("Get user")
@pytest.mark.negative
def test_get_missing_user_returns_404(users_api: UsersApi) -> None:
    with allure.step("Request non-existent user"):
        response = users_api.get_raw(NOT_FOUND_USER_ID)

    with allure.step("API responds 404 with a helpful message"):
        assert response.status_code == 404
        error = ErrorResponse.model_validate(response.json())
        assert "not found" in error.message.lower()


@allure.feature("Users")
@allure.story("List users")
@pytest.mark.regression
def test_list_users_pagination(users_api: UsersApi) -> None:
    with allure.step("Request 5 users skipping the first 10"):
        users = users_api.list_users(limit=5, skip=10)

    with allure.step("Pagination metadata is consistent"):
        assert users.skip == 10
        assert users.limit == 5
        assert users.total > 0
        assert len(users.users) == 5

    with allure.step("All ids in the page are unique"):
        ids = [user.id for user in users.users]
        assert len(ids) == len(set(ids))


@allure.feature("Users")
@allure.story("CRUD")
@pytest.mark.smoke
def test_create_user(users_api: UsersApi) -> None:
    payload = CreateUpdateUserRequest(first_name=fake.first_name(), last_name=fake.last_name())

    with allure.step(f"Create user {payload.first_name} {payload.last_name}"):
        created = users_api.create_user(payload)

    with allure.step("Response echoes payload and assigns an id"):
        assert created.first_name == payload.first_name
        assert created.last_name == payload.last_name
        assert created.id > 0


@allure.feature("Users")
@allure.story("CRUD")
@pytest.mark.regression
def test_update_user(users_api: UsersApi) -> None:
    payload = CreateUpdateUserRequest(first_name=fake.first_name(), last_name=fake.last_name())

    with allure.step(f"Update user {EXISTING_USER_ID}"):
        updated = users_api.update_user(EXISTING_USER_ID, payload)

    with allure.step("Response echoes the new name, id preserved"):
        assert updated.id == EXISTING_USER_ID
        assert updated.first_name == payload.first_name
        assert updated.last_name == payload.last_name


@allure.feature("Users")
@allure.story("CRUD")
@pytest.mark.regression
def test_delete_user(users_api: UsersApi) -> None:
    with allure.step("Delete user"):
        deleted = users_api.delete_user(EXISTING_USER_ID)

    with allure.step("API returns the deleted resource"):
        assert deleted.id == EXISTING_USER_ID
