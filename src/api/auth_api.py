"""Service layer: authentication endpoints."""

import requests

from src.clients.http_client import HttpClient
from src.schemas.users import AuthResponse, ErrorResponse, LoginRequest, User


class AuthApi:
    def __init__(self, client: HttpClient) -> None:
        self.client = client

    def login(
        self, username: str, password: str
    ) -> tuple[requests.Response, AuthResponse | ErrorResponse]:
        """Returns (response, parsed_body): AuthResponse on 200, ErrorResponse otherwise."""
        payload = LoginRequest(username=username, password=password)
        response = self.client.post("/auth/login", json=payload.model_dump())
        if response.ok:
            return response, AuthResponse.model_validate(response.json())
        return response, ErrorResponse.model_validate(response.json())

    def current_user(self, access_token: str) -> User:
        """GET /auth/me — profile behind a Bearer token."""
        response = self.client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
        return User.model_validate(response.json())
