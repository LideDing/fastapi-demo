from pydantic import BaseModel, field_validator


class UserInfo(BaseModel):
    id: str = ""
    sub: str
    name: str = ""
    groups: list[str] = []
    extra: dict = {}


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str | None = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class RegisterResponse(BaseModel):
    user_id: str
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
