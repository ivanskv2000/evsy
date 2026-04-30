from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

PasswordStr = Annotated[str, StringConstraints(min_length=6)]
ProviderName = Literal["github", "google"]


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserLogin(UserBase):
    password: str


class OAuthLogin(BaseModel):
    provider: ProviderName
    token: str = Field(
        ...,
        description="The authorization code received from the OAuth provider callback.",
    )


class UserOut(UserBase):
    id: int
    is_oauth: bool
    oauth_provider: Optional[ProviderName]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class TokenOut(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
