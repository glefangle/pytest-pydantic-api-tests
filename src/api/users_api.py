"""Service layer: user-related endpoints, each returning parsed pydantic models."""

import requests

from src.clients.http_client import HttpClient
from src.schemas.users import CreateUpdateUserRequest, MutatedUserResponse, User, UsersListResponse


class UsersApi:
    def __init__(self, client: HttpClient) -> None:
        self.client = client

    def get_user(self, user_id: int) -> User:
        response = self.client.get(f"/users/{user_id}")
        return User.model_validate(response.json())

    def list_users(self, limit: int = 10, skip: int = 0) -> UsersListResponse:
        response = self.client.get("/users", params={"limit": limit, "skip": skip})
        return UsersListResponse.model_validate(response.json())

    def create_user(self, payload: CreateUpdateUserRequest) -> MutatedUserResponse:
        response = self.client.post("/users/add", json=payload.model_dump(by_alias=True))
        return MutatedUserResponse.model_validate(response.json())

    def update_user(self, user_id: int, payload: CreateUpdateUserRequest) -> MutatedUserResponse:
        response = self.client.put(f"/users/{user_id}", json=payload.model_dump(by_alias=True))
        return MutatedUserResponse.model_validate(response.json())

    def delete_user(self, user_id: int) -> MutatedUserResponse:
        response = self.client.delete(f"/users/{user_id}")
        return MutatedUserResponse.model_validate(response.json())

    def get_raw(self, user_id: int) -> requests.Response:
        """Raw response access for negative tests asserting on status codes / error bodies."""
        return self.client.get(f"/users/{user_id}")
