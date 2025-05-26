from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

PasswordStr = Annotated[str, StringConstraints(min_length=6)]


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserLogin(UserBase):
    password: str


class OAuthLogin(BaseModel):
    provider: Literal["github", "google"]
    token: str


class UserOut(UserBase):
    id: int
    is_oauth: bool
    oauth_provider: Optional[str]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class TokenOut(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
