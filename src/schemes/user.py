from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    onboarded: bool
    profile: Optional[dict] = None

class OnboardPayload(BaseModel):
    dietary_preferences: Optional[list[str]] = []
    favorite_cuisines: Optional[list[str]] = []
    location: Optional[str] = None