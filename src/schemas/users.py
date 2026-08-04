"""Pydantic schemas describing API contracts: response validation happens here.

Python-side attributes are snake_case per PEP 8; `alias` keeps the camelCase
wire format of the API on both parsing and serialization (`by_alias=True`).
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: int
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    username: str | None = None
    age: int | None = None
    email: EmailStr | None = None
    phone: str | None = None


class UsersListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    users: list[User]


class CreateUpdateUserRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")


class MutatedUserResponse(BaseModel):
    """Body returned by POST /users/add, PUT and DELETE /users/{id}: echoes the resource."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: int
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(User):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class ErrorResponse(BaseModel):
    message: str
